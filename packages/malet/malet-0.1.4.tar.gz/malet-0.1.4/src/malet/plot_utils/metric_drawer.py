from typing import Literal

import pandas as pd
import matplotlib as mpl
import numpy as np

def select_df(df, filt_dict, *exclude_fields, drop=False):
    """Select df rows with matching from given filt_dict except ``exclude_fields``"""
    assert not (k:=set(filt_dict.keys()) - set(df.index.names)), f'filt_dict keys {k} is not in df.'
    filt_keys = set(filt_dict.keys()) - set(exclude_fields)    # filter out exclude field
    
    nest = lambda vs: vs if isinstance(vs, list) else [vs]
    for k in filt_keys:
        values = nest(filt_dict[k])
        assert not (v:=set(values)-(vs:=set(df.index.get_level_values(k)))), f"Values {v} are not in field '{k}': {sorted(vs)}"
        df = df.loc[df.index.get_level_values(k).isin(values)]
    
    if drop:
        df = df.reset_index([*filt_keys], drop=True)
        
    return df

def homogenize_df(df, ref_df, filt_dict, *exclude_fields):
    """Homogenize index values of ``df`` with reference to ``select_df(ref_df, filt_dict)``."""
    ref_idx = select_df(ref_df, filt_dict, drop=True).index
    slcted_dfs = [select_df(df, dict(zip(ref_idx.names, d))) for d in ref_idx.values]
    df = pd.concat(slcted_dfs)
    return df

def avgbest_df(df, metric_field,
               avg_over=None, 
               best_over=tuple(), 
               best_of=dict(), 
               best_at_max=True):
    """
    Average over ``avg_over`` and get best result over ``best_over``
    
    - aggregate index : avg_over, best_over
    - key index : best_of, others
    """
    df_fields = set(df.index.names)
    
    # avg over avg_over
    if avg_over is not None:
        df_fields -= {avg_over}
        avg_over_group = df.groupby([*df_fields])
        df = avg_over_group.mean(numeric_only=True)
        df[metric_field+'_std'] = avg_over_group.sem(numeric_only=True)[metric_field]  # add std column
    
    # best result over best_over
    if best_over:
        # find best result over best_over for best_of
        df_fields -= set(best_over)
        best_df = select_df(df, best_of)
        best_df = best_df.loc[best_df.groupby([*df_fields])[metric_field]
                                     .aggregate(('idxmin', 'idxmax')[best_at_max])]

        # match best_over values for non-best_of-key-index with best_of-key-index
        df_fields -= set(best_of)
        df = homogenize_df(df, best_df, best_of, *df_fields)
    
    return df


def ax_draw(ax: mpl.axes.Axes,
            df: pd.DataFrame,
            label: str,
            annotate = True,
            std_plot: Literal['none','fill','bar'] = 'fill',
            unif_xticks = False,
            plot_config = {'linewidth':4, 'color':'orange', 'marker':'D', 'markersize':10, 'markevery':1},
    ) -> mpl.axes.Axes:
    """
    Draws y_field over arbitrary x_field setted as index of the dataframe.
    If there is column 'y_field_sdv' is in dataframe, draws in errorbar or fill_between depending on ``sdv_bar_plot``
    """
    assert std_plot in {'bar', 'fill', 'none'}, 'std_plot should be one of {"bar","fill","none"}'
    y_field = list(df)[0]
    
    x_values, metric_values = map(np.array, zip(*dict(df[y_field]).items()))
    assert not isinstance(metric_values[0], pd.Series), 'y_field should have only 1 values for each index.'
    tick_values = x_values
    if unif_xticks:
        ax.set_xticks(range(len(x_values)), x_values, fontsize=10, rotation=45)
        tick_values = np.arange(len(x_values))
        
    if len(tick_values)==1:
        ax.axhline(metric_values, linewidth=plot_config['linewidth'], color=plot_config['color'], label=label)
        if f'{y_field}_std' in df:
            metric_std = float(df[f'{y_field}_std'])
            ax.axhspan(metric_values[0] + metric_std, metric_values[0] - metric_std, alpha=0.3, color=plot_config['color'])

    else:
        ax.plot(tick_values, metric_values, label=label, **plot_config)
        if f'{y_field}_std' in df:
            x_values, metric_std = map(np.array, zip(*dict(df[f'{y_field}_std']).items()))
            
            if std_plot=='bar':
                ax.errorbar(tick_values, metric_values, yerr=metric_std, color=plot_config['color'], elinewidth=3)
            elif std_plot=='fill':
                ax.fill_between(tick_values, metric_values + metric_std, metric_values - metric_std, alpha=0.3, color=plot_config['color'])
            
        if annotate:
            annot_field = set(df) - {'total_epochs', 'epoch', y_field, f'{y_field}_std'}
            abv = lambda s: ''.join([i[0] for i in s.split('_')] if '_' in s else \
                                      [s[0]] + [i for i in s[1:] if i not in 'aeiou']) if len(s)>3 else s
            abv_annot = [*map(abv, annot_field)]
            for x,y,t in zip(x_values, metric_values, tick_values):
                txt = '\n'.join(['' if unif_xticks else str(x)]+[f'{i}={df.loc[x][j]}' for i, j in zip(abv_annot, annot_field)])
                ax.annotate(txt, (t,y), textcoords="offset points", xytext=(0,10), ha='center')
    
    ax.tick_params(axis='both', which='major', labelsize=17, direction='in', length=5)

    return ax
