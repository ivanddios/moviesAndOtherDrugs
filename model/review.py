#!/usr/bin/env python
# coding=utf-8
# (c) Iván 2019 MIT License <ivanddf1994@gmail.com>
import calendar
import datetime

from google.appengine.ext import ndb


class Review(ndb.Model):
    user = ndb.TextProperty(indexed=True)
    id_movie = ndb.IntegerProperty()
    date = ndb.DateTimeProperty()
    content = ndb.TextProperty(indexed=True)


def create_empty_review():
    return Review(user="", id_movie=0, date=datetime.datetime.now(), content="")


@ndb.transactional
def update(review):
    return review.put()


def get_review(user, id_movie):
    if user and id_movie:
        found_list = Review.query(Review.user == user, Review.id_movie == id_movie).get()
        if found_list:
            return found_list
        else:
            return None
    else:
        return None


def get_others_reviews(user, id_movie):
    if user and id_movie:
        found_list = Review.query(Review.user != user, Review.id_movie == id_movie)
        if found_list.count() > 0:
            return found_list
        else:
            return None
    else:
        return None


def format_dates(reviews):
    dates_format = []
    for review in reviews:
        str_date = str(review.date)
        date_format = calendar.month_name[int(str_date[5:7])] + " " + str_date[8:10] + ", " + str_date[0:4]
        dates_format.append({"user": review.user, "date": date_format})
    return dates_format


def format_date(review):
    str_date = str(review)
    date_format = calendar.month_name[int(str_date[5:7])] + " " + str_date[8:10] + ", " + str_date[0:4]
    return date_format
