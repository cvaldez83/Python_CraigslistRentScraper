from datetime import datetime
import pandas as pd

def CleanDF(data_frame):
    df = data_frame
    print(f'number of rows for uncleaned df: {len(df.index)}')

    """ drop duplicate URLs """
    df = df.drop_duplicates(subset=['links'])
    print(f'number of rows after dropping duplicate links: {len(df.index)}')

    """ drop rows with nans for number of bedrooms """
    df = df.dropna(subset = ['bedrooms'])
    print(f'number of rows after dropping na for bedrooms: {len(df.index)}')

    """ make bedrooms to a float (since np.nan is a float too) """
    df['bedrooms'] = df['bedrooms'].apply(lambda x: float(x))

    """ convert datetime string into datetime object to be able to work with it """
    df.index = pd.to_datetime(df.index)
    # df['datetimes'] = pd.to_datetime(df['datetimes']) # Works if datetimes column is not the index

    """ remove parenthesis from neighborhoods """
    # df['neighborhoods'] = df['neighborhoods'].map(lambda x: x.lstrip('(').rstrip(')'))
    df['neighborhoods'] = df['neighborhoods'].map(lambda x: x.replace('(','').replace(')','').strip())
    """ title case them """
    df['neighborhoods'] = df['neighborhoods'].str.title()

    # """ use datetimes column as index """
    # df.set_index('datetimes', inplace=True)

    return df



