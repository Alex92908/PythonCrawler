# Python 哔哩哔哩搜索爬虫
1、需要本地配置浏览器驱动（mac下查看本地Chrome的版本，去http://npm.taobao.org/mirrors/chromedriver/ 下载对应版本chrome driver， 把下载好的Chrome driver放在  usr/local/bin）

2、通过pip install selenium 安装selenium库

3、运行该文件就可以在哔哩哔哩通过关键字搜索视频，将所有分页视频的(title, url)汇总成csv文件

4、若要显式浏览器过程需将self.br = webdriver.Chrome(options=chrome_options) 换成self.br = webdriver.Chrome()
