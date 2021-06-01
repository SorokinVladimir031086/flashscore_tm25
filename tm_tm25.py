import time
from selenium import webdriver
from bs4 import BeautifulSoup
import telebot
import pandas as pd

from openpyxl import Workbook
import csv
from array import array

chrome_path = r'C:\Python_mini\chromedriver.exe'
driver = webdriver.Chrome(chrome_path)
url = "https://www.flashscore.com/"
list=[]
home1=[]
away1=[]
country1=[]
TOKEN = '1260366546:AAHmSnNqjDUBfpQwr2D4mTpZKG9_4o4dVUw'
bot = telebot.TeleBot(TOKEN)

def main():
    try:
        driver.get(url)
        driver.maximize_window()
        driver.find_element_by_id("onetrust-accept-btn-handler").click()
        container = driver.find_element_by_css_selector("div[id=live-table]").get_attribute("innerHTML")
        main_page = driver.current_window_handle
    except Exception as e:
        print(e)
    else:
        soup = BeautifulSoup(container, 'html.parser')
        matches = soup.select(".event__match.event__match--scheduled.event__match--oneLine")
        for match in matches:
            try:
                time_match = match.select_one("div.event__time").text
                home = match.select_one("div.event__participant.event__participant--home").text
                away = match.select_one("div.event__participant.event__participant--away").text
                id_match = match["id"].split("_")[-1]
                print(time_match, home, away, id_match )
            except Exception as h:
                print(h)

            try:
                driver.execute_script("arguments[0].click();", driver.find_element_by_id(match["id"]))
            except Exception as h:
                print(h)

            time.sleep(3)
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
            time.sleep(2)

            try:
                html6 = BeautifulSoup(driver.page_source, 'html.parser')
                x1s = html6.find_all('div', class_= 'tabs__tab selected')

            except Exception as ee:
                print(ee)

            try:
                for x1 in x1s:
                    if 'Pre-match odds' in x1.text:
                        try:
                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text("H2H"))
                            time.sleep(2)
                        except Exception as ee:
                            print(ee)


                        try:
                            html5 = BeautifulSoup(driver.page_source, 'html.parser')
                            country = html5.find('span', class_= 'country___24Qe-aj')
                            print (country.text)
                            blocks = html5.find_all('div', class_= 'section___1a1N7yN false')
                            #print(name_hig)
                            for block in blocks[:2]:
                                print(block.text)
                                scores = block.find_all('span', class_= 'result___1sMZa9R')
                                for score in scores[:4]:
                                    print(score.text)
                                    if '(' not in score.text:
                                        score1 = score.text.split(' : ')[0]
                                        score2 = score.text.split(' : ')[1]
                                        print(score1)
                                        print(score2)
                                    else:
                                        score3=score.text[score.text.index('(')+1:score.text.index(')')]
                                        print(score3)
                                        score1 = score3.split(' : ')[0]
                                        score2 = score3.split(' : ')[1]
                                        print(score1)
                                        print(score2)
                                    if int(score1)+int(score2) < 2.5:
                                        list.append(-0.5)
                                    if int(score1)+int(score2) > 2.5:
                                        list.append(0.5)
                                    if int(score1) != 0 and int(score2) != 0:
                                        list.append(0.75)
                                    if int(score1) == 0 or int(score2) == 0:
                                        list.append(-0.75)
                                    print(list)
                                print(sum(list))
                            if sum(list) <= -5:
                                bot.send_message(561009671, driver.current_url+'\n'+f'<b>{home}</b>'+'\n'+f'<i>{away}</i>'+'\n'+f'<u>{country.text}</u>'+'✅', parse_mode='HTML')
                                print(driver.current_url)
                                home1.append(home)
                                away1.append(away)
                                country1.append(country.text)
                        except Exception as ee:
                            print(ee)


            except Exception:
                print(Exception)


            if len(driver.window_handles) > 1:
                driver.close()


            driver.switch_to.window(main_page)
            list.clear()
            print("----------------------------------------------------------------")

            df = pd.DataFrame.from_dict(
                {'Liga': country1, 'Home': home1, 'Away': away1})
            df.to_excel('result_tm25.xlsx', header=True, index=False)

if __name__ == "__main__":
    main()