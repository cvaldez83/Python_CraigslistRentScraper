from config import cities

import pathlib
import os
abs_path = pathlib.Path(__file__).parent.absolute()
print(abs_path)
file1 = open(os.path.join(abs_path, 'data', "test.txt"), "a")
file1.write(str(abs_path))
file1.close()


for city in cities:
    
    """ Scrape craigslist """
    from scraper import Scrape
    dict_scrape_results = Scrape(city)

    file1 = open(os.path.join(abs_path, 'data', "test.txt"), "a")
    file1.write(f'scrape complete for {city}\n' )
    file1.close()

    """ Create dataframe & clean """
    import pandas as pd
    df = pd.DataFrame(dict_scrape_results)
    df.set_index('datetimes', inplace=True)
    from pandasFuncs import CleanDF
    df = CleanDF(df)

    file1 = open(os.path.join(abs_path, 'data', "test.txt"), "a")
    file1.write(f'df cleaning complete for {city}\n' )
    file1.close()

    """ Save clean dataframe to individual csv file"""
    from time import time, localtime
    import os
    todayTime = localtime(time())
    todayDate = f'{todayTime.tm_year}-{todayTime.tm_mon}-{todayTime.tm_mday}'

    file1 = open(os.path.join(abs_path, 'data', "test.txt"), "a")
    file1.write(f'about to save file for {city}\n' )
    file1.close()

    df.to_csv(os.path.join(abs_path, 'data', f'cleaned_{city}_{todayDate}.csv'))

    file1 = open(os.path.join(abs_path, 'data', "test.txt"), "a")
    file1.write(f'saved file for {city}\n' )
    file1.close()

    """ Concatenate df to main.csv or create a main.csv if none exists"""
    if not os.path.isfile(os.path.join(abs_path, 'data', f'main_{city}.csv')):
        df.to_csv(os.path.join(abs_path, 'data', f'main_{city}.csv'))
    else:
        df_main = pd.read_csv(os.path.join(abs_path,'data',f'main_{city}.csv'), index_col='datetimes')
        # print(df_main)
        df_main = pd.concat([df_main, df])
        # print('after concat')
        # print(df_main)
        """ may as well clean the main df for duplicate links """
        df_main = CleanDF(df_main)
        df_main.to_csv(os.path.join(abs_path, 'data', f'main_{city}.csv'))

