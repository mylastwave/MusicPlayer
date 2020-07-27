from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SongListSpider:
    """
    爬取歌单内所有歌曲信息
    """
    def __init__(self):
        self.url = 'https://music.163.com/'

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
        # 用PhantomJS接口创建一个selenium的WebDriver
        self.driver = webdriver.PhantomJS(desired_capabilities=self.dcap)
        print('driver创建完成')

    def main(self, playlist_id):
        # 爬虫开始运行
        request_url = self.url + 'playlist?id={}'.format(playlist_id)
        # print(request_url)
        result = self.spider(request_url)
        return result

    def spider(self, url):
        # 用WebDriver加载页面
        print('加载请求页面……')
        self.driver.get(url)
        # 切换到内容的iframe
        self.driver.switch_to.frame('contentFrame')
        # 定位歌单标签
        print('定位标签……')
        trs = self.driver.find_element_by_class_name('j-flag').find_element_by_tag_name(
            'tbody').find_elements_by_tag_name('tr')
        dic1 = {}
        print('开始处理数据……')
        for index, tr in enumerate(trs):
            # print(index, tr)
            # 含有歌名和歌曲地址的标签
            song_span = tr.find_element_by_class_name('txt')
            href = song_span.find_element_by_tag_name('a').get_attribute('href')
            song_name = song_span.find_element_by_tag_name('a').find_element_by_tag_name('b').get_attribute('title')
            # 从地址里面获取到歌曲id
            song_id = href.split('id=')[1]
            # 歌曲的时长
            song_length = tr.find_element_by_class_name('u-dur').text
            # 演唱者
            singer = tr.find_element_by_class_name('text').get_attribute('title')
            # 将所有信息整合进字典内
            dic1[index] = {'name': song_name, 'id': song_id, 'length': song_length, 'singer': singer}
        print('返回数据')
        return dic1


if __name__ == '__main__':
    spider = SongListSpider()
    list_id = 5078855536
    spider.main(list_id)
