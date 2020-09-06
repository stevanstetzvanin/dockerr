from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from pathlib import Path
from urllib.parse import urlparse
import sys
import json
import os

url = 'http://www.twitch.tv/'

############# CHROME DRIVER ##############

def chromebrowser(proxy, nogui): # use proxy = None to disable it. nogui as boolen
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--lang=en-US,en")
    # chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--disable-notifications")
    chrome_driver_path = get_full_path('/drivers/chromedriver')
    if proxy != None:
        current_proxy = proxy
        chrome_options.add_argument("--proxy-server={}".format(current_proxy))
        print("Using proxy: [{}]".format(current_proxy))
    if nogui:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)
    return browser

############# FIREFOX DRIVER #############

def firefoxbrowser(nogui): # use nogui as boolean
    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en-US')
    # profile.set_preference('media.volume_scale', '0.0')
    firefox_driver_path = get_full_path('/drivers/geckodriver')
    options = webdriver.firefox.options.Options()
    options.headless = nogui
    browser = webdriver.Firefox(firefox_profile=profile, executable_path=firefox_driver_path, options=options)
    return browser

##########################################

##########################################
############## UNUSED STUFF ##############
# def search_tags_with_text(browser, tag, text):
#     elements = browser.find_elements_by_tag_name(tag)
#     for element in elements:
#         if element.text == text:
#             return element

# def search_tags_with_attribute(browser, tag, attribute, value):
#     elements = browser.find_elements_by_tag_name(tag)
#     for element in elements:
#         if element.get_attribute(attribute) == value:
#             return element

# def start_bonus_farm(browser):
#     input(' Press ENTER when bonus button appear to start farming...')
#     while True:
#             try:
#                 browser.find_element_by_class_name('tw-button--success').click()
#                 print(' Bonus successfully redeemed!')
#             except:
#                 print(' Error! stoping farm and exiting...')
#                 break
#             else:
#                 print(' Waiting 15 minutes for the next bonus...')
#                 sleep(905)

# def bonus_click(browser):
#     try:
#         browser.find_element_by_class_name('tw-button--success').click()
#         print(' Bonus reedemed.')
#     except:
#         print(' No bonus found.')
#         pass
##########################################
##########################################

def get_full_path(file_path):
    return str(Path("{}{}".format(os.getcwd(), file_path)))

def get_data():
    with open(get_full_path("/data.json")) as data_file:
        data = json.load(data_file)
    return data

def consult_database(data):
    for x in get_data()[data]:
        print("{} - {}" .format(x,get_data()[data][x]))

def change_theme(browser): # change color theme
    menu = browser.find_element_by_css_selector('[data-a-target="user-menu-toggle"')
    menu.click()
    browser.find_element_by_css_selector('[data-a-target="dark-mode-toggle"]').click()
    menu.click()
    print("Theme color changed.")

def mature_check(browser): # +18 channel check
    try:
        browser.find_element_by_css_selector('[data-a-target="player-overlay-mature-accept"]').click()
        print("Mature checked successfully.")
    except:
        print("No mature check needed.")
        pass

def chat_rules(browser):   # click on chat rules
    try:
        browser.find_element_by_tag_name('textarea').click() 
        browser.find_element_by_css_selector('[data-test-selector="chat-rules-ok-button"]').click()
        print("Chat rules accepted on first try.")
    except:
        try:
            browser.find_element_by_css_selector('[data-test-selector="chat-rules-ok-button"]').click()
            print("Chat rules accepted on second try.")
        except:
            print("Its ready to type!")
            pass

def type_in_chat(browser, sent): # type in chat
    try:
        browser.find_element_by_tag_name('textarea').send_keys(sent)
        browser.find_element_by_css_selector('[data-a-target="chat-send-button"]').click()
    except:
        print("Error can't type in chat.")
        pass

def channel_raid_check(browser, channel):
    parse = urlparse(browser.current_url)
    if parse.query == 'referrer=raid':
        print("Looks like channel is raided. Ganking in chat")
        mature_check(browser)
        chat_rules(browser)
        type_in_chat(browser, '#gank from {}' .format(channel))
        sleep(1)
        return True
    else:
        return False

def bonus_start(browser, channel):
    redeems = 1
    print("Starting farm points!")
    while bonus_redeem(browser, redeems):
        redeems += 1
        print("Waiting for the next bonus...")
        sleep(1)
    if channel_raid_check(browser, channel):
        print("Stoping farm.")
    elif channel_status(browser, channel, True):
        print("Some error occured. Restarting farm.")
        bonus_start(browser, channel)
        
def bonus_redeem(browser, redeems):
    try:
        bonus_el = WebDriverWait(browser, 910, poll_frequency=5).until(EC.presence_of_element_located((By.CLASS_NAME, 'tw-button--success')))
        bonus_el.click()
        print("Successfully redeemed {} bonus!" .format(redeems))
        return True
    except TimeoutException:
        return False

