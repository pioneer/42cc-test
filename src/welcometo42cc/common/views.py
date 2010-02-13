from byteflow.decorators import render_to
from byteflow.helpers import get_object_or_none

from django.contrib.auth.decorators import login_required

from common.models import User


@login_required
@render_to('homepage.html')
def homepage(request):
    """
    Home page view
    """
    user = request.user
    if not user.is_authenticated():
        user = get_object_or_none(User, email="serge.tarkovski@gmail.com") or request.user
    return {'u': user}
