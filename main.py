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
    matches[name] = defaultdict(int)

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
    for tl in team_left:
        try:
            tl.find_element(By.CLASS_NAME, "winner")
            #print("Left win")
            team_left_wins.append(1)
        except:
            #print("Right win")
            team_left_wins.append(0)

    # print("Clicked see more: ", iter, " times\n")
    # print("Collecting matches")
    match_names = driver.find_elements(By.CLASS_NAME, "player-name")
    match_num = 0
    num = 0
    num_ten = 0
    team_left = []
    team_right = []
    on_team_left = False
    for n in match_names:
        match_num = math.floor(num / 10)
        # is one left
        if num_ten < 5:
            if n.text.lower() == player.lower():
                on_team_left = True
            else:
                team_left.append(n.text)
        # is one right
        else:
            if n.text.lower() == player.lower():
                on_team_left = False
            if n.text.lower() != player.lower():
                team_right.append(n.text)

        if num_ten == 9: 
            team_left_win = team_left_wins[match_num] == 1
            print(player, "on team left: ", on_team_left)
            print("Left team won?: ", team_left_win)
            # on the left team and you won
            if on_team_left and team_left_win:
                for p in team_left:
                    matches[player][p]+=1
            # on the right team and you won
            elif not on_team_left and not team_left_win:
                for p in team_right:
                    matches[player][p]+=1
            team_left = []
            team_right = []

        num = num + 1
        num_ten = (num_ten + 1) % 10
    search_field.clear()

print(matches)
driver.close()

