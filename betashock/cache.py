import pylibmc
from datetime import date
from dogpile import Dogpile, NeedRegenerationException

mc_pool = pylibmc.ThreadMappedPool(pylibmc.Client(["127.0.0.1"]))

# Taken from the dogpile docs
def cached(key, expiration_time):
    """A decorator that will cache the return value of a function
    in memcached given a key."""

    def get_value():
         with mc_pool.reserve() as mc:
            value = mc.get(key)
            if value is None:
                raise NeedRegenerationException()
            return value

    dogpile = Dogpile(expiration_time, init=True)

    def decorate(fn):
        def gen_cached():
            value = fn()
            with mc_pool.reserve() as mc:
                mc.set(key, value)
            return value

        def invoke():
            with dogpile.acquire(gen_cached, get_value) as value:
                return value
        return invoke

    return decorate

def set_member_stats(member_name, member_stat):
    @cached(member_name, -1)
    def set_member_stat():
        return member_stat
    if set_member_stat():
        return True
    return False

def get_member_stats(member_name):
    with mc_pool.reserve() as mc:
        member_stat = mc.get(member_name)
    return member_stat