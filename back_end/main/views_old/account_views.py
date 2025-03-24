from .utils import *


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'qq', 'wechat', 'name', 'stu_id', 'department']

    def __init__(self, cid=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = current_classes + ' form-control'


def pre(request):
    is_authed = True if request.session.get('info') else False
    if not is_authed:
        return redirect('/login')
    context = {'is_authed': is_authed}
    return context


def view_info(request):
    context = pre(request)
    user_object = User.objects.get(uid=request.session.get('info').get('id'))
    context.update({'user': user_object})
    return render(request, 'user/view_info.html', context)


def edit_info(request):
    context = pre(request)
    user = User.objects.get(uid=request.session.get('info').get('id'))
    if request.method == 'POST':
        # 处理表单提交
        user.nickname = request.POST.get('nickname')
        user.qq = request.POST.get('qq')
        user.wechat = request.POST.get('wechat')
        user.name = request.POST.get('name')
        user.stu_id = request.POST.get('stu_id')
        user.department = Department.objects.get(id=int(request.POST.get('department')))
        user.save()
        return redirect('/account/info')  # 重定向到查看信息页面
    else:

        form = UserInfoForm(instance=user)

    context['form'] = form
    return render(request, 'user/edit_info.html', context)


def my_posts(request):
    context = pre(request)
    posts = Post.objects.filter(launcher_uid=request.session.get('info').get('id'))
    context['posts'] = posts
    return render(request, 'user/my_posts.html', context)


def my_comments(request):
    context = pre(request)
    comments = Comment.objects.filter(author__uid=request.session.get('info').get('id'))
    context['comments'] = comments
    return render(request, 'user/my_comments.html', context)


def subscription(request):
    context = pre(request)
    return render(request, 'user/subscription.html', context)
