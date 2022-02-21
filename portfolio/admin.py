from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Comment, UserCommentVote, Post, PostSection, PostSectionContent
import nested_admin
# Register your models here.

class PostSectionContentInline(nested_admin.NestedTabularInline):
  model = PostSectionContent
  classes = ('collapse',)

class PostSectionInline(nested_admin.NestedTabularInline):
  model = PostSection
  inlines = (PostSectionContentInline,)
  classes = ('collapse',)

class UserCommentVoteInline(nested_admin.NestedTabularInline):
  model = UserCommentVote
  classes = ('collapse',)

class CommentInline(nested_admin.NestedTabularInline):
  model = Comment
  classes = ('collapse',)

class UserInline(nested_admin.NestedTabularInline):
  model = User
  can_delete = False
  verbose_name_plural = 'users'

class CommentAdmin(nested_admin.NestedModelAdmin):
  inlines = (CommentInline,)
  list_display = ('text', 'replies',)
  list_filter = ('text',)
  fieldsets = (
    (None, {
      'fields': ('text', 'replies',),
    }),
  )
  search_fields = ('text',)
  ordering = ('text',)
  filter_horizontal = ()

class UserAdmin(BaseUserAdmin):
  inlines = (CommentInline,)
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

class PostAdmin(nested_admin.NestedModelAdmin):
  inlines = (PostSectionInline, CommentInline,)
  list_display = ('title', 'topic',)
  list_filter = ('title',)
  fieldsets = (
    (None, {
      'fields': ('title', 'topic',)
    }),
  )
  search_fields = ('title',)
  ordering = ('title',)
  filter_horizontal = ()

class PostSectionAdmin(nested_admin.NestedModelAdmin):
  inlines = (PostSectionContentInline,)
  list_display = ('title',)
  list_filter = ('title',)
  fields = ('title',)
  search_fields = ('title',)
  ordering = ('title',)
  filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserCommentVote)
admin.site.register(Post, PostAdmin)
admin.site.register(PostSection, PostSectionAdmin)
admin.site.register(PostSectionContent)

admin.site.unregister(Group)