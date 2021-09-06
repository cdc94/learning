import os
import time
from time import sleep
import urllib.parse

import requests  # 版本不能太高，使用的是2.20版本就没有问题了，否则的话会报错。但是使用selenium就没有这些问题了
import urllib.request as request
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver.edge.options import Options


# url = 'https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q=ambient+backscatter&btnG='


# proxies = {'http': 'http://127.0.0.1:7890',  # 18810566137@163.com:Delirium2528@
#            'https': 'https://127.0.0.1:7890'}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                          'Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
#            'Referer': 'https://scholar.google.com.hk/'}
# opener = request.build_opener(request.ProxyHandler(proxies))
# request.install_opener(opener)
# response = requests.get(url=url, headers=headers, proxies=proxies)
# response.encoding = 'utf-8'
# html = response.text
# print(html)


def buildEdgeDriver():
    # 创建一个在后台运行的EdgeDriver
    edge_option = EdgeOptions()
    edge_option.use_chromium = True
    edge_option.add_argument('headless')
    driver = Edge(options=edge_option)
    return driver


# 获取BibTex并保存到一个文件
def getBibTexSave(urls):
    base_dir = 'output_bibtex/'
    filename = base_dir + "BibTeX_" + time.strftime('%Y_%m_%d_%H%M%S', time.localtime(time.time())) + ".txt"
    driver = buildEdgeDriver()
    for url in urls:
        driver.get(url)
        driver.find_element_by_class_name('gs_or_cit.gs_nph').click()
        sleep(3)
        s = driver.find_element_by_class_name('gs_citi')
        if s.text == 'BibTeX':
            hr = s.get_attribute('href')
            driver.get(hr)
            bib = driver.find_element_by_xpath("//*").text
            # print(bib)
            with open(filename, 'a+') as fs:
                fs.write(bib + '\n')
    driver.quit()


# 获取CiteText并保存到一个文件
def getCiteTextSave(urls, scope=0):
    citeType = {1: 'GB/T 7714', 2: 'MLA', 3: 'APA', 0: ''}
    base_dir = 'output_GBT7714/'
    filename = base_dir + "GBT7714_" + time.strftime('%Y_%m_%d_%H%M%S', time.localtime(time.time())) + ".txt"
    driver = buildEdgeDriver()
    citeContent = ''
    for url in urls:
        driver.get(url)
        driver.find_element_by_class_name('gs_or_cit.gs_nph').click()
        sleep(3)
        ss = driver.find_element_by_class_name('gs_cith')
        if scope == 0:
            citeContent = driver.find_element_by_xpath('//*').text
        if scope == 1:
            citeContent = driver.find_element_by_class_name('gs_citr').text
        with open(filename, 'a+') as fs:
            fs.write(citeContent)
            fs.write('\n')
            fs.write('====================================================')
            fs.write('\n')
    driver.quit()


# 解析一下文件，并组合生成url列表
def createUrls(filename):
    urls = []
    urlHead = 'https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q='
    urlTail = '%20&btnG='
    with open(filename) as f:
        line = f.readline()
        while line:
            # 存在句内回车时，进行拼接
            nextLine = f.readline()
            while line != '\n' and nextLine and nextLine != '\n':   # 必须要对nextLine进行额外的判断，是否到文末('')
                line += nextLine
                nextLine = f.readline()

            if line != '\n':
                url = urlHead + urllib.parse.quote(line) + urlTail
                urls.append(url)
            line = nextLine
    return urls

