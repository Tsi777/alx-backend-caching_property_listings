from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    all_properties = cache.get('all_properties')
    if not all_properties:
        all_properties = list(Property.objects.all())
        cache.set('all_properties', all_properties, 3600)  # 1 hour
    return all_properties

def get_redis_cache_metrics():
    try:
        r = get_redis_connection("default")
        info = r.info("stats")
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0
        logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio}")
        return {"hits": hits, "misses": misses, "hit_ratio": hit_ratio}
    except Exception as e:
        logger.error(f"Failed to retrieve Redis cache metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0}
