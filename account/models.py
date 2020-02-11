from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


def validate_phone(value):
    """    Номер телефона должен быть:
    ^\d{6}$ - только цифры 6 знаков для городских номеров
    ^[9]\d{9}$ - 10 цифр начинается на девятку
    ^[7-8][9]\d{9}$ - 11 цифр начинается на 7 или 8 потом 9 и еще 9 знаков
    ^\+[7][9]\d{9}$ - 12 знаков в федеральном формате на +7     """
    import re
    reg = re.compile('^\d{6}$|^[9]\d{9}$|^[7-8][9]\d{9}$|^\+[7][9]\d{9}$')
    if not reg.match(value):
        raise ValidationError(_(u'%s hashtag doesnot comply' % value))


class CustomUser(AbstractUser):
    """ модель пользователя с расширением дополнительными полями """
    # поле выбора позиции пользователя
    TITLE_CHOICE = (
        (1, _('administrator')),
        (2, _('master')),
        (3, _('manager'))
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

    def get_full_name(self):  # Функция возвращает полное имя пользователя формат: Фамилия Имя Отчество
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_short_name(self):
        """Функция возвращает короткое имя пользователя в формате: Фамилия И.О.
        или адрес электронной почты если все поля пустые """
        if self.first_name != '' and self.middle_name != '' and self.last_name != '':
            return self.last_name + ' ' + self.first_name[0] + '.' + self.middle_name[0] + '.'
        else:
            return self.email

    def image_tag(self):  # функция вывода аватарки в админке
        return mark_safe('<img src="/directory/%s" width="150" height="150" />' % (self.avatar))

    def image_thumblr(self):  # эксперимент с выводом аватарки и подписи под ней с именем пользователя
        return mark_safe(
            '<figure class = "avtar"><img src="/directory/%s" width="50" height="50" />'
            '<figcaption>%s</figcaption></figure>' % (
                self.avatar, self.get_short_name()))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        """ переопределяем медод save дополняя его функцией сохранения
    номера телефона в правильном формате"""
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
