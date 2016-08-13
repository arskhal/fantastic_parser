# coding: utf-8
from parse.parse import FantasticParse
from proxy.proxy import Proxy
from settings.orm_settings import *
from proxy.models import FreeProxy
import requests
from sys import argv


if __name__ == "__main__":
    if len(argv) >= 2:
        if argv[1] == 'delete_proxies':
            delete_proxies = Proxy()
            delete_proxies.delete_proxies()

    proxy_object = Proxy()
    proxy = proxy_object.get_proxy()
    parse = FantasticParse(proxy=proxy, query='Фантастика', pages_count=3)
    try:
        parse.parse()
    except requests.ConnectionError:
        FreeProxy.objects.filter(ip=proxy).update(working=False)
        proxy = proxy_object.get_proxy()
        parse = FantasticParse(proxy=proxy, query='Фантастика', pages_count=3)
    print parse
