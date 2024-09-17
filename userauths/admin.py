from django.contrib import admin
from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']
    
class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['first_name', 'last_name', 'bio', 'phone_number', 'verified', 'image']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)