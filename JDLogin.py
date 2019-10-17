import cv2
import time
import numpy as np
from selenium import webdriver
import requests
from selenium.webdriver.common.action_chains import ActionChains
from urllib import request
from PIL import Image
import random
import math
from selenium.webdriver.chrome.options import Options
import selenium

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
brower = selenium.webdriver.Chrome(options=options)
cut_width =50
cut_height = 50
back_width = 360
back_height = 140
scaling_ratio = 1

def loadpage(userid,password):
    url = "https://passport.jd.com/new/login.aspx?"
    brower.get(url)
    time.sleep(3)
    userlogin = brower.find_element_by_xpath('//div/div[@class="login-tab login-tab-r"]/a')
    userlogin.click()
    time.sleep(1)
    username = brower.find_element_by_id('loginname')
    username.send_keys(userid)
    userpwd = brower.find_element_by_id('nloginpwd')
    userpwd.send_keys(password)

    brower.find_element_by_id("loginsubmit").click()
    time.sleep(2)
    while True:
        try:
            getPic()
        except:
            print("登陆成功...")
            break
    time.sleep(5)

def get_distance(back_img,cut_img):
    back_canny = get_back_canny(back_img)
    operator = get_operator(cut_img)
    pos_x, max_value = best_match(back_canny, operator)
    distance = pos_x * scaling_ratio
    return distance

def best_match(back_canny, operator):
    max_value, pos_x = 0, 0
    print(cut_width,back_width)
    for x in range(cut_width, back_width - cut_width):
        block = back_canny[:, x:x + cut_width]
        value = (block * operator).sum()
        if value > max_value:
            max_value = value
            pos_x = x
    return pos_x, max_value


def get_back_canny(back_img):
    img_blur = cv2.GaussianBlur(back_img,(3,3),0)
    img_gray = cv2.cvtColor(img_blur,cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray,100,200)
    return img_canny

