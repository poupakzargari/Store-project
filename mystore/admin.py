from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile, Store
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)

# Profile Admin with custom settings
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_approved')
    list_filter = ('role', 'is_approved')
    search_fields = ('user__username', 'user__email')  # Corrected fields for user lookups

# Register Profile only once, with ProfileAdmin
admin.site.register(Profile, ProfileAdmin)

# Profile Inline to add to User
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model with ProfileInline
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'city', 'store_kind']  # Include type in admin display
    list_filter = ['store_kind', 'city']  # Add filter options for type

# Unregister the default User admin to apply our custom UserAdmin
admin.site.unregister(User)

# Re-register User with UserAdmin
admin.site.register(User, UserAdmin)
