import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/home/alessandro/dadosCrl.csv')

# print(df.sort_values(by=['possession'], ascending=False)[['league_position', 'team_name', 'possession', 'season']])

# Pegar o top 5 de cada temporada e fazer uma média da posse

champion_teams = df.loc[df['league_position'] <= 1].sort_values(by=['season'], ascending=True)

print(champion_teams[['team_name', 'season']])

plt.ylabel("Posse de bola (%)")
plt.plot(champion_teams['season'], champion_teams['possession'])

for a,b in zip(champion_teams['season'], champion_teams['possession']):
    plt.text(a, b, str(b) + "%", verticalalignment='bottom', horizontalalignment='center')

plt.show()

print()
# print(df.loc[df['league_position'] <= 1][['league_position', 'team_name', 'possession', 'season']].sort_values(by=['possession'], ascending=False))
# print(df.loc[df['league_position'] <= 5]["possession"].mean())

