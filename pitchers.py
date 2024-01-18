import pandas as pd
import pybaseball as pb

pitches = pd.read_csv('data\pitchdata.csv')
PA = pd.read_csv('data\PA outcomes.csv').set_index('events')

# function to identify bad calls
def bad_call(zone, call):
    if zone in range(1, 9) and call == "B":
        return 1
    elif zone in range(11, 14) and call == "S":
        return 1
    else:
        return None

# function to generate the counts created/avoided by the bad calls
def bad_call_counts(balls, strikes, call, n=0):
    if n == 0: # called counts
        if call == 'B':
            return f'{balls + 1}-{strikes}'
        elif call == 'S':
            return f'{balls}-{strikes + 1}'
    else: # missed counts
        if call == 'B':
            return f'{balls}-{strikes + 1}'
        elif call == 'S':
            return f'{balls + 1}-{strikes}'

# drop unnecessary columns and sort
pitches = pd.concat([pitches['game_pk'], pitches['inning'], pitches['inning_topbot'], pitches['balls'], pitches['strikes'], pitches['at_bat_number'], pitches['pitcher'], pitches['zone'], pitches['type']], axis=1)
pitches['zone'] = pitches['zone'].replace(0.0, None).dropna()
pitches['count'] = pitches['balls'].astype(str).str.cat(pitches['strikes'].astype(str), sep='-')
pitches = pitches.set_index(['game_pk', 'inning', 'inning_topbot', 'at_bat_number', 'count'], drop=True).sort_index(level=['game_pk', 'inning', 'inning_topbot', 'at_bat_number', 'count'], ascending=[False, True, False, True, True])

# identify and only keep bad calls
pitches['bad_call'] = pitches.apply(lambda x: bad_call(x['zone'], x['type']), axis=1)
pitches = pitches.dropna(subset='bad_call')

# unpivot count data, return to og format
counts = pd.read_csv('data\counts.csv').set_index('balls').rename_axis('strikes', axis='columns')
counts = pd.melt(counts, ignore_index=False).reset_index()
counts['count'] = counts['balls'].astype(str).str.cat(counts['strikes'].astype(str), sep='-')
counts = counts.drop(['balls', 'strikes'], axis=1).set_index(['count'])['value'].to_dict()

# generate called and missed counts and their corresponding run expectancy values
pitches['called'] = pitches.apply(lambda x: bad_call_counts(x['balls'], x['strikes'], x['type']), axis=1)
pitches['missed'] = pitches.apply(lambda x: bad_call_counts(x['balls'], x['strikes'], x['type'], n=1), axis=1)
pitches['called_value'] = pitches['called'].map(lambda x: counts.get(x, x))
pitches['missed_value'] = pitches['missed'].map(lambda x: counts.get(x, x))

# account for edge cases - strikeouts and walks
pitches.loc[pitches['called_value'].astype(str).str.contains('-3'), 'called_value'] = PA.iat[27, 0]
pitches.loc[pitches['missed_value'].astype(str).str.contains('-3'), 'missed_value'] = PA.iat[27, 0]
pitches.loc[pitches['called_value'].astype(str).str.contains('4-'), 'called_value'] = PA.iat[31, 0]
pitches.loc[pitches['missed_value'].astype(str).str.contains('4-'), 'missed_value'] = PA.iat[31, 0]
pitches['called_value'] = pitches['called_value'].astype('float64')
pitches['missed_value'] = pitches['missed_value'].astype('float64')

# find change in value caused by the call
pitches['delta'] = pitches['called_value'] - pitches['missed_value']

print(pitches)