import pandas as pd
import numpy as np
import requests
from decouple import config


def getDemographics(state_code):
    # set the base url
    base_url = 'https://api.census.gov/data/2019/acs/acs5?get=NAME,B01003_001E,B06011_001E,group(B03002)&for=zip%20code%20tabulation%20area:*&in=state:{state}&key={key}'.format(
        state=state_code, key=config('CENSUS_KEY'))

    # get population and race totals organized by zip code
    response = requests.get(base_url)
    zip_code_data = response.json()

    # create a lookup for useful values
    census_codes = {'B01003_001E': 'total_pop',
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

    # turn into dataframe
    data = pd.DataFrame(zip_code_data[1:], columns=zip_code_data[0])

    # indicate columns to keep
    keep_columns = list(census_codes.keys())
    del data['NAME']  # remove duplicate name column before the for loop

    # remove unnecessary columns
    for column in data.columns:
        # remove columns not indicated to keep
        if column not in keep_columns:
            del data[column]

    # rename columns, set zip code as the index and chane values to int
    data = data.rename(columns=census_codes)
    data = data.set_index('zip_code')
    data = data.astype(int)

    # create percentage columns
    ethnicity_pairs = [('white_nh', 'white_h'), ('black_nh', 'black_h'), ('native_nh', 'native_h'), ('asian_nh', 'asian_h'),
                       ('other_nh', 'other_h'), ('biracial_nh', 'biracial_h'), ('multiracial_nh', 'multiracial_h')]
    for ethnicity in ethnicity_pairs:
        non_hispanic, hispanic = ethnicity
        column_name = non_hispanic[:-2] + 'percentage'
        data[column_name] = (data[non_hispanic] +
                             data[hispanic])/data['total_pop']

    return data


def main():
    # set the state code for Illinois
    state_code = 17
    data = getDemographics(state_code)
    return


if __name__ == '__main__':
    main()
