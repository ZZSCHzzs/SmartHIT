from .utils import *


class RegisForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(render_value=True), label='密码')
    password_confirm = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'type': 'password', 'autocomplete': 'new-password'}), label='确认密码')

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'nickname', 'stu_id', 'department')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput, label='用户名')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(render_value=True), label='密码')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return sha1(pwd.encode('utf-8')).hexdigest()


def generate_uid(username, regis_time):
    # 将用户名和注册时间组合成一个字符串
    combined_string = f"{username}{regis_time}"

    # 使用 SHA1 算法生成哈希值
    hashed_value = int(sha1(combined_string.encode()).hexdigest(), 16)

    # 取哈希值的后 10 位作为数字形式的 UID
    uid = int(str(hashed_value)[-10:])

    return uid


def regis(request):
    if request.session.get('info'):
        return redirect('/index')
    if request.method == 'POST':
        form = RegisForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = form.cleaned_data.get('password_confirm')
            if password != password_confirm:
                form.add_error('password_confirm', '两次输入的密码不匹配')
            else:
                username = form.cleaned_data.get('username')
                nickname = form.cleaned_data.get('nickname')
                stu_id = form.cleaned_data.get('stu_id')
                department = form.cleaned_data.get('department')
                regis_time = timezone.now()
                state = get_object_or_404(State, id=1)
                permission_group = get_object_or_404(PermissionGroup, id=1)
                uid = generate_uid(username, regis_time)
                password_hash = sha1(password.encode('utf-8')).hexdigest()
                # 创建用户实例
                new_user = User.objects.create(
                    username=username,
                    nickname=nickname,
                    password=password_hash,
                    stu_id=stu_id,
                    department=department,
                    state=state,
                    permission_group=permission_group,
                    uid=uid,
                    regis_time=regis_time
                )
                new_user.save()

                return redirect('/login')  # 重定向到登录
    else:
        form = RegisForm()

    return render(request, 'auth/regis.html', {'form': form})


def login(request):
    if request.session.get('info'):
        return redirect('/index')
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            user_object = User.objects.filter(username=username, password=password).first()
            if not user_object:
                form.add_error('password', "用户名或密码错误")
                return render(request, "auth/login.html", {'form': form})
            request.session['info'] = {'id': user_object.uid, 'nickname': user_object.nickname,
                                       'username': user_object.username}
            # next_url = request.POST['next']
            # if next_url:
            #     return redirect(next_url)
            return redirect('/index')

    form = LoginForm()
    return render(request, "auth/login.html", {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/index')
