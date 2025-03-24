from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名是必填项')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # 使用set_password加密密码
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须有is_superuser=True。')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须有is_staff=True。')

        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)



class State(models.Model):
    name = models.CharField(max_length=50, verbose_name="状态名称")

    def __str__(self):
        return self.name


class PermissionGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name="权限组名称")

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50, verbose_name="院系名称")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="帖子分类")
    description = models.TextField(verbose_name="分区描述", blank=True, null=True)
    top_pic = models.FileField(max_length=30, verbose_name="分区头图", upload_to="top_pic/", blank=True, null=True)
    cid = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class CategoryType(models.Model):
    name = models.CharField(max_length=50, verbose_name="大类")
    tid = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name="通知类型")

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30,unique=True ,verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")
    uid = models.BigIntegerField(verbose_name="UID")
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="账户状态")
    permission_group = models.ForeignKey(PermissionGroup, on_delete=models.PROTECT, verbose_name="权限组")
    nickname = models.CharField(max_length=30, verbose_name="昵称")
    qq = models.IntegerField(verbose_name="QQ", blank=True, null=True)
    wechat = models.CharField(max_length=30, verbose_name="微信号", blank=True, null=True)
    name = models.CharField(max_length=30, verbose_name="姓名", blank=True, null=True)
    stu_id = models.CharField(max_length=15, verbose_name="学工号", blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="院系")
    avatar = models.FileField(max_length=30, verbose_name="头像", upload_to="avatars/", blank=True, null=True)
    regis_time = models.DateTimeField(auto_now_add=True, verbose_name="注册日期")
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # 用于后台管理访问权限
    is_superuser = models.BooleanField(default=False)  # 标记超级用户

    objects = UserManager()  # 指定使用自定义管理器
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username if not self.is_deleted else "Deleted User"



class UserCategoryFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    launcher_uid = models.BigIntegerField(verbose_name="发布者ID")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="所属分类")
    launch_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    title = models.CharField(max_length=100, verbose_name="标题")
    text = models.TextField(max_length=6000, verbose_name="正文")
    additional_information = models.TextField(max_length=1000, verbose_name="附加信息", default=None, blank=True, null=True)
    additional_graphics = models.FileField(max_length=30, verbose_name="附加图片", upload_to="images/", default=None, blank=True, null=True)
    view_times = models.IntegerField(verbose_name="浏览次数", default=0)
    likes = models.IntegerField(verbose_name="赞", default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"


class Notification(models.Model):
    launcher = models.CharField(max_length=30, verbose_name="发布者")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="通知类型")
    title = models.CharField(max_length=100, verbose_name="标题")
    text = models.TextField(max_length=8000, verbose_name="正文")
    additional_graphics = models.FileField(max_length=30, verbose_name="附加图片", upload_to="images/", default=None, blank=True, null=True)
    view_times = models.IntegerField(verbose_name="浏览次数", default=0)
    launch_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    abstract = models.CharField(max_length=500, verbose_name="AI摘要", blank=True, null=True)
    keywords = models.JSONField(default=list, verbose_name="AI关键词", blank=True, null=True)
