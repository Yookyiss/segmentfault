from django.urls import path

from segmentfault.apps.users.views import (
    user_redirect_view,
    UserDetailView,
    UserUpdateView,
    UserList,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("userhome/",UserList.as_view(),name='userhome'),
    path("<str:username>/", UserDetailView.as_view(), name="detail"),

]
