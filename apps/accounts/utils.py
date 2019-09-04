from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse, resolve_url
from django.conf import settings


def get_index_url(user):
    # FIXME: want have: self.request.customer or self.request.supporter
    if user.is_customer:
        return reverse('toppage:customer_index')
    if user.is_supporter:
        return reverse('toppage:supporter_index')
    return resolve_url(settings.LOGIN_REDIRECT_URL)
