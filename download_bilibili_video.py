from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import json
import csv
import time
import urllib.parse
import os.path



class Search_On_Bili(object):

    def __init__(self, keyword):
        # PhantomJS() Selenium support for PhantomJS has been deprecated, please use headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.br = webdriver.Chrome(options=chrome_options)
        # self.br = webdriver.Chrome()
        if len(keyword) > 0:
            keyword = urllib.parse.quote(keyword, encoding='utf-8')
        self._url = "https://search.bilibili.com/all?keyword=" + keyword
        self._keyword = keyword

    @property
    def url(self):
        return self._url

    def start_driver_and_begin_download(self, url):
        self.br.get(url)
        print("开始爬取url= ",url, "的资源")
        print("开始爬取第一页")
        contents = self.getContents()
        self.save_content_csv(contents, need_close=False)

        try:
            while self.br.find_element_by_xpath('//li[@class="page-item next"]'):
                next_btn = self.br.find_element_by_xpath('//li[@class="page-item next"]').find_element_by_xpath(
                    "./button")
                print("开始爬取下一页")
                ActionChains(self.br).move_to_element(next_btn).perform()
                if self.br.find_element_by_xpath('//div[@class="close"]'):
                    close_btn = self.br.find_element_by_xpath('//div[@class="close"]')
                    tip_style = self.br.find_element_by_xpath('//div[@class="lt-row"]'). \
                        get_attribute("style")
                    if tip_style.find("display: none;") == -1:
                        close_btn.click()

                next_btn.click()
                contents_new = self.getContents()
                self.save_content_csv(contents_new, need_close=False)

            else:
                self.save_content_csv([], need_close=True)
                print("爬取完成url= ", url, "的资源")
        except:
            self.save_content_csv([], need_close=True)
            print("爬取完成url= ", url, "的资源")



    def getContents(self):
        time.sleep(3)
        li_list = self.br.find_elements_by_xpath('//ul[@class="video-list clearfix"]/li')
        contents = []
        for li in li_list:  # 遍历所有项
            item = {}
            li_a_data = li.find_element_by_xpath('./a')
            item["title"] = li_a_data.get_attribute("title")  # 获取视频名字
            item["url"] = li_a_data.get_attribute("href")
            contents.append(item)
        return contents


    def save_content_txt(self, contents, need_close=True):
        f = open("B站视频资料.txt", "a")
        for content in contents:
            json.dump(content, f, ensure_ascii=False, indent=2)
            f.write("\n")
        if need_close:
            f.close()

    def save_content_csv(self, contents, need_close=True):
        path = r"./%s.csv" % self._keyword
        # if not os.path.exists(path):
        f = open(path, "a", encoding='utf-8')
        csv_writer = csv.writer(f)
        # csv_writer.writerow(("title", "url"))
        for content in contents:
            csv_writer.writerow((content["title"], content["url"]))
        if need_close:
            f.close()
            if os.path.exists(path):
                try:
                    new_path = urllib.parse.unquote(path)
                    os.rename(path, new_path)
                    if os.path.exists(path):
                        os.remove(path)
                except:
                    print("文件名替换失败")

            else:
                print("not exists")

    def run(self):
        self.start_driver_and_begin_download(self.url)
        print("爬取完成")
            

if __name__ == '__main__':
    def input_method():
        keyword = input("请输入查找关键字：")
        if len(keyword) > 0:
            bili = Search_On_Bili(keyword)
            bili.run()
        else:
            input_method()


    while True:
        input_method()
