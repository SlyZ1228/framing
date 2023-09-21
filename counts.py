import pandas as pd
import PA
from pybaseball import cache
cache.enable()

# get the data
re, pitches, PA = PA.outcome_lin_weights()

# drop unnecessary columns and eventless pitches and create a "count" column
pitches = pd.concat([pitches['game_pk'], pitches['inning'], pitches['inning_topbot'], pitches['balls'], pitches['strikes'], pitches['events']], axis=1)
pitches.dropna(subset='events', inplace=True)
pitches['count'] = pitches['balls'].astype(str).str.cat(pitches['strikes'].astype(str), sep='-')
pitches.drop(columns=['balls', 'strikes'], inplace=True)

# map the run expectancy changes per event and then average them over counts
map = PA.to_dict()
pitches['count_values'] = pitches['events'].map(map)
counts = pitches.groupby(['count'])['count_values'].mean()

# create a df with the data labeled by ball and strike count
data = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2], [3, 0], [3, 1], [3, 2], [4, 2]]
df = pd.DataFrame(data, columns=['balls', 'strikes'])
df['count_values'] = counts.reset_index(drop=True).squeeze()
df.drop(index=12, inplace=True)

# pivot with strikes at top and balls on side
counts = df.pivot(index='balls', columns='strikes', values='count_values').copy()

print(counts)

counts.to_csv('data\counts.csv')