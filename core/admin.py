from django.contrib import admin
from .models import Trademark, TrademarkAsset, User, Plan
from .models import Testimonial

# Register your models here.

admin.site.register(Trademark)
admin.site.register(TrademarkAsset)
admin.site.register(User)
admin.site.register(Plan)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ("client_name", "brand_name", "rating", "approved", "created_at")
	list_filter = ("approved", "rating")
	search_fields = ("client_name", "brand_name", "content", "title")
