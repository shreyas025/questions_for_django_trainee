'''
Question: By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.
'''

'''
Answer: Django signals are by default synchronous. When a signal is sent using Django's send() method, it executes all connected receivers in the same thread i.e the code execution is blocked and resumed once the handler has completed.
'''

import time
import django
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, created, **kwargs):
    print("Signal handler started.")
    time.sleep(5)
    print("Signal handler finished.")

def create_user():
    print("User creation started.")
    user = User.objects.create(username="test_user")
    print("User creation finished.")

create_user()