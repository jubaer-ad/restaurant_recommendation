from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from csv import writer
import time
import threading
import inspect

def resource001():
    driver = webdriver.Chrome("./chromedriver")
    
    locations = []
    driver.get("https://madchef.com.bd/contact#branches")
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    replacer = {'\n':'','  ':''}
    for div in soup.find_all('div', attrs = {'class': 'branch-name'}):
        locations.append(div.text.strip())
    locations = [location.replace("\n","").replace("  ","") for location in locations]
    # print(locations)

    menus = []
    prices = []
    driver.get("https://madchef.com.bd/menu")
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for a in soup.find_all('a', href=True, attrs={'class': 'menu-item'}):
        menu = a.find('div', attrs={'class':'menu-item-title'})
        price = a.find('div', attrs={'class':'menu-item-price'})
        menus.append(menu.text.strip())
        prices.append(price.text.replace('৳','').strip())

    driver.close()

    df1 = pd.DataFrame({'menu':menus, 'price':prices})
    df1 = df1.reset_index()


    with open('madchef.csv','w',encoding='utf8',newline='') as f:
        theWriter = writer(f)
        header = ['resource', 'menu', 'price', 'location']
        theWriter.writerow(header)
        for location in locations:
            for index, data in df1.iterrows():
                row = ['madchef',data['menu'], data['price'], location]
                theWriter.writerow(row)
                
    print(inspect.getframeinfo(inspect.currentframe()).function, "Completed")
    
def resource002():
    driver = webdriver.Chrome("./chromedriver")
    
    menus = []
    prices = []
    
    driver.get("https://www.pizzahutbd.com/")
    time.sleep(2)
    driver.find_element("xpath", "//input[@placeholder='Enter your delivery location']").click()
    time.sleep(1)
    element = driver.find_element("id", "pac-input")
    element.send_keys('Mirpur')
    time.sleep(1)
    element.send_keys(Keys.DOWN)
    time.sleep(1)
    element.send_keys(Keys.ENTER)
    time.sleep(1)
    
    urls = ["https://www.pizzahutbd.com/pizza/all", "https://www.pizzahutbd.com/pasta/all", "https://www.pizzahutbd.com/appetisers/all", "https://www.pizzahutbd.com/drinks/all"]
    for url in urls:
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for div in soup.find_all('div', attrs={'class': 'container thame collapseExample'}):
            sizes = []
            menu = div.find('div', attrs={'class':'left-con-pizzas'}).text.strip()
            for data_panes in div.findAll('tbody', attrs={'id':'product_content'}):
                for size_pane in data_panes.findAll('td', attrs={'class':'custom_piza_check'}):
                    size = size_pane['data-size'].replace("price_","")
                    sizes.append(size)
                for price_pane in data_panes.findAll('div', attrs={'class','pizzaPrice'}):
                    price = price_pane.text.strip()
                    prices.append(price)
                    
            for size in sizes:
                menus.append(menu + " - " + size)
        
        print(len(menus), len(prices))

    locations = []
    driver.get("https://www.pizzahutbd.com/store-filter")
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for span in soup.find_all('span', attrs = {'class': 'storename'}):
        locations.append(span.text.strip())
    locations = [location.replace("\n","").replace("  ","").replace("Pizza Hut ","") for location in locations]
    # locations = [location.replace("Delivery ", "") + " (Delivery)" for location in locations if "Delivery " in location]
    for i in range(len(locations)):
        if "Delivery " in locations[i]:
            locations[i] = locations[i].replace("Delivery ", "") + "(Delivery)"
    print(locations)
    
    offers = []
    offer_prices = []
    driver.implicitly_wait(3)
    driver.get("https://www.pizzahutbd.com/deals/all")
    driver.implicitly_wait(3)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for div in soup.findAll('div', attrs={'class':'deals-card-content'}):
        item_name = div.find('div', attrs={'class':'deal-item-name'}).text.strip()
        item_description = div.find('div', attrs={'class':'deal-item-desc'}).text.strip()
        offers.append(item_name + " - " + item_description)
        price = div.find('span', attrs={'class':'pro_price'})
        if price is None:
            price = "NA"
        else:
            price = price.text.strip()
        offer_prices.append(price)
    print(offers)
    print(offer_prices)

    driver.close()
    
    df_offer = pd.DataFrame({'offer':offers, 'price': offer_prices})
    df_offer.to_csv('pizzahutbdOffers.csv', encoding='utf-8', index=False)

    df = pd.DataFrame({'menu':menus, 'price':prices})
    df = df.reset_index()


    with open('pizzahutbd.csv','w',encoding='utf8',newline='') as f:
        theWriter = writer(f)
        header = ['resource', 'menu', 'price', 'location']
        theWriter.writerow(header)
        for location in locations:
            for index, data in df.iterrows():
                row = ['pizzahutbd',data['menu'], data['price'], location]
                theWriter.writerow(row)
                
    
    print(inspect.getframeinfo(inspect.currentframe()).function, "Completed")

def combine_csv():
    df = pd.concat(map(pd.read_csv,['madchef.csv', 'pizzahutbd.csv']), ignore_index=True)
    df.to_csv('restaurantData.csv', encoding='utf-8', index=False)
    print(inspect.getframeinfo(inspect.currentframe()).function, "Completed")
    
if __name__=="__main__":
    t1 = threading.Thread(target=resource001, args=())
    t2 = threading.Thread(target=resource002, args=())
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    t3 = threading.Thread(target=combine_csv, args=())
    t3.start()
    t3.join()
    
    print(inspect.getframeinfo(inspect.currentframe()).function, "Completed")


