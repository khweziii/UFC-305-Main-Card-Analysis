import requests
import re
import pandas as pd
from bs4 import BeautifulSoup



ufc_fight_stats_raw = requests.get("http://ufcstats.com/fight-details/6c44af21414e4143")

ufc_fight_stats_soup = BeautifulSoup(ufc_fight_stats_raw.content, "html.parser")

ufc_stats_table = ufc_fight_stats_soup.find("table", class_="b-fight-details__table js-fight-table")

ufc_stats_table_body = ufc_stats_table.find_all("tbody")

ufc_stats_table_body_rows = ufc_stats_table.find_all("tr")


# numbers = re.findall(r"\d+", text) # /d+ matches one or more (+) digits (\d)

columns = ["Round", "Fighter", "Significant Strikes Landed", "Significant Strikes Attempted",
           "Takedowns Completed", "Takedowns Attempted"]

ufc_305_stats = pd.DataFrame(columns=columns)


for round in range(1, 5, 1):

    fighter_1_statistics = pd.DataFrame([{
        "Round": round,
        "Fighter": ufc_stats_table_body_rows[round].find_all("a")[0].getText(),
        "Significant Strikes Landed": re.findall(r"\d+",ufc_stats_table_body_rows[round].find_all("p", class_="b-fight-details__table-text")[
            4].getText().strip())[0],
        "Significant Strikes Attempted": re.findall(r"\d+",ufc_stats_table_body_rows[round].find_all("p", class_="b-fight-details__table-text")[
            4].getText().strip())[1],
        "Takedowns Completed": re.findall(r"\d+",ufc_stats_table_body_rows[round].find_all("p", class_="b-fight-details__table-text")[
            10].getText().strip())[0],
        "Takedowns Attempted": re.findall(r"\d+",ufc_stats_table_body_rows[round].find_all("p", class_="b-fight-details__table-text")[
            10].getText().strip())[1]
       }])

    ufc_305_stats = pd.concat([ufc_305_stats, fighter_1_statistics], ignore_index=True)

    fighter_2_statistics = pd.DataFrame([{
        "Round": round,
        "Fighter": ufc_stats_table_body_rows[round].find_all("a")[1].getText(),
        "Significant Strikes Landed": re.findall(r"\d+",ufc_stats_table_body_rows[round].find_all("p", class_="b-fight-details__table-text")[
            5].getText().strip())[0],
        "Significant Strikes Attempted": re.findall(r"\d+",ufc_stats_table_body_rows[round].find_all("p", class_="b-fight-details__table-text")[
            5].getText().strip())[1],
        "Takedowns Completed": re.findall(r"\d+",ufc_stats_table_body_rows[round].find_all("p", class_="b-fight-details__table-text")[
            11].getText().strip())[0],
        "Takedowns Attempted": re.findall(r"\d+",ufc_stats_table_body_rows[round].find_all("p", class_="b-fight-details__table-text")[
            11].getText().strip())[1]
    }])

    ufc_305_stats = pd.concat([ufc_305_stats, fighter_2_statistics], ignore_index=True)

ufc_305_stats.to_csv("ufc_fight_stats.csv", index=False) # export data frame as a csv file

print(ufc_305_stats)