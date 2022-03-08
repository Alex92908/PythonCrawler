from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

class Yapi(object):

    # url0 = https://apicenter.goldenpig.com.cn/project/413/interface/api/1587
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self._url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if isinstance(url, str):
            self._url = url

    def start_driver_and_begin_download(self):
        self.getContents()

    def getContents(self):
        time.sleep(3)
        try:
            while True:
                btn = self.driver.find_element_by_xpath(
                    '//span[@class="ant-table-row-expand-icon ant-table-row-collapsed"]')
                if btn:
                    btn.click()
                    time.sleep(1)
                else:
                    break
        except NoSuchElementException:
            pass

        table_list = self.driver.find_elements_by_xpath('//div[@class="ant-table-wrapper"]')
        for table in table_list:
            name_index = 0
            type_index = 0
            desc_index = 0
            is_optional_index = 0
            value_index = 0
            tr_header = table.find_element_by_xpath('.//thead[@class="ant-table-thead"]/tr')
            th_header = tr_header.find_elements_by_xpath('./th')
            i = 0
            for th in th_header:
                span = th.find_element_by_xpath('./span')
                if span.text == "类型":
                    type_index = i
                elif span.text == "备注":
                    desc_index = i
                elif span.text == "是否必须":
                    is_optional_index = i
                elif span.text == "参数值":
                    value_index = i
                i += 1
            tr_list = table.find_elements_by_xpath('.//tbody[@class="ant-table-tbody"]/tr')
            for tr in tr_list:
                td_list = tr.find_elements_by_xpath('./td')
                type = "String"
                default_value = '""'
                if type_index != 0:
                    if td_list[type_index].text == "string":
                        type = "String"
                        default_value = '""'
                    elif td_list[type_index].text == "number":
                        type = "Int"
                        default_value = 0
                    else:
                        type = td_list[type_index].text
                        default_value = 0
                desc = ""
                if desc_index != 0:
                    desc = td_list[desc_index].text
                if len(desc) > 0:
                    desc = "/// " + desc + "\n"
                content = desc + "var" + " " + td_list[name_index].text + ": " + type + " = " + str(default_value)
                print(content)
            print("*" * 20)
    def run(self, open_new_tab = False):
        if open_new_tab:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(self._url)
        time.sleep(5)
        while self.driver.current_url != self._url:
            pass
        self.start_driver_and_begin_download()

if __name__ == '__main__':
    page = 0
    yapi = 0
    def input_method():
        global page, yapi
        print("*" * 20)
        url = input("请输入Url：")
        if len(url) > 0:
            if yapi == 0:
                yapi = Yapi(url)
            else:
                yapi.url = url
            yapi.run(open_new_tab=page > 0)
            page += 1
        else:
            input_method()

    while True:
        input_method()