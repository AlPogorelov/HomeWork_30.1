from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.db.models import Q
from django.template.loader import render_to_string
from config import settings
from courses.models import Course
from users.models import Subscription
from django.core.mail import send_mail
User = get_user_model()


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        for subscription in subscriptions:
            user = subscription.user
            context = {
                'course': course,
                'user': user,
                'course_url': f"{settings.FRONTEND_URL}/courses/{course.id}/"
            }

            html_message = render_to_string(
                'emails/course_updated.html',
                context
            )

            send_mail(
                subject=f'Обновление курса "{course.course_name}"',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )

    except Exception as e:

        raise


@shared_task
def check_inactive_users(inactive_days=30):
    """
    Блокировка пользователей, не заходивших более указанных дней
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=inactive_days)

        inactive_users = User.objects.filter(
            Q(last_login__lt=cutoff_date) |
            Q(last_login__isnull=True, date_joined__lt=cutoff_date),
            is_active=True
        )

        count = inactive_users.update(is_active=False)

        return f"Успешно заблокировано {count} пользователей"

    except Exception as e:

        raise