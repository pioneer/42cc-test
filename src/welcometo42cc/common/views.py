from byteflow.decorators import render_to
from byteflow.helpers import get_object_or_none

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from common.models import User
from common.forms import UserForm


def get_user(request):
    user = request.user
    if not user.is_authenticated():
        user = get_object_or_none(User, email="serge.tarkovski@gmail.com") or request.user
    return user

@login_required
@render_to('homepage.html')
def homepage(request):
    """
    Home page view
    """
    return {'u': get_user(request)}

@login_required
@render_to('form.html')
def userform(request):
    """
    A view to edit info from homepage
    """
    user= get_user(request)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        try:
            form.save()
        except ValueError:
            pass
        else:
            return HttpResponseRedirect("/")
    else:
        form = UserForm(instance=user)
    return {'form': form}
