# website: https://pypi.org/project/free-proxy/

from fp.fp import FreeProxy

# proxy = FreeProxy().get()
proxy = FreeProxy(country_id='US').get()