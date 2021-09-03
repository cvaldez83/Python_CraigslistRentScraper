from datetime import datetime
import pandas as pd
import logging
logger = logging.getLogger('myapp')

def CleanDF(data_frame):
    df = data_frame
    logger.info(f'number of rows for uncleaned df: {len(df.index)}')

    """ drop duplicate URLs, post titles, and addresses """
    df = df.drop_duplicates(subset=['links'])
    df = df.drop_duplicates(subset=['titles'])
    df = df.drop_duplicates(subset=['addresses'])

    logger.info(f'number of rows after dropping duplicate links: {len(df.index)}')

    """ drop rows with nans for number of bedrooms """
    df = df.dropna(subset = ['bedrooms'])
    logger.info(f'number of rows after dropping na for bedrooms: {len(df.index)}')

    """ make bedrooms to a float (since np.nan is a float too) """
    df['bedrooms'] = df['bedrooms'].apply(lambda x: float(x))

    """ convert datetime string into datetime object to be able to work with it """
    df.index = pd.to_datetime(df.index)
    # df['datetimes'] = pd.to_datetime(df['datetimes']) # Works if datetimes column is not the index
    
    """ replace NaN values in neighborhoods column with 'none specified' """
    df['neighborhoods'] = df['neighborhoods'].fillna('none specified')

    """ remove parenthesis from neighborhoods """
    # df['neighborhoods'] = df['neighborhoods'].map(lambda x: x.lstrip('(').rstrip(')'))
    df['neighborhoods'] = df['neighborhoods'].map(lambda x: x.replace('(','').replace(')','').strip())
    """ title case them """
    df['neighborhoods'] = df['neighborhoods'].str.title()

    # """ use datetimes column as index """
    # df.set_index('datetimes', inplace=True)

    return df



