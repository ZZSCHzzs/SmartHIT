from .utils import *
from django.db.models import OuterRef, Subquery, Case, When, F
from django import forms
from django.core.validators import FileExtensionValidator


class PostForm(BaseImageForm):
    class Meta:
        model = Post
        fields = ["category", "title", "text", "additional_information", "additional_graphics"]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'fixed-height-textarea'}),
        }

    def __init__(self, *args, **kwargs):
        cid = kwargs.pop('cid', None)
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "additional_graphics":
                continue
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = current_classes + ' form-control'
        if cid is not None:
            self.fields['category'].initial = Category.objects.get(cid=cid)


def create_post(request):
    is_authed = True if request.session.get('info') else False
    if not is_authed:
        return redirect('login')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            launcher_uid = request.session.get('info').get('id')
            post = form.save(commit=False)
            post.launcher_uid = launcher_uid
            post.author = User.objects.get(uid=launcher_uid)
            post.save()
            return redirect(f'/p/{post.pk}')
    else:
        cid = request.GET.get('cid')
        form = PostForm(cid=cid)

    return render(request, 'post/post.html', {'form': form, 'is_authed': is_authed})


def post_detail(request, pk):
    is_authed = True if request.session.get('info') else False
    if is_authed:
        info_data = request.session.get('info')
        user_object = User.objects.filter(uid=info_data['id']).first()
    else:
        user_object = None

    # 获取特定主键对应的帖子，如果不存在则返回 404 错误页面
    post = get_object_or_404(Post, pk=pk)
    post.formatted_launch_time = format_time(post.launch_time)

    comments = post.comments.all()
    if comments:
        comments_object = Pagination(request, comments, 20)

        for i, comment in enumerate(comments_object.page_queryset, start=1):
            comment.formatted_time = format_time(comment.created_at)
            comment.index = i + (comments_object.page - 1) * comments_object.page_size
        context = {'post': post,
                   'is_authed': is_authed,
                   'user': user_object,
                   'comments': comments_object.page_queryset,
                   'page_string': comments_object.html()
                   }
    else:
        context = {'post': post,
                   'is_authed': is_authed,
                   'user': user_object,
                   }

    # 增加帖子的浏览次数
    post.view_times += 1
    post.save()

    # 渲染模板并将帖子数据传递给模板
    return render(request, 'post/p.html', context)


def get_posts(cid, request):
    is_authed = True if request.session.get('info') else False
    context = {
        'is_authed': is_authed
    }

    last_comment_time = Comment.objects.filter(post=OuterRef('pk')).order_by('-created_at').values('created_at')[:1]

    queryset = Post.objects.all()

    if cid != 0:
        queryset = queryset.filter(category__cid=cid)

    queryset = queryset.annotate(
        last_comment_time=Subquery(last_comment_time)
    ).annotate(
        sort_by=Case(
            When(last_comment_time__isnull=False, then=F('last_comment_time')),
            default=F('launch_time'),
            output_field=models.DateTimeField()
        )
    ).order_by('-sort_by')

    if queryset:
        page_object = Pagination(request, queryset)

        for post in page_object.page_queryset:
            post.formatted_launch_time = format_time(post.launch_time)
            last_comment = post.comments.last()
            if last_comment:
                post.formatted_last_comment_time = format_time(last_comment.created_at)
        context.update({
            'posts': page_object.page_queryset,
            'page_string': page_object.html()
        })
    return context


def post_list(request):
    context = get_posts(0, request)
    return render(request, 'post/post_list.html', context)


def category(request):
    is_authed = True if request.session.get('info') else False
    category_types = CategoryType.objects.all()
    for category_type in category_types:
        category_type.categories = Category.objects.filter(cid__gte=category_type.tid * 10, cid__lte=(category_type.tid + 1) * 10)
    context = {
        'is_authed': is_authed,
        "category_types": category_types
    }
    return render(request, 'post/category.html', context)


def category_detail(request, cid):
    context = get_posts(cid, request)
    category_object = Category.objects.get(cid=cid)
    context.update({'category_object': category_object})
    return render(request, 'post/c.html', context)


def add_comment(request, pk):
    if not request.session.get('info'):
        redirect('/login')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('comment')
        info_data = request.session.get('info')
        user_object = User.objects.filter(uid=info_data['id']).first()
        if content:
            Comment.objects.create(post=post, author=user_object, content=content)
    return redirect(f'/p/{post.pk}')


def delete_comment(request, pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=pk)
        info_data = request.session.get('info')
        user_object = User.objects.filter(uid=info_data['id']).first()
        if user_object == (comment.author or comment.post.author):
            comment.delete()
            return JsonResponse({'message': 'Comment deleted successfully'})
        else:
            return JsonResponse({'error': 'You are not allowed to delete this comment'}, status=403)


def delete_post(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        info_data = request.session.get('info')
        user_object = User.objects.filter(uid=info_data['id']).first()
        if user_object == post.author:
            cid = post.category_id
            post.delete()
            return redirect(f'/category/{cid}')
        else:
            return JsonResponse({'error': 'You are not allowed to delete this comment'}, status=403)
