from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Boardgames)
admin.site.register(Users)
admin.site.register(Matches)
admin.site.register(Friends)
admin.site.register(Plays)
admin.site.register(Favourites)
admin.site.register(Dictionary)
admin.site.register(Templates)
admin.site.register(DetailedPoints)
