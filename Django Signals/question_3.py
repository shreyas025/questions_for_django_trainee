'''
Question- By default do django signals run in the same database transaction as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.
'''

'''
Answer- Django signals do run in the same database transaction as the caller. This is critical for ensuring the atomicity of database operations.
'''

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import connection

@receiver(post_save, sender=User)
def signal_handler(sender, instance, created, **kwargs):
    if created:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO auth_user (username) VALUES ('signal_user')")

def test_transaction():
    try:
        with transaction.atomic():
            User.objects.create(username="test_user")
            raise ValueError("Rollback transaction")
    except ValueError:
        pass

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM auth_user WHERE username='test_user'")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM auth_user WHERE username='signal_user'")
        signal_user_count = cursor.fetchone()[0]

    print(user_count, signal_user_count)

test_transaction()
