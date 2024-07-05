from django.shortcuts import render, redirect
import requests
from blog.models import Post, Contact, Category, Tag, Comment
from django.core.paginator import Paginator
from django.db.models import Count

BOT_TOKEN = '6791913442:AAG7cVQzAAwUYj2OQB2jVnpwxl3VGP44Fuc'
CHAT_ID = '5937168278'


def index_view(request):
    data = request.GET
    posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True)
    categories = Category.objects.all()
    page = data.get('page')
    page_obj = Paginator(posts, 8)
    tags = Tag.objects.all()
    context = {
        'initial_posts': posts.order_by('created_at')[:4],
        'more_posts': page_obj.get_page(page),
        'face_posts': posts.filter(is_banner=True)[:6],
        'latest_posts': posts.order_by('-created_at')[:4],
        'face_posts2': posts.order_by('-view_count')[:3],
        'popular_posts': posts.order_by('-comment_count')[:4],
        'categories': categories,
        'tags': tags,
        'home': 'active',
        # 'comment_count': len('comments'),
    }
    return render(request, 'index.html', context=context)


def about_view(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    data = request.GET
    page = data.get('page')
    posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True)
    page_obj = Paginator(posts, 8)
    context = {
        'categories': categories,
        'tags': tags,
        'latest_posts': posts.order_by('-created_at')[:4],
        'popular_posts': posts.order_by('-comment_count')[:4],
        'latest_posts_for_about': page_obj.get_page(page),
        'about': 'active'
    }
    return render(request, 'about.html', context=context)


def contact_view(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True)

    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(name=data['name'], email=data['email'], phone=data['phone'],
                                     message=data['message'])
        obj.save()
        TEXT = f"""
             From : Balita 2
             id: {obj.id}
             name: {obj.name}
             email: {obj.email}
             message: {obj.message}
             time: {obj.created_at}
             """
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={TEXT}'
        response = requests.get(url)
        print(response)
        return redirect('/contact')
    context = {
        'categories': categories,
        'tags': tags,
        'popular_posts': posts.order_by('-comment_count')[:4],
        'latest_posts': posts.order_by('-created_at')[:4],
        'contact': 'active'
    }

    return render(request, 'contact.html', context=context)


def blog_detail_view(request, pk):
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(name=data['name'], email=data['email'], message=data['message'], post_id=pk)
        obj.save()
        return redirect(f'/blog/{pk}')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True)
    comments = Comment.objects.filter(post_id=pk, is_visible=True)
    post = Post.objects.get(is_published=True, id=pk)
    post.view_count += 1
    post.save(update_fields=['view_count'])
    # post = Post.objects.get(id=pk)
    # post.view_count += 1
    # post.save(update_fields=['view_count'])
    context = {
        'comments': comments,
        'categories': categories,
        'tags': tags,
        'popular_posts': posts.order_by('-comment_count')[:4],
        'latest_posts': posts.order_by('-created_at')[:4],
        'comment_count': len(comments),
        'post': post,
        'home': 'active'
    }
    return render(request, 'blog-single.html', context=context)


def category_view(request, pk):
    categories = Category.objects.all()
    data = request.GET
    page = data.get('page', 1)

    category = Category.objects.filter(id=pk).first()
    posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True, category_id=pk)
    # popular_posts = Post.objects.filter(is_published=True)
    page_obj = Paginator(posts, per_page=3)
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'posts': page_obj.get_page(page),
        'tags': tags,
        'popular_posts': posts.order_by('-comment_count')[:4],
        'latest_posts': posts.order_by('-created_at')[:4],
        "category_name": category,
        'category': 'active'
    }
    return render(request, 'category.html', context=context)


def tag_view(request):
    data = request.GET
    tag = data.get('tag')
    tags = Tag.objects.all()
    categories = Category.objects.all()
    if tag:
        posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True, tag=tag)
    else:
        posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True)
    context = {
        'posts': posts,
        'popular_posts': posts.order_by('-comment_count')[:4],
        'latest_posts': posts.order_by('-created_at')[:4],
        'category': 'active',
        'tags': tags,
        'categories': categories,
    }
    return render(request, 'category.html', context=context)


def search_view(request):
    postlar = Post.objects.filter(is_published=True)
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')
    query = request.GET.get('q')
    if query is not None and len(query) >= 1:
        posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True, title__icontains=query)
    else:
        posts = Post.objects.annotate(comment_count=Count('comments')).filter(is_published=True)
    context = {
        'posts': posts,
        'categories': Category.objects.all(),
        'latest_posts': posts.order_by('-created_at')[:4],
        'popular_posts': posts.order_by('-comment_count')[:4],
    }

    return render(request, 'category.html', context=context)
