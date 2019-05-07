#!/usr/bin/env python
# coding=utf-8
# (c) Ivan de Dios 2018 MIT License <ivanddf1994@gmail.com>

import webapp2
import json

from google.appengine.api import users, urlfetch
from webapp2_extras import jinja2
from time import sleep

from model.list import List
import model.movieList as movielist_mgt
import model.list as list_mgt

from model.message import Message
from model.tmdb import TMDB
from model.appinfo import AppInfo


class ListsManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        try:
            message_success = Message.message.get(self.request.GET['info'])
        except:
            message_success = None

        try:
            message_danger = Message.message.get(self.request.GET['error'])
        except:
            message_danger = None

        if user:
            access_link = users.create_logout_url("/")

            user_lists = list_mgt.get_user_lists_without_default(user.email())
            user_lists = list(user_lists)
            lists_elements = []
            for list_u in user_lists:
                lists_elements.append(movielist_mgt.count_movies(list_u.key.id()))

            user_default_lists = list_mgt.get_user_lists_default(user.email())
            user_default_lists = list(user_default_lists)
            lists_default_elements = []
            for list_default in user_default_lists:
                lists_default_elements.append(movielist_mgt.count_movies(list_default.key.id()))

            template_values = {
                "info": AppInfo,
                "access_link": access_link,
                "user": user,
                "lists": user_lists,
                "lists_elements": lists_elements,
                "defaultLists": user_default_lists,
                "defaultElements": lists_default_elements,
                "message_success": message_success,
                "message_danger": message_danger,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("lists/lists.html", **template_values))

        else:
            self.redirect("/")


