from .auth_views import *
from .notice_views import *
from .post_views import *


# Create your views here.
def index(request):
    is_authed = False
    if request.session.get('info'):
        is_authed = True
    return render(request, 'index.html', {'is_authed': is_authed})



