import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import csv

headers ={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Cookie':'',
    #you can fill with your cookie
    }

#options=webdriver.ChromeOptions()
#options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

name =input('请输入电影名称：')
url_douban="https://www.douban.com/search?source=suggest&q="+name
#chrome_path=r"C:\Users\lingyi\Downloads\chromedriver-win64\chromedriver-win64"
option=webdriver.ChromeOptions()
option.add_argument('--headless')

browser = webdriver.Chrome(options=option)
browser.get(url_douban)
time.sleep(3)
a = browser.find_element(By.XPATH, "//ul/li/div/div/div/div/a")
#print(a.text)
#print(a.get_attribute("href"))
href = a.get_attribute("href")
print(href)
id = re.match('https.*movie/(.*)',href).group(1)
browser.close()
print(id)
#print(id)
#print(id)
# print(r.text)
# with open('test.txt','a+',encoding='utf-8') as f:
#     f.write('评论内容： %s\n' % r.text)


# id = input('请输入id：')

url = "https://movie.douban.com/subject/"+id+"/comments?status=P"

r = requests.get(url,headers=headers).text

html = etree.HTML(r)

comments = html.xpath('//div[@class="comment"]')
for comment in comments:
    #names = comment.xpath('.//a[@class=""]')
    grades = comment.xpath('.//span[contains(@class,"rating")]')
    texts = comment.xpath('.//span[@class="short"]')
    text = texts[0].xpath('./text()')[0]
    # filename = name+'.txt'
    if len(grades)>0:
        grade = grades[0].xpath('./@class')[0][7:8]+'stars'
    else:
        grade = '暂无评价'
    filename = name+'.csv'
    with open(filename,'a+',encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([text,grade])

for i in range(20,2000,20):
    # data = {
    #     'start':i,
    #     'limit':20,
    #     'status':'P',
    #     'sort':'new_score'
    # }
    start = str(i)
    url = 'https://movie.douban.com/subject/'+id+'/comments?start='+start+"&limit=20&status=P&sort=new_score"
    
    r = requests.get(url,headers=headers).text

    html = etree.HTML(r)

    comments = html.xpath('//div[@class="comment"]')
    for comment in comments:
        #names = comment.xpath('.//a[@class=""]')
        grades = comment.xpath('.//span[contains(@class,"rating")]')
        texts = comment.xpath('.//span[@class="short"]')
        text = texts[0].xpath('./text()')[0]
        if len(grades)>0:
            grade = grades[0].xpath('./@class')[0][7:8]+'stars'
        else:
            grade = '暂无评价'
        
        filename = name+'.csv'
        with open(filename,'a+',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([text,grade])
            # f.write('评论内容： %s\n' % text)
            # f.write('评价：%s\n' % grade)
            # f.write('=====================================================================\n')
    
