from django.contrib import admin
from .models import Trademark, TrademarkAsset, User, Plan

# Register your models here.

admin.site.register(Trademark)
admin.site.register(TrademarkAsset)
admin.site.register(User)
admin.site.register(Plan)
