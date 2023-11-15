from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Choice, Answer


@receiver(post_save, sender=Choice)
@receiver(post_delete, sender=Choice)
@receiver(post_save, sender=Answer)
@receiver(post_delete, sender=Answer)
def clear_poll_results_cache(sender, instance, **kwargs):
    print("Invalidating the cache")
    if hasattr(instance, 'question'):
        poll_id = instance.question.poll_id
    else:
        poll_id = instance.choice.question.poll_id

    cache_key = f'poll_results_{poll_id}'
    cache.delete(cache_key)
