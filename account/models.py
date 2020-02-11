from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


def validate_phone(value):
    import re
    '''
    Номер телефона должен быть:
    ^\d{6}$ - только цифры 6 знаков для городских номеров
    ^[9]\d{9}$ - 10 цифр начинается на девятку
    ^[7-8][9]\d{9}$ - 11 цифр начинается на 7 или 8 потом 9 и еще 9 знаков
    ^\+[7][9]\d{9}$ - 12 знаков в федеральном формате на +7 
    '''
    reg = re.compile('^\d{6}$|^[9]\d{9}$|^[7-8][9]\d{9}$|^\+[7][9]\d{9}$')
    if not reg.match(value):
        raise ValidationError(_(u'%s hashtag doesnot comply' % value))


class CustomUser(AbstractUser):
    TITLE_CHOICE = (
        (1, _('administrator')),
        (2,_('master')),
        (3,_('manager'))
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    middle_name = models.CharField(_('Middle name'), max_length=32, blank=True)
    phone = models.CharField(_('Phone Number'), max_length=12, unique=True, validators=[validate_phone])
    address = models.CharField(_('Address'), max_length=64, blank=True)
    position = models.IntegerField(_('Position in company'), choices=TITLE_CHOICE, default=2)
    birth_to_day = models.DateField(_('User BirthDay'), blank=True, null=True)
    avatar = models.ImageField(verbose_name=_('Photo'), upload_to='users/', default='../static/images/avatar/women.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def image_tag(self):
        return mark_safe('<img src="/directory/%s" width="150" height="150" />' % (self.avatar))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if len(self.phone) == 6:
            self.phone = '+73822' + self.phone
        elif len(self.phone) == 10:
            self.phone = '+7' + self.phone
        elif len(self.phone) == 11:
            if self.phone[0] == '7' or self.phone[0] == '8':
                self.phone = '+7' + self.phone[1:]
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
