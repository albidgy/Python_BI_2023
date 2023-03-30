import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# 1.1
response_scores = requests.get('https://www.imdb.com/chart/top/', params={'sort': 'nv,desc', 
                                                                          'mode': 'simple', 
                                                                          'page': 1})
soup_scores = BeautifulSoup(response_scores.content, 'lxml')
table_for_scores = soup_scores.find_all('tbody')[0]
title_cols_for_scores = table_for_scores.find_all('td', class_='titleColumn')
scores = table_for_scores.find_all('strong')
for idx in range(4):
    title_movie = title_cols_for_scores[idx].find_all('a')[0].text
    cur_score = re.search(r'\ ([\d\,]+?) ', str(scores[idx])).group(1)
    print(f'{str(idx+1)}. {title_movie} has {cur_score} scores.')

# 1.2
response_rating = requests.get('https://www.imdb.com/chart/top/', params={'ref_': 'nv_mp_mv250'})
soup_rating = BeautifulSoup(response_rating.content, 'lxml')
table_for_rating = soup_rating.find_all('tbody')[0]
title_cols_for_rating = table_for_rating.find_all('td', class_='titleColumn')
rating = table_for_rating.find_all('strong')
for idx in range(4):
    title_movie = title_cols_for_rating[idx].find_all('a')[0].text
    cur_rating = rating[idx].text
    
    print(f'{str(idx+1)}. {title_movie} has an average rating {cur_rating}.')

# 1.3
n_mov_by_directors = {}
response = requests.get('https://www.imdb.com/chart/top/', params={'ref_': 'nv_mp_mv250'})
soup = BeautifulSoup(response.content, 'lxml')
table = soup.find_all('tbody')[0]
title_cols = table.find_all('td', class_='titleColumn')
for idx in range(len(title_cols)):
    director = re.search(r'title=\"(.+?) \(dir.\)', str(title_cols[idx].find_all('a')[0])).group(1)
    n_mov_by_directors[director] = n_mov_by_directors.get(director, 0) + 1

directors_more_2mov_sorted = {key: val for key, val in sorted(n_mov_by_directors.items(), 
                                                              key=lambda item: item[1]) if val > 1}
plt.figure(figsize=(15,9))
sns.barplot(x=list(directors_more_2mov_sorted.keys()), y=list(directors_more_2mov_sorted.values()))
plt.ylabel('Number of movies', size=16)
plt.xticks(rotation=90, size=10);

# 1.4
scores_mov_by_directors = {}
response = requests.get('https://www.imdb.com/chart/top/', params={'ref_': 'nv_mp_mv250'})
soup = BeautifulSoup(response.content, 'lxml')
table = soup.find_all('tbody')[0]
title_cols = table.find_all('td', class_='titleColumn')
scores = table.find_all('strong')

for idx in range(len(scores)):
    director = re.search(r'title=\"(.+?) \(dir.\)', str(title_cols[idx].find_all('a')[0])).group(1)
    n_scores = re.search(r'\ ([\d\,]+?) ', str(scores[0])).group(1)
    n_scores = int(n_scores.replace(',', ''))
    scores_mov_by_directors[director] = scores_mov_by_directors.get(director, 0) + n_scores

scores_mov_by_directors_sorted = {key: val for key, val in sorted(scores_mov_by_directors.items(), 
                                                                  key=lambda item: item[1], reverse=True)}

counter = 0
for key, val in scores_mov_by_directors_sorted.items():
    if counter < 4:
        print(f'{int(counter + 1)}. {key}\'s films have been rated by {val} people.')
        counter += 1
    else:
        break

# 1.5
result_l = []

response = requests.get('https://www.imdb.com/chart/top/', params={'ref_': 'nv_mp_mv250'})
soup = BeautifulSoup(response_rating.content, 'lxml')
table = soup.find_all('tbody')[0]
title_cols = table.find_all('td', class_='titleColumn')
rating = table.find_all('strong')
for idx in range(len(rating)):
    name = title_cols[idx].find_all('a')[0].text
    rank = list(title_cols[idx].children)[0].strip().strip('.')
    year = title_cols[idx].find_all('span')[0].text.strip('()')
    cur_rating = rating[idx].text
    n_scores = re.search(r'\ ([\d\,]+?) ', str(scores[idx])).group(1)
    n_viewers = int(n_scores.replace(',', ''))
    director = re.search(r'title=\"(.+?) \(dir.\)', str(title_cols[idx].find_all('a')[0])).group(1)
    
    result_l.append([name, rank, year, cur_rating, n_viewers, director])
columns = ['name', 'rank', 'year', 'rating', 'n_viewers', 'director']
top250_movies = pd.DataFrame(result_l, columns=columns)
print(top250_movies)
