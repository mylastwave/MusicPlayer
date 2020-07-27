# MusicPlayer
>这是python+Qt Designer开发的一个有界面的音乐播放器
>>在网上看了十天pyqt的视频，断断续续写了半个月，终于有了当前这个版本，目前已经能玩一玩了，后续还会做优化和功能新增，现在这个版本离我设想中的完成品还很远

### 上手指南
把项目下载下来运行主程序 `main_play.py` 就能启动主界面了
数据来源由爬虫爬取，全部都是以本地文件的方式保存
歌单数据爬取的网易云网站的歌单，爬取一次比较耗时，考虑到爬取太快可能会被发现而且每天都要爬的话不方便开发，所以现在默认使用的日期为**2020.7.14** 的歌单数据，如果想每天都使用最新的数据，就需要把我注释的代码解开
```python
# /MusicPlayer/resource/widget/all_playlist_widget.py
# 77-79行
# today = datetime.date.today().strftime("%Y%m%d")  # 获得今天日期的字符串
# self.path = os.getcwd() +  r'\core\spider_files\playlist_{}.csv'.format(today)
self.file_path = os.getcwd() + r'\core\spider\spider_files\playlist_{}.csv'.format('20200714')
```
爬取歌单数据需要运行`MusicPlayer/core/spider/playlist_spider.py`，会爬取当天的网易云歌单，文件名字会携带日期，作为独一无二的命名，使用最新爬取的数据只需要找到上面代码块中的日期改成最新爬取的日期，或者直接使用被注释的代码，会自动使用当天的歌单数据，但记得每天都要先爬取一次再运行主程序哦
>没有使用异步爬取，爬取一次大概要花一两分钟，因为时间太久了就没放在程序启动的时候爬，先爬好再运行程序启动会快很多，因为数据是从网易云网站拿的，每个歌单只有十首歌，客户端才有所有数据，这些方面后续会进行优化

***
#### 开发环境
+ IDE：pycharm 2019.3 x64
+ python版本：3.7
***
#### 第三方包
+ PyQt5
+ pygame
+ mutagen
+ requests
+ selenium
>运行报了缺少什么包直接装就完事了

***
#### 设想中的正式版本
> 以下想法都是脑洞，正式版本可能会有所改动，正式版本完成后我会打包成exe文件放进来
>> 可能后续部分功能必须要用到网站平台的账号密码，_(我自己写的自己用肯定放心，出啥事自己作的自己负责没什么，路人不放心的话可以不使用那部分功能，真要使用建议阅读程序代码，真出事了我也付不了责任，使用那部分功能请考虑清楚)_

1. 有多个搜索引擎_（目前还只有网易云）_，查询歌曲时可以切换引擎获取结果， ~~再也不用找一首歌开几个播放器了~~ ，播放没有版权的歌曲会自动调用另外可用的引擎播放，全部都不行再提示`没有版权无法播放`
2. 可以导入各个音乐网站的已经创建的个人歌单，争取能放会员歌曲，_(没尝试过，实在不行就放弃了)_
3. 分区增多_（目前只有歌单）_，排行榜、歌手、专辑等等我全都要
4. 还在想……
