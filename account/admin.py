from django.contrib import admin
from .models import Profile


from django.contrib.auth.models import User
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'middle_name', 'date_of_birth', 'photo']

@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'user.profile.middle_name' 'last_name', 'is_active', 'last_login']

#admin.site.unregister(User)
#admin.site.register(User, MyUserAdmin)