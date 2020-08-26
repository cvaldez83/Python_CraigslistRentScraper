def Scrape(city):
    """ import get to call a get request on the site """
    from time import sleep
    from time import time
    from random import randint # for scrape throttling
    from warnings import warn
    from requests import get
    from bs4 import BeautifulSoup
    import numpy as np
    import re
    from fp.fp import FreeProxy
#    import os
#    os.mkdir('test')

    def get_proxies():
        print('getting proxies...')
        proxy = FreeProxy(country_id='US').get()
        proxies = {'http': proxy}
        print(f'obtained proxies: {proxies}')
        return proxies

    """ get an initial proxy, hopefully it works thru entire script """
    proxies = get_proxies()

    def get_response(url, proxiess):
        try:
            response = get(url, proxies=proxiess)
        except:
            print('exception code ran for get_response')
            global proxies
            proxies = get_proxies()
            response = get(url, proxies=proxies)
        # while response.status_code != 200:
        #     print(f'response code not 200: {response.status_code}')
        #     print(f'for url {url}')
        #     global proxies
        #     proxies = get_proxies()
        #     response = get(url, proxies=proxies)
        #     resp_code = response.status_code
        print(f'obtained response code: {response.status_code}')
        return response
        

    """ get the first page of apts/hsg for rent in {city} """
    response = get_response(f'https://{city}.craigslist.org/search/apa?hasPic=1&availabilityMode=0&sale_date=all+dates', proxiess=proxies)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    """ find the total number of posts to find the limit of the pagination """
    results_total_soup = html_soup.find('div', class_='search-legend')
    results_total = results_total_soup.find('span', class_='totalcount').text
    results_total = int(results_total)
    print(f'total number of results: results_total = {results_total}')


    """ each page has 119 posts so each new page is defined
        as follows: s=120, s=240, s=360, and so on.
        So we need to step in size 120 in the np.arange function """
    pages = np.arange(0, results_total+1, 120)

    """ initialize variables """
    iterations = 0
    post_datetimes = []
    post_hoods = []
    post_titles = []
    post_addresses = []
    post_property_types = []
    post_bedrooms = []
    post_bathrooms = []
    post_sqfts = []
    post_prices = []
    post_links = []

    for page in pages: # TODO: remove [0:1]

        url_str = ("https://"
                    + city
                    + ".craigslist.org/search/apa?"
                    + "s="
                    + str(page)
                    + "&availabilityMode=0"
                    + "&hasPic=1")
        print(f'page: {url_str}')

        """ get response from url_str and throttle requests"""
        response = get_response(url_str, proxiess=proxies)
        sleep(randint(1,5))

        # """ throw warning for status codes that are not 200 """
        # if response.status_code != 200:
        #     warn(f'Request: {requests}; Status code: {response.status_code}')
        
        """ define the html text """
        html_soup = BeautifulSoup(response.text, 'html.parser')

        """ define the posts """
        posts_soup = html_soup.find_all('li', class_='result-row')

        """ loop thru each post to scrape its data """
        for post in posts_soup: # TODO: remove [0:2]

            if post.find('span', class_='result-hood') is not None:

                """ grab the datetime element 0 for date and 1 for time """
                post_datetime = post.find('time', class_='result-date')['datetime']
                

                """ grab the neighborhoods """
                post_hood = post.find('span', class_='result-hood').text
                

                """ grab post title """
                post_title = post.find('a', class_='result-title hdrlnk').text
                

                """ grab post link """
                post_link = post.find('a', class_='result-title hdrlnk')['href']
                # print(post_link)

                """ grab post prices """
                post_price = post.find('span', class_='result-price').text
                """ removes the \n whitespace from each side, removes the $ and comma symbols, and turns it into an int """
                post_price = post_price.strip().replace("$", "")
                post_price = post_price.replace(",","")
                # print(post_price)

                """ Dive deeper by scraping each post_link """

                response_deepdive = get_response(post_link, proxiess=proxies)
                if response_deepdive.status_code == 404:
                    print('response code 404, continuing loop and getting new proxies')
                    continue
                sleep(randint(1,5))

                html_soup_deepdive = BeautifulSoup(response_deepdive.text, 'html.parser')
    
                """ grab property address from deep dive"""
                post_address = html_soup_deepdive.find('div', class_='mapaddress')
                
                """ grab & split text inside attr_grp (may contain Ba, Br, sqft) """
                attr_group = html_soup_deepdive.find('p', class_='attrgroup')
                if attr_group is not None:
                    attr_group = attr_group.text

                """ grab bedrooms using regex from deep dive"""
                if attr_group is not None and re.findall("\dBR",attr_group):
                # if 'BR' in attr_group:
                    post_bedroom = re.findall("\dBR",attr_group)[0]
                    post_bedroom = int(post_bedroom[:-2])
                    # print('post_bedroom')
                    # print(post_bedroom)
                else:
                    print(f'couldnt find # of bedrooms: {post_link}')
                    post_bedroom = np.nan

                """ grab bathrooms using regex from deep dive """
                if attr_group is not None and re.findall("\dBa",attr_group):
                # if 'Ba' in attr_group:
                    post_bathroom = re.findall("(\d.\dBa|\dBa)",attr_group)[0]
                    post_bathroom = float(post_bathroom[:-2])
                    
                    # print('post_bathroom')
                    # print(post_bathroom)
                else:
                    print(f'couldnt find # of bathrooms: {post_link}')
                    post_bathroom = np.nan

                """ grab squarefootage using regex from deep dive """
                if attr_group is not None and re.findall("\d*ft",attr_group):
                # if 'ft2' in attr_group:
                    post_sqft = re.findall("\d*ft",attr_group)[0]
                    post_sqft = int(post_sqft[:-2])
                    # print('sqft')
                    # print(post_sqft)
                else:
                    print(f'couldnt find squarefootage: {post_link}')
                    post_sqft = np.nan

                """ grab property type if available """
                attr_group = html_soup_deepdive.findAll('p', class_='attrgroup')
                # print(attr_group)
                if any("apartment" in s.text for s in attr_group):
                    post_property_types.append('apartment')
                elif any("house" in s.text for s in attr_group):
                    post_property_types.append('house')
                elif any("duplex" in s.text for s in attr_group):
                    post_property_types.append('duplex')
                elif any("condo" in s.text for s in attr_group):
                    post_property_types.append('condo')
                else:
                    post_property_types.append('other')
                
                post_datetimes.append(post_datetime)
                post_hoods.append(post_hood)
                post_titles.append(post_title)
                post_links.append(post_link)
                post_prices.append(post_price)
                if post_address is not None:
                    post_addresses.append(post_address.text)
                else:
                    print(f'couldnt find address: {post_link}')
                    post_addresses.append(np.nan)
                post_bedrooms.append(post_bedroom)
                post_bathrooms.append(post_bathroom)
                post_sqfts.append(post_sqft)
                
    
        iterations += 1
        print("Page " + str(iterations) + " scraped successfully!")
    print("\nScrape complete!")
    return {'datetimes': post_datetimes,
            'neighborhoods': post_hoods,
            'titles': post_titles,
            'addresses': post_addresses,
            'property_types': post_property_types,
            'bedrooms': post_bedrooms,
            'bathrooms': post_bathrooms,
            'sqfts': post_sqfts,
            'prices': post_prices,
            'links': post_links
            }
if __name__=="__main__":
    print('you need to import scrape function')
