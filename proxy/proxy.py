# coding: utf-8
from .proxy_parse import ParseProxy
from settings.orm_settings import *
from .models import FreeProxy


class Proxy(object):
    """ Нужен для получения адреса прокси
    Работает c экземпляром класса ParseProxy
    """
    def __init__(self):
        """
        Проверяем достаточно ли прокси, если нет, то ищем новые
        """
        if FreeProxy.objects.filter(working=True).count() < 5:
            parser = ParseProxy(url=u'http://foxtools.ru/Proxy', ip_xpath="//tr[@class]//td[2]/text()",
                                port_xpath="//tr[@class]//td[3]/text()")
            parser.parse()

    def delete_proxies(self):
        FreeProxy.objects.all().delete()
        print "Все прокси из Базы Данных были удалены"

    def get_proxy(self):
        """ Возвращает прокси, который реже использовался
        :return: адрес proxy
        """
        try:
            proxy = FreeProxy.objects.filter(working=True).order_by('number_of_uses')[0]
            proxy.number_of_uses += 1
            proxy.save()
            return proxy.ip
        except IndexError:
            return False
