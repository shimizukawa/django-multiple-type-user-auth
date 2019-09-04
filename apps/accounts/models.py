from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist


class FrontUser(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = BaseUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_staff = False  # Admin画面アクセス時に500エラーにしないために必要
    has_module_perms = lambda *args: False  # Admin画面アクセス時に500エラーにしないために必要

    class Meta:
        verbose_name = _('front user')
        verbose_name_plural = _('front users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_customer(self):
        try:
            return bool(self.customer)
        except ObjectDoesNotExist:
            return False

    @property
    def is_supporter(self):
        try:
            return bool(self.supporter)
        except ObjectDoesNotExist:
            return False


class CustomerUser(FrontUser):
    user = models.OneToOneField(
        FrontUser, on_delete=models.CASCADE,
        parent_link=True,
        related_name='customer',
    )
    tel = models.CharField('電話番号', max_length=20)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class SupporterUser(FrontUser):
    user = models.OneToOneField(
        FrontUser, on_delete=models.CASCADE,
        parent_link=True,
        related_name='supporter',
    )
    organization = models.CharField('組織', max_length=64)

    class Meta:
        verbose_name = _('Supporter')
        verbose_name_plural = _('Supporters')
