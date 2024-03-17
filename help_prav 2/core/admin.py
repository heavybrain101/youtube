from django.contrib import admin


from core.models import Employe, News, ShopCategory, ShopItems, Wallet, Profile, Cart, User

# Register your models here.


admin.site.register(Employe)
admin.site.register(News)
admin.site.register(ShopCategory)
admin.site.register(ShopItems)
admin.site.register(Wallet)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(User)
