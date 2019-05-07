#!/usr/bin/env python
# (c) Ivan de Dios 2018 MIT License <ivanddf1994@gmail.com>

import webapp2
from google.appengine.api import users
import model.list as list_mgt
import model.movieList as movielist_mgt


class AddToDefaultList(webapp2.RequestHandler):

    def get(self, id_movie):

        if self.request.GET['type'] == "f263d9a8b7cb4a9e573c18e5b9e15091":
            route = "/tv/" + id_movie
        else:
            route = "/movies/" + id_movie

        user = users.get_current_user()
        if user:
            if self.request.GET['list'] == "d78986947356ddd37b43d57df289dee9":
               user_default_list = list_mgt.get_favorite(user.email())
            else:
                user_default_list = list_mgt.get_watchlist(user.email())

            movie_to_add_default_list = movielist_mgt.get_item(user.email(), user_default_list.key.id(), int(id_movie))
            if not movie_to_add_default_list:
                movie_to_add_default_list = movielist_mgt.create_empty_movie_list()
                movie_to_add_default_list.user = user.email()
                movie_to_add_default_list.id_list = user_default_list.key.id()
                movie_to_add_default_list.id_movie = int(id_movie)
                if "movies" in route:
                    movie_to_add_default_list.type_movie = "Movie"
                else:
                    movie_to_add_default_list.type_movie = "TV Show"

                # Chk
                if len(movie_to_add_default_list.user) < 1:
                    self.redirect(route + "?error=C4CA4238A0B923820DCC509A6F75849B")
                    return

                if not movie_to_add_default_list.id_movie:
                    self.redirect(route + "?error=C81E728D9D4C2F636F067F89CC14862C")
                    return
                # Save
                movielist_mgt.update(movie_to_add_default_list)
                if self.request.GET['list'] == "d78986947356ddd37b43d57df289dee9":
                    self.redirect(route + "?info=A87FF679A2F3E71D9181A67B7542122C")
                else:
                    self.redirect(route + "?info=34173cb38f07f89ddbebc2ac9128303f")
            else:
                self.redirect(route + "?error=ECCBC87E4B5CE2FE28308FD9F2A7BAF3")
        else:
            self.redirect("/")


class DeleteToDefaultList(webapp2.RequestHandler):

    def get(self, id_movie):

        if self.request.GET['type'] == "f263d9a8b7cb4a9e573c18e5b9e15091":
            route = "/tv/" + id_movie
        else:
            route = "/movies/" + id_movie

        user = users.get_current_user()
        if user:
            if self.request.GET['list'] == "d78986947356ddd37b43d57df289dee9":
                user_default_list = list_mgt.get_favorite(user.email())
            else:
                user_default_list = list_mgt.get_watchlist(user.email())
            movie_to_delete_default_list = movielist_mgt.get_item(user.email(), user_default_list.key.id(), int(id_movie))
            if movie_to_delete_default_list:
                # Delete
                movie_to_delete_default_list.key.delete()
                if self.request.GET['list'] == "d78986947356ddd37b43d57df289dee9":
                    self.redirect(route + "?info=E4DA3B7FBBCE2345D7772B0674A318D5")
                else:
                    self.redirect(route + "?info=6ea9ab1baa0efb9e19094440c317e21b")
                return
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    (r'/lists/addDefaultList/(\d*)', AddToDefaultList),
    (r'/lists/deleteDefaultList/(\d*)', DeleteToDefaultList),
], debug=True)
