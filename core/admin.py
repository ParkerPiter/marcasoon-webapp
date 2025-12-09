from django.contrib import admin
from .models import Trademark, TrademarkAsset, User, Plan
from .models import Testimonial
from .models import BlogPost

# Register your models here.

admin.site.register(Trademark)
admin.site.register(TrademarkAsset)
admin.site.register(User)
admin.site.register(Plan)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ("client_name", "brand_name", "country", "rating", "approved", "created_at")
	list_filter = ("approved", "rating")
	search_fields = ("client_name", "brand_name", "country", "content", "title")

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "author", "is_published", "created_at")
	list_filter = ("is_published", "created_at")
	search_fields = ("title", "body", "author__username", "author__full_name")
	prepopulated_fields = {"slug": ("title",)}
