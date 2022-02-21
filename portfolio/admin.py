from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Comment, UserCommentVote, Post, PostSection, PostSectionContent
# Register your models here.

class UserInline(admin.StackedInline):
  model = User
  can_delete = False
  verbose_name_plural = 'users'

class UserAdmin(BaseUserAdmin):
  list_display = ('username', 'email', 'is_staff', 'is_superuser',)
  list_filter = ('is_superuser',)
  fieldsets = (
    (None, {'fields': ('email', 'password',)}),
    ('Permissions', {'fields': ('is_superuser',)}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('username', 'password1', 'password2',),
    })
  )
  search_fields = ('email',)
  ordering = ('email',)
  filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(UserCommentVote)
admin.site.register(Post)
admin.site.register(PostSection)
admin.site.register(PostSectionContent)

admin.site.unregister(Group)