def idler(browser, channel):
    print("Idle started on selected channel. Page will be refreshed every 15 minutes.\n")
    timecounter = 0
    while True:
        sleep(900)
        browser.get(url + channel)
        timecounter += 15
        print("Currently idle for {} minutes" .format(timecounter))

def chat_spam(browser, src_text): # enable forsen spam
    text = src_text
    for _ in range(10):
        type_in_chat(browser, text)
        text += ' ' + src_text
        sleep(1.5)

def spam(browser): # small spam
    type_in_chat(browser, 's')
    sleep(0.3)
    type_in_chat(browser, 'p')
    sleep(0.3)
    type_in_chat(browser, 'a')
    sleep(0.3)
    type_in_chat(browser, 'm')

def channel_status(browser, channel, refresh):
    if refresh:
        browser.refresh()
        sleep(3)
    try:
        if (urlparse(browser.current_url).path == '/{}' .format(channel)) and (browser.find_element_by_class_name('tw-channel-status-text-indicator--mask').text == 'LIVE'):
            print("This channel is live.")
            return True
    except:
        print("This channel is not live.")
        return False

def set_low_quality(browser):
    browser.find_element_by_css_selector('[data-a-target="player-settings-button"]').click()
    browser.find_element_by_css_selector('[data-a-target="player-settings-menu-item-quality"]').click()
    qualities = browser.find_elements_by_class_name('tw-radio__label')
    q = len(qualities)
    print("Video quality set to {}" .format(qualities[q-1].text))
    qualities[q-1].click()

##########################################

def exit_script():
    print("Exiting.")
    b.quit()
    sys.exit()

def start_bonus(channel):
    print("\n\n--------- checking stuff --------- \n")
    if channel_status(b, channel, False) == True:
        mature_check(b)
        chat_rules(b)
        # set_low_quality(b)
        print("\n---------------------------------- \n\n")
        bonus_start(b, channel)
    print("\n---------------------------------- \n\n")
    exit_script()

def start_idler(channel):
    print("\n\n--------- checking stuff --------- \n")
    mature_check(b)
    chat_rules(b)
    # set_low_quality(b)
    print("\n---------------------------------- \n\n")
    idler(b, channel)
    exit_script()

def main():
    print("\nGetting accounts listing to login.")
    consult_database('accounts')
    acc = input("\n Enter account number to login: ")
    if acc in get_data()['accounts']:
        username = get_data()['accounts'][acc]
        password = get_data()['passwords'][acc]
    else:
        print("Number doesn't match, insert the credentials.")
        username = input(" Login username: ")
        password = input(" Login password: ")
    print("Attempting login to {} account." .format(username))

    WebDriverWait(b, 5).until(EC.presence_of_element_located((By.ID, 'login-username'))).send_keys(username)
    b.find_element_by_id('password-input').send_keys(password)
    b.find_element_by_css_selector('[data-a-target="passport-login-button"]').click()
    code = input("\n Enter here the 6-digit verification code: ")
    b.find_element_by_css_selector('[pattern="[0-9]*"]').click()
    b.find_element_by_css_selector('[pattern="[0-9]*"]').send_keys(code)
    sleep(3)

    print("\nAvailable channels:")
    consult_database('channels')
    cchannel = input("\n Enter channel number to navigate: ")
    if cchannel in get_data()['channels']:
        channel = get_data()['channels'][cchannel]
    else:
        channel = input("Number doesn't match with any channel \n Insert channel name: ")
    print("Redirecting to {}{}" .format(url,channel))

    b.get(url + channel)
    sleep(6)
    change_theme(b)
    if nogui:
        start_idler(channel)
    else:
        start_bonus(channel)

##########################################

print("\n     TWITCH AUTOMATION SCRIPT.\n     MADE BY")
print("     -----------------------------------------------------------------")
print("      :::::::: ::::::::::: ::::::: :::     :::     :::     :::.    :::")
print("     :+:+:         :+:     :+:     :+:     :+:   :+: :+:   :+::.   :+:")
print("     +:+:+         +:+     +:+     +:+     +:+  +:+   +:+  +:++:+  +:+")
print("      #+#+#+#      +#+     +#++#+# +#++   ++#+ +#++:++#++: +#+ +:+++#+")
print("         +#+#+     +#+     +#+      +#+   +#+  +#+     +#+ +#+   +#+#+")
print("         #+#+#     #+#     #+#       #+# #+#   #+#     #+# #+#    #+#+")
print("     ########      ###     #######     ###     ###     ### ###     ###")
print("     -----------------------------------------------------------------")

driver = input("\nSelect the browser:\n1 - to use chrome\n2 - to use firefox\n Type browser number: ")
while (driver != '1' and driver != '2'):
    driver = input("Wrong browser number try again: ")

hl = input("\nRun without graphic user interface?\n Type Y to yes. N to no: ")
if (hl == 'Y' or hl == 'y'):
    nogui = True
else:
    nogui = False

if driver == '1':
    b = chromebrowser(None, nogui)
else:
    b = firefoxbrowser(nogui)

b.get(url + 'login')
sleep(3)
main()