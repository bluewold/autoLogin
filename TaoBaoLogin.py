import re
import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import random
import math
import json



options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = selenium.webdriver.Chrome(options=options)
wait = WebDriverWait(driver,20)
keyword = "ipad"
session = requests.session()

def login():
    print("正在登陆")
    driver.execute_script('Object.defineProperties(navigator,{webdriver:{get:()=>false}})')
    wait = WebDriverWait(driver, 10)
    driver.get(url='https://login.taobao.com')
    driver.implicitly_wait(15)

    wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="login-switch"]//i[last()]')))

    switch = driver.find_element_by_xpath('//div[@class="login-switch"]//i[last()]')
    switch.click()
    driver.implicitly_wait(2)

    time.sleep(2)
    name = driver.find_element_by_xpath('//input[@name="TPL_username"]')
    name.send_keys("cover")
    time.sleep(2)
    name.send_keys("moon")

    time.sleep(1)

    password = driver.find_element_by_xpath('//input[@name="TPL_password"]')
    password.send_keys("1989edward0331lee")

    wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="nc_scale"]//span[@class="nc_iconfont btn_slide"]')))
    dragger = driver.find_element_by_xpath('//div[@class="nc_scale"]//span[@class="nc_iconfont btn_slide"]')
    result =[(0, 0),(2, 0),(7, 0),(15, 0),(24, 0),(31, 0),(31, 0),(33, 0),(35, 0),(37, 0),(40, 0),(40, 0),(44, 0),(46, 0),(48, 0),(51, 0),(51, 0),(53, 0),(55, 0),(56, 0),(57, 0),(58, 0),(60, 0),(64, 0),(65, 0),(66, 0),(68, 0),(71, 0),(73, 0),(75, -2),(78, -2),(80, -2),(82, -2),(85, -2),(86, -2),(89, -2),(91, -2),(95, -4),(98, -4),(100, -4),(104, -4),(107, -4),(109, -6),(111, -6),(116, -7),(117, -7),(124, -7),(126, -7),(128, -7),(129, -7),(131, -7),(131, -7),(134, -7),(135, -7),(136, -7),(138, -7),(142, -7),(144, -7),(145, -7),(146, -7),(148, -7),(151, -6),(153, -6),(155, -6),(156, -6),(158, -6),(160, -6),(160, -4),(162, -4),(162, -4),(164, -4),(165, -4),(166, -4),(168, -2),(169, -2),(171, -2),(173, -2),(175, -2),(177, -2),(178, -2),(180, -2),(182, -2),(182, -2),(184, -2),(187, -2),(188, -2),(189, -2),(191, -2),(193, -2),(195, -2),(196, -2),(197, -2),(198, -2),(200, -2),(202, -2),(202, -2),(204, -2),(205, -2),(206, -2),(208, -2),(209, -2),(211, -2),(211, -2),(213, -1),(214, -1),(214, -2),(215, -2),(216, -2),(217, -2),(220, -2),(220, -4),(222, -4),(224, -4),(225, -4),(226, -4),(227, -4),(228, -4),(231, -4),(231, -4),(233, -4),(235, -4),(237, -4),(237, -4),(238, -2),(240, -2),(242, -1),(242, 0),(244, 0),(245, 0),(248, 0),(248, 1),(249, 2),(251, 2),(255, 2),(255, 5),(256, 5),(260, 5),(262, 5),(266, 5),(267, 5),(271, 3),(275, 2),(280, 1),(284, 1),(287, 0),(288, 0),(293, 0),(295, 0),(296, 0),(298, 0),(300, 0),(302, 0),(302, 0),(304, 0),(305, 0),(306, 0),(307, 0),(308, -1),(309, -1),(311, -1),(313, -1),(314, -1),(315, -1),(316, -1),(317, -1),(320, -1),(322, -1),(322, -1),(326, 0),(328, 1),(331, 1),(333, 1),(335, 2),(336, 2),(337, 2),(338, 2),(340, 2),(342, 2),(342, 2),(344, 2)]
    action = ActionChains(driver)
    action.click_and_hold(dragger).perform()
    for x in result:
        time.sleep(0.1)
        action.move_by_offset(xoffset=x[0], yoffset=x[1])
    # ActionChains(driver).drag_and_drop_by_offset(dragger,500,0).perform()
    time.sleep(2)
    action.release(on_element=dragger).perform()
    time.sleep(1)
    sumbit = driver.find_element_by_xpath('//form[@id="J_Form"]//div[@class="submit"]//button[@class="J_Submit"]')
    print(sumbit)
    sumbit.click()
    time.sleep(2)
    cookies = driver.get_cookies()
    with open("cookies.txt", "w") as fp:
        json.dump(cookies, fp)
    read_cookies()

