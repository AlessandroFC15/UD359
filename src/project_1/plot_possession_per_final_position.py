import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/home/alessandro/dadosCrl.csv')

# Pegar o top 5 de cada temporada e fazer uma média da posse
top_5_teams = df.loc[df['league_position'] <= 5][['team_name', 'season', 'possession', 'league_position']].sort_values(by=['season'], ascending=True)

plt.scatter(top_5_teams['league_position'], top_5_teams['possession'])
# plt.xticks([5, 4, 3, 2, 1])
plt.yticks([30, 35, 40, 45, 50, 55, 60, 65, 70])

# Pegar o top 5 de cada temporada e fazer uma média da posse
relegated_teams = df.loc[df['league_position'] >= 17][['team_name', 'season', 'possession', 'league_position']].sort_values(by=['season'], ascending=True)

print(relegated_teams['possession'].mean())

relegated_teams_with_at_least_50_possession = relegated_teams[relegated_teams['possession'] >= 50]

print(relegated_teams_with_at_least_50_possession)
print(len(relegated_teams_with_at_least_50_possession))
print(len(relegated_teams_with_at_least_50_possession) / len(relegated_teams))

plt.scatter(relegated_teams['league_position'], relegated_teams['possession'])
plt.xticks([1, 2, 3, 4, 5, 16, 17, 18, 19, 20])
plt.yticks([35, 40, 45, 50, 55, 60, 65])

middle_teams = df.loc[df['league_position'] < 17].loc[df['league_position'] > 5][['team_name', 'season', 'possession', 'league_position']].sort_values(by=['season'], ascending=True)

plt.scatter(middle_teams['league_position'], middle_teams['possession'])
plt.xticks(range(1, 21))
plt.yticks([35, 40, 45, 50, 55, 60, 65])

plt.show()
