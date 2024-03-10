from tinydes.core.Simulation import Simulation
from tinydes.core.Monitor import Monitor
from tinydes.core.Distribution import Distribution
from tinydes.core.Resource import Resource
from tinydes.core.ArrivalSimulator import ArrivalSimulator
from tinydes.core.NextServiceScheduler import NextServiceScheduler
from tinydes.core.DecisionPoint import DecisionPoint
import yaml
from datetime import timedelta

class SimulationEnvironment:
   def __init__(self, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        self.sim = Simulation()
        self.sim.end_time = self.sim.current_time + timedelta(minutes=config['simulation']['duration'])

        self.arrival_monitor = Monitor()
        self.service_monitors = {resource['name']: Monitor() for resource in config['resources']}
        self.queue_monitors = {resource['name']: Monitor() for resource in config['resources']}
        self.wait_monitors = {resource['name']: Monitor() for resource in config['resources']}

        self.decision_points = {dp['name']: DecisionPoint(dp['name'], dp['branches'], dp['probabilities'])
                                for dp in config['decision_points']}

        self.resources = {resource['name']: Resource(resource['name'], resource['capacity'],
                                                     Distribution(resource['service_time_distribution']['type'],
                                                                  **resource['service_time_distribution']),
                                                     resource['schedule'])
                          for resource in config['resources']}

        self.service_sequence = config['service_sequence']
        self.patient_arrival_distribution = Distribution(config['patient_arrival_distribution']['type'],
                                                         **config['patient_arrival_distribution'])


   def run_simulation(self):
        patient_arrival_simulator = ArrivalSimulator(self.sim, self.resources, self.arrival_monitor,
                                                        self.service_monitors, self.queue_monitors, self.wait_monitors,
                                                        self.decision_points, self.service_sequence,
                                                        self.patient_arrival_distribution)
        self.sim.process_generator(patient_arrival_simulator.simulate_arrivals())

        for resource in self.resources.values():
            next_service_scheduler = NextServiceScheduler(self.sim, resource, self.service_monitors[resource.name],
                                                          self.queue_monitors[resource.name], self.wait_monitors[resource.name])
            self.sim.schedule_event(timedelta(minutes=0), next_service_scheduler.schedule_next_service)

        self.sim.run(self.sim.end_time)

   def print_statistics(self):
        for resource_name, service_monitor in self.service_monitors.items():
            print(f"Average service time for {resource_name}: {service_monitor.mean():.2f} minutes")
        for resource_name, queue_monitor in self.queue_monitors.items():
            print(f"Average queue length for {resource_name}: {queue_monitor.mean():.2f}")
        for resource_name, wait_monitor in self.wait_monitors.items():
            print(f"Average waiting time for {resource_name}: {wait_monitor.mean():.2f} minutes")
            print(f"Max waiting time for {resource_name}: {wait_monitor.max():.2f} minutes")
        print(f"Total patients served: {self.arrival_monitor.count()}")