def slide_solve():
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="btn_slide"]')))
    except Exception as e:
        print(e)
        return
    slide = driver.find_element_by_xpath('//div[@class="btn_slide"]')
    if slide:
        html = lxml.html.fromstring(driver.page_source)
        slide = html.xpath('//div[@class="btn_slide"]')
        if slide:
            for item in slide:
                print("slide"+item)
            result = [(0, 0),(6, 0),(14, 0),(18, 0),(20, 0),(22, 0),(24, 0),(25, 0),(26, 0),(27, 0),(29, 0),(31, 0),(32, 0),(34, 0),(35, 0),(38, 0),(38, 0),(40, 0),(42, 0),(44, 0),(45, 0),(47, 0),(49, 0),(51, 0),(53, 0),(54, 0),(55, 0),(58, 0),(58, 0),(60, -1),(60, -1),(62, -1),(63, -2),(64, -2),(65, -2),(66, -2),(67, -2),(69, -2),(69, -2),(71, -2),(72, -2),(73, -2),(75, -4),(78, -4),(78, -4),(80, -4),(82, -4),(84, -4),(85, -4),(86, -4),(87, -4),(89, -4),(91, -4),(92, -4),(93, -4),(94, -4),(95, -4),(98, -4),(98, -4),(100, -4),(100, -4),(102, -4),(104, -4),(105, -3),(107, -3),(109, -3),(111, -3),(112, -3),(113, -3),(114, -3),(115, -3),(116, -3),(118, -3),(120, -3),(120, -3),(122, -3),(123, -3),(124, -3),(126, -3),(127, -3),(129, -3),(131, -2),(133, -2),(134, -2),(135, -2),(138, -2),(138, -1),(138, -1),(140, -1),(140, -1),(142, -1),(143, -1),(144, -1),(145, -1),(146, -1),(147, -1),(149, -1),(151, -1),(151, 0),(152, 0),(153, 0),(155, 0),(158, 0),(160, 0),(160, 0),(162, 0),(163, 0),(164, 0),(166, 0),(167, 0),(169, 0),(169, 0),(171, 0),(173, 0),(174, 0),(175, 0),(176, 0),(178, 0),(180, 0),(180, 0),(184, 1),(189, 1),(198, 1),(202, 1),(205, 1),(206, 1),(209, 3),(211, 3),(213, 3),(215, 3),(218, 3),(220, 3),(220, 3),(222, 3),(223, 3),(225, 3),(226, 3),(227, 3),(229, 3),(231, 3),(232, 3),(233, 3),(234, 3),(235, 3),(236, 3),(238, 3),(240, 3),(240, 3),(242, 3),(243, 3),(244, 3),(245, 3),(246, 3),(247, 3),(249, 3),(249, 3),(253, 3),(255, 3),(256, 3),(258, 3),(260, 3),(262, 3),(263, 3),(265, 3),(266, 3),(267, 3),(269, 3),(269, 3),(271, 3),(272, 3),(273, 3),(274, 1),(275, 1),(276, 1),(278, 0),(280, 0),(282, -2),(283, -2),(284, -2),(285, -2),(286, -2),(289, -2),(289, -2),(291, -2),(293, -2),(295, -2),(296, -2),(298, -2),(298, -2),(300, -2),(302, -2),(303, -2),(305, -2),(306, -2),(309, -2),(309, -2),(311, -2),(312, -2),(313, -2),(314, -2),(315, -2),(316, -2),(318, -2),(320, -2),(322, -2),(322, -1),(325, 0),(326, 0),(327, 0),(329, 0),(329, 0),(332, 0),(333, 1),(334, 3),(335, 3),(343, 3),(344, 3),(347, 3),(349, 3),(349, 5),(351, 5),(353, 5),(354, 5),(355, 5),(358, 5),(358, 7),(360, 7),(360, 7),(362, 7),(363, 7),(364, 7),(369, 7),(371, 7),(373, 7),(374, 7),(375, 7),(376, 7),(378, 7)]
            action = ActionChains(driver)
            action.click_and_hold(slide).perform()
            for x in result:
                time.sleep(0.1)
                action.move_by_offset(xoffset=x[0], yoffset=x[1])
            # ActionChains(driver).drag_and_drop_by_offset(dragger,500,0).perform()
            time.sleep(2)
            action.release(on_element=slide).perform()
            time.sleep(1)
        else:
            for item in slide:
                print("slide" + item)
            time.sleep(2)

if __name__ == '__main__':
    login()
