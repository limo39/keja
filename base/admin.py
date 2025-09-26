from django.contrib import admin
from .models import Room, Topic, Message, User, Property, PropertyImage


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'landlord', 'property_type', 'rent_amount', 'location', 'is_available', 'created']
    list_filter = ['property_type', 'is_available', 'created', 'location']
    search_fields = ['title', 'location', 'address', 'landlord__username']
    list_editable = ['is_available']
    readonly_fields = ['created', 'updated']


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'caption', 'created']
    list_filter = ['created']


admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
