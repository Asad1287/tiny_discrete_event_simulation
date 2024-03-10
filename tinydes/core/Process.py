class Process:
    def __init__(self, sim, patient_id, resources, arrival_monitor, service_monitors, queue_monitors, wait_monitors, decision_points,service_sequence):
        self.sim = sim
        self.patient_id = patient_id
        self.resources = resources
        self.arrival_monitor = arrival_monitor
        self.service_monitors = service_monitors
        self.queue_monitors = queue_monitors
        self.wait_monitors = wait_monitors
        self.decision_points = decision_points
        self.service_sequence = service_sequence
    def process(self):
        arrival_time = self.sim.current_time
        patient = Entity("Patient", {"id": self.patient_id, "arrival_time": arrival_time}, arrival_time, self.service_sequence)
        self.arrival_monitor.record(arrival_time.timestamp())

        for current_step in self.service_sequence:
            if current_step in self.decision_points:
                decision_point = self.decision_points[current_step]
                next_step = decision_point.next_branch()
                patient.attributes[current_step] = next_step  # Store the decision outcome in patient attributes
            else:
                resource = self.resources[current_step]
                queue_monitor = self.queue_monitors[current_step]
                wait_monitor = self.wait_monitors[current_step]

                if resource.is_available():
                    wait_monitor.record(0)
                    resource.start_service(self.sim, patient, self.service_monitors[current_step], queue_monitor, wait_monitor)
                else:
                    resource.enqueue_entity(self.sim, patient, queue_monitor)
                    print(f"Patient {self.patient_id} queued at {resource.name} at {self.sim.current_time}")
                    return

        print(f"Patient {self.patient_id} exited the system at {self.sim.current_time}")

