from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import login_customer_required, login_supporter_required
from accounts.utils import get_index_url
from django.shortcuts import redirect


@login_required
def index(request):
    url = get_index_url(request.user)
    return redirect(url)


@login_customer_required
def customer_index(request):
    return render(request, 'customer.html', context={'customer': request.user.customer})


@login_supporter_required
def supporter_index(request):
    return render(request, 'supporter.html', context={'supporter': request.user.supporter})
