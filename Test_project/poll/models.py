from django.db import models
from django.urls import reverse
from datetime import datetime
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
# Create your models here.


class Personal(models.Model):
    personal_id = models.AutoField(primary_key=True)
    ext_id = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=30, verbose_name="ФИО")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('views.detail', args=[str(self.personal_id)])

class Photo(models.Model):

    photo_id = models.AutoField(primary_key=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, null=True, blank=True)
    data_pub = models.DateField(auto_now=True, db_index=True)
    data_photo = models.ImageField(upload_to='static/poll', null=True, blank=True, verbose_name="Фото")
    owner = models.ForeignKey('auth.User', related_name='photos', on_delete=models.CASCADE, null=True, blank=True)
    highlighted = models.TextField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return str(self.personal)

    def get_absolute_url(self):
        return reverse('views.detail', args=[str(self.photo_id)])

    def save(self, *args, **kwargs):
        photo_id = get_lexer_by_name(self.photo_id)
        personal = 'table' if self.personal else False
        options = {'data_photo': self.data_photo} if self.data_photo else {}
        formatter = HtmlFormatter(data_photo=self.data_photo, personal=personal,
                                  full=True, **options)
        self.highlighted = highlight(self.photo_id, personal, formatter)
        super(Photo, self).save(*args, **kwargs)

class Tests(models.Model):
    tests_id = models.AutoField(primary_key=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, null=True, blank=True)
    expected_time = models.DateTimeField(blank=True, null=True, verbose_name="Назначенное время теста", default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    result_time = models.DateTimeField(blank=True, null=True, verbose_name="Фактическое время сдачи теста", default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    result = models.BooleanField(default=False, verbose_name="Результат: да/нет")
    owner = models.ForeignKey('auth.User', related_name='tests', on_delete=models.CASCADE, null=True, blank=True)
    highlighted = models.TextField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return str(self.personal)

    def get_absolute_url(self):
        return reverse('views.detail', args=[str(self.tests_id)])

    def save(self, *args, **kwargs):
        tests_id = get_lexer_by_name(self.tests_id)
        personal = 'table' if self.personal else False
        options = {'result': self.result, 'expected_time': self.expected_time, 'result_time': self.result_time} if self.result else {}
        formatter = HtmlFormatter(result=self.result, expected_time=self.expected_time, result_time=self.result_time, personal=personal,
                                  full=True, **options)
        self.highlighted = highlight(self.tests_id, personal, formatter)
        super(Tests, self).save(*args, **kwargs)