# website: https://github.com/JaredLGillespie/proxyscrape

from proxyscrape import create_collector
collector = create_collector('my-collector', 'http')

proxy = collector.get_proxy()
# proxy = collector.get_proxy({'code': 'us'})
# proxy = collector.get_proxy({'country': 'canada'})
print(proxy.host)