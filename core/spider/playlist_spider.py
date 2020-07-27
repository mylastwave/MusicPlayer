from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import csv
import datetime


class PlayListSpider:
    def __init__(self):
        self.url = 'https://music.163.com/'
        self.request_url = self.url + '/discover/playlist'
        # 记号，是否到达尾页
        self.flag = True

        # 伪装
        self.heards = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
        # )
        self.dcap["phantomjs.page.settings.userAgent"] = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        )
        # 不加载图片
        self.dcap["phantomjs.page.settings.loadImages"] = False

    def run(self):
        # 用PhantomJS接口创建一个selenium的WebDriver
        self.driver = webdriver.PhantomJS(desired_capabilities=self.dcap)

        # 创建一个csv文件用来保存爬取的歌单数据
        today = datetime.date.today().strftime("%Y%m%d")  # 获得今天日期的字符串
        self.file = open('../spider_files/playlist_{}.csv'.format(today), 'w', encoding='utf-8', newline='')
        fieldnames = {'id', 'title', 'img', 'href'}
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

        # 开始爬取
        self.spider(self.request_url)

        # 结束退出
        self.file.close()
        self.driver.quit()

    def spider(self, url):
        """
        爬取歌单信息的函数
        url 为请求地址
        有下一页就调用自身递归爬取所有页面
        """
        # 跳出递归的条件
        if not self.flag:
            return
        # 用WebDriver加载页面
        self.driver.get(url)
        # 切换到内容的iframe
        self.driver.switch_to.frame('contentFrame')
        # 定位歌单标签
        lis = self.driver.find_element_by_id('m-pl-container').find_elements_by_tag_name('li')
        print(len(lis))
        # 提取歌单的地址、标题、图片地址、歌单id编号
        for li in lis:
            href = li.find_element_by_class_name('msk').get_attribute('href')
            title = li.find_element_by_class_name('msk').get_attribute('title').replace(',', '，')  # 防止文本中有英文逗号影响csv文件分隔
            img = li.find_element_by_class_name('j-flag').get_attribute('src').replace('param=140y140',
                                                                                       'param=200y200')  # 换成200×200的图片地址
            song_list_id = href.split('=')[1]

            dic = {'id': song_list_id, 'title': title, 'img': img, 'href': href}
            self.writer.writerow(dic)

        # 下一页按钮的标签的url地址
        next_url = self.driver.find_element_by_class_name('znxt').get_attribute('href')
        if 'void(0)' in next_url:
            self.flag = False
        else:
            self.spider(next_url)


if __name__ == '__main__':
    # 实例化爬虫对象
    spider = PlayListSpider()
    spider.run()
