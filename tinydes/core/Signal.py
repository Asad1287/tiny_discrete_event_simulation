class Signal:
    def __init__(self, env):
        self.env = env
        self.event = simpy.Event(env)

    def trigger(self):
        self.event.succeed()
        self.event = simpy.Event(self.env)

    def wait(self):
        return self.event.wait()
