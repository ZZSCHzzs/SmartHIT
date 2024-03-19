from .utils import *


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('launcher', 'type', 'title', 'text', 'additional_graphics')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'fixed-height-textarea'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "additional_graphics":
                continue
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = current_classes + ' form-control'


def launch(request):
    is_authed = True if request.session.get('info') else False
    if not is_authed:
        return redirect('/login/?next=/notice/launch')
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    info_data = request.session.get('info')
    user_object = User.objects.filter(uid=info_data['id']).first()
    if user_object and user_object.permission_group and user_object.permission_group.id < 4:
        return redirect('/notice')
    form = NoticeForm()
    return render(request, 'launch.html', {'form': form, 'is_authed': is_authed})


def n(request, nid):
    is_authed = True if request.session.get('info') else False
    notification = get_object_or_404(Notification, pk=nid)
    notification.view_times += 1
    notification.save()
    return render(request, 'n.html', {'notification': notification, 'is_authed': is_authed})


def notice_list(request):
    is_authed = True if request.session.get('info') else False
    notifications = Notification.objects.all().order_by('-launch_time')
    page_object = Pagination(request, notifications)
    context = {
        'notifications': page_object.page_queryset,
        'page_string': page_object.html(),
        'is_authed': is_authed
    }
    return render(request, 'notice_list.html', context)


def notice(request):
    is_allowed = False
    is_authed = True if request.session.get('info') else False
    if is_authed:
        info_data = request.session.get('info')
        user_object = User.objects.filter(uid=info_data['id']).first()
        is_allowed = True if user_object and user_object.permission_group and user_object.permission_group.id >= 4 else False
    latest_notifications = Notification.objects.order_by('-launch_time')[:5]
    return render(request, 'notice.html', {'latest_notifications': latest_notifications,
                                           'is_authed': is_authed, 'is_allowed': is_allowed})
