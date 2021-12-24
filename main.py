import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

# 设置endDate和numOfSeeLaters
beforeDays = 2  # 设定几天前
numOfSeeLaters = 100  # 想要添加到稍后再看的视频数量
# endDate = (datetime.date.today() + datetime.timedelta(-beforeDays)).strftime('%m-%d')  # 寻找视频的终止日期为设定的几天前
endDate = '2020-08-20'  # 自定义程序寻找视频的终止日期(请注意，endDate的值一定要出现在网页中，否则将无限循环下去)


def __isEndDate__(theDates, theEndDate):  # 检测是否翻到指定日期
    if theEndDate in theDates:
        return True
    else:
        return False


def __listMaker__():  # 将未添加到稍后再看的视频的BV号和链接写入一个文本内
    bvLinks = []  # 完整链接列表
    bvs = []  # 完整BV号列表
    newBvLinks = []  # 去掉已添加到稍后再看的链接列表
    newBvs = []  # 去掉已添加到稍后再看的BV号列表
    for link in driver.find_elements(By.XPATH, "//*[@href]"):  # 提取链接写入列表
        if not link.get_attribute('href').find('https://www.bilibili.com/video/') == -1:
            bvLinks.append(link.get_attribute('href'))
            bvs.append(link.get_attribute('href').replace('https://www.bilibili.com/video/', ''))
    if len(bvs) > numOfSeeLaters or len(bvLinks) > numOfSeeLaters:  # 检测是否有超过指定数量的视频
        j = numOfSeeLaters
        while j < len(bvs) or j < len(bvLinks):  # 将指定数量以上的视频添加到新列表内
            newBvLinks.append(bvLinks[j])
            newBvs.append(bvs[j])
            j = j + 1
        txt = open('未加入到稍后再看的视频列表.txt', 'a')  # 在目录内创建一个文本
        txt.write('\n\n' + datetime.date.today().strftime('%y-%m-%d') + '\n\n')  # 写入今日日期

        for bv in newBvs:  # 写入新列表到文本
            txt.write(bv + '\n')
        txt.writelines('\n-------------------\n\n')  # 链接列表和BV号列表的分隔符
        for bvLink in newBvLinks:
            txt.write(bvLink + '\n')


def __locate__():  # 将网页定位到指定日期附近的位置
    dates = []  # 每个视频的发布时间的列表
    while not __isEndDate__(dates, endDate):  # 检测是否到达目标日期，否则持续翻页
        time.sleep(2)
        oriDates = driver.find_elements(By.CLASS_NAME, 'detail-link')  # 收集所有发布时间
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # 执行下滑到底部的操作
        for date in oriDates:  # 将发布时间转换为字符串并添加到发布时间的列表内
            dates.append(date.text)


def __addToSeeLater__():  # 执行添加到稍后再看的操作
    i = 0
    seeLaters = driver.find_elements(By.CLASS_NAME, 'see-later')  # 定位每一个稍后再看按钮
    while i < len(seeLaters) and i < numOfSeeLaters:  # 点击每一次稍后再看按钮
        seeLater = seeLaters[i]
        seeLater.click()
        i = i + 1


print('程序将记录从现在到' + endDate + '附近您关注的UP所发布的视频')

# 配置webdriver
PATH = 'C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/chromedriver.exe'  # chromedriver.exe的位置
driver = webdriver.Chrome(PATH)  # 定义浏览器

# webdriver开始运行
driver.get('https://passport.bilibili.com/login')  # 浏览器定位到b站登录界面
time.sleep(10)  # 自定义登录时长
driver.get('https://t.bilibili.com/?tab=8')  # 浏览器定位到已关注的所有UP的视频投稿界面
time.sleep(3)  # 等待网页加载

__locate__()  # 将网页定位到指定日期附近的位置
__listMaker__()  # 将未添加到稍后再看的视频的BV号和链接写入一个文本内
__addToSeeLater__()  # 执行添加到稍后再看的操作
