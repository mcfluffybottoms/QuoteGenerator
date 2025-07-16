from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("quote/", views.change_quote, name="change_quote"),
    path("quote/<int:quote_id>", views.get_quote_by_id, name="get_quote_by_id"),
    path("quote/<int:quote_id>/incr", views.get_quote_by_id_incr, name="get_quote_by_id_incr"),
    path("quote/<int:quote_id>/update/", views.update_quote_weight, name="update_quote_weight"),
    path("quote/<int:quote_id>/like/", views.like, name="like"), # щас пока по-даунски
    path("quote/<int:quote_id>/dislike/", views.dislike, name="dislike"), # щас пока по-даунски
    path("top_quotes/", views.get_top_quotes, name="top_quotes"),
    path("add/", views.add_quote, name="add_quote"),
]