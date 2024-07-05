from django.contrib import admin

from blog.models import Post, Comment, Contact, Category, Tag

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('name', 'email', 'message')

class PostInline(admin.TabularInline):
    model = Post
    extra = 1
    fields = ['title', 'author']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_display_links = ('title', 'author')
    search_fields = ('title', 'author')
    inlines = [CommentInline,]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'created_at')
    list_display_links = ('post', 'name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_display_links = ('name', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_display_links = ('name', 'created_at')
    inlines = [PostInline,]



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_display_links = ('name', 'created_at')
