from bs4 import BeautifulSoup as bsoup
import requests
from datetime import datetime
import re

class Movie:
    genres: list[str] = []
    origins: list[str] = []
    duration: int = 0
    score: float = 0.0
    release_date: datetime = None
    
    def __init__(self, title: str) -> None:
        self.title = title
        
    def set_geners(self, geners: list[str]) -> 'Movie':
        self.genres = geners
        return self
    
    def set_origins(self, origins: list[str]) -> 'Movie':
        self.origins = origins
        return self
    
    def set_duration(self, duration: int) -> 'Movie':
        self.duration = duration
        return self
    
    def set_release_date(self, release_date: datetime) -> 'Movie':
        self.release_date = release_date
        return self
    
    def set_score(self, score: float) -> 'Movie':
        self.score = score
        return self
    
    def __str__(self) -> str:
        return f"<Moive \ntitle:{self.title} \ngeners:{self.genres} \norigins:{self.origins} \nduration:{self.duration} \nrelease_date:{self.release_date}>"
        
        

REQ_URL = 'https://ssr1.scrape.center/page'
movies: list[Movie] = []

page = 1
while True:
    response = requests.get(
        url=f"{REQ_URL}/{page}"
    )
    if response.status_code != 200:
        break

    soup = bsoup(response.text, features="html.parser")
    result = soup.find_all(name='div', class_='el-card item m-t is-hover-shadow')
    
    for el in result:
        title = el.h2.string
        movie = Movie(title=title)
        
        buttons =  el.find_all(name='button', class_='el-button category el-button--primary el-button--mini')
        genres = [s.span.string for s in buttons]
        
        info = el.find_all(name='div', class_='m-v-sm info')
        producing_info = tuple(filter(lambda string: string != ' / ',map(lambda span: span.string, info[0].find_all(name='span'))))
        
        origins = producing_info[0].split('、')
        duration = int(producing_info[1].replace(' 分钟', ''))
        
        if (info[1].span):
            # YYYY-MM-DD XX
            date_match = re.search(r'\d{4}-\d{2}-\d{2}',info[1].span.string)
            if date_match:
                release_date = date_match.group(0)
                movie.set_release_date(datetime.strptime(release_date, '%Y-%m-%d'))
                
        score = float(el.find(name='p', class_='score').string.strip())
        movie.set_geners(genres).set_duration(duration).set_origins(origins).set_score(score)
        
        movies.append(movie)
    
    page += 1
    
for movie in movies:
    print(movie)    
    print("\n")
    
print(len(movies))
    
    
    
        