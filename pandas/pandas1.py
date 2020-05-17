import pandas as pd

url = "https://raw.githubusercontent.com/dm-fedorov/pandas_basic/master/data/football.csv"

football = pd.read_csv(url)
print("[Файл 1][Задание 1]Средний возраст футболистов:", int(football['Age'].mean()))
print("[Файл 1][Задание 2]Количество хладнокровных футболистов:", football['Composure'].count())
print("[Файл 1][Задание 3]Стандартное отклонение:", round(football['ShortPassing'].std(), 2))
print("[Файл 1][Задание 4]Сумма заработных плат:", football['Wage'].sum())
print("[Файл 1][Задание 5]Минимальная стоимость:", football['Value'].min())
print("[Файл 1][Задание 1]Средняя скорость с зарплатой выше среднего:",
      round(football[football.Wage > football.Wage.mean()].SprintSpeed.mean(), 2))
print("[Файл 1][Задание 2]Средняя скорость с зарплатой ниже среднего:",
      round(football[football.Wage < football.Wage.mean()].SprintSpeed.mean(), 2))
print("[Файл 1][Задание 3]Позиция игрока с высочайшей зарплатой:", football[football.Wage == football.Wage.max()]['Position'][0])
print("[Файл 1][Задание 4]Количество пенальти, сделанных бразильцами:", football[football.Nationality == 'Brazil'].Penalties.sum())
print("[Файл 1][Задание 5]Средний возраст игроков с точностью ударов головой выше 50:",
      round(football[football.HeadingAccuracy > 50]['Age'].mean(), 2))
print("[Файл 1][Задание 6]Самый молодой игрок с хладнокровием и реакцией выше 90:",
      football[(football.Composure > football.Composure.max() * 0.9) &
               (football.Reactions > football.Reactions.max() * 0.9)]['Age'].min())
print("[Файл 1][Задание 7]Разница в реакции самых старых и самых молодых:",
      round(football[football['Age'] == football['Age'].max()]['Reactions'].mean() -
            football[football['Age'] == football['Age'].min()]['Reactions'].mean(), 2))
print("[Файл 1][Задание 8]Страна с самыми дорогими игроками:",
      football[football['Value'] > football['Value'].mean()]['Nationality'].value_counts().keys()[0])
print("[Файл 1][Задание 9]Отношение зарплат у голкиперов с лучшими рефлексами и с лушим владением мячом:",
      round(football[(football['Position'] == 'GK') & (football['GKReflexes'] == football['GKReflexes'].max())][
                'Wage'].mean() /
            football[(football['Position'] == 'GK') & (football['GKHandling'] == football['GKHandling'].max())][
                'Wage'].mean(), 2))
print("[Файл 1][Задание 10]Отношение силы ударов наиболее и наименее агрессивных игроков:",
      round(football[football['Aggression'] == football['Aggression'].max()]['ShotPower'].mean() /
            football[football['Aggression'] == football['Aggression'].min()]['ShotPower'].mean(), 2))

print("[Файл 2][Задача 1]Испанцев с зарплатой не более четверти от максимальной:",
      football[football['Wage'] <= football[football['Nationality'] == 'Spain']
      ['Wage'].value_counts(bins=4).index[0].right]['Wage'].count())
print("[Файл 2][Задача 2]Различных национальностей в Manchester United:",
      len(football[football['Club'] == 'Manchester United']['Nationality'].unique()))
print("[Файл 2][Задача 3]Бразильцы, играющие в Juventus:",
      football[(football['Club'] == 'Juventus') & (football['Nationality'] == 'Brazil')]
      ['Name'].unique())
players = 0
top_club = ''
for club in football['Club'].unique():
    if football[(football['Club'] == club) & (football['Age'] > 35)]['Name'].count() > players:
        players = football[(football['Club'] == club) & (football['Age'] > 35)]['Name'].count()
        top_club = club
print("[Файл 2][Задача 4]Клуб с наибольшим числом игроков старше 35 лет:", top_club)
print("[Файл 2][Задача 5]Количество старейших аргентинцев-футболистов:",
      football[(football['Nationality'] == 'Argentina') &
               (football['Age'] >= football['Age'].value_counts(bins=4).index[3].left)]['Age'].count())
print("[Файл 2][Задача 6]Процент 21-летних футболистов от всего испанского состава:",
      round(football[football['Nationality'] == 'Spain']['Age'].value_counts(normalize=True)[21], 2))

print("[Файл 3][Задание 1]Средняя запрплата на различных позициях:",
      football.groupby(['Position']).mean()['Wage'].sort_values(ascending=False))
print("[Файл 3][Задание 1]Средняя запрплата в различных клубах:\n",
      football.groupby(['Club']).agg(['mean', 'median'])['Wage'])
clubs = []
max_salary_club = ''
max_salary = 0
for club in football['Club'].unique():
    if football[football['Club'] == club]['Wage'].mean() == football[football['Club'] == club]['Wage'].median():
        clubs.append(club)
        if football[football['Club'] == club]['Wage'].mean() > max_salary:
            max_salary = football[football['Club'] == club]['Wage'].mean()
            max_salary_club = club

print("[Файл 3][Задание 2]Клубы с одинаковой медианной и средней зарплатами:", clubs)
print("[Файл 3][Задание 2]Максимальная средняя оплата среди этих клубов:", max_salary)
print("[Файл 3][Задача ]Наименование этого клуба:", max_salary_club)

print("[Файл 3][Задача 1]Бюджет Chelsea:", football.groupby(['Club']).sum().loc['Chelsea']['Wage'])
print("[Файл 3][Задача 2]Максимальная зарплата двадцатилетнего аргентинца-футболиста:",
      football[(football['Nationality'] == 'Argentina') & (football['Age'] == 20)]['Wage'].max())
print("[Файл 3][Задача 3]Максимальная зарплата тридцатилетнего аргентинца-футболиста:",
      football[(football['Nationality'] == 'Argentina') & (football['Age'] == 30)]['Wage'].max())
print("[Файл 3][Задача 4]Минимальная зарплата тридцатилетнего аргентинца-футболиста:",
      football[(football['Nationality'] == 'Argentina') & (football['Age'] == 30)]['Wage'].min())
max_strength = football[(football['Club'] == 'FC Barcelona') &
                        (football['Nationality'] == 'Argentina')]['Strength'][0].max()
max_balance = football[(football['Club'] == 'FC Barcelona') &
                       (football['Nationality'] == 'Argentina')]['Balance'].max()
print("[Файл 3][Задача 5]Максимальные сила и баланс аргентинцев:", str(max_strength) + ';' + str(max_balance))
