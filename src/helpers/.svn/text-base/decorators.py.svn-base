from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def post_or_redirect_to_front(view, *args):
    """
    If request method isn't POST, redirect to front pages
    """
    def decorated_view(*args):
        if args[0].method == 'POST':
            return view(*args)
        else:
            return HttpResponseRedirect(reverse('newtype.front.views.front'))
    return decorated_view
        