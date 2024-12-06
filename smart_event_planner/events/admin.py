from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event, Category  


class CustomUserAdmin(UserAdmin):
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'score', 'is_staff', 'is_active')
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    list_filter = ('is_staff', 'is_active')
    
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'score', 'location', 'interests', 'birth_date', 'gender', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'score', 'location', 'interests', 'birth_date', 'gender', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    
    add_permission = True


admin.site.register(User, CustomUserAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'event_date', 'event_time', 'user')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'event_date')
    ordering = ('-event_date',)

admin.site.register(Event, EventAdmin)
admin.site.register(Category)
