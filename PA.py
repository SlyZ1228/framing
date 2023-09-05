import pandas as pd
import matrix

# re, pitches = matrix.re_matrix(2023)

pd.set_option('display.max_rows', None)

re = pd.read_csv('RE24 Matrix - 2023.csv')
pitches = pd.read_csv('statcast data.csv')

pitches.set_index(['game_pk', 'inning', 'inning_topbot'])
# pitches = pitches.sort_values(by=['game_pk', 'inning', 'inning_topbot'])
# df1 = pitches.set_index(['game_pk', 'inning', 'inning_topbot'])['base_state'].unstack()

# new = pd.concat([df1.shift(-1, axis=1).stack(), 
#                  df1.shift(axis=1).stack()], 
#                  keys=['next_base_state','prev_base_state'], axis=1)

# pitches = pitches.join(new, on=['game_pk', 'inning', 'inning_topbot'])

pitches.head()
