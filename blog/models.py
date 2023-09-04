from django.db import models

NULLABLE = {'blank': True, 'null': True}


class BlogEntru(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(**NULLABLE, verbose_name='содержимое статьи')
    preview = models.ImageField(upload_to='main/', **NULLABLE, verbose_name='превью (изображение)')
    creation_date = models.DateField(**NULLABLE, verbose_name='дата публикации')
    number_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.title} {self.number_views}'

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'