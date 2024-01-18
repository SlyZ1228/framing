import pandas as pd

def count_re():
    # import data
    PA = pd.read_csv('data\PA outcomes.csv')
    pitches = pd.read_csv('data\pitchdata.csv')

    # drop unnecessary columns, create "count" column, and backfill events list
    pitches = pd.concat([pitches['game_pk'], pitches['inning'], pitches['inning_topbot'], pitches['balls'], pitches['strikes'], pitches['events'], pitches['game_year'], pitches['at_bat_number']], axis=1)
    pitches['count'] = pitches['balls'].astype(str).str.cat(pitches['strikes'].astype(str), sep='-')
    pitches = pitches.set_index(['game_pk', 'inning', 'inning_topbot', 'at_bat_number', 'count'], drop=True).sort_index(level=['game_pk', 'inning', 'inning_topbot', 'at_bat_number', 'count'], ascending=[False, True, False, True, True]).drop(columns=['balls', 'strikes'])
    pitches['events'] = pitches['events'].bfill()

    # map the run expectancy changes by event and average them over the counts
    map = PA.set_index('events')['change_re'].to_dict()
    pitches['count_values'] = pitches['events'].map(map)
    counts = pitches.reset_index().set_index(['count'], drop=True).sort_index(level=['count'], ascending=True)
    counts = pitches.groupby(['count'])['count_values'].mean()

    # create a df with the data labeled by ball and strike count
    data = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2], [3, 0], [3, 1], [3, 2], [4, 2]]
    df = pd.DataFrame(data, columns=['balls', 'strikes'])
    df['count_values'] = counts.reset_index(drop=True).squeeze()

    # pivot with strikes at top and balls on side
    counts = df.drop(index=12).pivot(index='balls', columns='strikes', values='count_values').copy()

    # return and save data
    print(counts)
    counts.to_csv('data\counts.csv')

count_re()