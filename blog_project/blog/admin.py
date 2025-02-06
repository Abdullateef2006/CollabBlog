# blog/admin.py
from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django.db import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Post)  # This registers the Post model with the PostAdmin configuration
class PostAdmin(admin.ModelAdmin):
    # Use CKEditor for editing TextField content in the admin
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    list_display = ['title', 'author', 'published_date', 'is_premium']
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate the slug field
    search_fields = ['title', 'author__username']  # Enable search by title and author
    list_filter = ['category', 'is_premium', 'published_date']  # Add filters for the admin panel


@admin.register(UserProfile)
class ModelNameAdmin(admin.ModelAdmin):
    '''Admin View for ModelName'''

    list_filter = ['bio','status',]
    
    
admin.site.register(Comments)
admin.site.register(Invitation)
admin.site.register(Subscription)