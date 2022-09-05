from django.db import models


class NewsletterEmail(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='время изменения')

    class Meta:
        verbose_name = 'email для рассылки'
        verbose_name_plural = 'email для рассылки'

    def __str__(self):
        return f'{self.email}'
