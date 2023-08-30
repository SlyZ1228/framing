from pybaseball import statcast, cache
cache.enable() # Optional

import datetime
import pandas as pd

def re_matrix(year):
  count = 1
  ym, y1m, y2m = None, None, None

  #loop for all three years
  for yr in [year, year - 1, year - 2]:
    season_start = datetime.datetime(yr, 3, 1)
    season_end = datetime.datetime(yr, 11, 1)

    ### load season data w pybaseball
    pitch_data = statcast(start_dt=season_start.strftime('%Y-%m-%d'),end_dt=season_end.strftime('%Y-%m-%d'))

    ### create base state representations
    for base in ['1b','2b','3b']:
      pitch_data.loc[pitch_data['on_'+base].notna(),'on_'+base] = int(base[0])
      pitch_data['on_'+base] = pitch_data['on_'+base].astype('str').replace('<NA>','_')
    pitch_data['base_state'] = pitch_data['on_1b']+' '+pitch_data['on_2b']+' '+pitch_data['on_3b']

    ### determine number of run innings
    pitch_data['start_inning_score'] = pitch_data['bat_score'].groupby([pitch_data['game_pk'],pitch_data['inning'],pitch_data['inning_topbot']]).transform('min')
    pitch_data['end_inning_score'] = pitch_data['bat_score'].groupby([pitch_data['game_pk'],pitch_data['inning'],pitch_data['inning_topbot']]).transform('max')
    pitch_data['inning_runs'] = pitch_data['end_inning_score'].sub(pitch_data['start_inning_score']).astype('int')

    ### make the dataframe for the matrix
    ### 3 outs x 8 base states
    data = (pitch_data
                .dropna(subset=['events']) # removes pitches that dont lead to pa change
                .groupby(['game_year','base_state','outs_when_up']) # average runs for each base out state
                ['inning_runs']
                .mean()
                .reset_index()
                .pivot(index=['game_year','base_state'], # pivots for 2d axis
                      columns='outs_when_up',
                      values='inning_runs')
                .copy()
    )

    match count:
      case 1:
        ym = data
      case 2: 
        y1m = data
      case 3: 
        y2m = data

    count += 1

  ym = ym.mul(0.5)
  y1m = y1m.mul(0.25)
  y2m = y2m.mul(0.25)

  final = ym.reset_index(level='game_year', drop=True).add(y1m.reset_index(level='game_year', drop=True).add(y2m.reset_index(level='game_year', drop=True)))

  print(final)
  final.to_csv(f'RE24 Matrix - {year}.csv')

re_matrix(2023)