import time
import json
import os
import random
from selenium import webdriver

url = 'http://www.higherlowergame.com/'
START_DELAY = 2
NEXT_LEVEL_DELAY = 4
NEXT_LEVEL_MID_DELAY = NEXT_LEVEL_DELAY / 2
DATABASE_FILENAME = 'db.json'

def wait(t):
    print 'Sleep for %s sec' % t
    time.sleep(t)

def load_database():
    if not os.path.exists(DATABASE_FILENAME):
        return {}
    with open(DATABASE_FILENAME, 'r') as f:
        return json.loads(f.read())

def save_database(db):
    with open(DATABASE_FILENAME, 'w') as f:
        print 'Dumping data to file'
        json.dump(db, f)

def start_game():
    driver.get(url)
    start_game_btn = driver.find_element_by_id('game-start-btn')
    wait(START_DELAY)
    start_game_btn.click()

def click_higher():
    print 'Click higher'
    driver.find_element_by_id('game-higher-btn').click()

def click_lower():
    print 'Click lower'
    driver.find_element_by_id('game-lower-btn').click()


def get_prev_card_data():
    root_div = '//div[@class="card card--prev"]'
    title = driver.find_element_by_xpath('%s/h1' % root_div).text
    number_field = driver.find_element_by_xpath('%s/h2' % root_div).text
    number = int(number_field.replace(',', '')) if number_field else None
    return title, number


def get_current_title():
    current_card = driver.find_element_by_xpath('//div[@class="card card--current"]/h1')
    return current_card.text

def take_screenshot():
    screenshots_dir = 'hl-screenshots'
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    pic_name = str(time.time()).replace('.', '') + '.png'
    print 'Taking screenshot'
    driver.save_screenshot(os.path.join(screenshots_dir, pic_name))

def play_again():
    print 'Playing again'
    driver.find_element_by_id('game-over-btn').click()

def make_decision(condition):
    if condition:
        click_higher()
    else:
        click_lower()

def play(rounds_num):
    start_game()

    for i in xrange(rounds_num):
        wait(NEXT_LEVEL_DELAY)
        prev_title, prev_num = get_prev_card_data()

        if not prev_num:
            print 'Game over'
            take_screenshot()
            play_again()
            continue

        db[prev_title] = prev_num
        current_title = get_current_title()

        if current_title in db.keys():
            print 'Yay! Found %s in database' % current_title
            make_decision(db[current_title] >= db[prev_title])
        else:
            print 'Choose random'
            make_decision(random.choice([True, False]))

if __name__ == '__main__':
    db = load_database()
    driver = webdriver.Firefox()
    try:
        play(100)
    except Exception as e:
        print e
    save_database(db)
    driver.close()
    
