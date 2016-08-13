# coding: utf-8
from lxml import html
import requests
from .models import FreeProxy
from django.core.exceptions import ObjectDoesNotExist


class ParseProxy(object):
    def __init__(self, url, ip_xpath, port_xpath=False):
        """
        :param url: ссылка на ресурс с прокси
        :param ip_xpath: путь к нахождению элемента с ip
        :param port_xpath: путь к нахождению элемента с port, указывается если port отделен от ip
        """
        self.url = url
        self.ip_xpath = ip_xpath
        self.port_xpath = port_xpath
        self.proxy_list = []

    def parse(self):
        """ Ищем прокси по заданным в конструкторе параметрам
        :return: None
        """
        print 'Поиск прокси ...'
        req = requests.get(self.url)
        content = html.fromstring(req.content)
        self.proxy_list = content.xpath(self.ip_xpath)
        if self.port_xpath:
            port_list = content.xpath(self.port_xpath)
            i = 0
            for port in port_list:
                self.proxy_list[i] += ":{}".format(port)
                i += 1
        self._save()
        self._validate()

    def _save(self):
        """ Сохраняет найденные прокси, которых еще нет в Таблице
        :return: None
        """
        db_proxies = FreeProxy.objects.all()
        # проверяем есть ли найденные прокси в таблице
        for db_proxy in db_proxies:
            for proxy in self.proxy_list:
                if db_proxy.ip == proxy:
                    self.proxy_list.remove(proxy)
        # сохраняем оставшиеся прокси
        for proxy in self.proxy_list:
            new_proxy = FreeProxy(ip=proxy)
            new_proxy.save()

    def _validate(self):
        """ Проверяет работают ли прокси.
        :return: None
        """
        for proxy in self.proxy_list:
            proxy_url = "http://" + proxy
            try:
                req = requests.get('https://ya.ru', proxies=proxy_url)
                if req.status_code != 200:
                    self._dont_working(proxy)
            except requests.ConnectionError:
                self._dont_working(proxy)
                continue

    def _dont_working(self, proxy):
        """ Изменяем запись в бд если прокси не работает
        :param proxy: прокси
        :return: Boolean
        """
        try:
            bad_proxy = FreeProxy.objects.get(ip=proxy)
        except ObjectDoesNotExist:
            return False
        bad_proxy.working = False
        bad_proxy.save()
        return True
