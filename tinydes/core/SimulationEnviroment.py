from tinydes.core.Simulation import Simulation
from tinydes.core.Monitor import Monitor
from tinydes.core.Distribution import Distribution
from tinydes.core.Resource import Resource
from tinydes.core.ArrivalSimulator import ArrivalSimulator


class SimulationEnvironment:
    def __init__(self, simulation_duration):
        self.sim = Simulation()
        self.sim.end_time = self.sim.current_time + simulation_duration

        # Create monitors for different statistics
        self.arrival_monitor = Monitor()
        self.service_monitor = Monitor()
        self.queue_monitor = Monitor()
        self.wait_monitor = Monitor()

        # Define service time distributions for resources
        service_time_dist1 = Distribution("Normal", mean=5, std_dev=2)
        service_time_dist2 = Distribution("Normal", mean=5, std_dev=3)

        # Initialize resources with multiple servers
        resource1 = Resource("Counter 1", 2, service_time_dist1, {"start": "09:00", "end": "17:00"})
        resource2 = Resource("Counter 2", 2, service_time_dist2, {"start": "09:00", "end": "17:00"})
        self.resources = [resource1, resource2]

    def run_simulation(self):
        # Start the process of simulating customer arrivals and service
        customer_arrival_simulator = ArrivalSimulator(self.sim, self.resources, self.arrival_monitor,
                                                      self.service_monitor, self.queue_monitor, self.wait_monitor,
                                                      "Customer")
        self.sim.process_generator(customer_arrival_simulator.simulate_arrivals())

        # Run the simulation
        self.sim.run(self.sim.end_time)

    def print_statistics(self):
        # Calculate and print statistics
        print(f"Average service time: {self.service_monitor.mean():.2f} minutes")
        print(f"Average queue length: {self.queue_monitor.mean():.2f}")
        print(f"Average waiting time: {self.wait_monitor.mean():.2f} minutes")
        print(f"Max queue length: {self.queue_monitor.max()}")
        print(f"Max waiting time: {self.wait_monitor.max():.2f} minutes")
        print(f"Total customers served: {self.service_monitor.count()}")