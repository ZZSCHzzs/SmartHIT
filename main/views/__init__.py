from .auth_views import *
from .notice_views import *
from .post_views import *
from .account_views import *


# Create your views here.
def index(request):
    is_authed = True if request.session.get('info') else False
    five_days_ago = timezone.now() - timedelta(days=5)
    start_of_today = timezone.make_aware(datetime.combine(timezone.localdate(), datetime.min.time()))
    context = {'is_authed': is_authed,
               'tops': Notification.objects.filter(type_id=2).order_by('-launch_time')[:7],
               'notifications': Notification.objects.filter(type_id__gte=3).order_by('-launch_time')[:7],
               'posts1': Post.objects.filter(launch_time__gte=five_days_ago).order_by('view_times')[:7],
               'posts2': Post.objects.filter(category__cid__in=range(20, 30)).order_by('-launch_time')[:7],
               'posts3': Post.objects.filter(category__cid__in=range(30, 40)).order_by('-launch_time')[:7],
               'posts4': Post.objects.filter(category__cid__in=range(51, 53)).order_by('-launch_time')[:7],
               'posts5': Post.objects.filter(category__cid__in=range(53, 55)).order_by('-launch_time')[:7],
               'notification_count': Notification.objects.all().count(),
               'post_count': Post.objects.all().count(),
               'new_post_count': Post.objects.filter(launch_time__gte=start_of_today).count(),
               'new_notice_count': Notification.objects.filter(launch_time__gte=start_of_today).count(),
               'user_count': User.objects.all().count()
               }
    return render(request, 'index.html', context)



