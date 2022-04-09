import sqlite3 as sql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re

conn = sql.connect('database.db')
cur = conn.cursor()
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Billets' ''')
if cur.fetchone()[0]!=1 :
    cur.execute('''create table if not exists Billets (DataId integer,price float,delivery_time integer,needle_size text,composition text)''')
conn.commit()
conn.close()

df = pd.read_excel(r"C:/billets.xlsx", sheet_name='billets1')
cols = ['Brand', 'Name']
df['combined_search']= df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
df = df.drop(cols, axis = 1)
print(df)
print(len(df.index))
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=r'.\app\chromedriver.exe')
driver.get("https://www.wollplatz.de/")

conn = sql.connect('database.db')
cur = conn.cursor()
sql = 'INSERT INTO Billets (DataId,price,delivery_time,needle_size,composition) VALUES (%s,%s,%s, %s,%s,)'

for i in range(len(df.index)):
    current_url = driver.current_url
    inputElement = driver.find_element_by_id("searchSooqrTop").send_keys(df.iloc[i])
    link_string_contains = df.iloc[i].to_string(header=False, index=False)
    link_string_contains = link_string_contains.replace(" ","-")
    link_string_contains = link_string_contains.lower()
    print(link_string_contains)
    WebDriverWait(driver, 3).until(EC.url_changes(current_url))
    time.sleep(3)
    elems = driver.find_elements_by_xpath("//a[@href]")
    elem_id = driver.find_element_by_xpath("//div[@class = 'productlistholder productlist25 sqr-resultItem']")
    data_id_val = int(elem_id.get_attribute("data-id"))  # First column of the DB
    #elems = list(set(elems))
    value = None
    for elem in elems:
        if link_string_contains in elem.get_attribute("href"): #elem.get_attribute == str()
            elem.send_keys(Keys.CONTROL + Keys.RETURN)
            driver.switch_to.window(driver.window_handles[1])
            elems_table_size = driver.find_element_by_xpath("//*[@id='pdetailTableSpecs']/table")
            price_db =  driver.find_element_by_class_name("product-price-amount").text   #2nd column of db
            price_db = price_db.replace(",",".")
            price_db = float(price_db)
            #cur.execute("INSERT INTO table (`delivery_time`) VALUES (%s)", (price_db,)) # 3th column of the db

            try:
                elems_table = driver.find_elements_by_xpath("//*[@id='pdetailTableSpecs']/table/tbody/tr[4]/td[2]")
                for elem_table in elems_table:
                    if("%" in elem_table.text):
                        composition_db = elem_table.text # 5th column of db
                        break
                for elem_table_size in ((elems_table_size.text).splitlines()):
                    if("Nadelstärke" in elem_table_size):
                        needle_size = (re.findall(r'\d+',elem_table_size))            
                        needle_size_db =  int(''.join(needle_size)) #4th column of db
                        print("Needle size: " + str(needle_size_db))
                        print("Composition " + composition_db)
                        print("Price " + str(price_db))
                        
                # I couldn't find delivery time on the site so that I passed None to sql
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                #val = (data_id_val,price_db,value,needle_size_db,composition_db)
                cur.execute("INSERT INTO Billets VALUES (:DataId,:price,:delivery_time,:needle_size,:composition)",(data_id_val,price_db,value,needle_size_db,composition_db))
                #cur.execute(sql,val)
                conn.commit()
                break
            except:
                print("Exception Raised")
                try:
                    elems_table = driver.find_elements_by_xpath("//*[@id='pdetailTableSpecs']/table/tbody/tr[4]/td[2]/font/font")
                    for elem_table in elems_table:
                        print(elem_table.text)
                        if('%' in elem_table.text):
                            print(type(elem_table.text)+ "********************************")

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except:
                    print("Failed")
            print(price_db)
    time.sleep(5)
    print()
    WebDriverWait(driver, 3).until(EC.url_changes(current_url))
    driver.find_element_by_id('searchSooqrTop').clear()

conn.commit()
conn.close()
####################################################
