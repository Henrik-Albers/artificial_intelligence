import random


def create_swarms(smart_meters: list, num_swarms: int) -> list:
    """Creates 'num_swarms' randomly generated swarms"""

    swarms = list()
    for i in range(num_swarms):
        swarm = random.sample(smart_meters, random.randint(2, len(smart_meters)))
        for sm in swarm:
            sm.increment_swarm_count()
        swarms.append(swarm)

    return swarms
