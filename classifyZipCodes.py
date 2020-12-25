import pandas as pd


def main():
    state_code = 'IL'
    state_data_file = 'state_data/{state}.csv'.format(state=state_code)
    state_data = pd.read_csv(state_data_file)

    # identify predominately white communities
    white_third_quartile = state_data.white_percentage.describe()['75%']
    white_percentage_threshold = 0.6 if 0.6 > white_third_quartile else white_third_quartile
    white_zips = state_data.loc[state_data['white_percentage']
                                >= white_percentage_threshold]

    # idenitfy predominately black communities
    black_third_quartile = state_data.black_percentage.describe()['75%']
    black_percentage_threshold = 0.6 if 0.6 > black_third_quartile else black_third_quartile
    black_zips = state_data.loc[state_data['black_percentage']
                                >= black_percentage_threshold]

    return


if __name__ == '__main__':
    main()
