from main.models import Notification

notifications = Notification.objects.all()

for i in notifications:
    print(i.title)
    i.abstract.clear()

    i.keywords.clear()
    i.save()