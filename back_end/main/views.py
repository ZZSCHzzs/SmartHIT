# views.py
import requests, re, json
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User, Notification, State, PermissionGroup, Type
from .serializers import *
from .forms import *
from hashlib import sha1
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from .utils import format_time, Pagination
from django.db.models import OuterRef, Subquery, Case, When, F
from .abstract import generate_summary_and_keywords
from django_ratelimit.decorators import ratelimit
from .assistant import get_answer


@api_view(['GET'])
def index_api(request):
    is_authed = True if request.session.get('info') else False
    five_days_ago = timezone.now() - timedelta(days=5)
    start_of_today = timezone.make_aware(datetime.combine(timezone.localdate(), datetime.min.time()))

    tops = Notification.objects.filter(type_id=2).order_by('-launch_time')[:7]
    notifications = Notification.objects.filter(type_id__gte=3).order_by('-launch_time')[:7]
    posts1 = Post.objects.filter(launch_time__gte=five_days_ago).order_by('view_times')[:7]
    posts2 = Post.objects.filter(category__cid__in=range(20, 30)).order_by('-launch_time')[:7]
    posts3 = Post.objects.filter(category__cid__in=range(30, 40)).order_by('-launch_time')[:7]
    posts4 = Post.objects.filter(category__cid__in=range(51, 53)).order_by('-launch_time')[:7]
    posts5 = Post.objects.filter(category__cid__in=range(53, 55)).order_by('-launch_time')[:7]

    context = {
        'is_authed': is_authed,
        'tops': NotificationSerializer(tops, many=True).data,
        'notifications': NotificationSerializer(notifications, many=True).data,
        'posts1': PostSerializer(posts1, many=True).data,
        'posts2': PostSerializer(posts2, many=True).data,
        'posts3': PostSerializer(posts3, many=True).data,
        'posts4': PostSerializer(posts4, many=True).data,
        'posts5': PostSerializer(posts5, many=True).data,
        'notification_count': Notification.objects.all().count(),
        'post_count': Post.objects.all().count(),
        'new_post_count': Post.objects.filter(launch_time__gte=start_of_today).count(),
        'new_notice_count': Notification.objects.filter(launch_time__gte=start_of_today).count(),
        'user_count': User.objects.all().count()
    }
    return Response(context)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            password_hash = sha1(password.encode('utf-8')).hexdigest()
            user = User.objects.filter(username=username, password=password_hash).first()
            if user is not None:
                # 生成JWT令牌
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.session.clear()
        return Response({'success': True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

def get_notifcation_abstract(notification):
    if notification.abstract:
        return notification.abstract
    else:
        result = generate_summary_and_keywords(notification.text)
        notification.abstract = result['abstract']
        notification.keywords = result['keywords']
        notification.save()
        return notification.abstract


class AssistantViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def live(self, request):
        user_message = request.data.get('message')
        if user_message:
            answer = get_answer("你是一个有用的助手，现在需要你帮助用户解决生活上的问题，请用亲切的口吻，请用你的智慧回答用户的问题："+
                user_message)
            return Response({'answer': answer}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def study(self, request):
        user_message = request.data.get('message')
        if user_message:
            answer = get_answer("你是一个有用的助手，现在需要你帮助用户解决学习上的问题，请你严谨、条理性地思考，请用你的智慧回答用户的问题："+
                user_message)
            return Response({'answer': answer}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def write(self, request):
        user_message = request.data.get('topic')
        if user_message:
            answer = get_answer(
                "你是一个有用的助手，现在需要你帮助用户解决语言组织上的任何问题，"
                "请完全遵循用户的想法和主旨，输出格式(json)：{\"title\": ,\"content\":   }(文本中禁止使用单引号，换行请使用转义字符，不要直接输出多行文本)，"
                "根据用户的需求帮助他完成帖子的撰写。"
                "请注意：如果主题是一个问题，并不是让你回答这个问题，而是完善这个问题作为帖子的内容。"
                "主题: " + user_message
            )

            try:
                # 优先尝试完整解析
                context = json.loads(answer)
            except json.JSONDecodeError:
                try:
                    # 如果直接解析失败，尝试去掉头尾字符后解析
                    context = json.loads(answer[8:-3])
                except json.JSONDecodeError:
                    # 捕获解析错误并记录日志
                    context = {'error': 'AI回答格式错误'}

            # 返回结果
            return Response(context, status=status.HTTP_200_OK)

        return Response({'error': '缺少主题信息'}, status=status.HTTP_400_BAD_REQUEST)



def get_today_news(department_id=70):
    response = requests.get(f'http://today.hit.edu.cn/department-list/{department_id}?wc=40&nl=8&format=2&order=2&cid=10/')
    if response.status_code == 200:
        content = re.search(r'<ul.*/ul>', response.text)[0]
        content = re.sub(r'\\', '', content)
    else:
        content = "获取失败"
    return content

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(detail=False, methods=['post'])
    def launch(self, request):
        form = NoticeForm(request.data, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=status.HTTP_201_CREATED)
        return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        notification = get_object_or_404(Notification, pk=pk)
        notification.view_times += 1
        notification.save()
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=['get'])
    def listall(self, request):
        notifications = Notification.objects.all().order_by('-launch_time')
        page = self.paginate_queryset(notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def notice_center(self, request):
        # 向外部 API 发送请求
        info_data = request.session.get('info')
        is_authed = True if info_data else False
        is_allowed = False
        if is_authed:
            user_object = User.objects.filter(uid=info_data['id']).first()
            if user_object and user_object.permission_group and user_object.permission_group.id >= 4:
                is_allowed = True

        types = Type.objects.filter(id__gte=3)
        for type_obj in types:
            type_obj.notifications = Notification.objects.filter(type=type_obj).order_by('-launch_time')[:5]

        latest_notifications = Notification.objects.order_by('-launch_time')[:5]
        types_serialized = NoticeCenterTypeSerializer(types, many=True).data
        context = {
            'latest_notifications': NotificationSerializer(latest_notifications, many=True).data,
            'types': types_serialized,
            'is_authed': is_authed,
            'is_allowed': is_allowed,
            'content': get_today_news(),
            'content2': get_today_news(111)
        }
        return Response(context)

    @action(detail=False, methods=['GET'])
    def types(self, request):
        notification_types = Type.objects.all()
        serializer = TypeSerializer(notification_types, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    # @ratelimit(key='user', rate='5/m', method='ALL', block=True)
    def abstract(self, request, pk=None):
        return Response({'abstract': get_notifcation_abstract(get_object_or_404(Notification, pk=pk))})



def get_posts(request, cid):
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
                post.last_comment_user = last_comment.author.nickname
        context = page_object.page_queryset
    else:
        context = {}
    return context


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def launch(self, request):
        form = PostForm(request.data, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.launcher_uid = request.user.uid
            post.author = request.user
            post.save()
            return Response({'success': True, 'post_id': post.pk}, status=status.HTTP_201_CREATED)
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.view_times += 1
        post.save()
        comments = post.comments.all()

        # comment.index =  i + (comments_object.page - 1) * comments_object.page_size

        post_data = self.get_serializer(post).data
        comments_data = CommentSerializer(comments, many=True).data
        return Response({'post': post_data, 'comments': comments_data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def listall(self, request):
        posts = get_posts(request, 0)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        content = request.data.get('comment')
        user = request.user
        if content:
            Comment.objects.create(post=post, author=user, content=content)
            return Response({'message': 'Comment added successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_comment(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user == (comment.author or comment.post.author):
            comment.delete()
            return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not allowed to delete this comment'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def delete(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        info_data = request.session.get('info')
        user_object = User.objects.filter(uid=info_data['id']).first()
        if user_object == post.author:
            post.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not allowed to delete this post'}, status=status.HTTP_403_FORBIDDEN)


class CategoryTypeViewSet(viewsets.ModelViewSet):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'])
    def type(self, request):
        category_types = CategoryType.objects.all()
        for category_type in category_types:
            category_type.categories = Category.objects.filter(cid__gte=category_type.tid * 10,
                                                               cid__lte=(category_type.tid + 1) * 10)
        serializer = CategoryTypeSerializer(category_types, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        posts = get_posts(request, pk)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        category = get_object_or_404(Category, cid=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)




class UserCenterViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def edit_info(self, request):
        if not request.session.get('info'):
            return Response({'error': '用户未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        user = get_object_or_404(User, uid=request.session.get('info').get('id'))
        form = UserInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def comments(self, request):
        comments = Comment.objects.filter(author=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def subscription(self, request):
        subscriptions = UserCategoryFollow.objects.filter(user=request.user)
        serializer = UserCategoryFollowSerializer(subscriptions, many=True)
        return Response(serializer.data)



class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class UserCategoryFollowViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        cid = request.data.get('cid')
        user = request.user

        try:
            category = Category.objects.get(cid=cid)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # 检查用户是否已经关注该分类帖子
        if UserCategoryFollow.objects.filter(user=user, category=category).exists():
            return Response({'error': 'You have already followed this category.'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建关注关系
        UserCategoryFollow.objects.create(user=user, category=category)
        return Response({'success': 'Category followed successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        user = request.user


        try:
            follow_instance = UserCategoryFollow.objects.get(user=user, category_id=pk)
        except UserCategoryFollow.DoesNotExist:
            return Response({'error': 'You are not following this category.'}, status=status.HTTP_404_NOT_FOUND)

        # 删除关注关系
        follow_instance.delete()
        return Response({'success': 'Category unfollowed successfully.'}, status=status.HTTP_204_NO_CONTENT)

    def check(self, request):
        user = request.user
        cid = request.data.get('cid')
        try:
            category = Category.objects.get(cid=cid)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        subscription = UserCategoryFollow.objects.filter(user=user, category=category)
        is_following = subscription.exists()
        return Response({'is_following': is_following, 'subscription': subscription})
