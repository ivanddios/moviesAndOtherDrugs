#!/usr/bin/env python
# coding=utf-8
# (c) Ivan de Dios 2018 MIT License <ivanddf1994@gmail.com>
from time import sleep

import webapp2
from google.appengine.api import users
from model.list import List
import model.movieList as movielist_mgt


class AddMovieList(webapp2.RequestHandler):

    def post(self, id_movie):

        if self.request.GET['type'] == "f263d9a8b7cb4a9e573c18e5b9e15091":
            route = "/tv/" + id_movie
        else:
            route = "/movies/" + id_movie

        user = users.get_current_user()
        if user:
            # First, we remove the content from the user lists for the given movie
            delete_movies = movielist_mgt.delete_movie_in_lists(user.email(), int(id_movie))
            if not delete_movies:
                self.redirect(route + "?error=9BF31C7FF062936A96D3C8BD1F8F2FF3")

            # Then, we get the new assignations from form
            lists_form = self.request.get("list[]", allow_multiple=True)
            if lists_form:
                # We built each movie and added it to the correct list
                for list_id in lists_form:
                    list_select = List.get_by_id(int(list_id))
                    if not list_select:
                        self.redirect(route + "?error=C74D97B01EAE257E44AA9D5BADE97BAF")
                    movie_to_add_list = movielist_mgt.get_item(user.email(), list_select.key.id(), int(id_movie))

                    if movie_to_add_list:
                        self.redirect( route + "?error=70EFDF2EC9B086079795C442636B55FB")
                    else:
                        movie_to_add_list = movielist_mgt.create_empty_movie_list()
                        movie_to_add_list.user = user.email()
                        movie_to_add_list.id_movie = int(id_movie)
                        movie_to_add_list.id_list = list_select.key.id()
                        if "movies" in route:
                            movie_to_add_list.type_movie = "Movie"
                        else:
                            movie_to_add_list.type_movie = "TV Show"

                        # Chk
                        if len(movie_to_add_list.user) < 1:
                            self.redirect(route + "?error=C4CA4238A0B923820DCC509A6F75849B")

                        if movie_to_add_list.id_movie:
                            self.redirect(route + "?error=C81E728D9D4C2F636F067F89CC14862C")

                        if movie_to_add_list.id_list:
                            self.redirect(route + "?error=37693CFC748049E45D87B8C7D8B9AACD")

                        # Save
                        movielist_mgt.update(movie_to_add_list)
                self.redirect(route + "?info=1FF1DE774005F8DA13F42943881C655F")
            else:
                self.redirect(route + "?info=8E296A067A37563370DED05F5A3BF3EC")
        else:
            self.redirect("/")


class DeleteMovieList(webapp2.RequestHandler):

    def get(self, id_list, id_movie):
        user = users.get_current_user()
        if user:
            list_select = List.get_by_id(int(id_list))
            if list_select:
                movieList_to_delete = movielist_mgt.get_item(user.email(), int(id_list), int(id_movie))
                if movieList_to_delete:
                    # Delete
                    movieList_to_delete.key.delete()
                    sleep(1)
                    self.redirect("/lists/"+id_list+"?info=4E732CED3463D06DE0CA9A15B6153677")
                else:
                    self.redirect("/lists?error=02E74F10E0327AD868D138F2B4FDD6F0")
            else:
                self.redirect("/lists?error=C20AD4D76FE97759AA27A0C99BFF6710")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    (r'/lists/movies/add/(\d*)', AddMovieList),
    (r'/lists/(\d*)/movies/(\d*)/delete', DeleteMovieList),
], debug=True)
