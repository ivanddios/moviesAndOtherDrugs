#!/usr/bin/env python
# coding=utf-8
# (c) Ivan de Dios 2018 MIT License <ivanddf1994@gmail.com>

import json

import webapp2
from google.appengine.api import users, urlfetch
from webapp2_extras import jinja2

import model.review as review_mgt
import model.list as list_mgt
import model.movieList as movieList_mgt
from model.message import Message
from model.appinfo import AppInfo
from model.tmdb import TMDB


class MoviesNowPlaying(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        access_link = users.create_logout_url("/")

        if user:
            fav_list_user = list_mgt.get_favorite(user.email())
            if not fav_list_user:
                fav_list_user = list_mgt.create_empty_list()
                fav_list_user.user = user.email()
                fav_list_user.name_list = "Favorites"
                fav_list_user.description_list = "Your favorites of always"
                list_mgt.update(fav_list_user)

            watch_list_user = list_mgt.get_watchlist(user.email())
            if not watch_list_user:
                watch_list_user = list_mgt.create_empty_list()
                watch_list_user.user = user.email()
                watch_list_user.name_list = "Watchlist"
                watch_list_user.description_list = "To see on your next free day"
                list_mgt.update(watch_list_user)

            api_key = TMDB.tmdb_api_key
            url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + api_key + "&language=en-US"
            result = urlfetch.fetch(url, method=urlfetch.GET)
            json_response = json.loads(result.content)
            movies = json_response.get("results")

            template_values = {
                "info": AppInfo,
                "user": user,
                "access_link": access_link,
                "movies": movies,
                "popular": False
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("movies/movies.html", **template_values))
        else:
            self.redirect("/")


class MoviesPopular(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        access_link = users.create_logout_url("/")

        if user:
            api_key = TMDB.tmdb_api_key
            url = "https://api.themoviedb.org/3/movie/popular?api_key=" + api_key + "&language=en-US"
            result = urlfetch.fetch(url, method=urlfetch.GET)
            json_response = json.loads(result.content)
            movies = json_response.get("results")

            template_values = {
                "info": AppInfo,
                "user": user,
                "access_link": access_link,
                "movies": movies,
                "popular": True
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("movies/movies.html", **template_values))
        else:
            self.redirect("/")


class MoviesUpcoming(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        access_link = users.create_logout_url("/")

        if user:
            api_key = TMDB.tmdb_api_key
            url = "https://api.themoviedb.org/3/movie/upcoming?api_key=" + api_key + "&language=en-US"
            result = urlfetch.fetch(url, method=urlfetch.GET)
            json_response = json.loads(result.content)
            movies = json_response.get("results")

            template_values = {
                "info": AppInfo,
                "user": user,
                "access_link": access_link,
                "movies": movies,
                "upcoming": True
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("movies/movies.html", **template_values))
        else:
            self.redirect("/")


class SearchMovie(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()
        access_link = users.create_logout_url("/")

        if not user:
            self.redirect("/")

        title = self.request.get("title", "").strip()
        title_format = title.replace(" ", "+")
        api_key = TMDB.tmdb_api_key
        url = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&query=" + title_format
        result = urlfetch.fetch(url, method=urlfetch.GET)
        json_response = json.loads(result.content)
        movies = json_response.get("results")

        url = "https://api.themoviedb.org/3/search/tv?api_key=" + api_key + "&query=" + title_format
        result = urlfetch.fetch(url, method=urlfetch.GET)
        json_response = json.loads(result.content)
        tvshows = json_response.get("results")

        template_values = {
            "info": AppInfo,
            "user": user,
            "access_link": access_link,
            "movies": movies,
            "tvshows":tvshows,
            "title": title
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("movies/searchMovies.html", **template_values))


class ShowMovie(webapp2.RequestHandler):

    def get(self, id_movie):
        try:
            message_success = Message.message.get(self.request.GET['info'])
        except:
            message_success = None

        try:
            message_danger = Message.message.get(self.request.GET['error'])
        except:
            message_danger = None

        user = users.get_current_user()
        access_link = users.create_logout_url("/")

        if not user:
            self.redirect("/")

        api_key = TMDB.tmdb_api_key
        url_movie = "https://api.themoviedb.org/3/movie/" + id_movie + "?api_key=" + api_key + "&language=en-US"
        result = urlfetch.fetch(url_movie, method=urlfetch.GET)
        movie = json.loads(result.content)

        # Check if the movie is in favorite list user
        fav_list = list_mgt.get_favorite(user.email())
        is_fav_movie = movieList_mgt.get_item(user.email(), fav_list.key.id(), int(id_movie))

        # Check if the movie is in watchlist user
        watchlist_list = list_mgt.get_watchlist(user.email())
        is_pending_movie = movieList_mgt.get_item(user.email(), watchlist_list.key.id(), int(id_movie))

        # Check and if exists, get the user review for this movie
        my_review = review_mgt.get_review(user.email(), int(id_movie))
        # We have to format dates of the review user for template
        if my_review:
            my_review_date_format = review_mgt.format_date(my_review.date)
        else:
            my_review_date_format = None

        # Check and it exists, ge the others users reviews
        others_reviews = review_mgt.get_others_reviews(user.email(), int(id_movie))
        if others_reviews:
            others_reviews = list(others_reviews)
            # Format the users dates reviews for template
            others_reviews_dates_format = review_mgt.format_dates(others_reviews)
        else:
            others_reviews_dates_format = None

        # Get the user lists
        my_lists = list_mgt.get_user_lists(user.email())
        my_lists = list(my_lists)

        # Returns the lists in which the movie is found
        movie_lists = movieList_mgt.get_all_lists(user.email(), int(id_movie))
        movie_lists = list(movie_lists)
        # Get only the lists identifier to match withe the __contains__ function in template
        lists_movies = []
        for movie_list in movie_lists:
            lists_movies.append(movie_list.id_list)

        template_values = {
            "info": AppInfo,
            "access_link": access_link,
            "user": user,
            "movie": movie,
            "my_review": my_review,
            "my_review_date": my_review_date_format,
            "other_reviews": others_reviews,
            "others_reviews_dates": others_reviews_dates_format,
            "is_favorite": is_fav_movie,
            "is_pending": is_pending_movie,
            "my_lists": my_lists,
            "lists_select": lists_movies,
            "message_success": message_success,
            "message_danger": message_danger,
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("movies/reviews.html", **template_values))


app = webapp2.WSGIApplication([
    ('/movies/now_playing', MoviesNowPlaying),
    ('/movies/popular', MoviesPopular),
    ('/movies/upcoming', MoviesUpcoming),
    ('/movies/search', SearchMovie),
    (r'/movies/([0-9]*)', ShowMovie),
], debug=True)
