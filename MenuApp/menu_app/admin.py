from django.contrib import admin
from .models import Item

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("meal", "price", "meal_type", "status", "date_created")
    list_filter = ("status", "meal_type", "date_created")
    search_fields = ("meal", "description")
    readonly_fields = ("date_created", "date_updated")
    fieldsets = (
        ('Basic Information', {
            'fields': ('meal', 'description', 'price', 'meal_type', 'status')
        }),
        ('Image', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('author', 'date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Item, MenuItemAdmin)