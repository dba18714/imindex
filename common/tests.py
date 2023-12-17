from django.test import TestCase
from django.core.cache import cache


class RedisTestCase(TestCase):
    def test_redis_connection(self):
        cache.set('test_key', 'test_value', timeout=60)
        value = cache.get('test_key')
        self.assertEqual(value, 'test_value')
