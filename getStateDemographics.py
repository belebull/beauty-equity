import pandas as pd
import numpy as np
import requests
import constants as cs
from decouple import config


def get_raw_data(state_code):
    # set the base url
    state_code = '{0:0=2d}'.format(state_code)
    base_url = 'https://api.census.gov/data/2019/acs/acs5?get=NAME,B01003_001E,B06011_001E,group(B03002)&for=zip%20code%20tabulation%20area:*&in=state:{state}&key={key}'.format(
        state=state_code, key=config('CENSUS_KEY'))

    # get population and race totals organized by zip code
    response = requests.get(base_url)
    zip_code_data = response.json()

    # turn into dataframe
    data = pd.DataFrame(zip_code_data[1:], columns=zip_code_data[0])

    return data


def clean_data(data):
    # indicate columns to keep
    keep_columns = list(cs.CENSUS_CODES.keys())
    del data['NAME']  # remove duplicate name column before the for loop

    # remove unnecessary columns
    for column in data.columns:
        # remove columns not indicated to keep
        if column not in keep_columns:
            del data[column]

    # rename columns, set zip code as the index and chane values to int
    data = data.rename(columns=cs.CENSUS_CODES)
    data = data.set_index('zip_code')
    data = data.astype(int)

    # create percentage columns
    for ethnicity in cs.ETHNICITY_PAIRS:
        non_hispanic, hispanic = ethnicity
        column_name = non_hispanic[:-2] + 'percentage'
        data[column_name] = (data[non_hispanic] +
                             data[hispanic])/data['total_pop']

    return data


def main():

    for state in cs.STATE_CONVERTER.index:
        # set the state code for Illinois
        state_code = cs.STATE_CONVERTER.loc[state]['state_id']
        raw_data = get_raw_data(state_code)
        data = clean_data(raw_data)

        # generate data file for the state
        data_file_path = 'state_data/{state}.csv'.format(state=state)
        data.to_csv(data_file_path, index=True, header=True)
        print('Just finished state: ', state)
    return


if __name__ == '__main__':
    main()
