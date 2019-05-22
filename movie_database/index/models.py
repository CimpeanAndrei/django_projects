from django.db import models
import json
import urllib
import urllib.request
from urllib.parse import quote
from django.urls import reverse
# Create your models here.


class Title(models.Model):
  def getDataByTitle(self, title):
    title = urllib.parse.quote(title)
    request = urllib.request.Request("https://api.themoviedb.org/3/search/movie?api_key=c90b536a5d99162685d310661b1141a5&language=en-US&query=%s&page=1&include_adult=false" % title)
    response = urllib.request.urlopen(request)
    json_string = response.read().decode('utf-8')
    titleDict = json.loads(json_string)
    results = titleDict.get('results', [])
    for res in results:
      if res.get('id', None):
        self.movieData = {}
        self.movieData['Id'] = res['id']
        self.movieData['Title'] = res['title']
        self.movieData['Year'] = res['release_date']
        self.movieData['Plot'] = res['overview']
        if res['vote_average'] != 0:
          self.movieData['Rating'] = res['vote_average']
        else:
          self.movieData['Rating'] = "No ratings available"
        self.movieData['Date'] = res['release_date']
        for i in res['genre_ids']:
          genre = self.switchID_genres(i)
          self.movieData.setdefault('Genre', []).append(genre)
        self.movieData['Poster'] = self.generateImageLink(res['poster_path'])
      return self.movieData

  def generateImageLink(self, poster_path):
    imageURL = 'https://image.tmdb.org/t/p/w185' + poster_path
    return imageURL

  def switchID_genres(self, id):
    request = urllib.request.Request("https://api.themoviedb.org/3/genre/movie/list?api_key=c90b536a5d99162685d310661b1141a5&language=en-US")
    response = urllib.request.urlopen(request)
    json_string = response.read().decode('utf-8')
    genresDict = json.loads(json_string)
    genres = genresDict.get('genres', [])
    for dic in genres:
      if dic.get('id', None) == id:
        return dic.get('name')


class Year(models.Model):
  def getDataByYear(self, year, page):
    year = urllib.parse.quote(year)
    request = urllib.request.Request('https://api.themoviedb.org/3/discover/movie?primary_release_year=%s&page=%s&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key=c90b536a5d99162685d310661b1141a5' % (year, page))
    response = urllib.request.urlopen(request)
    json_string = response.read().decode('utf-8')
    yearDict = json.loads(json_string)
    if yearDict.get('total_results', None):
      self.yearData = {}
      self.yearData['Total_Results'] = yearDict['total_results']
      self.yearData['Total_Pages'] = yearDict['total_pages']
      results = yearDict.get('results', [])
      for item in results:
        temp_dict = {}
        temp_dict['Title'] = item['title']
        self.yearData.setdefault('Items', []).append(temp_dict)
    return self.yearData


class Genre(models.Model):
  def switchGenre_Id(self, genre):
    request = urllib.request.Request("https://api.themoviedb.org/3/genre/movie/list?api_key=c90b536a5d99162685d310661b1141a5&language=en-US")
    response = urllib.request.urlopen(request)
    json_string = response.read().decode('utf-8')
    genresDict = json.loads(json_string)
    genres = genresDict.get('genres', [])
    for dic in genres:
      if dic.get('name', None) == genre:
        return dic.get('id')

  def getDataByGenre(self, genre, page):
    request = urllib.request.Request("https://api.themoviedb.org/3/discover/movie?with_genres=%s&page=%s&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key=c90b536a5d99162685d310661b1141a5" % (genre, page))
    response = urllib.request.urlopen(request)
    json_string = response.read().decode('utf-8')
    genresDict = json.loads(json_string)
    if genresDict.get('total_results', None):
      self.genresData = {}
      self.genresData['Total_Results'] = genresDict['total_results']
      self.genresData['Total_Pages'] = genresDict['total_pages']
      results = genresDict.get('results', [])
      for item in results:
        temp_dict = {}
        temp_dict['Title'] = item['title']
        self.genresData.setdefault('Items', []).append(temp_dict)
    return self.genresData


class Keyword(models.Model):
  def getKeywordData(self, keyword, page):
    keyword = urllib.parse.quote(keyword)
    request = urllib.request.Request("https://api.themoviedb.org/3/search/movie?api_key=c90b536a5d99162685d310661b1141a5&language=en-US&query=%s&page=%s&include_adult=false" % (keyword, page))
    response = urllib.request.urlopen(request)
    json_string = response.read().decode('utf-8')
    movieDict = json.loads(json_string)
    results = movieDict.get('results', [])
    self.keywordData = {}
    self.keywordData['Total_Results'] = movieDict['total_results']
    self.keywordData['Total_Pages'] = movieDict['total_pages']
    for instance in results:
      if instance.get('id', None):
        temp_dict = {}
        temp_dict['Id'] = instance['id']
        temp_dict['Title'] = instance['title']
        temp_dict['Plot'] = instance['overview']
        temp_dict['Year'] = instance['release_date']
        if instance['vote_average'] != 0:
          temp_dict['Rating'] = instance['vote_average']
        else:
          temp_dict['Rating'] = "No movie data"
        temp_dict['Date'] = instance['release_date']
        for id in instance['genre_ids']:
          genre = self.switchID_genres(id)
          temp_dict.setdefault('Genre', []).append(genre)
        imageURL = 'https://image.tmdb.org/t/p/w185' + str(instance['poster_path'])
        temp_dict['Poster'] = imageURL
        self.keywordData.setdefault('Items', []).append(temp_dict)
    return self.keywordData

  def switchID_genres(self, id):
    request = urllib.request.Request("https://api.themoviedb.org/3/genre/movie/list?api_key=c90b536a5d99162685d310661b1141a5&language=en-US")
    response = urllib.request.urlopen(request)
    json_string = response.read().decode('utf-8')
    genresDict = json.loads(json_string)
    genres = genresDict.get('genres', [])
    for dic in genres:
      if dic.get('id', None) == id:
        return dic.get('name')
