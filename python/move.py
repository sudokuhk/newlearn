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
            sleep(1)
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

url='https://ad4-ex2016/owa'
b.get(url)

username=b.find_element_by_id("username")
password=b.find_element_by_id("password")
signin=b.find_element_by_class_name("signinbutton")

username.send_keys("ad4\\administrator")
password.send_keys("Password123")

signin.click()
sleep(3)

read_message("Administrator@ad4.ca.amazon", "sentitems")
#read_message("SecondUser@ad4.ca.amazon", "inbox")
#read_message("SharedMailbox@ad4.ca.amazon", "sentitems")
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

email = b.find_element_by_xpath("//span[contains(text(),'aaaa')]")
name = email.get_attribute('textContent')
print(name)

div = email.find_element_by_xpath("..//..//..")
class_attribute = div.get_attribute('class')

print("read")
ActionChains(b).context_click(email).perform()
sleep(1)

mark = b.find_element_by_xpath("//div[@aria-label='Context menu']")
print(mark)
print(mark.get_attribute('class'))
print(mark.get_attribute('textContent'))
btn = mark.find_element_by_xpath(".//span[contains(text(),'Move')]")
print(btn)
print(btn.get_attribute('class'))
#btn.click()
ActionChains(b).click(btn).perform()

move = b.find_element_by_xpath("//span[contains(text(), 'Move to a different folder...')]")
ActionChains(b).click(move).perform()
sleep(3)

#popupitem = b.find_element_by_xpath("//span[contains(text(), 'Move 1 conversation')]/../../span[contains(text(), 'Deleted Items')]")
#print(popupitem.get_attribute('textContent'))
popupitem = b.find_element_by_xpath("//span[contains(text(), 'Move 1 conversation')]//..//..")
print(popupitem.get_attribute('textContent'))
sleep(3)

deleteitem = popupitem.find_element_by_xpath(".//span[contains(text(), 'Drafts')]")
print("deleteitem.get_attribute('textContent')")
print(deleteitem.get_attribute('textContent'))
ActionChains(b).click(deleteitem).perform()

btn_move = b.find_element_by_xpath("//span[text()='Move']")
btn_move = btn_move.find_element_by_xpath("..")
print(btn_move.get_attribute('class'))
btn_move.click()



