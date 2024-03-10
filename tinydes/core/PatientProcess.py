class PatientProcess:
    def __init__(self, sim, patient_id, resources, arrival_monitor, service_monitors, queue_monitors, wait_monitors, decision_points):
        self.sim = sim
        self.patient_id = patient_id
        self.resources = resources
        self.arrival_monitor = arrival_monitor
        self.service_monitors = service_monitors
        self.queue_monitors = queue_monitors
        self.wait_monitors = wait_monitors
        self.decision_points = decision_points

    def process(self):
        arrival_time = self.sim.current_time
        service_sequence = ["NurseOrAdmin", "Doctor", "Billing"]
        patient = Entity("Patient", {"id": self.patient_id, "arrival_time": arrival_time}, arrival_time, service_sequence)
        self.arrival_monitor.record(arrival_time.timestamp())

        current_step = patient.next_service()
        while current_step:
            if current_step in self.decision_points:
                decision_point = self.decision_points[current_step]
                next_resource_name = decision_point.next_branch()
            else:
                next_resource_name = current_step

            resource = self.resources[next_resource_name]
            queue_monitor = self.queue_monitors[next_resource_name]
            wait_monitor = self.wait_monitors[next_resource_name]

            if resource.is_available():
                wait_monitor.record(0)
                resource.start_service(self.sim, patient, self.service_monitors[next_resource_name], queue_monitor, wait_monitor)
                patient.advance_service()
                current_step = patient.next_service()
            else:
                resource.enqueue_entity(self.sim, patient, queue_monitor)
                print(f"Patient {self.patient_id} queued at {resource.name} at {self.sim.current_time}")
                break

        if current_step is None:
            print(f"Patient {self.patient_id} exited the system at {self.sim.current_time}")


