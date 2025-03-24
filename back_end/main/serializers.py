from hashlib import sha1

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *
from django.utils import timezone

from .utils import format_time


def generate_uid(username, regis_time):
    # 将用户名和注册时间组合成一个字符串
    combined_string = f"{username}{regis_time}"
    # 使用 SHA1 算法生成哈希值
    hashed_value = int(sha1(combined_string.encode()).hexdigest(), 16)
    # 取哈希值的后 10 位作为数字形式的 UID
    uid = int(str(hashed_value)[-10:])
    return uid


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'nickname', 'stu_id', 'department']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("两次输入的密码不匹配")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        password_hash = sha1(password.encode('utf-8')).hexdigest()
        regis_time = timezone.now()
        state = get_object_or_404(State, id=1)
        permission_group = get_object_or_404(PermissionGroup, id=1)
        uid = generate_uid(validated_data['username'], regis_time)

        user = User.objects.create(
            password=password_hash,
            state=state,
            permission_group=permission_group,
            uid=uid,
            regis_time=regis_time,
            **validated_data
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class PermissionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionGroup
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    permission_group = PermissionGroupSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.nickname', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    formatted_launch_time = serializers.SerializerMethodField()
    formatted_last_comment_time = serializers.SerializerMethodField()
    last_comment_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'  # Include all model fields along with the custom fields

    def get_formatted_launch_time(self, obj):
        return format_time(obj.launch_time)

    def get_formatted_last_comment_time(self, obj):
        last_comment = obj.comments.last()
        if last_comment:
            return format_time(last_comment.created_at)
        return None

    def get_last_comment_user(self, obj):
        last_comment = obj.comments.last()
        if last_comment:
            return last_comment.author.nickname
        return None


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.nickname', read_only=True)
    # Optionally, include minimal post data if needed
    post_title = serializers.CharField(source='post.title', read_only=True)
    formatted_time = serializers.SerializerMethodField()
    author_id = serializers.IntegerField(source='author.uid', read_only=True)
    index = serializers.SerializerMethodField()
    post_id = serializers.IntegerField(source='post.pk', read_only=True)

    def get_formatted_time(self, obj):
        return format_time(obj.created_at)

    def get_index(self, obj):
        # Assuming comments are ordered by `created_at` in ascending order
        # This method calculates the index based on the comment's position in the queryset
        all_comments = obj.post.comments.order_by('created_at')
        return list(all_comments).index(obj) + 1

    class Meta:
        model = Comment
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that controls
    which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class NotificationSerializer(DynamicFieldsModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'


class NoticeCenterTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    notifications = NotificationSerializer(many=True, fields=['id', 'title', 'type', 'launcher', 'keywords', 'abstract'], read_only=True)

class CategoryTypeSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = CategoryType
        fields = '__all__'


class UserCategoryFollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = UserCategoryFollow
        fields = '__all__'
