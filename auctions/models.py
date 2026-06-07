from django.contrib.auth.models import AbstractUser
from django.db import models


class Like(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    likes = models.ManyToManyField(Like, blank=True, related_name="users")

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=364)
    description = models.CharField(max_length=999)
    img_url = models.CharField(max_length=999)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name="producer")
    min_bid = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    owned = models.BooleanField(default=False)
    category = models.CharField(
        max_length=50,
        choices=[
            ("clothing", "Clothing & Accessories"),
            ("toys", "Toys & Games"),
            ("technology", "Technology & Electronics"),
            ("books", "Books & Media"),
            ("home", "Home & Living"),
            ("sports", "Sports & Outdoors"),
            ("beauty", "Beauty & Personal Care"),
            ("food", "Food & Drink"),
            ("collectibles", "Collectibles"),
            ("other", "Other"),
        ],
        default="other"
    )
    theme = models.CharField(
        max_length=50,
        choices=[
            ("any", "Any"),
            ("fantasy", "Fantasy"),
            ("children", "Children"),
            ("gaming", "Gaming"),
            ("normies", "Normies"),
            ("girls", "Girls"),
            ("boys", "THE BOYS"),
            ("sci-fi", "Sci-Fi"),
            ("fashion", "Fashion"),
            ("humor", "Humor"),
            ("anime", "Anime"),
            ("animals", "Animals"),
            ("cute", "Cute"),
            ("luxury", "Luxury"),
        ],
        default="normies")
    is_real = models.BooleanField()
    def __str__(self):
        return f"{self.code} - {self.name}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bids")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidign")
    money = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} bids {self.money} for {self.product}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="commenter", default=2)
    comment = models.CharField(max_length=364)
    link = models.ForeignKey(Listing, models.CASCADE, related_name="commentary")
    flaged = models.BooleanField(default=False)
    
    def __str__(self):
        return f"comment for {self.link}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="cart_items")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="cart_entries")
    watching = models.BooleanField(default=False)
    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):
        return f"{self.user}, watching {self.listing}"
    