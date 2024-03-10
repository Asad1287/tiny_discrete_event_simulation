import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from simulation import (
    Distribution,
    Entity,
    Resource,
    Queue,
    Monitor,
    Simulation,
    HospitalSimulationEnvironment,
    PatientProcess,
    NextServiceScheduler,
    PatientArrivalSimulator,
)

class TestHospitalSimulationEnvironment(unittest.TestCase):
    def setUp(self):
        self.config_file = "test_config.yaml"
        with open(self.config_file, "w") as file:
            file.write(
                """
                simulation:
                  duration: 120
                resources:
                  - name: "Reception"
                    capacity: 2
                    service_time_distribution:
                      type: "Exponential"
                      mean: 5
                    schedule:
                      start: "09:00"
                      end: "17:00"
                  - name: "Doctor"
                    capacity: 3
                    service_time_distribution:
                      type: "Normal"
                      mean: 15
                      std_dev: 3
                    schedule:
                      start: "09:00"
                      end: "17:00"
                decision_points:
                  - name: "TestDecision"
                    branches: ["Branch1", "Branch2"]
                    probabilities: [0.6, 0.4]
                service_sequence: ["Reception", "TestDecision", "Doctor"]
                patient_arrival_distribution:
                  type: "Exponential"
                  mean: 10
                """
            )

    def tearDown(self):
        import os

        os.remove(self.config_file)

    def test_run_simulation(self):
        env = HospitalSimulationEnvironment(self.config_file)

        with patch("builtins.print") as mock_print:
            env.run_simulation()

        self.assertGreater(env.arrival_monitor.count(), 0)
        self.assertGreater(env.service_monitors["Reception"].count(), 0)
        self.assertGreater(env.service_monitors["Doctor"].count(), 0)
        self.assertGreater(env.queue_monitors["Reception"].max(), 0)
        self.assertGreater(env.queue_monitors["Doctor"].max(), 0)
        self.assertGreater(env.wait_monitors["Reception"].max(), 0)
        self.assertGreater(env.wait_monitors["Doctor"].max(), 0)

        mock_print.assert_any_call(f"Average service time for Reception: {env.service_monitors['Reception'].mean():.2f} minutes")
        mock_print.assert_any_call(f"Average service time for Doctor: {env.service_monitors['Doctor'].mean():.2f} minutes")
        mock_print.assert_any_call(f"Average queue length for Reception: {env.queue_monitors['Reception'].mean():.2f}")
        mock_print.assert_any_call(f"Average queue length for Doctor: {env.queue_monitors['Doctor'].mean():.2f}")
        mock_print.assert_any_call(f"Average waiting time for Reception: {env.wait_monitors['Reception'].mean():.2f} minutes")
        mock_print.assert_any_call(f"Average waiting time for Doctor: {env.wait_monitors['Doctor'].mean():.2f} minutes")

class TestPatientProcess(unittest.TestCase):
    def test_process_with_decision_point(self):
        sim = MagicMock()
        resources = {
            "Reception": MagicMock(),
            "Branch1": MagicMock(),
            "Branch2": MagicMock(),
        }
        decision_points = {
            "TestDecision": MagicMock(next_branch=MagicMock(return_value="Branch1")),
        }
        service_sequence = ["Reception", "TestDecision", "Branch1", "Branch2"]

        patient_process = PatientProcess(
            sim,
            1,
            resources,
            MagicMock(),
            {"Reception": MagicMock(), "Branch1": MagicMock(), "Branch2": MagicMock()},
            {"Reception": MagicMock(), "Branch1": MagicMock(), "Branch2": MagicMock()},
            {"Reception": MagicMock(), "Branch1": MagicMock(), "Branch2": MagicMock()},
            decision_points,
            service_sequence,
        )

        with patch("builtins.print") as mock_print:
            patient_process.process()

        resources["Reception"].is_available.assert_called_once()
        resources["Branch1"].is_available.assert_called_once()
        resources["Branch2"].is_available.assert_not_called()
        decision_points["TestDecision"].next_branch.assert_called_once()

        mock_print.assert_any_call(f"Patient 1 exited the system at {sim.current_time}")

class TestNextServiceScheduler(unittest.TestCase):
    def test_schedule_next_service(self):
        sim = MagicMock()
        resource = MagicMock(
            queue=MagicMock(
                is_empty=MagicMock(side_effect=[False, True]),
                dequeue=MagicMock(return_value=MagicMock(next_service=MagicMock(return_value=None))),
            ),
            is_available=MagicMock(return_value=True),
            start_service=MagicMock(),
        )

        scheduler = NextServiceScheduler(
            sim,
            resource,
            MagicMock(),
            MagicMock(record=MagicMock()),
            MagicMock(),
        )

        scheduler.schedule_next_service()

        resource.queue.is_empty.assert_called()
        resource.queue.dequeue.assert_called_once()
        resource.is_available.assert_called_once()
        resource.start_service.assert_called_once()

class TestPatientArrivalSimulator(unittest.TestCase):
    def test_simulate_arrivals(self):
        sim = MagicMock(current_time=datetime(2023, 1, 1), end_time=datetime(2023, 1, 1, 1))
        resources = [MagicMock(), MagicMock()]
        arrival_monitor = MagicMock()
        service_monitors = {"Resource1": MagicMock(), "Resource2": MagicMock()}
        queue_monitors = {"Resource1": MagicMock(), "Resource2": MagicMock()}
        wait_monitors = {"Resource1": MagicMock(), "Resource2": MagicMock()}
        decision_points = {"Decision1": MagicMock(), "Decision2": MagicMock()}
        service_sequence = ["Resource1", "Decision1", "Resource2", "Decision2"]
        arrival_distribution = MagicMock(generate=MagicMock(return_value=[5]))

        simulator = PatientArrivalSimulator(
            sim,
            resources,
            arrival_monitor,
            service_monitors,
            queue_monitors,
            wait_monitors,
            decision_points,
            service_sequence,
            arrival_distribution,
        )

        with patch("simulation.PatientProcess") as mock_patient_process:
            for _ in simulator.simulate_arrivals():
                pass

        mock_patient_process.assert_called_with(
            sim,
            1,
            resources,
            arrival_monitor,
            service_monitors,
            queue_monitors,
            wait_monitors,
            decision_points,
            service_sequence,
        )
        mock_patient_process.return_value.process.assert_called_once()

if __name__ == '__main__':
    unittest.main()