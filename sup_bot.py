# Supreme_Bot-v1.0
# 6.8.19

# - Automates adding items from the shop to cart and filling out payment info
# - Requires human intervention to complete CAPTCHA
# - When attempting to add an item from the shop that is sold out, all size 
# and style combinations will try to be added to the cart until an in stock
# combo is found. If all sizes and styles are sold out, the process will 
# return to the shop_url and contiune with the rest of the desired items
# - As of now, the first item of the item type (ie bags, hats, shirts) is
# selected to be added to the cart.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

shop_url     = "https://www.supremenewyork.com/shop"
checkout_url = "https://www.supremenewyork.com/checkout"
driver       = webdriver.Firefox()

class Billing:
    name  = "Foo Bar" 
    email = "foo.bar@gmail.com"
    tel   = "617-420-6969"
    addr  = "50 Winthrop St"
    zip   = "02474"
    city  = "Arlington"
    state = "MA"
    
# should store credentials in ENV variables
class CC:
    num = "1111 2222 3333 4444"
    mon = "03"
    yr  = "2020"
    cvv = "123"

bill_info = Billing()
cc_info   = CC()

def open_shop():
    driver.get(shop_url)
    sleep(1)

def open_checkout():
    driver.get(checkout_url)
    sleep(.5)

def add_with_style_and_sizes(styles):
    for i in range(len(styles)):
        styles[i].click()
        select,sizes = get_sizes()
        for j in range(len(sizes)):
            select.select_by_value(sizes[j].get_attribute("value"))
            bought = add_item()
            if bought:
                return

def add_with_style(styles):
    for i in range(len(styles)):
        styles[i].click()
        bought = add_item()
        if bought:
            return

def add_with_size(select, sizes):
    for j in range(len(sizes)):
        select.select_by_value(sizes[j].get_attribute("value"))
        bought = add_item()
        if bought:
            return

def add_item():
    try:
        add_button = driver.find_element_by_name("commit")
        add_button.click()
        return True
    except: 
        print("sold out")
        return False

def get_sizes():
    try:
        size = driver.find_element_by_name("s")
        select = Select(size)
        options = select.options
    except: 
        print("one size")
        options = None
        select = None

    return select,options

        
def add_item_from_shop(item):
    item_elem = driver.find_element_by_class_name(item)
    item_elem.click()
    sleep(.5)

    try:
        styles = driver.find_element_by_class_name("styles ")
        color_ways = styles.find_elements_by_tag_name("li")
    except: 
        print("no styles")
        color_ways = None
        
    try:
        size = driver.find_element_by_name("s")
        select = Select(size)
        options = select.options
    except: 
        print("one size")
        options = None

    if color_ways == None and options == None:
        add_item()
    elif color_ways == None:
        add_with_size(select, options)
    elif options == None:
        add_with_style(color_ways)
    else:
        add_with_style_and_sizes(color_ways)
    
def fill_billing():
    name = driver.find_element_by_id("order_billing_name")
    name.send_keys(bill_info.name)
    email = driver.find_element_by_id("order_email")
    email.send_keys(bill_info.email)
    tel = driver.find_element_by_id("order_tel")
    tel.send_keys(bill_info.tel)
    addr = driver.find_element_by_id("bo")
    addr.send_keys(bill_info.addr)
    zip = driver.find_element_by_id("order_billing_zip")
    zip.send_keys(bill_info.zip)
    city = driver.find_element_by_id("order_billing_city")
    city.send_keys(bill_info.city)
    state = driver.find_element_by_id("order_billing_state")
    select = Select(state)
    select.select_by_value(bill_info.state)

def fill_cc():
    cc_num = driver.find_element_by_id("nnaerb")
    cc_num.send_keys(cc_info.num)
    cc_mon = driver.find_element_by_id("credit_card_month")
    cc_yr = driver.find_element_by_id("credit_card_year")
    select = Select(cc_mon)
    select.select_by_value(cc_info.mon)
    select = Select(cc_yr)
    select.select_by_value(cc_info.yr)
    cc_cvv = driver.find_element_by_id("orcer")
    cc_cvv.clear()
    cc_cvv.send_keys(cc_info.cvv)

# remembers info for next time and accepts Terms and Condos.
def fill_checkbox():
    boxes = driver.find_elements_by_class_name("iCheck-helper")
    for i in range(0,len(boxes)):
        boxes[i].click()

def main():
    items = ["sweatshirts", "bags", "accessories", "hats", "shirts"]
    for item in items:
        print "Purchasing {}".format( item )
        open_shop()
        add_item_from_shop(item)
    open_checkout()
    fill_billing()
    fill_cc()
    fill_checkbox()
    add_item() # process payment - open CAPTCHA

if __name__ == "__main__":
    main()
