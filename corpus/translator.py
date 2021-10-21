import time
from selenium import webdriver
import json
from tqdm import tqdm

f = open('artists_test1.json')
data = json.load(f)
f.close()

lang_code = 'si'
browser = webdriver.Chrome("/home/aari/Projects/web-scraping/chromedriver")

for i in tqdm(range(len(data))):
    source_text = data[i]["name"]
    if ord(source_text[0]) < 200:
        browser.get("https://translate.google.co.in/?sl=en&tl="+lang_code+"&text="+source_text+"&op=translate")
        time.sleep(8)
        target_text = browser.find_element_by_xpath('/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]').text
        data[i]["name"] = target_text

with open('artists_translated.json', 'a') as f:
    f.write("%s,\n" % data)