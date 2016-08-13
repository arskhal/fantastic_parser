# coding: utf-8
from lxml import html
import requests
from settings.orm_settings import *
from .models import Site


class FantasticParse(object):
    """ Парсит поисковую выдачу яндекс.
    Использует прокси, чтоб не попасть в бан. Так же на вход нужны запрос и количество страниц
    """
    def __init__(self, proxy, query, pages_count):
        """
        :param proxy: прокси
        :param query: запрос, по которому будет осуществляться поиск
        :param pages_count: количество страниц,  которые будут обрабатываться
        """
        self.proxy = proxy
        self.query = query
        self.pages_count = pages_count
        # удаляем ранее внесенные записи
        Site.objects.all().delete()

    def parse(self):
        """ Парсит поисковую выдачу и сохраняет найденные данные
        :return: None
        """
        print 'Парсим Яндекс по запросу "Фантастика" '
        proxy_url = "http://" + self.proxy
        for page in range(0, self.pages_count):
            req = requests.get('https://yandex.ru/search/?text={0}&p={1}'.format(self.query, page), proxies=proxy_url)
            content = html.fromstring(req.content)
            elements = content.xpath("//h2[@class='serp-item__title']/a[@href]")
            for element in elements:
                title = element.text_content()
                url = element.get('href')
                site = Site(title=title, url=url, page=page)
                site.save()

    def __str__(self):
        """ Выводит сохраненные данные
        :return: str
        """
        sites_in_page_1 = Site.objects.filter(page=0)
        sites_in_page_2 = Site.objects.filter(page=1)
        sites_in_page_3 = Site.objects.filter(page=2)
        sites_list = [sites_in_page_1, sites_in_page_2, sites_in_page_3]
        page = 1
        number = 1
        text = u''
        for sites in sites_list:
            text += u'#'*140 + u'\n'
            text += u'# страница №{0}'.format(page) + u' '*126 + u'#\n'
            text += u'#' + u' '*138 + u'#\n'
            for site in sites:
                part = u'#  {0}) {1} -> {2}'.format(number, site.title, site.url)
                space_num = 139 - len(part)
                text += part + u' '*space_num + u'#\n'
                number += 1
            page += 1
        text += u'#' + u' '*138 + u'#\n'
        text += u'#'*140 + u'\n'
        return text.encode('utf-8')
