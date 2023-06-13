from django.contrib import admin
from user_auth.models import User


# Register your models here.
# admin.site.register(Category)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    first_name
    last_name
    is_staff
    is_superuser
    """
    list_display = ('id', 'email', 'first_name', 'last_name', 'country')

    list_filter = ('id', 'email', 'first_name', 'last_name', 'country')
    list_display_links = ('id', 'email', 'first_name', 'last_name', 'country')
