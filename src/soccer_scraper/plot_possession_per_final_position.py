import pandas as pd
import matplotlib.pyplot as plt
import sys


def plot_top_5_teams(dataframe, size_point=20):
    top_5_teams = dataframe.loc[dataframe['league_position'] <= 5][
        ['team_name', 'season', 'possession', 'league_position']].sort_values(by=['season'], ascending=True)

    plt.scatter(top_5_teams['league_position'], top_5_teams['possession'], s=size_point)


def plot_relegated_teams(dataframe, last_position_relegated, size_point=20):
    relegated_teams = dataframe.loc[dataframe['league_position'] >= last_position_relegated][
        ['team_name', 'season', 'possession', 'league_position']].sort_values(by=['season'], ascending=True)

    plt.scatter(relegated_teams['league_position'], relegated_teams['possession'], s=size_point)


def plot_middle_teams(dataframe, last_position_relegated, total_num_teams, size_point=20):
    middle_teams = \
    dataframe.loc[dataframe['league_position'] < last_position_relegated].loc[dataframe['league_position'] > 5][
        ['team_name', 'season', 'possession', 'league_position']].sort_values(by=['season'], ascending=True)

    plt.scatter(middle_teams['league_position'], middle_teams['possession'], s=size_point)
    plt.ylabel("Possession (%)")
    plt.xlabel("Final Position")
    plt.xticks(range(1, total_num_teams + 1))
    plt.yticks([35, 40, 45, 50, 55, 60, 65])


league_data = {
    'league_name': 'La Liga',
    'last_position_relegated': 18,
    'total_num_teams': 20
}

# file_name = "Liga NOS_2018-02-21 14:42:10.021122"

size_point = 20

df = pd.read_csv('/home/alessandro/{file_name}.csv'.format(file_name=league_data['league_name']))

number_seasons_played = len(df.season.unique())

plot_top_5_teams(dataframe=df, size_point=size_point)

plot_relegated_teams(dataframe=df, last_position_relegated=league_data['last_position_relegated'],
                     size_point=size_point)

plot_middle_teams(dataframe=df, last_position_relegated=league_data['last_position_relegated'],
                  total_num_teams=league_data['total_num_teams'], size_point=size_point)

plt.title("{league_name} | Last {num_seasons_played} Seasons".format(league_name=league_data['league_name'],
                                                                     num_seasons_played=number_seasons_played))

plt.savefig('./graphics/{league_name}/possession_per_final_position.png'.format(league_name=league_data['league_name']))

plt.show()
