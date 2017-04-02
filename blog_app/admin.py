from django.contrib import admin
from blog_app.models import UserForm
# Register your models here.

class UserFormAdmin (admin.ModelAdmin):
    # fields = ('name', 'tel', 'address')
    # exclude = ('address', 'birthday')
    fieldsets = (['base', {'fields': ('username', 'email', 'userlogo')}],
                 ['personal', {'fields': ('userid',)}])
    list_display = ('userid', 'username', 'email', 'lastloginIP', 'lastlogintime')
    # list_filter = ('address',)
    search_fields = ('username',)
admin.site.register(UserForm, UserFormAdmin)