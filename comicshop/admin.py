from django.contrib import admin

from .models import Category, Customer, Product, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)

class Profileinline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'email', 'first_name', 'last_name']
    inlines = [Profileinline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
