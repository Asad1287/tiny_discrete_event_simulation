import heapq
from datetime import datetime, timedelta
class Simulation:
   def __init__(self):
        self.current_time = datetime.now()
        self.event_queue = []
        self.event_id = 0
        self.resources = {}  # Dictionary to hold resources

   def schedule_event(self, duration, callback):
        event_time = self.current_time + duration
        # Add event_id as a tiebreaker to ensure the heap can always order events
        heapq.heappush(self.event_queue, (event_time, self.event_id, callback))
        self.event_id += 1
   def add_resource(self, name, resource):
        self.resources[name] = resource

   def run(self, until):
        while self.event_queue and self.current_time <= until:
            event_time, _, callback = heapq.heappop(self.event_queue)  # Adjust to unpack the event_id
            self.current_time = event_time
            callback()

   def process_generator(self, generator_func):
        def step(*args):
            try:
                # Attempt to advance the generator to its next yield, which should be a timedelta
                duration = next(generator_func)
                if isinstance(duration, timedelta):
                    self.schedule_event(duration, lambda: step())
            except StopIteration:
                pass
        step()