from .models import Cart

def cart_views(request):
    if request.user.is_authenticated:
        return {
            "cart_views": Cart.objects.filter(user=request.user, watching=True),
        }
    return {"cart_views": []}