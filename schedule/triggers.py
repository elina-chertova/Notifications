from apscheduler.triggers.cron import CronTrigger

tasks_trigger = {
    'email.auto.best_movies': CronTrigger(
        year="*", month="*", day="*", hour="*", minute="4", second="15"
    ),
    'email.admin.any': CronTrigger(
        year="*", month="*", day="*", hour="*", minute="4", second="10"
    )
}

