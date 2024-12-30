from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile, Store
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_approved')
    list_filter = ('role', 'is_approved')
    search_fields = ('user__username', 'user__email')  # Corrected fields for user lookups

admin.site.register(Profile, ProfileAdmin)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'city', 'store_kind']
    list_filter = ['store_kind', 'city']

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
