from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    admin.site.empty_value_display = '-empty-'
    
    # To display image not just image name
    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100"/>'.format(obj.profile_picture.url))

    image_tag.short_description = 'Profile Picture'

    # Modify the list_display as follow-
    list_display = ['image_tag', 'user_id', 'address', 'city', 'country', 'postal_code', 'profession', 'university', 'about_me']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        return super().delete_queryset(request, queryset)

@admin.register(Contacts)
class Contact_Admin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'message', 'date']

@admin.register(Feature)
class Contact_Admin(admin.ModelAdmin):
    list_display = ['id', 'image', 'title', 'text', 'alt', 'url']