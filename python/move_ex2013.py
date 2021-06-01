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

url='https://ex2-ex2013/owa'
b.get(url)

username=b.find_element_by_id("username")
password=b.find_element_by_id("password")
signin=b.find_element_by_class_name("signinbutton")

username.send_keys("ex2\\administrator")
password.send_keys("Password123")

signin.click()
sleep(3)


find_element_by_xpath_block(["//span[contains(text(),'New')]", "..//.."]).click()
find_element_by_xpath_block(["//input[starts-with(@aria-label,'To')]"]).send_keys("Administrator@ex2.ca.amazon")
#find_element_by_xpath_block(["//input[@aria-label='To recipients. Enter an email address or a name from your contact list.']"]).send_keys(to)
find_element_by_xpath_block(["//span[contains(text(), 'Use this address:')]", ".."]).click()
#find_element_by_xpath_block(["//input[@placeholder='Add a subject']"]).send_keys("xxxx")
find_element_by_xpath_block(["//input[@aria-labelledby='MailCompose.SubjectWellLabel']"]).send_keys("xxxx")

find_element_by_xpath_block(["//button[@aria-label='Send']"]).click()



