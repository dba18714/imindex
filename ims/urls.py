from django.urls import path

from . import views

# app_name = "polls"
# urlpatterns = [
#     # ex: /polls/
#     path("", views.index, name="index"),
#     # ex: /polls/5/
#     path("<int:question_id>/", views.detail, name="detail"),
#     # ex: /polls/5/results/
#     path("<int:question_id>/results/", views.results, name="results"),
#     # ex: /polls/5/vote/
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]

app_name = "ims"
urlpatterns = [
    path("item/<str:uuid>/", views.DetailView.as_view(), name="detail"),
    path('ad/<int:id>/redirect/', views.ad_redirect_view, name='ad-redirect'),
    path("get-telegram-url/<str:uuid>/", views.get_telegram_url, name="get-telegram-url"),
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("add_v2/", views.add_v2, name="add_v2"),  # 还未完成，已弃用，因为太繁琐了，还不如直接SSR前后端分离
]