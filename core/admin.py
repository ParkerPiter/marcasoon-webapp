from django.contrib import admin
from .models import Trademark, TrademarkAsset, User, Plan
from .models import Testimonial
from .models import BlogPost
from .models import Webinar

# Register your models here.

@admin.register(Trademark)
class TrademarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'status', 'plan', 'created_at', 'is_verified')
    list_filter = ('status', 'plan', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'name', 'status')

admin.site.register(TrademarkAsset)
admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Webinar)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ("client_name", "brand_name", "country", "rating", "approved", "created_at")
	list_filter = ("approved", "rating")
	search_fields = ("client_name", "brand_name", "country", "content", "title")

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "author", "is_published", "created_at")
	list_filter = ("is_published", "created_at")
	search_fields = ("title", "body", "author")
	prepopulated_fields = {"slug": ("title",)}