def get_operator(cut_img):
    cut_img = get_back_canny(cut_img)
    cv2.imwrite("test.png",cut_img)
    cut_gray = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)


    ret, cut_binary = cv2.threshold(cut_gray, 170, 255, cv2.THRESH_BINARY)

    # 获取边界
    contours, hierarchy = cv2.findContours(cut_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 获取最外层边界
    contour = contours[-1]
    cv2.drawContours(cut_img, contours, -1, (0, 0, 255), 3)
    cv2.putText(cut_img, "{:.3f}".format(len(contours)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 1)
    #cv2.imshow("img", cut_img)

    # operator矩阵
    operator = np.zeros((cut_height, cut_width))
    # 根据 contour填写operator
    for point in contour:
        operator[point[0][1]][point[0][0]] = 1
    return operator


'''def getPic():
    # 用于找到登录图片的大图
    s2 = r'//div/div[@class="JDJRV-bigimg"]/img'
    # 用来找到登录图片的小滑块
    s3 = r'//div/div[@class="JDJRV-smallimg"]/img'
    bigimg = brower.find_element_by_xpath(s2).get_attribute("src")
    smallimg = brower.find_element_by_xpath(s3).get_attribute("src")
    # 背景大图命名
    backimg = "backimg.jpg"
    # 滑块命名
    slideimg = "slideimg.png"
    # 下载背景大图保存到本地
    request.urlretrieve(bigimg, backimg)
    # 下载滑块保存到本地
    request.urlretrieve(smallimg, slideimg)

    back_img = cv2.imread(backimg)
    cut_img = cv2.imread(slideimg)
    back_width = Image.open(backimg).size[0]
    back_height = Image.open(backimg).size[1]
    cut_width = Image.open(slideimg).size[0]
    cut_height = Image.open(slideimg).size[1]
    scaling_ratio = brower.find_element_by_xpath(s2).size['width'] / back_width
    print(get_distance(back_img,cut_img))'''


'''def getPic():
    # 用于找到登录图片的大图
    s2 = r'//div/div[@class="JDJRV-bigimg"]/img'
    # 用来找到登录图片的小滑块
    s3 = r'//div/div[@class="JDJRV-smallimg"]/img'
    bigimg = brower.find_element_by_xpath(s2).get_attribute("src")
    smallimg = brower.find_element_by_xpath(s3).get_attribute("src")
    # 背景大图命名
    backimg = "backimg.png"
    # 滑块命名
    slideimg = "slideimg.png"
    # 下载背景大图保存到本地
    request.urlretrieve(bigimg, backimg)
    # 下载滑块保存到本地
    request.urlretrieve(smallimg, slideimg)
    image = cv2.imread(backimg)
    blurred = cv2.GaussianBlur(image,(5,5),0)
    canny = cv2.Canny(blurred,200,400)
    contours,hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    for i,contour in enumerate(contours):
        M = cv2.moments(contour)
        if M['m00'] == 0:
            cx = cy = 0
        else:
            cx,cy = M['m10'] / M['m00'], M['m01'] / M['m00']
        print(cv2.contourArea(contour))
        if 6000 < cv2.contourArea(contour) < 8000 and 370 < cv2.arcLength(contour, True) < 390:
            if cx < 400:
                continue
            x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imshow('image', image)
            # 获取滑块
            element = brower.find_element_by_xpath(s3)
            ActionChains(brower).click_and_hold(on_element=element).perform()
            ActionChains(brower).move_to_element_with_offset(to_element=element, xoffset=x, yoffset=0).perform()
            ActionChains(brower).release(on_element=element).perform()
            time.sleep(3)
        return 0
'''

def set_track(distance):
    distance = distance - 12
    result = [(0, 0),(1, 0),(6, 0),(10, 0),(12, 0),(15, 0),(19, 0),(23, 0),(30, 0),(37, 0),(41, 0),(50, 0),(55, 0),(57, 0),(60, 0),(62, 0),(63, 0),(66, 0),(68, 0),(70, 0),(71, 0),(72, 0),(73, 0),(75, 0),(77, 0),(77, 0),(77, 0),(79, 0),(81, -2),(81, -2),(83, -2),(86, -2),(90, -2),(91, -4),(93, -4),(95, -4),(97, -4),(100, -4),(102, -4),(103, -4),(106, -4),(117, -6),(119, -6),(122, -6),(126, -6),(128, -6),(129, -6),(132, -6),(135, -6),(137, -6),(140, -6),(141, -6),(143, -6),(144, -6),(146, -6),(146, -6),(149, -6),(150, -6),(152, -6),(155, -6),(155, -6),(157, -6),(159, -6),(159, -6),(161, -6),(162, -6),(163, -6),(166, -6),(166, -6),(168, -6),(169, -6),(172, -6),(172, -6),(173, -6),(175, -6),(177, -6),(179, -6),(181, -6),(182, -6),(183, -6),(184, -6),(186, -6),(186, -6),(188, -6),(188, -6),(189, -6),(190, -6),(191, -6),(192, -6),(195, -6),(197, -6),(197, -6),(199, -6),(201, -6),(201, -6),(203, -6),(206, -6),(206, -6),(208, -6),(210, -6),(212, -6),(215, -6),(215, -6),(217, -5),(217, -5),(219, -5),(219, -4),(221, -4),(221, -2),(222, -2),(223, -2),(224, -2),(226, -2),(226, -2),(228, -2),(228, -2),(229, -2),(230, -2),(232, -2),(235, -2),(235, -2),(239, -2),(241, 0),(241, 0),(242, 0),(244, 0),(246, 0),(248, 0),(250, 0),(251, 0),(255, 0),(255, 0),(257, 0),(261, 0),(264, 0),(266, 2),(270, 2),(272, 4),(275, 4),(275, 4),(277, 4),(280, 4),(282, 4),(283, 4),(284, 5),(286, 5),(286, 5),(288, 5),(290, 5),(291, 5),(292, 5),(292, 5),(295, 5),(295, 5),(297, 5),(299, 5),(300, 5),(301, 5),(302, 5),(303, 5),(303, 5),(306, 5),(306, 5),(308, 5),(309, 5),(310, 5),(312, 5),(312, 5),(315, 5),(319, 5),(320, 5)]
    track = []
    for location in result:
        print(location)
        if location[0] > distance-2 and location[0] < distance+2:
            return track
        elif location[0] > distance+4:
            return []
        track.append(location)
    print(track)
    return track

def move_to_gap(driver,slider,track):
    ActionChains(driver).click_and_hold(slider).perform()
    '''while track:
        x = random.choice(track)
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
        track.remove(x)
        time.sleep(0.2)'''
    for index in range(0,len(track)):
        time.sleep(random.randint(5, 20) / 100)
        if index > 0 and index < len(track):
            print(track[index][0]-track[index-1][0])
            ActionChains(driver).move_by_offset(xoffset=track[index][0]-track[index-1][0], yoffset=track[index][1]).perform()
    x = math.floor(random.randint(0,5))
    ActionChains(driver).move_by_offset(xoffset=x,yoffset=random.randint(-5,5)).perform()
    time.sleep(random.randint(5, 20) / 100)
    ActionChains(driver).move_by_offset(xoffset=-x+1,yoffset=random.randint(-5,5)).perform()
    time.sleep(random.randint(15, 30) / 100)
    ActionChains(driver).release(slider).perform()


def auto_drag(driver,slider,distance):


    # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
    # distance -= element.size.get('width') /
    tracklist= []
    distance = distance - 16
    has_gone_dist = 0
    remaining_dist = distance
    # distance += randint(-10, 10)

    # 按下鼠标左键
    ActionChains(driver).click_and_hold(slider).perform()
    time.sleep(0.2)
    lastdoudong = 0
    while remaining_dist > 0:
        ratio = remaining_dist / distance
        if ratio < 0.25:
            # 开始阶段移动较慢
            span = random.randint(2, 5)
        elif ratio > 0.88:
            # 结束阶段移动较慢
            span = random.randint(1, 5)
        else:
            # 中间部分移动快
            span = random.randint(13, 18)
        lastdoudong = random.randint(-3,5)
        if random.randint(0,7) > 5:
            if(ratio < 0.7):
                lastdoudong = random.randint(-3,5)
            else:
                lastdoudong = random.randint(-2, 3)
        ActionChains(driver).move_by_offset(span, lastdoudong).perform()
        tracklist.append((span,lastdoudong))
        remaining_dist -= span
        has_gone_dist += span
        if(ratio <  0.4):
            time.sleep(random.randint(15,30) / 100)
        elif(ratio > 0.75):
            time.sleep(random.randint(15,25) / 100)
        else:
            time.sleep(random.randint(5,12) / 100)

    ActionChains(driver).move_by_offset(remaining_dist, random.randint(-1, 1)).perform()
    time.sleep(random.randint(50, 80) / 100)
    ActionChains(driver).release(on_element=slider).perform()
    print(tracklist)

def getPic():
    # 用于找到登录图片的大图
    s2 = r'//div/div[@class="JDJRV-bigimg"]/img'
    # 用来找到登录图片的小滑块
    s3 = r'//div/div[@class="JDJRV-smallimg"]/img'
    bigimg = brower.find_element_by_xpath(s2).get_attribute("src")
    bk_block = brower.find_element_by_xpath(s2)
    bk_block_x = bk_block.location['x']
    smallimg = brower.find_element_by_xpath(s3).get_attribute("src")
    slide_block = brower.find_element_by_xpath(s3)
    slide_block_x = slide_block.location['x']
    # 背景大图命名
    backimg = "backimg.png"
    web_image_width = bk_block.size
    web_image_width = web_image_width['width']
    # 滑块命名
    slideimg = "slideimg.png"
    # 下载背景大图保存到本地
    request.urlretrieve(bigimg, backimg)
    # 下载滑块保存到本地
    request.urlretrieve(smallimg, slideimg)
    # 获取图片并灰度化
    block = cv2.imread(slideimg, 0)
    template = cv2.imread(backimg, 0)
    image = Image.open(backimg)
    real_width = image.size[0]
    width_scale = float(real_width) / float(web_image_width)
    # 二值化后的图片名称
    blockName = "block.png"
    templateName = "template.jpg"
    # 将二值化后的图片进行保存
    cv2.imwrite(blockName, block)
    cv2.imwrite(templateName, template)
    block = cv2.imread(blockName)
    block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
    block = abs(255 - block)
    cv2.imwrite(blockName, block)
    block = cv2.imread(blockName)
    template = cv2.imread(templateName)
    block = get_back_canny(block)
    template = get_back_canny(template)

    # 获取偏移量
    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)  # 查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
    x, y = np.unravel_index(result.argmax(), result.shape)
    # print("x方向的偏移", int(y * 0.4 + 18), 'x:', x, 'y:', y)
    real_position = y/width_scale
    real_position = real_position - (slide_block_x - bk_block_x)+15
    # 获取滑块
    #track = set_track(real_position)
    element = brower.find_element_by_xpath(s3)
   
   # move_to_gap(brower,element,track)
    auto_drag(brower,element,real_position)
    time.sleep(3)



if __name__ == '__main__':
    id = "xxxxxxxx"
    passwd = "xxxxxx"
    loadpage(id,passwd)


