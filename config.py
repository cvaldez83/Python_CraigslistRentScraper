import os
import pathlib

""" Files and Directories """
abs_path = pathlib.Path(__file__).parent.absolute()
path_to_datadir = os.path.join(abs_path, 'data')
path_to_logfile = os.path.join(path_to_datadir, 'log.txt')

cities = [
   'sandiego',
   'palmsprings',
   'phoenix'
]
# cities = ['phoenix']
