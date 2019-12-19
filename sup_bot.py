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
SLEEP        = .75

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

# checkout only works if cart is non-empty
def open_url(url):
    driver.get(url)
    sleep(SLEEP)

def add_with_style_and_sizes(styles):
    for style in styles:
        style.click()
        select,sizes = get_sizes()
        for size in sizes:
            select.select_by_value(size.get_attribute("value"))
            if add_item():
                return True

    return False

# TODO: multiple buttons for one item
def add_with_style(styles):
    for style in styles:
        style.click()
        if add_item():
            return True

    return False

def add_with_size(select, sizes):
    for size in sizes:
        select.select_by_value(size.get_attribute("value"))
        if add_item():
            return True

    return False

# TODO: Won't actually add to cart ... ever
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

        
def add_item_from_shop(item, loaded):
    # go to page of item if not loaded
    if not loaded:
        item_elem = driver.find_element_by_class_name(item)
        item_elem.click()
        sleep(SLEEP)

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
        return add_item()
    elif color_ways == None:
        return add_with_size(select, options)
    elif options == None:
        return add_with_style(color_ways)
    else:
        return add_with_style_and_sizes(color_ways)
    
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
    for box in boxes:
        box.click()

def get_clothes(clothes):
    if clothes == None or clothes == []:
        items = ["sweatshirts", "bags", "accessories", "hats", "shirts"]
    else:
        items = clothes
    for item in ["bags"]:
        print("Purchasing %s" % item)
        open_url(shop_url)
        if not add_item_from_shop(item, False):
            try:
                next = driver.find_element_by_class_name("next")
                next.click()
                sleep(SLEEP)
                add_item_from_shop(item, True)
            except:
                print("no next")
    open_url(checkout_url)

    ## Below only works once at checkout page
    if driver.current_url == checkout_url:
        fill_billing()
        fill_cc()
        fill_checkbox()
        add_item() # process payment - open CAPTCHA

if __name__ == '__main__':
  get_clothes(None)

