#!/usr/bin/env python
# (c) Ivan de Dios 2018 MIT License <ivanddf1994@gmail.com>

import datetime

import webapp2
from google.appengine.api import users

from model.review import Review
import model.review as review_mgt


class AddReview(webapp2.RequestHandler):

    def post(self, id_movie):

        if self.request.GET['type'] == "f263d9a8b7cb4a9e573c18e5b9e15091":
            route = "/tv/" + id_movie
        else:
            route = "/movies/" + id_movie

        user = users.get_current_user()
        if user:
            review_to_add = review_mgt.get_review(user.email(), int(id_movie))
            if not review_to_add:
                review_to_add = review_mgt.create_empty_review()
            review_to_add.user = user.email()
            review_to_add.id_movie = int(id_movie)
            review_to_add.date = datetime.datetime.now()
            review_to_add.content = self.request.get("review", "").strip()

            # Chk
            if len(review_to_add.user) < 1:
                self.redirect(route + "?error=C4CA4238A0B923820DCC509A6F75849B")
                return
            elif not review_to_add.id_movie:
                self.redirect(route + "?error=C81E728D9D4C2F636F067F89CC14862C")
                return
            elif len(review_to_add.content) < 1:
                self.redirect(route + "?error=6F4922F45568161A8CDF4AD2299F6D23")
                return
            else:
                # Save
                review_mgt.update(review_to_add)
                self.redirect(route + "?info=33e75ff09dd601bbe69f351039152189")
        else:
            self.redirect("/")


class UpdateReview(webapp2.RequestHandler):

    def post(self, id_review):

        if self.request.GET['type'] == "f263d9a8b7cb4a9e573c18e5b9e15091":
            route = "/tv/"
        else:
            route = "/movies/"

        user = users.get_current_user()
        if user:
            review_to_modify = Review.get_by_id(int(id_review))
            if review_to_modify:
                review_to_modify.date = datetime.datetime.now()
                review_to_modify.content = self.request.get("review", "").strip()

                # Chk
                if len(review_to_modify.user) < 1:
                    self.redirect(
                        route + str(review_to_modify.id_movie) + "?error=C4CA4238A0B923820DCC509A6F75849B")
                    return
                elif not review_to_modify.id_movie:
                    self.redirect(
                        route + str(review_to_modify.id_movie) + "?error=C81E728D9D4C2F636F067F89CC14862C")
                    return
                elif len(review_to_modify.content) < 1:
                    self.redirect(
                        route + str(review_to_modify.id_movie) + "?error=6F4922F45568161A8CDF4AD2299F6D23")
                    return
                else:
                    # Save-Update
                    review_mgt.update(review_to_modify)
                    self.redirect(
                        route + str(review_to_modify.id_movie) + "?info=1F0E3DAD99908345F7439F8FFABDFFC4")
            else:
                self.redirect(route + str(review_to_modify.id_movie) + "?error=98F13708210194C475687BE6106A3B84")
                return
        else:
            self.redirect("/")


class DeleteReview(webapp2.RequestHandler):

    def post(self, id_review):

        if self.request.GET['type'] == "f263d9a8b7cb4a9e573c18e5b9e15091":
            route = "/tv/"
        else:
            route = "/movies/"

        user = users.get_current_user()
        if user:
            review_to_delete = Review.get_by_id(int(id_review))
            if review_to_delete:
                # Delete
                review_to_delete.key.delete()
                self.redirect(route + str(review_to_delete.id_movie) + "?info=3C59DC048E8850243BE8079A5C74D079")
            else:
                self.redirect(route + str(review_to_delete.id_movie) + "?error=B6D767D2F8ED5D21A44B0E5886680CB9")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    (r'/reviews/add/(\d*)', AddReview),
    (r'/reviews/update/(\d*)', UpdateReview),
    (r'/reviews/delete/(\d*)', DeleteReview),
], debug=True)
