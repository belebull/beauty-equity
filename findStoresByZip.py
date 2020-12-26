import pandas as pd
import requests
import os
from selenium import webdriver


def findTarget(zip_code):
    hasTarget = False
    url = 'https://www.target.com/store-locator/find-stores/{zip_code}'.format(
        zip_code=zip_code)

    # set up selenium
    path = '/Users/beleiciabullock/beauty-equity/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=path, chrome_options=options)
    generated_zips = []

    driver.get(url)
    addresses = driver.find_elements_by_xpath(
        '//a[@data-test="@store-locator/StoreAddress"]')
    for address in addresses:
        curr_zip = address.text[-10:-5]
        generated_zips.append(curr_zip)

    if str(zip_code) in generated_zips:
        hasTarget = True

    return hasTarget


def main():
    state_code = 'IL'
    data_path = 'race_by_zips/{state}'.format(state=state_code)

    races = [race[:-9] for race in os.listdir(data_path)]
    zip_code = '60429'
    hasTarget = findTarget(zip_code)
    return


if __name__ == '__main__':
    main()
