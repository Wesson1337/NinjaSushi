import os
from datetime import timedelta
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NinjaSushi.settings')

app = Celery('NinjaSushi')
app.conf.timezone = 'Europe/London'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(timedelta(days=1),
                             sender.signature('app_newsletter.tasks.newsletter_email_task'),
                             name='email newsletter every day')
