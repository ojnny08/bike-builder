from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Components
from .serializer import ComponentsSerializer


def _clear_query_caches():
    delete_pattern = getattr(cache, "delete_pattern", None)
    if delete_pattern:
        delete_pattern("components:list:*")
        delete_pattern("components:brands:*")


@receiver(post_save, sender=Components)
def refresh_component_cache(sender, instance, **kwargs):
    cache.set(f"components:detail:{instance.pk}", ComponentsSerializer(instance).data, 60 * 60)
    _clear_query_caches()


@receiver(post_delete, sender=Components)
def clear_component_cache(sender, instance, **kwargs):
    cache.delete(f"components:detail:{instance.pk}")
    _clear_query_caches()
