import pandas as pd
import datetime
from random import randint
from time import sleep
import os.path
from urllib.request import Request, urlopen
import json
import numpy as np
from tqdm import tqdm

# Running this python file will ask you a year between 2016 and 2024 and a file path. It will then download in the file
# path all of the play by play data from that year in the NHL that is not already present in the file path mentionned.

# Ask the year of the NHL data wanted (between 2016 and 2024 inclusively)
year = str(input("Enter the year of the NHL season and playoffs' data you want to download (between 2016 and 2024 "
                 "inclusively): "))
assert int(year) < 2025 and int(year) > 2015
# Ask the file path for data saving
file_save_loc = str(input("Enter the file path to where you want to store the data: "))
filepath_exists = os.path.isdir(file_save_loc)
assert filepath_exists

url_1 = "https://api-web.nhle.com/v1/gamecenter/"
url_2 = "/play-by-play"
game_types = ["02", "03"] # Only interested in regular season and playoffs games
file_type = ".npy"

# Game number for regular season goes from 0001 to the total of games played that year
# We add 10 to each total of games to make sure there is not any game left to download
game_number_rs_2016 = 1230 + 10
game_number_rs_2017 = 1271 + 10
game_number_rs_2021 = 1312 + 10

# For playoffs, the game number is 0(round)(matchup)(game number)
rounds = ["1", "2", "3", "4"]
# We compute the matchup later
game_oo7 = ["1", "2", "3", "4", "5", "6", "7"]

for type in game_types:
    if type == "02": # Regular season
        if year == "2016":
            max_gn = int(game_number_rs_2016)
        elif year == "2017" or year == "2018" or year == "2019" or year == "2020":
            max_gn = int(game_number_rs_2017)
        else:
            max_gn = int(game_number_rs_2021)
        for i in tqdm(range(max_gn)):
            gn = i + 1
            if gn < 10:
                gn_str = "000" + str(gn)
            elif gn < 100:
                gn_str = "00" + str(gn)
            elif gn < 1000:
                gn_str = "0" + str(gn)
            else:
                gn_str = str(gn)

            gid = year + type + gn_str

            # Procedure to see if the file is alreay downloaded
            already_downloaded = os.path.isfile(file_save_loc + gid + file_type)
            if already_downloaded:
                print("Already downloaded " + gid)
                continue

            # The file was not downloaded
            
            # We used the code from the source below for reading a json file by accessing it with its url
            # https://stackoverflow.com/questions/67475470/while-reading-json-data-from-url-using-python-gives-error-
            # urllib-error-httperro

            url = url_1 + gid + url_2
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

            try:
                response = urlopen(req).read()
                data = json.loads(response)
                np.save(file_save_loc + gid, data)
            except:
                print("Could not open : " + url)

    else: # Playoffs
        for rnd in rounds:
            gn_1 = "0" + rnd
            max_matchup = round(8 / (2**(int(rnd) - 1)))
            for i in range(max_matchup):
                matchup = i + 1
                gn_2 = gn_1 + str(matchup)
                for game in game_oo7:
                    gn = gn_2 + game

                    gid = year + type + gn

                    # Procedure to see if the file is alreay downloaded
                    already_downloaded = os.path.isfile(file_save_loc + gid + file_type)
                    if already_downloaded:
                        print("Already downloaded " + gid)
                        continue

                    # The file was not downloaded
                    url = url_1 + gid + url_2
                    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

                    try:
                        response = urlopen(req).read()
                        data = json.loads(response)
                        np.save(file_save_loc + gid, data)
                    except:
                        print("Could not open : " + url)
                        break
