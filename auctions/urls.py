from django.urls import path

from . import views

#your superuser name is "Admin_Kijuro" in case you forget

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cr_listing", views.cr_listing, name="cr_listing"),
    path("fil", views.fil, name="fil"),
    path("listing/<int:id>", views.listing_view, name='listing_view'),
    path("biding/<int:id>", views.biding, name="biding"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("rm_watch/<int:id>", views.rm_watch, name="rm_watch"),
    path("owning<int:id>", views.owning, name="owning"),
]
