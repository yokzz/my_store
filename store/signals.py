from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'myapp':
        User = get_user_model()
        if not User.objects.filter(email='an').exists():
            User.objects.create_superuser(
                username='an0nymous_8kqwjsdhfsdssadfj',
                password='an0nymous_8kqwjsdhfsdssadfjkjsfdhkjsadhfksadhfkadshfksdahfkasdhkfashfkashfksadhfkadshfkjsadhfaksfhadksfhaskh',
                email='an0nymous_8kqwjsdhfsdssadfj@example.com'    
            )