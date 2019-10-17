'''
1.先将滑块验证的图片给下载下来
'''
import selenium
import time
from selenium import webdriver
import lxml
from lxml import html
from PIL import Image
from io import StringIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import re
from selenium.webdriver.common.action_chains import ActionChains
import requests
from urllib.request import urlretrieve
import cv2
import numpy as np

def get_captcha():
    wait = WebDriverWait(driver, 30)
    element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME,
                                        "gt_box")))
    time.sleep(random.uniform(3.0, 5.0))

    captcha_el = driver.find_element_by_xpath("//div[@class=\"gt_box\"]")
    location = captcha_el.location
    size = captcha_el.size
    left = int(location['x'])
    top = int(location['y'])
    right = int(location['x'] + size['width'])
    bottom = int(location['y'] + size['height'])
    # print(left,top,right,bottom)

    file1 = "test1.png"
    screenshot = driver.save_screenshot(file1)
    im = Image.open(file1)
    captcha = im.crop((left, top, right, bottom))
    captcha.save(file1)

def get_merge_image(filename,locationlist):
    im = Image.open(filename)
    new_im = Image.new("RGB",(260,116))
    list_upper = []
    list_down = []

    for location in locationlist:
        if(location['y'] == 0):
            list_down.append(im.crop((abs(location['x']),0,abs(location['x'])+10,58)))
        if location['y'] == -58:
            list_upper.append(im.crop((abs(location['x']),58,abs(location['x'])+10,116)))


    x_offset = 0
    for im in list_upper:
        new_im.paste(im,(x_offset,0))
        x_offset += im.size[0]

    x_offset = 0
    for im in list_down:
        new_im.paste(im, (x_offset, 58))
        x_offset += im.size[0]

    new_im.save(filename)

    return new_im

def pixel_equal(img1,img2,x,y):
    pix1 = img1.load()[x,y]
    pix2 = img2.load()[x,y]

    threshold = 50
    if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
                pix1[2] - pix2[2] < threshold)):
        return True
    else:
        return False

def get_gap():
    '''基于调试的代码'''
    img1 = Image.open("full.png")
    img2 = Image.open("cut.png")
    left = 43
    print(img1.size[0],img1.size[1])
    for i in range(left,img1.size[0]):
        for j in range(img1.size[1]):
            if not pixel_equal(img1,img2,i,j):
                print("不相同")
                left = i
                return left
    return left
    '''基于opencv的代码'''
    '''target = cv2.imread("cut.png",0)
    template = cv2.imread("full.png",0)
    w,h = target.shape[::-1]
    temp = "temp.jpg"
    targ = "targ.jpg"
    cv2.imwrite(temp,template)
    cv2.imwrite(targ,target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target,cv2.COLOR_BGR2GRAY)
    target = abs(255-target)
    cv2.imwrite(targ,target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target,template,cv2.TM_CCOEFF_NORMED)
    x,y = np.unravel_index(result.argmax(),result.shape)
    print("x方向的偏移", int(y * 0.4 + 18), 'x:', x, 'y:', y)
    cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
    cv2.imshow('Show', template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return int(y * 0.4 + 18)'''

def get_track(distance):
    print(distance)
    track = []
    current = 0
    mid = distance*4/5
    t = 0.2
    v = 0

    while current < distance:
        if current < mid:
            a = 20
        else:
            a = -3
        v0 = v
        v = v0 + a*t
        move = v0*t + 1/2*a*t*t
        current += move
        track.append(round(move))

    return track

