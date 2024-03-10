import unittest
from datetime import datetime, timedelta
from simulation import Distribution, Entity, Resource, Queue, Monitor, Simulation

class TestDistribution(unittest.TestCase):
    def test_exponential_distribution(self):
        dist = Distribution("Exponential", mean=5)
        samples = dist.generate(1000)
        self.assertAlmostEqual(samples.mean(), 5, delta=0.5)

    def test_normal_distribution(self):
        dist = Distribution("Normal", mean=10, std_dev=2)
        samples = dist.generate(1000)
        self.assertAlmostEqual(samples.mean(), 10, delta=0.5)
        self.assertAlmostEqual(samples.std(), 2, delta=0.5)

class TestEntity(unittest.TestCase):
    def test_entity_creation(self):
        arrival_time = datetime.now()
        service_sequence = ["Reception", "Triage", "Doctor"]
        entity = Entity("Patient", {"id": 1}, arrival_time, service_sequence)
        self.assertEqual(entity.entity_type, "Patient")
        self.assertEqual(entity.attributes, {"id": 1})
        self.assertEqual(entity.arrival_time, arrival_time)
        self.assertEqual(entity.service_sequence, service_sequence)

    def test_next_service(self):
        arrival_time = datetime.now()
        service_sequence = ["Reception", "Triage", "Doctor"]
        entity = Entity("Patient", {"id": 1}, arrival_time, service_sequence)
        self.assertEqual(entity.next_service(), "Reception")
        entity.advance_service()
        self.assertEqual(entity.next_service(), "Triage")
        entity.advance_service()
        self.assertEqual(entity.next_service(), "Doctor")
        entity.advance_service()
        self.assertIsNone(entity.next_service())

class TestResource(unittest.TestCase):
    def test_resource_availability(self):
        dist = Distribution("Exponential", mean=5)
        resource = Resource("Doctor", 2, dist, {"start": "09:00", "end": "17:00"})
        self.assertTrue(resource.is_available())
        resource.busy = 2
        self.assertFalse(resource.is_available())

class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        queue = Queue()
        entity1 = Entity("Patient", {"id": 1}, datetime.now(), [])
        entity2 = Entity("Patient", {"id": 2}, datetime.now(), [])
        queue.enqueue(entity1)
        queue.enqueue(entity2)
        self.assertEqual(len(queue.entities), 2)
        self.assertEqual(queue.dequeue(), entity1)
        self.assertEqual(queue.dequeue(), entity2)
        self.assertTrue(queue.is_empty())

class TestMonitor(unittest.TestCase):
    def test_monitor_recording(self):
        monitor = Monitor()
        monitor.record(10)
        monitor.record(20)
        monitor.record(15)
        self.assertEqual(monitor.count(), 3)
        self.assertEqual(monitor.mean(), 15)
        self.assertEqual(monitor.max(), 20)
        self.assertEqual(monitor.min(), 10)

if __name__ == '__main__':
    unittest.main()