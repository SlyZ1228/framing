import pandas as pd

def outcome_lin_weights():
       # get pitch data
       re = pd.read_csv('data\RE24 Matrix - 2023.csv')
       pitches = pd.read_csv('data\countdata.csv')

       # drop unnecessary columns and no PA outcomes
       pitches = pd.concat([pitches['game_pk'], pitches['events'], pitches['base_state'], pitches['inning'], pitches['inning_topbot'], pitches['outs_when_up'], pitches['bat_score'], pitches['post_bat_score'], pitches['balls'], pitches['strikes'], pitches['at_bat_number']], axis=1)
       pitches['change_score'] = pitches['post_bat_score'].subtract(pitches['bat_score'])
       pitches['count'] = pitches['balls'].astype(str).str.cat(pitches['strikes'].astype(str), sep='-')
       pitches.drop(columns=['bat_score', 'post_bat_score', 'balls', 'strikes'], inplace=True)
       # drop unnecessary columns and no PA outcomes
       pitches = pd.concat([pitches['game_pk'], pitches['events'], pitches['base_state'], pitches['inning'], pitches['inning_topbot'], pitches['outs_when_up'], pitches['bat_score'], pitches['post_bat_score'], pitches['balls'], pitches['strikes'], pitches['at_bat_number']], axis=1)
       pitches['change_score'] = pitches['post_bat_score'].subtract(pitches['bat_score'])
       pitches['count'] = pitches['balls'].astype(str).str.cat(pitches['strikes'].astype(str), sep='-')
       pitches.drop(columns=['bat_score', 'post_bat_score', 'balls', 'strikes'], inplace=True)

       # encode the top/bot inning values
       pitches = pitches.replace('Bot', 1).replace('Top', 0)
       pitches['inning_topbot'] = pitches['inning_topbot'].astype(int)
       # encode the top/bot inning values
       pitches = pitches.replace('Bot', 1).replace('Top', 0)
       pitches['inning_topbot'] = pitches['inning_topbot'].astype(int)

       # set dataframe to multiindex and sort based on game, inning, top/bot of inning, and outs number
       pitches = pitches.set_index(['game_pk', 'inning', 'inning_topbot', 'outs_when_up', 'at_bat_number', 'count'], drop=False)
       pitches = pitches.sort_index(level=['game_pk', 'inning', 'inning_topbot', 'outs_when_up', 'at_bat_number', 'count'], ascending=[False, True, True, True, True, True]).droplevel('outs_when_up').drop(columns=['game_pk', 'inning', 'inning_topbot'])
       # set dataframe to multiindex and sort based on game, inning, top/bot of inning, and outs number
       pitches = pitches.set_index(['game_pk', 'inning', 'inning_topbot', 'outs_when_up', 'at_bat_number', 'count'], drop=False)
       pitches = pitches.sort_index(level=['game_pk', 'inning', 'inning_topbot', 'outs_when_up', 'at_bat_number', 'count'], ascending=[False, True, True, True, True, True]).droplevel('outs_when_up').drop(columns=['game_pk', 'inning', 'inning_topbot'])

       # shift base states and outs for each half inning (don't need next base state if inning ends after the PA)
       pitches['next_base_state'] = pitches['base_state'].groupby(level=['game_pk', 'inning', 'inning_topbot']).shift(-1)
       pitches['next_outs'] = pitches['outs_when_up'].groupby(level=['game_pk', 'inning', 'inning_topbot']).shift(-1).astype('Int64')
       # shift base states and outs for each half inning (don't need next base state if inning ends after the PA)
       pitches['next_base_state'] = pitches['base_state'].groupby(level=['game_pk', 'inning', 'inning_topbot']).shift(-1)
       pitches['next_outs'] = pitches['outs_when_up'].groupby(level=['game_pk', 'inning', 'inning_topbot']).shift(-1).astype('Int64')

       # combine the base states with out count
       pitches['pre_base_out'] = pitches['outs_when_up'].astype(str).str.cat(pitches['base_state'], sep='-')
       pitches['post_base_out'] = pitches['next_outs'].astype(str).str.cat(pitches['next_base_state'], sep='-')
       pitches.drop(columns=['next_base_state', 'next_outs', 'outs_when_up', 'base_state'], inplace=True) # dont need these anymore
       # combine the base states with out count
       pitches['pre_base_out'] = pitches['outs_when_up'].astype(str).str.cat(pitches['base_state'], sep='-')
       pitches['post_base_out'] = pitches['next_outs'].astype(str).str.cat(pitches['next_base_state'], sep='-')
       pitches.drop(columns=['next_base_state', 'next_outs', 'outs_when_up', 'base_state'], inplace=True) # dont need these anymore

       # dictionary of each unique run expectancy based on format of the combined base_out states in the dataframe
       map = {'0-_ _ _': re.iloc[0].iat[1], '1-_ _ _': re.iloc[0].iat[2], '2-_ _ _': re.iloc[0].iat[3], 
              '0-1 _ _': re.iloc[1].iat[1], '1-1 _ _': re.iloc[1].iat[2], '2-1 _ _': re.iloc[1].iat[3], 
              '0-_ 2 _': re.iloc[2].iat[1], '1-_ 2 _': re.iloc[2].iat[2], '2-_ 2 _': re.iloc[2].iat[3], 
              '0-1 2 _': re.iloc[3].iat[1], '1-1 2 _': re.iloc[3].iat[2], '2-1 2 _': re.iloc[3].iat[3],
              '0-_ _ 3': re.iloc[4].iat[1], '1-_ _ 3': re.iloc[4].iat[2], '2-_ _ 3': re.iloc[4].iat[3],
              '0-1 _ 3': re.iloc[5].iat[1], '1-1 _ 3': re.iloc[5].iat[2], '2-1 _ 3': re.iloc[5].iat[3],
              '0-_ 2 3': re.iloc[6].iat[1], '1-_ 2 3': re.iloc[6].iat[2], '2-_ 2 3': re.iloc[6].iat[3],
              '0-1 2 3': re.iloc[7].iat[1], '1-1 2 3': re.iloc[7].iat[2], '2-1 2 3': re.iloc[7].iat[3]}
       # dictionary of each unique run expectancy based on format of the combined base_out states in the dataframe
       map = {'0-_ _ _': re.iloc[0].iat[1], '1-_ _ _': re.iloc[0].iat[2], '2-_ _ _': re.iloc[0].iat[3], 
              '0-1 _ _': re.iloc[1].iat[1], '1-1 _ _': re.iloc[1].iat[2], '2-1 _ _': re.iloc[1].iat[3], 
              '0-_ 2 _': re.iloc[2].iat[1], '1-_ 2 _': re.iloc[2].iat[2], '2-_ 2 _': re.iloc[2].iat[3], 
              '0-1 2 _': re.iloc[3].iat[1], '1-1 2 _': re.iloc[3].iat[2], '2-1 2 _': re.iloc[3].iat[3],
              '0-_ _ 3': re.iloc[4].iat[1], '1-_ _ 3': re.iloc[4].iat[2], '2-_ _ 3': re.iloc[4].iat[3],
              '0-1 _ 3': re.iloc[5].iat[1], '1-1 _ 3': re.iloc[5].iat[2], '2-1 _ 3': re.iloc[5].iat[3],
              '0-_ 2 3': re.iloc[6].iat[1], '1-_ 2 3': re.iloc[6].iat[2], '2-_ 2 3': re.iloc[6].iat[3],
              '0-1 2 3': re.iloc[7].iat[1], '1-1 2 3': re.iloc[7].iat[2], '2-1 2 3': re.iloc[7].iat[3]}

       # add columns for RE based on pre and post PA base out states and find change in RE
       pitches['pre_re'] = pitches['pre_base_out'].map(map)
       pitches['post_re'] = pitches['post_base_out'].map(map)
       pitches['change_re'] = pitches['post_re'].subtract(pitches['pre_re'], fill_value=0).add(pitches['change_score'])
       # group the change in run expectencies and average them
       pitches = pitches.set_index(['events'])
       PA = pitches.groupby(['events'])['change_re'].mean()
       # add columns for RE based on pre and post PA base out states and find change in RE
       pitches['pre_re'] = pitches['pre_base_out'].map(map)
       pitches['post_re'] = pitches['post_base_out'].map(map)
       pitches['change_re'] = pitches['post_re'].subtract(pitches['pre_re'], fill_value=0).add(pitches['change_score'])
       # group the change in run expectencies and average them
       pitches = pitches.set_index(['events'])
       PA = pitches.groupby(['events'])['change_re'].mean()

       PA.to_csv("data\PA outcomes.csv")
       PA.to_csv("data\PA outcomes.csv")

outcome_lin_weights()