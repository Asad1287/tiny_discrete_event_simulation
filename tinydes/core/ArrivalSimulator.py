import heapq
from datetime import datetime, timedelta
from scipy import stats
import numpy as np
from tinydes.core.EntityProcess import EntityProcess
class ArrivalSimulator:
    def __init__(self, sim, resources, arrival_monitor, service_monitors, queue_monitors, wait_monitors,decision_points,service_sequence, arrival_distribution):
        self.sim = sim
        self.resources = resources
        self.arrival_monitor = arrival_monitor
        self.service_monitors = service_monitors
        self.queue_monitors = queue_monitors
        self.wait_monitors = wait_monitors
        self.patient_id = 1
        self.decision_points = decision_points
        self.service_sequence = service_sequence
        self.arrival_distribution = arrival_distribution
        
    def simulate_arrivals(self):
        while True:
            arrival_delay = abs(np.random.normal(loc=5, scale=2))
            next_arrival_time = self.sim.current_time + timedelta(minutes=arrival_delay)
            if next_arrival_time > self.sim.end_time:
                break
            yield timedelta(minutes=arrival_delay)

            patient_process = PatientProcess(self.sim, self.patient_id, self.resources, self.arrival_monitor,
                                             self.service_monitors, self.queue_monitors, self.wait_monitors,
                                             self.decision_points, self.service_sequence)
            patient_process.process()
            self.patient_id += 1