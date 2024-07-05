# from django.test import TestCase

# # Create your tests here.

# def blog_view(request):
#     data = request.GET
#     cat = data.get('cat')
#     page = data.get('page')
#     if cat:
#         posts = Post.objects.filter(category=cat)

#         context = {
#             'posts': posts,
#             'blog': 'active',
#         }
#         return render(request, 'blog.html', context)
#     else:
#         posts = Post.objects.all()
#         page_obj = Paginator(posts, 3)
#     context = {

#         'blog': 'active',
#         'posts': page_obj.get_page(page)
#     }
#     return render(request, 'blog.html', context=context)
