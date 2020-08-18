from config import cities

for city in cities:
    
    """ Scrape craigslist """
    from scraper import Scrape
    dict_scrape_results = Scrape(city)

    """ Create dataframe & clean """
    import pandas as pd
    df = pd.DataFrame(dict_scrape_results)
    df.set_index('datetimes', inplace=True)
    from pandasFuncs import CleanDF
    df = CleanDF(df)

    """ Save clean dataframe to individual csv file"""
    from time import time, localtime
    import os
    todayTime = localtime(time())
    todayDate = f'{todayTime.tm_year}-{todayTime.tm_mon}-{todayTime.tm_mday}'
    df.to_csv(os.path.join(os.getcwd(), 'data', f'cleaned_{city}_{todayDate}.csv'))

    """ Concatenate df to main.csv or create a main.csv if none exists"""
    if not os.path.isfile(os.path.join(os.getcwd(), 'data', f'main_{city}.csv')):
        df.to_csv(os.path.join(os.getcwd(), 'data', f'main_{city}.csv'))
    else:
        df_main = pd.read_csv(os.path.join(os.getcwd(),'data','main.csv'), index_col='datetimes')
        print(df_main)
        df_main = pd.concat([df_main, df])
        print('after concat')
        print(df_main)
        """ may as well clean the main df for duplicate links """
        df_main = CleanDF(df_main)
        df_main.to_csv(os.path.join(os.getcwd(), 'data', 'main.csv'))

