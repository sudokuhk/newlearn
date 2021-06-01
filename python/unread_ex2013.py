from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.common.action_chains import ActionChains


def find_element_by_xpath(paths):
    element = b
    for path in paths:
        element = element.find_element_by_xpath(path)
    print(element)
    return element

def find_element_by_xpath_no_exception(paths):
    print("find_element_by_xpath_no_exception ---> ")
    print(paths)
    try:
        return find_element_by_xpath(paths)
    except BaseException:
        print("find_element_by_xpath_no_exception, do not found.")
        return None

def find_element_by_xpath_block(paths):
    print("find_element_by_xpath_block ---> ")
    print(paths)
    count = 120
    while True:
        try:
            return find_element_by_xpath(paths)
        except BaseException as e:
            print("do not found element: ")
            print(paths)
            count = count - 1
            if count == 0:
                raise e
                
def read_message(mailbox, folder):
    __get_url(mailbox, folder, sys._getframe().f_code.co_name)
        
        
def __get_url(mailbox, folder, msg):
    url = "https://ad4-ex2016/owa/" + mailbox + "/#path=/mail/" + folder
    print(msg + url)
    b.get(url)
        
#browser=webdriver.Firefox()

b=webdriver.Chrome() 

url='https://ex2-ex2013/owa'
b.get(url)

username=b.find_element_by_id("username")
password=b.find_element_by_id("password")
signin=b.find_element_by_class_name("signinbutton")

username.send_keys("ex2\\administrator")
password.send_keys("Password123")

signin.click()
sleep(3)


paths = [
    #"//span[contains(text(),'Sent Items')]",
    "//div[contains(@class,'subfolders')]/child::div",
    #"../.."
]
#sentitems = find_element_by_xpath_block(paths)
#sentitems = b.find_element_by_xpath("//div[contains(@class,'subfolders')]")
#name = sentitems.get_attribute('textContent')
#print(name)

sentitems = b.find_element_by_xpath("//span[contains(text(),'Sent Items')]")
name = sentitems.get_attribute('textContent')
print(name)
ActionChains(b).click(sentitems).perform()
sleep(3)

email = b.find_element_by_xpath("//span[contains(text(),'xxxx')]")
name = email.get_attribute('textContent')
print(name)

div = email.find_element_by_xpath("..//..//..")
class_attribute = div.get_attribute('class')
if 'ms-fwt-sb' in class_attribute:
    print("unread")
else:
    print("read")
    ActionChains(b).context_click(email).perform()
    sleep(1)
    
    mark = b.find_element_by_xpath("//div[@aria-label='Context menu']")
    print(mark)
    print(mark.get_attribute('class'))
    print(mark.get_attribute('textContent'))
    btn = mark.find_element_by_xpath(".//span[contains(text(),'Mark as unread')]")
    print(btn)
    print(btn.get_attribute('class'))
    #btn.click()
    ActionChains(b).click(btn).perform()
    
    

sentitems = b.find_element_by_xpath("//span[contains(text(),'Sent Items')]")
name = sentitems.get_attribute('textContent')
print(name)
ActionChains(b).context_click(sentitems).perform()
sleep(3)

mark = b.find_element_by_xpath("//div[@aria-label='Context menu']")
print(mark)
print(mark.get_attribute('class'))
print(mark.get_attribute('textContent'))
btn = mark.find_element_by_xpath(".//span[contains(text(),'Empty folder')]")
print(btn)
print(btn.get_attribute('class'))
#btn.click()
ActionChains(b).click(btn).perform()

btn_ok = b.find_element_by_xpath("//span[text()='OK']")
btn_ok = btn_ok.find_element_by_xpath("..")
btn_ok.click()




