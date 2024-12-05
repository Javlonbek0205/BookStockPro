from statistics import quantiles
from django.contrib import admin
from django.utils.html import format_html

from .models import Book, Category, AdditionalInfo, Review
#Register your models here.

class AdditionalInline(admin.TabularInline):
    model = AdditionalInfo
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )

@admin.register(AdditionalInfo)
class AdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ['book']
    search_fields = ('book', )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at']
    search_fields = ('user', 'book', )
    list_filter = ['created_at']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'image_preview', 'quantity', 'owner']
    search_fields = ['title', 'author', 'sku', 'isbn']
    list_filter = ('author', )
    inlines = [AdditionalInline, ReviewInline]

    def image_preview(self, obj: Book):
        return format_html(f'<a href = "{obj.cover.url}"><img src = "{obj.cover.url}" style = "width:100px; border-radius:10px"></img></a>')