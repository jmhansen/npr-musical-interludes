from .base import *

from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    'get_latest_ats_episode': {
        'task': 'songs.tasks.update_npr_program',
        'schedule': crontab(hour=16, minute=0, day_of_week=[1, 2, 3, 4, 5, 6]),
        'kwargs': {'program_pk': 1}
    },
    'get_latest_me_episode': {
        'task': 'songs.tasks.update_npr_program',
        'schedule': crontab(hour=11, minute=0, day_of_week=[1, 2, 3, 4, 5, 6]),
        'kwargs': {'program_pk': 2}
    },
    'get_latest_me_saturday_episode': {
        'task': 'songs.tasks.update_npr_program',
        'schedule': crontab(hour=12, minute=0, day_of_week=[6]),
        'kwargs': {'program_pk': 3}
    },
    'get_latest_me_sunday_episode': {
        'task': 'songs.tasks.update_npr_program',
        'schedule': crontab(hour=12, minute=0, day_of_week=[0]),
        'kwargs': {'program_pk': 4}
    },
}
