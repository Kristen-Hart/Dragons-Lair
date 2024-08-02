import simpy

# Resource
def resource_ex(env, resource):
    with resource.request() as req:
        yield req
        print(f'Resource acquired at {env.now}')
        yield env.timeout(1)
        print(f'Resource released at {env.now}')

# PriorityResource
def priority_resource_ex(env, resource, priority):
    with resource.request(priority=priority) as req:
        yield req
        print(f'PriorityResource acquired at {env.now} with priority {priority}')
        yield env.timeout(1)
        print(f'PriorityResource released at {env.now}')

# PreemptiveResource
def preemptive_resource_ex(env, resource, preempt=False):
    with resource.request(preempt=preempt) as req:
        try:
            yield req
            print(f'PreemptiveResource acquired at {env.now}')
            yield env.timeout(1)
            print(f'PreemptiveResource released at {env.now}')
        except simpy.Interrupt:
            print(f'PreemptiveResource preempted at {env.now}')

# Store
def store_ex(env, store):
    yield store.put('item')
    print(f'Item put in store at {env.now}')
    item = yield store.get()
    print(f'Item retrieved from store at {env.now}')

# Container
def container_ex(env, container):
    yield container.put(5)
    print(f'Container now has {container.level} at {env.now}')
    yield container.get(3)
    print(f'Container now has {container.level} at {env.now}')

env = simpy.Environment()

# Resource 
resource = simpy.Resource(env, capacity=1)
env.process(resource_ex(env, resource))

# PriorityResource
priority_resource = simpy.PriorityResource(env, capacity=1)
env.process(priority_resource_ex(env, priority_resource, priority=1))
env.process(priority_resource_ex(env, priority_resource, priority=0))

# PreemptiveResource
preemptive_resource = simpy.PreemptiveResource(env, capacity=1)
p1 = env.process(preemptive_resource_ex(env, preemptive_resource, preempt=False))
env.process(preemptive_resource_ex(env, preemptive_resource, preempt=True))

# Store
store = simpy.Store(env, capacity=1)
env.process(store_ex(env, store))

# Container
container = simpy.Container(env, init=0, capacity=10)
env.process(container_ex(env, container))

env.run()
