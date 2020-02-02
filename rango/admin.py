from django.contrib import admin
from rango.models import Category, Page

# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url")

# Set the prepopulated slug field
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

# admin.site.register(ModelName, AdminName)

