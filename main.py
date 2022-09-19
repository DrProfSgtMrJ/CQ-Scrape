from array import array
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import math


player_set = set()
matches = {}
win = {}
URL_MATCH_HISTORY = "https://championsqueue.lolesports.com/en-us/match-history"
URL_MAIN = "https://championsqueue.lolesports.com/en-us/"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL_MAIN)


time.sleep(3)
loop = 0


# # Get Player Names
while loop < 10:
    #print("loop ", loop)
    try:
        element = driver.find_element(By.CLASS_NAME, "see-more-button")
        driver.execute_script("arguments[0].click();", element)
        loop = loop + 1
        time.sleep(3)
    except:
        break

names = driver.find_elements(By.CLASS_NAME, "player-row")

for n in names:
    split_text = n.text.split('\n')
    #print("Adding: ", split_text[3])
    name = split_text[3]
    player_set.add(name)
    matches[name] = defaultdict(list)
    win[name] = defaultdict(int)

time.sleep(3)

# Populate Matches
driver.get(URL_MATCH_HISTORY)
time.sleep(3)


search_field = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/main/div[2]/div[1]/div/input")
time.sleep(3)

#team_left = driver.find_elements(By.CSS_SELECTOR, "div[class ='team left")
# team_right = driver.find_elements(By.CSS_SELECTOR, "div[class ='team right")

# for tl in team_left:
#     try:
#         tl.find_element(By.CLASS_NAME, "winner")
#         print("left")
#     except:
#         print("right")

# print(len(team_left))
# print(len(team_right))

for player in player_set:
    #print("Searching for player: ", player)
    search_field.send_keys(player)
    time.sleep(3)
    # print("Clicking see more button")
    iter = 0
    while iter < 20:
        try:
            element = driver.find_element(By.CLASS_NAME, "see-more-button")
            driver.execute_script("arguments[0].click();", element)
            iter = iter + 1
            time.sleep(3)
        except:
            break

    team_left = driver.find_elements(By.CSS_SELECTOR, "div[class ='team left")

    team_left_wins = []
    team_right_wins = []
    for tl in team_left:
        try:
            tl.find_element(By.CLASS_NAME, "winner")
            #print("Left win")
            team_left_wins.append(1)
            team_right_wins.append(0)
        except:
            #print("Right win")
            team_left_wins.append(0)
            team_right_wins.append(1)

    # print("Clicked see more: ", iter, " times\n")
    # print("Collecting matches")
    match_names = driver.find_elements(By.CLASS_NAME, "player-name")
    match_num = 0
    num = 0
    num_ten = 0
    for n in match_names:
        match_num = math.floor(num / 10)
        # print("Match: ", match_num + 1)
        #print("Adding ", n.text, " to matches")
        matches[player][match_num].append(n.text)

        if n.text.lower() == player.lower():
            if num_ten < 5:
                #print(player, " Left Team result: ", team_left_wins[match_num])
                win[player][match_num] = team_left_wins[match_num]
            else :
                #print(player, " Right Team result: ", team_right_wins[match_num])
                win[player][match_num] = team_right_wins[match_num]
        num = num + 1
        num_ten = (num_ten + 1) % 10
    #print(matches[player])
    search_field.clear()

driver.close()

