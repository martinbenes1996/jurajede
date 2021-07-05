
from datetime import datetime
import io
import logging
import numpy as np
import pandas as pd
import requests

#def raw():
#    """Load raw."""
#    return pd.read_csv('data/data.csv')

def raw():
    """Load raw."""
    logging.warning("fetching data from google drive")
    URL = 'https://docs.google.com/uc?export=download'
    # session
    session = requests.Session()
    response = session.get(URL, params = {'id': '1kHE_NB4gvIJxNJmjYklYgePA47jxp7eY'})
    # confirm token
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = { 'id' : id, 'confirm' : value }
            response = session.get(URL, params = params)
            break
    # parse csv
    return pd.read_csv(io.StringIO(response.text))

def monthly():
    """Load monthly means."""
    x = raw()
    return x\
        .groupby('month')\
        .aggregate({'km': 'mean'}, axis=1)\
        .reset_index()


config = {
    'join_behind': True,
    'fill_missing': True
}
def load(join_behind = True):
    x = raw()
    # join behind
    if config['join_behind']:
        for r in x[x.join_behind == 1].itertuples():
            # get the location
            m,y = r.month + 1,r.year
            if m > 12:
                m = (m % 12) + 1
                y = y + 1
            jb = (x.year == y) & (x.month == m)
            # half the second
            if jb.any():
                x.loc[jb,'days'] = x[jb].days / 2
                x.loc[jb,'km'] = x[jb].km / 2
            else:
                x.append(
                    pd.DataFrame({
                        'year':y, 'month':m,
                        'days': r.days//2, 'km': r.km//2,
                        'join_behind': np.nan
                    })
                )
            # half the fist
            x.loc[x.index == r.Index,'days'] = x[x.index == r.Index]['days'] // 2
            x.loc[x.index == r.Index,'km'] = x[x.index == r.Index]['km'] // 2
    # arrange
    x = x\
        .sort_values(['year','month'])\
        .drop('join_behind', axis=1)
    # dates
    x['date'] = x.apply(lambda r: datetime.strptime('%04d-%02d-01'%(r.year,r.month),'%Y-%m-%d'), axis=1)
    # time window
    def steps(i, limit):
        assert((i >= 1) & (i <= 12))
        def sign(i):
            if i > 0: return 1
            elif i < 0: return -1
            else: return 0
        r = []
        for j in range(1,abs(limit)):
            step = (i + j * sign(limit))%12
            step = step if step > 0 else 12
            r.append(step)
        return r
    def left(i, by = 1): return steps(i, -by)
    def right(i, by = 1): return steps(i, by)
    def avg_daily_portion(x,i,monthdiff=12):
        x = x[(x.index >= (i-monthdiff)) & (x.index <= (i+monthdiff))]
        x = x[(~x.days.isna()) & (x.days != 0)]
        # ratio average
        x['ratio'] = x.km / x.days
        x = x\
            .groupby('month')\
            .aggregate({'ratio': 'mean'})\
            .merge(pd.DataFrame({'month': range(1,13)}), how='right', on='month')
        # mean using neighbors
        for r in x[x.ratio.isna()].itertuples():
            r_l = left(r.month)
            r_r = right(r.month)
            x.loc[r.Index,'ratio'] = x.loc[x.month.isin([r_l,r_r]),'ratio'].mean()
        return x
    # estimate missing from neighborhood
    x = x.reset_index(drop=True)
    x['est'] = False
    for r in x[(x.days.isna()) & (~x.km.isna())].itertuples():
        # get average +- 2y
        ngh = avg_daily_portion(x, r.Index, 48)
        avg = ngh.loc[ngh.month == r.month,'ratio']
        # count rounded days
        x.loc[x.index == r.Index,'days'] = float(round(r.km / avg))
        x.loc[x.index == r.Index,'est'] = True
    # total yearly
    x_yearly = x[~x.km.isna()]\
        .groupby('year')\
        .aggregate({'km': 'sum'}, axis=1)\
        .rename({'km': 'yearly'}, axis=1)\
        .reset_index()
    # total monthly
    x_monthly = x[~x.km.isna()]\
        .groupby('month')\
        .aggregate({'km': 'mean'}, axis=1)\
        .rename({'km': 'monthly'}, axis=1)\
        .reset_index()
    # km ratio
    x = x\
        .merge(x_yearly, on='year')
    x['km_y'] = x.km / x.yearly
    x['km_y_cumsum'] = x\
        .groupby('year').km_y\
        .transform(pd.Series.cumsum)
    # day lengths
    def month_length(r):
        if r.month in {1,3,5,7,8,10,12}: return 31
        elif r.month in {4,6,9,11}: return 30
        elif r.year % 400 == 0: return 29
        elif r.year % 100 == 0: return 28
        elif r.year % 4 == 0: return 29
        else: return 28
    x['day_len'] = x.apply(month_length, axis=1)
    # days off
    x['days_off'] = x.day_len - x.days
    # km per day
    x['km_p_day'] = x.km / x.day_len
    x['km_p_activeday'] = (x.km / x.days).fillna(0)
    x['equators'] = x.km / 40075 # Earth equator
    # age
    x['age'] = (x.date - datetime(1971,1,13)).apply(lambda a: a.days / 365.24)
    # return
    return x