class AddList(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            access_link = users.create_logout_url("/")
            try:
                message_danger = self.request.GET['error']
            except:
                message_danger = None

            template_values = {
                "info": AppInfo,
                "user": user,
                "access_link": access_link,
                "messageDanger": message_danger
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("/lists/add.html", **template_values))
        else:
            self.redirect("/")

    def post(self):
        user = users.get_current_user()
        if user:
            list_to_add = list_mgt.create_empty_list()
            list_to_add.user = user.email()
            list_to_add.name_list = self.request.get("name_list", "").strip()
            list_to_add.description_list = self.request.get("description_list", "").strip()

            # Chk
            if len(list_to_add.name_list) < 1:
                self.redirect("/lists/add?error=1679091C5A880FAF6FB5E6087EB1B2DC")
                return
            elif list_to_add.name_list == 'Favorites':
                self.redirect("/lists/add?error=8F14E45FCEEA167A5A36DEDD4BEA2543")
                return
            elif list_to_add.name_list == 'Watchlist':
                self.redirect("/lists/add?error=c16a5320fa475530d9583c34fd356ef5")
                return
            elif len(list_to_add.description_list) < 1:
                self.redirect("/lists/add?error=C9F0F895FB98AB9159F51FD0297E236D")
                return
            else:
                # Save
                list_mgt.update(list_to_add)
                sleep(1)
                self.redirect("/lists?info=45C48CCE2E2D7FBDEA1AFC51C7C6AD26")
        else:
            self.redirect("/")


class GetList(webapp2.RequestHandler):
    def get(self, id_list):
        user = users.get_current_user()
        access_link = users.create_logout_url("/")
        try:
            message_success = Message.message.get(self.request.GET['info'])
        except:
            message_success = None

        try:
            message_danger = Message.message.get(self.request.GET['error'])
        except:
            message_danger = None

        if user:
            # Get the information from the list from its id
            list_select = List.get_by_id(int(id_list))
            # Get all the movies that have the list
            id_movies = movielist_mgt.get_id_movies(user.email(), list_select.key.id())
            # Build the request to the API to get the information of each movie that was in the list and save this information in movies_values array
            api_key = TMDB.tmdb_api_key
            movies_values = []
            for id_movie in id_movies:
                url_movie = "https://api.themoviedb.org/3/movie/" + str(
                    id_movie) + "?api_key=" + api_key + "&language=en-US"
                result = urlfetch.fetch(url_movie, method=urlfetch.GET)
                movie = json.loads(result.content)
                movies_values.append(movie)

            id_tvshows = movielist_mgt.get_id_tvshow(user.email(), list_select.key.id())
            # Build the request to the API to get the information of each TV SHOW that was in the list and save this information in movies_values array
            tvshows_values = []
            for id_tv in id_tvshows:
                url_movie = "https://api.themoviedb.org/3/tv/" + str(
                    id_tv) + "?api_key=" + api_key + "&language=en-US"
                result = urlfetch.fetch(url_movie, method=urlfetch.GET)
                tvshow = json.loads(result.content)
                tvshows_values.append(tvshow)

            template_values = {
                "info": AppInfo,
                "user": user,
                "access_link": access_link,
                "list": list_select,
                "movies": movies_values,
                "tvshows": tvshows_values,
                "message_success": message_success,
                "message_danger": message_danger,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("/lists/seeListMovies.html", **template_values))
        else:
            self.redirect("/")


class UpdateList(webapp2.RequestHandler):
    def get(self, id_list):
        user = users.get_current_user()
        if user:
            access_link = users.create_logout_url("/")

            try:
                message_danger = self.request.GET['error']
            except:
                message_danger = None

            list_to_edit = List.get_by_id(int(id_list))
            if not list_to_edit:
                self.redirect("/lists/?error=Error! List not found!")

            template_values = {
                "info": AppInfo,
                "user": user,
                "list": list_to_edit,
                "access_link": access_link,
                "message_danger": message_danger
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("/lists/update.html", **template_values))
        else:
            self.redirect("/")
        return

    def post(self, id_list):
        user = users.get_current_user()
        if user:
            list_to_edit = List.get_by_id(int(id_list))
            if list_to_edit:
                list_to_edit.user = user.email()
                list_to_edit.name_list = self.request.get("name_list", "").strip()
                list_to_edit.description_list = self.request.get("description_list", "").strip()

                # Chk
                if len(list_to_edit.name_list) < 1:
                    self.redirect("/lists/update/" + id_list + "?error=1679091C5A880FAF6FB5E6087EB1B2DC")
                    return
                elif list_to_edit.name_list == 'Favorites':
                    self.redirect("/lists/update/" + id_list + "?error=8F14E45FCEEA167A5A36DEDD4BEA2543")
                    return
                elif len(list_to_edit.description_list) < 1:
                    self.redirect("/lists/update/" + id_list + "?error=C9F0F895FB98AB9159F51FD0297E236D")
                    return
                else:
                    # Save
                    list_mgt.update(list_to_edit)
                    sleep(1)
                    self.redirect("/lists?info=6512BD43D9CAA6E02C990B0A82652DCA")
            else:
                self.redirect("/lists?error=C20AD4D76FE97759AA27A0C99BFF6710")
        else:
            self.redirect("/")


class DeleteList(webapp2.RequestHandler):

    def post(self, id_list):
        user = users.get_current_user()
        if user:
            list_to_delete = List.get_by_id(int(id_list))
            if list_to_delete:
                # Get all the movies vinculated with the list to delete
                delete_movies = movielist_mgt.delete_all_movies_for_list(user.email(),
                                                                         list_to_delete.key.id())
                if not delete_movies:
                    self.redirect("/lists?error=C51CE410C124A10E0DB5E4B97FC2AF39")
                else:
                    # Delete the list
                    list_to_delete.key.delete()
                    sleep(1)
                    self.redirect("/lists?info=AAB3238922BCC25A6F606EB525FFDC56")
            else:
                self.redirect("/lists?error=C20AD4D76FE97759AA27A0C99BFF6710")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    (r'/lists', ListsManager),
    (r'/lists/add', AddList),
    (r'/lists/(\d*)', GetList),
    (r'/lists/update/(\d*)', UpdateList),
    (r'/lists/delete/(\d*)', DeleteList),
], debug=True)
