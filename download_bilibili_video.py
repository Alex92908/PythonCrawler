"""
module docstring for download video urls
from Bilibili_webpage
"""
import json
import csv
import time
import urllib.parse
import os.path
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
# from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def save_content_txt(contents, need_close=True):
    """
    save content text
    :param contents:
    :param need_close:
    :return:
    """
    with open("B站视频资料.txt", "a") as file:
        for content in contents:
            json.dump(content, file, ensure_ascii=False, indent=2)
            file.write("\n")
        if need_close:
            file.close()


class SearchOnBili:
    """
    SearchOnBili docstring
    """
    def __init__(self, keyword):
        """
        init
        :param keyword:
        """

        # PhantomJS() Selenium support for PhantomJS has been deprecated, please use headless
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.PhantomJS()
        if len(keyword) > 0:
            keyword = urllib.parse.quote(keyword, encoding='utf-8')
        self._url = "https://search.bilibili.com/all?keyword=" + keyword
        self._keyword = keyword

    @property
    def url(self):
        """
        @property
        :return:
        """
        return self._url

    def start_driver_and_begin_download(self, url):
        """
        init driver and begin download
        :param url:
        :return:
        """
        self.driver.get(url)
        contents = self.get_contents()
        print("开始爬取url= ", url, "的资源")
        print("开始爬取第一页")
        self.save_content_csv(contents, need_close=False)
        # noinspection PyBroadException
        try:
            while self.driver.find_element_by_xpath(
                    '//li[@class="page-item next"]'):
                next_btn = self.driver.find_element_by_xpath(
                    '//li[@class="page-item next"]').find_element_by_xpath("./button")
                print("开始爬取下一页")
                ActionChains(self.driver).move_to_element(next_btn).perform()
                if self.driver.find_element_by_xpath('//div[@class="close"]'):
                    close_btn = self.driver.find_element_by_xpath(
                        '//div[@class="close"]')
                    tip_style = self.driver.find_element_by_xpath(
                        '//div[@class="lt-row"]').get_attribute("style")
                    if tip_style.find("display: none;") == -1:
                        close_btn.click()

                next_btn.click()
                contents_new = self.get_contents()
                self.save_content_csv(contents_new, need_close=False)
        except NoSuchElementException:
            self.save_content_csv([], need_close=True)
            print("爬取完成url= ", url, "的资源")

    def get_contents(self):
        """
        get content of element
        :return:
        """
        time.sleep(3)
        li_list = self.driver.find_elements_by_xpath(
            '//ul[@class="video-list clearfix"]/li')
        contents = []
        for li_item in li_list:  # 遍历所有项
            item = {}
            li_a_data = li_item.find_element_by_xpath('./a')
            item["title"] = li_a_data.get_attribute("title")  # 获取视频名字
            item["url"] = li_a_data.get_attribute("href")
            contents.append(item)
        return contents

    def save_content_csv(self, contents, need_close=True):
        """
        save content to csv
        :param contents:
        :param need_close:
        :return:
        """
        path = r"./%s.csv" % self._keyword
        # if not os.path.exists(path):
        with open(path, "a", encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            # csv_writer.writerow(("title", "url"))
            for content in contents:
                csv_writer.writerow((content["title"], content["url"]))
            if need_close:
                file.close()
                if os.path.exists(path):
                    # noinspection PyBroadException
                    try:
                        new_path = urllib.parse.unquote(path)
                        if new_path != path:
                            os.rename(path, new_path)
                            if os.path.exists(path):
                                os.remove(path)
                    except NotImplementedError:
                        print("文件名替换失败")
                else:
                    print("not exists")

    def run(self):
        """
        run driver
        :return:
        """
        self.start_driver_and_begin_download(self.url)
        print("爬取完成")


if __name__ == '__main__':
    def input_method():
        """
        input keyword
        :return:
        """
        keyword = input("请输入查找关键字：")
        if len(keyword) > 0:
            bili = SearchOnBili(keyword)
            bili.run()
        else:
            input_method()
    while True:
        input_method()
