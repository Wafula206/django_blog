from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Post, Profile, Category, Comment

# 1️⃣ Make a Profile inline — so it appears inside the User admin page.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# 2️⃣ Extend the default UserAdmin to add the Profile inline.
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# 3️⃣ Unregister the original User admin, then register the new one.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# 4️⃣ Register other models too (optional, but recommended):
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
