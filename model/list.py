#!/usr/bin/env python
# coding=utf-8
# (c) Ivan de Dios 2019 MIT License <ivanddf1994@gmail.com>

from google.appengine.ext import ndb


class List(ndb.Model):
    user = ndb.TextProperty(indexed=True)
    name_list = ndb.TextProperty(indexed=True)
    description_list = ndb.TextProperty(indexed=True)


def create_empty_list():
    return List(user="", name_list="", description_list="")


@ndb.transactional
def update(list_to_db):
    return list_to_db.put()


def get_favorite(user):
    if user:
        list_fav = List.query(List.user == user, List.name_list == "Favorites").get()
        if list_fav:
            return list_fav
        else:
            return None
    else:
        return None


def get_watchlist(user):
    if user:
        watchlist_user = List.query(List.user == user, List.name_list == "Watchlist").get()
        if watchlist_user:
            return watchlist_user
        else:
            return None
    else:
        return None


def get_user_lists(user):
    if user:
        user_lists = List.query(List.user == user)
        if user_lists:

            return user_lists
        else:
            return None
    else:
        return None


def get_user_lists_default(user):
    if user:
        user_list_fav = List.query(List.user == user, List.name_list == "Favorites" )
        user_list_watchlist = List.query(List.user == user, List.name_list == "Watchlist")
        user_default_list = list(user_list_fav) + list(user_list_watchlist)
        if user_default_list:
            return user_default_list
        else:
            return None
    else:
        return None


def get_user_lists_without_default(user):
    if user:
        user_lists = List.query(List.user == user, List.name_list != "Favorites", List.name_list != "Watchlist")
        if user_lists:
            return user_lists
        else:
            return None
    else:
        return None
