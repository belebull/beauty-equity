import pandas as pd

CENSUS_CODES = {'B01003_001E': 'total_pop',
                'B03002_003E': 'white_nh',
                'B03002_013E': 'white_h',
                'B03002_004E': 'black_nh',
                'B03002_014E': 'black_h',
                'B03002_005E': 'native_nh',
                'B03002_015E': 'native_h',
                'B03002_006E': 'asian_nh',
                'B03002_016E': 'asian_h',
                'B03002_007E': 'hawaiian_nh',
                'B03002_017E': 'hawaiian_h',
                'B03002_009E': 'other_nh',
                'B03002_018E': 'other_h',
                'B03002_010E': 'biracial_nh',
                'B03002_020E': 'biracial_h',
                'B03002_011E': 'multiracial_nh',
                'B03002_021E': 'multiracial_h',
                'B06011_001E': 'median_income',
                'state': 'state',
                'zip code tabulation area': 'zip_code'}

ETHNICITY_PAIRS = [('white_nh', 'white_h'), ('black_nh', 'black_h'), ('native_nh', 'native_h'), ('asian_nh', 'asian_h'),
                   ('other_nh', 'other_h'), ('biracial_nh', 'biracial_h'), ('multiracial_nh', 'multiracial_h')]

# generate state converter dictionary
STATE_CONVERTER = pd.read_csv('state_converter.csv')
STATE_CONVERTER = STATE_CONVERTER.set_index('state_abbr')