def set_track(distance):
    result = [(0, 0), (6, 0), (14, 0), (18, 0), (20, 0), (22, 0), (24, 0), (25, 0), (26, 0), (27, 0), (29, 0), (31, 0),
              (32, 0), (34, 0), (35, 0), (38, 0), (38, 0), (40, 0), (42, 0), (44, 0), (45, 0), (47, 0), (49, 0),
              (51, 0), (53, 0), (54, 0), (55, 0), (58, 0), (58, 0), (60, -1), (60, -1), (62, -1), (63, -2), (64, -2),
              (65, -2), (66, -2), (67, -2), (69, -2), (69, -2), (71, -2), (72, -2), (73, -2), (75, -4), (78, -4),
              (78, -4), (80, -4), (82, -4), (84, -4), (85, -4), (86, -4), (87, -4), (89, -4), (91, -4), (92, -4),
              (93, -4), (94, -4), (95, -4), (98, -4), (98, -4), (100, -4), (100, -4), (102, -4), (104, -4), (105, -3),
              (107, -3), (109, -3), (111, -3), (112, -3), (113, -3), (114, -3), (115, -3), (116, -3), (118, -3),
              (120, -3), (120, -3), (122, -3), (123, -3), (124, -3), (126, -3), (127, -3), (129, -3), (131, -2),
              (133, -2), (134, -2), (135, -2), (138, -2), (138, -1), (138, -1), (140, -1), (140, -1), (142, -1),
              (143, -1), (144, -1), (145, -1), (146, -1), (147, -1), (149, -1), (151, -1), (151, 0), (152, 0), (153, 0),
              (155, 0), (158, 0), (160, 0), (160, 0), (162, 0), (163, 0), (164, 0), (166, 0), (167, 0), (169, 0),
              (169, 0), (171, 0), (173, 0), (174, 0), (175, 0), (176, 0), (178, 0), (180, 0), (180, 0), (184, 1),
              (189, 1), (198, 1), (202, 1), (205, 1), (206, 1), (209, 3), (211, 3), (213, 3), (215, 3), (218, 3),
              (220, 3), (220, 3), (222, 3), (223, 3), (225, 3), (226, 3), (227, 3), (229, 3), (231, 3), (232, 3),
              (233, 3), (234, 3), (235, 3), (236, 3), (238, 3), (240, 3), (240, 3), (242, 3), (243, 3), (244, 3),
              (245, 3), (246, 3), (247, 3), (249, 3), (249, 3), (253, 3), (255, 3), (256, 3), (258, 3), (260, 3),
              (262, 3), (263, 3), (265, 3), (266, 3), (267, 3), (269, 3), (269, 3), (271, 3), (272, 3), (273, 3),
              (274, 1), (275, 1), (276, 1), (278, 0), (280, 0), (282, -2), (283, -2), (284, -2), (285, -2), (286, -2),
              (289, -2), (289, -2), (291, -2), (293, -2), (295, -2), (296, -2), (298, -2), (298, -2), (300, -2),
              (302, -2), (303, -2), (305, -2), (306, -2), (309, -2), (309, -2), (311, -2), (312, -2), (313, -2),
              (314, -2), (315, -2), (316, -2), (318, -2), (320, -2), (322, -2), (322, -1), (325, 0), (326, 0), (327, 0),
              (329, 0), (329, 0), (332, 0), (333, 1), (334, 3), (335, 3), (343, 3), (344, 3), (347, 3), (349, 3),
              (349, 5), (351, 5), (353, 5), (354, 5), (355, 5), (358, 5), (358, 7), (360, 7), (360, 7), (362, 7),
              (363, 7), (364, 7), (369, 7), (371, 7), (373, 7), (374, 7), (375, 7), (376, 7), (378, 7)]
    track = []
    for location in result:
        print(location)
        if location[0] > distance-2 and location[0] < distance+2:
            return track
        elif location[0] > distance+4:
            return []
        track.append(location)
    return track

def move_to_gap(driver,slider,track):
    ActionChains(driver).click_and_hold(slider).perform()
    '''while track:
        x = random.choice(track)
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
        track.remove(x)
        time.sleep(0.2)'''
    for index in range(0,len(track)):
        time.sleep(0.1)
        if index > 0 and index < len(track):
            print(track[index][0]-track[index-1][0])
            ActionChains(driver).move_by_offset(xoffset=track[index][0]-track[index-1][0], yoffset=track[index][1]).perform()
    ActionChains(driver).release(slider).perform()

driver = selenium.webdriver.Chrome()
url = ("http://gsxt.hljaic.gov.cn/index.jspx")
driver.get(url)
time.sleep(2)

input = driver.find_element_by_xpath("//input[@class=\"searchInput\"]")
search = driver.find_element_by_xpath("//div[@id=\"click\"]")

input.send_keys(u"师范大学")
search.click()
wait = WebDriverWait(driver, 30)
element = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME,
                                    "gt_box")))
time.sleep(random.uniform(3.0, 5.0))

captacha = lxml.html.fromstring(driver.page_source)

fullbglist = captacha.xpath("//div[@class=\"gt_cut_fullbg_slice\"]/@style")
cutbglist = captacha.xpath("//div[@class=\"gt_cut_bg_slice\"]/@style")


fullurllist =[]
for fullbg in fullbglist:
    fullurllist.append(re.findall('url\(\"(.*?)\"\);',fullbg)[0].replace('webp', 'jpg'))

cuturllist = []
for cutbg in cutbglist:
    cuturllist.append(re.findall('url\(\"(.*?)\"\);',cutbg)[0].replace('webp', 'jpg'))

full_location_list = []
for fullbg in fullbglist:
    location = {}
    location['x'] = eval(re.findall('background-position: (.*?)px (.*?)px',fullbg)[0][0])
    location['y'] = eval(re.findall('background-position: (.*?)px (.*?)px',fullbg)[0][1])
    full_location_list.append(location)

print(full_location_list)

cut_location_list=[]
for cutbg in cutbglist:
    location={}
    location['x'] =  eval(re.findall('background-position: (.*?)px (.*?)px',cutbg)[0][0])
    location['y'] = eval(re.findall('background-position: (.*?)px (.*?)px',cutbg)[0][1])
    cut_location_list.append(location)

print(fullurllist)
urlretrieve(fullurllist[0],"full.png")
urlretrieve(cuturllist[0],"cut.png")

get_merge_image("full.png",full_location_list)
get_merge_image("cut.png",cut_location_list)


gap = get_gap()
print(gap)
#track = get_track(gap-9)
track = set_track(gap-5)
print(track)

slider = driver.find_element_by_xpath("//div[@class=\"gt_slider_knob gt_show\"]")

move_to_gap(driver,slider,track)








