import pathlib
import os
import d

abs_path = pathlib.Path(__file__).parent.absolute()
file_path = os.path.join(abs_path, 'data', 'test.txt')

with open(file_path, 'a') as f:
    f.write('hello')