'''
Question- Do django signals run in the same thread as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.
'''

'''
Answer- Yes, Django signals are executed in the same thread as the caller by default. When a signal is sent using the send() method, Django triggers all connected signal handlers.
Signal handlers execute synchronously, they block the sender function until all handlers are executed.
The thread used by the caller is the same used to run the signal handlers.
'''


import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, created, **kwargs):
    print(f"Signal handler thread ID: {threading.get_ident()}")

def create_user():
    print(f"Caller thread ID: {threading.get_ident()}")
    User.objects.create(username="test_user")

create_user()