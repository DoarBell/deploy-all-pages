from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .models import User, Listing, Comment, Bid, Cart

def index(request):
    listing = Listing.objects.filter(is_real=True)
    scattergories = Listing._meta.get_field("category").choices
    themenopark = Listing._meta.get_field("theme").choices
    return render(request, "auctions/index.html",{
        "listings": listing,
        "categories": scattergories,
        "themes": themenopark,
    })

def biding(request, id):
    user = request.user
    product = Listing.objects.get(pk=id)
    money = request.POST['bid']
    min_bid = product.min_bid
    if Decimal(money) >= min_bid:
        correct = Bid(
            user = user,
            product = product,
            money = Decimal(money),
        )
        correct.save()
        product.min_bid = Decimal(money)
        product.save()
        messages.success(request, "Your bid was placed successfully")
    else:
        messages.error(request, "Your bid is not correct")
    return HttpResponseRedirect(reverse("listing_view", args=[id]))

def rm_watch(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    reset = Cart.objects.filter(listing = listing, user=user).first()
    if reset:
        reset.delete()
    return HttpResponseRedirect(reverse("index"))
    
def owning(request, id):
    if request.method=="GET":
        user = request.user
        listing = Listing.objects.filter(owned=True, seller=user)
        return render(request, "auctions/owning.html",{
            "listings":listing
        })
    elif request.method=="POST":
        try:
            product=Listing.objects.get(pk=id)
            max_bidder = Bid.objects.filter(product=product).order_by('-money').first()
            product.owned = True
            product.seller = max_bidder.user
        except AttributeError:
            product.seller = request.user
        else:
            product.is_real = False
            product.save()
        return render(request, "auctions/winner.html",{
            "listing": product,
            "bid": max_bidder,
            "winner": max_bidder.user if max_bidder else None,
        })


def fil(request):
    if request.method=="POST":
        button = True
        category_fil = request.POST['category']
        theme_fil = request.POST['theme']
        listing = Listing.objects.filter(is_real=True, category=category_fil)
        if theme_fil != "any":
            listing = listing.filter(theme=theme_fil)
        scattergories = Listing._meta.get_field("category").choices
        themenopark = Listing._meta.get_field("theme").choices
        return render(request, "auctions/index.html",{
            "listings": listing,
            "categories": scattergories,
            "themes": themenopark,
            "on": button,
        })

def cr_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        theme = request.POST["theme"]
        price = Decimal(request.POST["price"])
        TheUser= request.user
        usercode = request.user.username
        owned = False
        code = title[:2] + theme[:2] + category[:2] + usercode[:2]
        product = Listing(
            code=code.upper(), 
            name=title,
            description = description,
            img_url = image_url,
            seller = TheUser,
            min_bid = price,
            owned = owned,
            date = timezone.now(),
            category = category,
            theme = theme,
            is_real = True,
        )
        product.save()

        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        scattergories = Listing._meta.get_field("category").choices
        themenopark = Listing._meta.get_field("theme").choices
        return render(request, "auctions/listing.html",{
            "scattergories": scattergories,
            "themenopark": themenopark
        })
    
def watch(request, id):
    list = Listing.objects.get(pk=id)
    user = request.user
    seeing = True
    try:
        new_watch = Cart(
            user = user,
            listing = list,
            watching = seeing,
        )
        new_watch.save()
    except IntegrityError:
        messages.warning(request, "Listing already added")
    return HttpResponseRedirect(reverse("listing_view", args=[id]))

def listing_view(request, id):
    if request.method=="GET":
        list = Listing.objects.get(pk=id)
        max_bidder = Bid.objects.filter(product=list).order_by('-money').first()
        comments = Comment.objects.filter(link=list)
        user = request.user
        return render(request, "auctions/product.html",{
            "listing": list,
            "comments": comments,
            "user": user,
            "bidder_king": max_bidder.user if max_bidder else None,
        })
    elif request.method=="POST":
        listing = Listing.objects.get(pk=id)
        new_comment = request.POST["comment"]
        user = request.user
        comment = Comment(
            comment = new_comment, 
            link = listing,
            user = user,
            )
        comment.save()
        return HttpResponseRedirect(reverse("listing_view", args=[id]))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
