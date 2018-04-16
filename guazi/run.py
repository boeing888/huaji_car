#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os
import uuid
import time

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.binary_location = '/usr/bin/chromium'

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.guazi.com/sh/buy/")
    carlist = driver.find_element_by_class_name('carlist')
    cars = carlist.find_elements_by_tag_name('li')
    urls = []
    for car in cars:
        urls.append(car.find_element_by_tag_name('a').get_attribute('href'))

    header = {'User-Agent':
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
              'Connection': 'close'}
    session = requests.session()
    session.keep_alive = False
    session.headers.update(header)

    for url in urls:
        # url=urls[0]
        driver.get(url)
        name = driver.find_element_by_tag_name('h2').text
        name_ele = driver.find_element_by_tag_name('h2')
        spans = name_ele.find_elements_by_tag_name('span')
        if len(spans):
            tmp = name.split()[0:-len(spans)]
            name = ' '.join(tmp)
        print(name)

        price_ele = driver.find_element_by_class_name('pricestype').text
        price = str(int(int(price_ele.split()[0].split('.')[0][1:]) * 10000 * 1.5))
        sale_price = str(int(int(price_ele.split()[0].split('.')[0][1:]) * 10000))
        print(price, sale_price)

        detail_ele = driver.find_element_by_class_name('detailcontent')
        table1_ele = detail_ele.find_elements_by_tag_name('table')[0]
        brand_ele = table1_ele.find_elements_by_tag_name('tr')[2]
        brand = brand_ele.find_elements_by_tag_name('td')[1].text
        print(brand)

        type_ele = table1_ele.find_elements_by_tag_name('tr')[3]
        car_type = type_ele.find_elements_by_tag_name('td')[1].text
        print(car_type)

        mile = str(float(driver.find_element_by_class_name('two').text.split()[0][:-3]) * 10000)
        print(mile)

        door_seat_ele = table1_ele.find_elements_by_tag_name('tr')[6]
        door_seat = door_seat_ele.find_elements_by_tag_name('td')[1].text
        print(door_seat)

        table2_ele = detail_ele.find_elements_by_tag_name('table')[1]
        volume_ele = table2_ele.find_elements_by_tag_name('tr')[1]
        volume = volume_ele.find_elements_by_tag_name('td')[1].text
        print(volume)

        shift_ele = table1_ele.find_elements_by_tag_name('tr')[5]
        shift = shift_ele.find_elements_by_tag_name('td')[1].text
        print(shift)

        fuel_ele = table2_ele.find_elements_by_tag_name('tr')[6]
        fuel = fuel_ele.find_elements_by_tag_name('td')[1].text
        print(fuel)

        detail = driver.find_element_by_class_name('test-con').text
        print(detail)

        feature_ele = driver.find_element_by_class_name('people-infor').find_element_by_tag_name('dd')
        spans = feature_ele.find_elements_by_tag_name('span')
        feature = []
        for span in spans:
            feature.append(span.text)
        feature = ';'.join(feature)
        print(feature)

        pictures_ele = driver.find_element_by_class_name('car-picture-infor').find_elements_by_tag_name('img')[:4]
        srcs = []
        try:
            for pic in pictures_ele:
                src = pic.get_attribute('src')
                s = src.split('/')
                s[-5] = '1200'
                s[-3] = '800'
                src = '/'.join(s)
                ir = session.get(src)
                if not os.path.exists(name):
                    os.makedirs(name)
                if ir.status_code == 200:
                    with open(os.path.join(name, uuid.uuid4().hex) + '.jpg', 'wb') as file:
                        file.write(ir.content)
                    with open(os.path.join(name, 'info') + '.txt', 'w') as file:
                        file.write('\r\n'.join(
                            [name, price, brand, car_type, mile, door_seat, volume, shift, sale_price, fuel, detail,
                             feature]))
        except Exception:
            continue

        time.sleep(1)
