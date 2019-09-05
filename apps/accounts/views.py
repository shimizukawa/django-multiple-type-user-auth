from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from .utils import get_index_url


class LoginView(BaseLoginView):

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or get_index_url(self.request.user)


def logout_view(request):
    logout(request)
    return redirect('toppage:index')
