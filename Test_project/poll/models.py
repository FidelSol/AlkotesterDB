from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse




# Create your models here.


class Personal(models.Model):
    personal_id = models.AutoField(primary_key=True)
    ext_id = models.IntegerField(null=True, blank=True, verbose_name="Расширенный ID")
    full_name = models.CharField(max_length=30, verbose_name="ФИО")
    birth_date = models.DateField(db_index=True, verbose_name="Дата рождения", null=True, blank=True)
    position = models.CharField(max_length=30, verbose_name="Должность", null=True, blank=True)
    punishment = models.IntegerField(null=True, blank=True, verbose_name="Дисциплинарные взыскания")


    objects = models.Manager()

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('views.card', args=[str(self.personal_id)])

    def save(self, *args, **kwargs):
        super(Personal, self).save(*args, **kwargs)

class Photo(models.Model):

    photo_id = models.AutoField(primary_key=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, null=True, blank=True)
    data_pub = models.DateField(auto_now=True, db_index=True, verbose_name="Дата публикации")
    data_photo = models.ImageField(upload_to='static/poll', null=True, blank=True, verbose_name="Фото")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return str(self.personal)

    def get_absolute_url(self):
        return reverse('views.photo', args=[str(self.photo_id)])

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

class Tests(models.Model):
    RESULT_CHOICES = [
        (False, 'Провален'),
        (True, 'Успешно'),
    ]

    tests_id = models.AutoField(primary_key=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, null=True, blank=True)
    expected_time = models.DateTimeField(blank=True, null=True, verbose_name="Назначенное время теста")
    result_time = models.DateTimeField(blank=True, null=True, verbose_name="Фактическое время сдачи теста")
    result = models.BooleanField(choices=RESULT_CHOICES, default=False, verbose_name="Результат")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['-result_time']

    def __str__(self):
        return str(self.personal)

    def get_absolute_url(self):
        return reverse('views.tests', args=[str(self.tests_id)])

    def save(self, *args, **kwargs):
        super(Tests, self).save(*args, **kwargs)

class CustomAccountManager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self.model(username=username, email=email, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        return self.get(username=username_)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, verbose_name="Username", unique=True)
    email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.username

    def natural_key(self):
        return self.username

    def __str__(self):
        return self.username

ROLE_CHOICES = [
        ('Chief', 'Руководитель'),
        ('Manager', 'Менеджер'),
    ]

class UserGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=30, verbose_name="Уровень доступа")
    members = models.ManyToManyField(CustomUser)

User = get_user_model()









