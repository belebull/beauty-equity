import pandas as pd
import constants as cs
import numpy as np
import os


def classifyByRace(directory_path, data):
    # generate data files for each race
    for race in cs.RACES:
        # identify zip codes and associated data
        race_column = '{race}_percentage'.format(race=race)
        race_zips = data.loc[data[race_column] > 0.6]
        race_zips = race_zips[['zip_code', race_column, 'median_income']]
        race_zips = race_zips.rename(
            {'zip_code': 'zip_code', race_column: 'percentage', 'median_income': 'income'})

        # save data in folder with state if the data frame is not empty
        if not race_zips.empty:
            filename = '{parent_directory}/{race}_zips.csv'.format(
                parent_directory=directory_path, race=race)
            race_zips.to_csv(filename, index=False, header=True)

    return


def classifyByEthnicity(directory_path, data):
    # get lables for race with Latino ethnicities
    latino_labels = [label[1] for label in cs.ETHNICITY_PAIRS]

    # create a column for the percentage of Latino communities
    latino_zips = data[latino_labels]
    data['latino_percentage'] = np.empty(len(data['zip_code']))

    # sum all of the races with Latino ethnicity
    for label in latino_labels:
        data[label] = data[label].astype(int)
        data['latino_percentage'] = data['latino_percentage'] + data[label]

    # calculate percentage across total population
    data['latino_percentage'] = data['latino_percentage']/data['total_pop']

    # calcualte percentage of non-white Latino communities
    data['non_white_latino_percentage'] = data['latino_percentage'] - \
        (data['white_h']/data['total_pop'])

    # remove extra data
    latino_zips = data.loc[data['latino_percentage'] > 0.6]
    latino_zips = latino_zips[['zip_code',
                               'latino_percentage',
                               'non_white_latino_percentage', 'median_income']]

    # save to a seperate file
    if not latino_zips.empty:
        filename = '{parent_directory}/latino_zips.csv'.format(
            parent_directory=directory_path)
        latino_zips.to_csv(filename, index=False, header=True)

    return


def main():
    for state in cs.STATE_CONVERTER.index:
        # get data file for each state
        state_data_file = 'state_data/{state}.csv'.format(state=state)
        state_data = pd.read_csv(state_data_file)

        # create state directory
        state_folder = 'race_by_zips/{state}'.format(state=state)
        if not os.path.isdir(state_folder):
            os.mkdir(state_folder)

        # change the zip codes to strings for easier retrieval
        state_data['zip_code'] = state_data['zip_code'].astype(str)

        # create files for each zip code dominated by a certain race
        classifyByRace(state_folder, state_data)

        # create files for Latino and non-White Latino communities
        classifyByEthnicity(state_folder, state_data)
        print('finished state: ', state)

    return


if __name__ == '__main__':
    main()
