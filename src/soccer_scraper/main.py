import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import re
import datetime
from src.soccer_scraper.exceptions import TeamStatisticsNotFound


class LeagueScraper:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=options)
    base_url = "https://www.whoscored.com"

    def __init__(self, league_name, league_url):
        self.league_name = league_name
        self.league_url = league_url
        self.seasons = []
        self.league_data = []
        self.data_frame = None

    @staticmethod
    def bypass_access_denied_page():
        LeagueScraper.driver.get(LeagueScraper.base_url)
        print('Ready to go!')

    def get_seasons_urls(self):
        LeagueScraper.driver.get(self.league_url)

        select_seasons = LeagueScraper.driver.find_element_by_css_selector('#seasons')

        seasons = select_seasons.find_elements_by_tag_name('option')

        for s in seasons:
            self.seasons.append(
                {
                    'season': s.text,
                    'relative_url': s.get_attribute('value')
                }
            )

    @staticmethod
    def get_teams_statistics_url(season_relative_url):
        full_url = LeagueScraper.base_url + season_relative_url

        if LeagueScraper.driver.current_url != full_url:
            LeagueScraper.driver.get(full_url)

        sub_menu = LeagueScraper.driver.find_element_by_css_selector("#sub-navigation")

        menu_items = sub_menu.find_elements_by_tag_name('a')

        for item in menu_items:
            if item.text == "Team Statistics":
                return item.get_attribute('href')

        return None

    @staticmethod
    def find_league_id(team_statistics_url):
        p = re.compile('.*Stages/([0-9]*)/.*')

        return p.match(team_statistics_url).group(1)

    @staticmethod
    def get_teams_position_data(league_relative_url):
        """ This method will return a dictionary with an example as follows:
            'Arsenal' : { 'league_position': 3 }
        """
        LeagueScraper.driver.get(LeagueScraper.base_url + league_relative_url)

        teams_data = {}

        standings_table_body = LeagueScraper.driver.find_element_by_css_selector('.standings')

        for row in standings_table_body.find_elements_by_tag_name('tr'):
            team_name = row.find_element_by_class_name('team').text

            teams_data[team_name] = {'league_position': row.find_element_by_class_name('o').text}

        return teams_data

    def get_teams_detailed_stats(self, team_statistics_url, season):
        teams_data = {}

        LeagueScraper.driver.get(team_statistics_url)

        try:
            WebDriverWait(LeagueScraper.driver, 3).until(
                EC.presence_of_element_located((By.ID, 'top-team-stats-summary-grid')))

            summary_table_body = LeagueScraper.driver.find_element_by_id('top-team-stats-summary-content')

            teams_rows = summary_table_body.find_elements_by_tag_name('tr')

            for tr in teams_rows:
                team_name = tr.find_element_by_css_selector('.tn').text

                teams_data[team_name] = {
                    'league_name': self.league_name,
                    'goals': tr.find_element_by_css_selector('.goal').text,
                    'shots_per_game': tr.find_element_by_css_selector('.shotsPerGame').text,
                    'possession': tr.find_element_by_css_selector('.possession').text,
                    'num_yellow_cards': tr.find_element_by_css_selector('.yellow-card-box').text,
                    'num_red_cards': tr.find_element_by_css_selector('.red-card-box').text,
                    'pass_completion_rate': tr.find_element_by_css_selector('.passSuccess').text,
                    'season': season,
                }
        except TimeoutException:
            print("Loading took too much time!")

        return teams_data

    @staticmethod
    def get_teams_specific_passes_data(team_statistics_url):
        if LeagueScraper.driver.current_url != team_statistics_url:
            LeagueScraper.driver.get(team_statistics_url)

        pass_types_button = LeagueScraper.driver.find_element_by_css_selector('a[href="#stage-passes"]')

        pass_types_button.click()

        WebDriverWait(LeagueScraper.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#stage-passes-content tr')))

        league_id = LeagueScraper.find_league_id(team_statistics_url)

        LeagueScraper.driver.get(
            "https://www.whoscored.com/stagestatfeed/{league_id}/stageteams/?against=0&field=2&teamId=-1&type=11".format(
                league_id=league_id))

        raw_data = LeagueScraper.driver.find_element_by_tag_name('body').text.replace("'", '"')

        json_data = json.loads(raw_data)[0]

        detailed_data = {}

        for team_data in json_data:
            detailed_data[team_data[1]] = {
                'normal_cross': 0,
                'assist_cross': 0,
                'normal_longball': 0,
                'assist_longball': 0,
                'normal_short': 0,
                'assist_short': 0,
                'normal_throughball': 0,
                'assist_throughball': 0,
            }

            for pass_type in team_data[3][0][1]:
                detailed_data[team_data[1]]["{}_{}".format(pass_type[0], pass_type[1])] = pass_type[2][0]

        return detailed_data

    def scrape_teams_statistics(self, season_data):
        team_statistics_url = LeagueScraper.get_teams_statistics_url(season_data['relative_url'])

        if not team_statistics_url:
            print("# Season {} doesn't have team statistics".format(season_data['season']))
            raise TeamStatisticsNotFound()

        teams_data = LeagueScraper.get_teams_position_data(season_data['relative_url'])

        detailed_stats = self.get_teams_detailed_stats(team_statistics_url, season_data['season'])

        for key, value in detailed_stats.items():
            teams_data[key].update(value)

        specific_passes_data = LeagueScraper.get_teams_specific_passes_data(team_statistics_url)

        for key, value in specific_passes_data.items():
            teams_data[key].update(value)

        for team_name, team_data in teams_data.items():
            team_data['team_name'] = team_name

            self.league_data.append(team_data)

    def start(self):
        # LeagueScraper.bypass_access_denied_page()

        self.get_seasons_urls()

        print(self.seasons)

        for season in self.seasons:
            print('>> Scraping season {}'.format(season['season']))

            try:
                self.scrape_teams_statistics(season)
            except TeamStatisticsNotFound:
                break

        self.data_frame = pd.DataFrame(self.league_data)

        self.data_frame.to_csv('/home/alessandro/{}.csv'.format(self.league_name), index=False)


league_scraper = LeagueScraper(league_url="https://www.whoscored.com/Regions/206/Tournaments/4/Spain-La-Liga",
                                       league_name="La Liga")

league_scraper.start()

