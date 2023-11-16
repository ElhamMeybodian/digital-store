import random

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, send_mail, BaseUserManager
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create and saves a User with the given username, email, phone number and password
        """
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username,
                          email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, date_joined=now, **extra_fields)
        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghigklmnopqrstuwxyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))
        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)

    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    """
    Username, password, email and phone number are required. Other fields are optional.
    """

    class Types(models.TextChoices):
        CUSTOMER = "CUSTOMER", "customer"
        STAFF = "STAFF", "staff"
        ADMIN = "ADMIN", "admin"

    type = models.CharField(max_length=8, choices=Types.choices,
                            # Default is user is customer
                            default=Types.CUSTOMER)
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(
                                        r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists")
                                })

    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    phone_number = models.BigIntegerField(_('mobile_number'), unique=True, null=True, blank=True
                                          , validators=[
            validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                      _('Enter a valid phone number'), 'invalid')
        ],
                                          error_messages={
                                              'unique': _("A user with that phone number already exists")

                                          }
                                          )
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_("last seen date"), null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def is_logged_in_user(self):
        """
        :return: True is user has logged in with valid credential.
        """
        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)


class Profile(models.Model):
    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDER = (
        (MALE, 'male'),
        (FEMALE, 'female'),
        (OTHER, 'other')

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_("nick_name"), max_length=150, blank=True)
    avatar = models.ImageField(_("avatar"), blank=True)
    birthday = models.DateField(_("birthday"), null=True, blank=True)
    gender = models.PositiveSmallIntegerField(_("gender"), choices=GENDER, default=OTHER)
    province = models.ForeignKey(verbose_name=_("province"), to="Province", null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "profiles"
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    @property
    def get_first_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICES_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android')
    )

    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('Device UUID'), null=True)
    last_login = models.DateTimeField(_('last login date'), null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICES_TYPE_CHOICES, default=WEB)
    device_os = models.CharField(_('device os'), max_length=20, blank=True)
    device_model = models.CharField(_('device model'), max_length=50, blank=True)
    app_version = models.CharField(_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_devices"
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together = ('user', 'device_uuid')


class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerManager(models.Manager):
    def create_user(self, username, phone_number, email, password, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username,
                          email=email, is_staff=False, is_active=True,
                          is_superuser=False, date_joined=now, **extra_fields)
        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=User.Types.CUSTOMER)
        return queryset


class Customer(User):
    class Meta:
        proxy = True
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    objects = CustomerManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.CUSTOMER
        return super().save(*args, **kwargs)


class AdminManager(models.Manager):
    def create_user(self, username, phone_number, email, password, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username,
                          email=email, is_staff=True, is_active=True,
                          is_superuser=True, date_joined=now, **extra_fields)
        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=User.Types.ADMIN)
        return queryset


class AdminSite(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admin'

    objects = AdminManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.ADMIN
        return super().save(*args, **kwargs)
