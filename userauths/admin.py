from django.contrib import admin
from userauths.models import ContactUs, Profile, User
# from import_export.admin import ImportExportModelAdmin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)