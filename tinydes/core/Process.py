class Process:
    def __init__(self, env, generator):
        self.env = env
        self.generator = generator

    def run(self):
        try:
            next(self.generator)
            self.env.schedule_event(self.env.current_time, self)
        except StopIteration:
            pass

    def __next__(self):
        return next(self.generator)