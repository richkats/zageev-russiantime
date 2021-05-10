# -*- coding: utf-8 -*-

import time
from selenium import webdriver
import word_db as db
import requests as req


def guesser(sel_driver):
    words = db.get_words()
    req.get(f'http://127.0.0.1:5000/set_words/{[word.russian for word in words]}')
    while True:
        time.sleep(1)
        try:
            # guessings = sel_driver.find_elements_by_class_name("chat-line__message")
            # guessings = sel_driver.find_elements_by_xpath("//*[@data-a-target='chat-message-text']")
            nicknames = sel_driver.find_elements_by_xpath("//*[@data-a-target='chat-message-username']")
            messages = sel_driver.find_elements_by_xpath("//*[@data-a-target='chat-message-text']")
            for i in range(len(messages)):
                word_guessed = db.compare(messages[i].text.lower(), words)
                if word_guessed:
                    print(f"{nicknames[i].text} guessed word {word_guessed.russian} ({word_guessed.english})")
                    req.get(f'http://127.0.0.1:5000/set_words/{[word.russian for word in words]}')
            if not words:
                break
        except Exception:
            continue


def login(username, password, driver):
    driver.get('https://www.twitch.tv/moderator/zageev')
    search_form = driver.find_element_by_id('login-username')
    search_form.send_keys(username)
    search_form = driver.find_element_by_id('password-input')
    search_form.send_keys(password)
    search_form.submit()
    driver.implicitly_wait(10)


def start_driver(d_type="chrome"):
    global chrome_options, driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    if d_type in ["chrome", "c"]:
        driver = webdriver.Chrome(chrome_options=chrome_options)  # Optional argument, if not specified will search path.
    elif d_type in ["opera", "o"]:
        driver = webdriver.Opera(options=chrome_options)
    driver.get('https://www.twitch.tv/popout/zageev/chat?popout=')


d_type = input("Insert your browser type: opera (o) or chrome (c): ")

start_driver(d_type)
while True:
    time.sleep(1)
    try:
        events = driver.find_elements_by_class_name('tw-c-text-alt-2')
        for event in events:
            if "Guess 3 russian words" in event.text:
                print(event.text)
                guesser(driver)
                driver.quit()
                start_driver(d_type)
                break
    except Exception:
        continue


time.sleep(60)

driver.quit()
