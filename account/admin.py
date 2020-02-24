from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Offices, WorkStation


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_per_page = 15
    list_display = ('get_short_name', 'phone', 'image_thumblr', 'email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'last_name',
            'first_name',
            'middle_name',
            'phone',
            'address',
            'birth_to_day',
            'avatar',
            'image_tag',
            'position'
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),

            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    readonly_fields = ['image_tag']
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)


class OfficesAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_code', 'address','get_phone_number','view_on_front',)


admin.site.register(Offices, OfficesAdmin)




class WorkStationAdmin(admin.ModelAdmin):
    list_display = ('get_work_station_name',)

    def get_work_station_name(self, obj):
        return ("%s (%s)" % (obj.host, obj.ip_address)).upper()


    get_work_station_name.short_description = 'Name'


admin.site.register(WorkStation, WorkStationAdmin)
