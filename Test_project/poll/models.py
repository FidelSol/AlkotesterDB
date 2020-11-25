from django.db import models
from django.urls import reverse

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

    objects = models.Manager()

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return str(self.personal)

    def get_absolute_url(self):
        return reverse('views.detail', args=[str(self.photo_id)])

class Tests(models.Model):
    tests_id = models.AutoField(primary_key=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, null=True, blank=True)
    expected_time = models.DateTimeField(blank=True, null=True, verbose_name="Назанченное время теста")
    result_time = models.DateTimeField(blank=True, null=True, verbose_name="Фактическое время сдачи теста")
    result = models.BooleanField(default=False, verbose_name="Результат: да/нет")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return str(self.personal)

    def get_absolute_url(self):
        return reverse('views.detail', args=[str(self.tests_id)])