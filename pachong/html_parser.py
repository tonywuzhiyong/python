#!/usr/bin/env python
#encoding:utf8
from bs4 import  BeautifulSoup
import re
import urlparse

class HtmlParser(object):
    def parse(self,page_url,html_content):
        if page_url is None or html_content is None:
            return

        soup = BeautifulSoup(html_content,"html.parser",from_encoding="utf-8")
        new_urls = self._get_new_urls(page_url,soup)

        new_data = self._get_new_data(page_url,soup)

        return new_urls,new_data

    def _get_new_urls(self,page_url,soup):
        new_urls = set()
        links = soup.find_all('a',href=re.compile(r"/item/.+"))
        for link in links:
            new_url = link['href']
           # new_full_url = urlparse.urljoin(page_url,new_url)
            new_full_url = r"http://baike.baidu.com%s"%new_url
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self,page_url,soup):
        #res_data = set() 
        res_data = {}           
        res_data["url"] =  page_url

        #标题  <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = soup.find('dd',class_="lemmaWgt-lemmaTitle-title").find("h1")
        res_data["title"] = title_node.get_text()

        #简介        
        summary_node = soup.find('div',class_="lemma-summary")
        res_data["summary"] = summary_node.get_text()   

        return res_data