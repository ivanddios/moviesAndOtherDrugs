#!/usr/bin/env python
# coding=utf-8
# (c) Ivan de Dios 2019 MIT License <ivanddf1994@gmail.com>

from google.appengine.ext import ndb


class MovieList(ndb.Model):
    user = ndb.TextProperty(indexed=True)
    id_list = ndb.IntegerProperty()
    id_movie = ndb.IntegerProperty()
    type_movie = ndb.TextProperty(indexed=True)


def create_empty_movie_list():
    return MovieList(user="", id_list=0, id_movie=0, type_movie="")


@ndb.transactional
def update(movie_list):
    return movie_list.put()


@ndb.transactional
def delete_movie_in_lists(user, id_movie):
    lists_user = MovieList.get_all_lists(user, id_movie)
    lists_user = list(lists_user)
    if lists_user:
        for lists in lists_user:
            lists.key.delete()
        return True
    else:
        return False


def delete_all_movies_for_list(user, id_list):
    movies_list = MovieList.query(MovieList.user == user, MovieList.id_list == id_list)
    movies_list = list(movies_list)
    if movies_list:
        for movie in movies_list:
            movie.key.delete()
        return True


def delete_movie_in_lists(user, id_movie):
    user_lists = MovieList.query(MovieList.user == user, MovieList.id_movie == id_movie)
    user_lists = list(user_lists)
    if user_lists:
        for movie in user_lists:
            movie.key.delete()
        return True


def get_item(user, id_list, id_movie):
    if user and id_list and id_movie:
        found_movie_list = MovieList.query(MovieList.user == user, MovieList.id_list == id_list,
                                           MovieList.id_movie == id_movie).get()
        if found_movie_list:
            return found_movie_list
        else:
            return None
    else:
        return None


def get_all_lists(user, id_movie):
    if user and id_movie:
        movies_lists = MovieList.query(MovieList.user == user, MovieList.id_movie == id_movie)
        if movies_lists:
            return movies_lists
        else:
            return None
    else:
        return None


def get_movies(user, id_list):
    if user and id_list:
        movies_lists = MovieList.query(MovieList.user == user, MovieList.id_list == id_list)
        if movies_lists:
            return movies_lists
        else:
            return None
    else:
        return None


def get_id_movies(user, id_list):
    id_movies = []
    movies_list = MovieList.query(MovieList.user == user, MovieList.id_list == id_list, MovieList.type_movie == "Movie")
    movies_list = movies_list.fetch()
    # Save the id of the movie from each tuple in movies array
    for movie in movies_list:
        id_movies.append(movie.id_movie)
    return id_movies


def get_id_tvshow(user, id_list):
    id_tv = []
    movies_list = MovieList.query(MovieList.user == user, MovieList.id_list == id_list,
                                  MovieList.type_movie == "TV Show")
    movies_list = movies_list.fetch()
    # Save the id of the movie from each tuple in movies array
    for movie in movies_list:
        id_tv.append(movie.id_movie)
    return id_tv


def count_movies(id_list):
    movies_list = MovieList.query(MovieList.id_list == id_list)
    movies_list = list(movies_list)
    return len(movies_list)+1
