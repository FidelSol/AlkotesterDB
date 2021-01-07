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
        return reverse('views.card_for_json', args=[str(self.personal_id)])

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
        return reverse('views.card_for_json', args=[str(self.photo_id)])

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
        return reverse('views.card_for_json', args=[str(self.tests_id)])

    def save(self, *args, **kwargs):
        super(Tests, self).save(*args, **kwargs)

