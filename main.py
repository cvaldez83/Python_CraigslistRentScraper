import os
import pathlib

from config import cities
from config import path_to_datadir
from logScript import setup_custom_logger
logger = setup_custom_logger('myapp')

for city in cities:
    
    """ Scrape craigslist """
    from scraper import Scrape
    logger.info(f'scrape started for {city}')
    dict_scrape_results = Scrape(city)
    logger.info(f'scrape complete for {city}')

    """ Create dataframe & clean """
    import pandas as pd
    df = pd.DataFrame(dict_scrape_results)
    df.set_index('datetimes', inplace=True)
    from pandasFuncs import CleanDF
    logger.info(f'cleaning df for {city}')
    df = CleanDF(df)
    logger.info(f'cleaning complete')
    

    """ Save clean dataframe to individual csv file"""
    # from time import time, localtime
    # import os
    # todayTime = localtime(time())
    # todayDate = f'{todayTime.tm_year}-{todayTime.tm_mon}-{todayTime.tm_mday}'
    # logger.info(f'saving file for {city}\n')
    # df.to_csv(os.path.join(abs_path, 'data', f'cleaned_{city}_{todayDate}.csv'))
    # logger.info(f'saved file for {city}\n')

    """ Concatenate df to main.csv or create a main.csv if none exists"""
    path_to_main_csv_file = os.path.join(path_to_datadir, f'main_{city}.csv')
    if not os.path.isfile(path_to_main_csv_file):
        df.to_csv(path_to_main_csv_file)
    else:
        logger.info(f'reading main csv for {city} and assigning to df_main')
        df_main = pd.read_csv(path_to_main_csv_file, index_col='datetimes')

        logger.info(f'concatenating df with df_main for {city}')
        df_main = pd.concat([df_main, df])

        """ may as well clean the main df for duplicate links """
        logger.info(f'cleaning df_main for {city}')
        df_main = CleanDF(df_main)
        logger.info(f'cleaning complete')
        logger.info(f'saving df_main to csv')
        df_main.to_csv(path_to_main_csv_file)
    logger.info(f'{city.upper()} HAS BEEN COMPLETED')

