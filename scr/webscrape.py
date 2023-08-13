import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List
import random, json

config = {
    "preferred_teams" : [
        "Clemson",
        "Alabama",
        "Georgia",
        "Ohio State",
        "Michigan",
        "USC",
        "Florida State",
        "LSU"
    ],
}

def scrape_team_links() -> List:
    url = "https://www.cbssports.com/college-football/teams/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    ## Find all tables containing team information
    tables = soup.find_all("table", class_="TableBase-table")

    urls = []

    # Iterate through each table
    for table in tables:
        # Iterate through rows in the table
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 4:  # Ensure there are at least 4 cells in a row
                link = cells[2].find("a")
                if link:
                    roster_suffix = link.get("href")
                    team_link = f"https://www.cbssports.com/{roster_suffix}"
                    print("Team Link:", team_link)
                    urls.append(team_link)
    return urls

def scrape_rosters(urls) -> dict:

    team_dict = {}

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract team information
        team_div = soup.find("div", class_="PageTitle-content")
        team_name = team_div.find("h1", class_="PageTitle-header").text.split("-")[0].strip()
        record_info = team_div.find("aside", class_="PageTitle-description").text.split(" • ")
        win_loss_record = record_info[0].strip()
        conference = record_info[1].split()[-1]  # Extract only the last part of the conference information
        conference_position = record_info[2].strip()
        roster_data = []

        # Find the table containing player information
        table = soup.find("table", class_="TableBase-table")

        # Iterate through rows in the table
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 3:  # Ensure there are at least 3 cells in a row
                number = cells[0].text.strip()
                name = cells[1].find("a").text.strip()
                position = cells[2].text.strip()
                height = cells[3].text.strip()
                weight = cells[4].text.strip()
                graduating_class = cells[5].text.strip()
                hometown = cells[6].text.strip()
                roster_data.append((number, name, position, height, weight, graduating_class, hometown))

        # Organize data into a DataFrame using pandas
        columns = ["Number", "Name", "Position", "Height", "Weight", "Graduating Class", "Hometown"]
        df = pd.DataFrame(roster_data, columns=columns)
        team_dict[team_name] = {
            "team_name": team_name,
            "record" : win_loss_record,
            "conference": conference,
            "conference_position": conference_position,
            "roster" : df.to_dict('records')
        }
    return team_dict

def scrape_random_game_this_week(week: str):

    returned_teams = []

    url = f"https://www.cbssports.com/college-football/schedule/FBS/2023/regular/{week}/"
    response_linked = requests.get(url)
    soup_linked = BeautifulSoup(response_linked.content, "html.parser")
    tables = soup_linked.find_all("table", class_="TableBase-table")
    #random_table = random.choice(tables)
    for table in tables:
       
        rows = table.find_all("tr")[1:]  # Exclude the header row
        for row in rows:
        #random_row = random.choice(rows) 
        
        # Extract spans with class "TeamName" from the random row
            team_name_spans = row.find_all("span", class_="TeamName")
            
            if len(team_name_spans) == 2:
                for preferred_team in config['preferred_teams']:
                    if (preferred_team in team_name_spans[0].get_text() or preferred_team in team_name_spans[1].get_text()):
                        team1_name = team_name_spans[0].get_text()
                        team2_name = team_name_spans[1].get_text()

                        # append tuple pair
                        returned_teams.append((team1_name, team2_name))
                            
    return returned_teams
