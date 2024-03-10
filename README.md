# tiny_discrete_event_simulation
Discrete event simulation package written in pure python 


Tiny Discrete Event Simulation
A lightweight and flexible discrete event simulation library in Python.

Features
Easy-to-use API for defining and running simulations
Supports various probability distributions for event generation
Customizable entities, resources, and processes
Built-in monitoring and statistics collection
Modular and extensible architecture
Installation

pip install tiny-des

from tinydes import Simulation, Resource, Distribution

def patient_process(patient, resources):
    # Define the patient process logic
    # ...

# Create a simulation environment
env = Simulation()

# Define resources
nurse = Resource("Nurse", capacity=2, service_time=Distribution("exponential", mean=10))
doctor = Resource("Doctor", capacity=1, service_time=Distribution("normal", mean=20, std_dev=5))

# Add resources to the simulation environment
env.add_resource(nurse)
env.add_resource(doctor)

# Define the patient arrival process
env.process(patient_process, patient_arrival=Distribution("exponential", mean=15))

# Run the simulation for 1000 time units
env.run(until=1000)

# Generate reports and statistics
env.print_statistics()

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License.

Feel free to customize the content based on your project's specific features, installation instructions, and documentation. The README should provide a concise overview of your project, highlighting its key features and providing instructions for getting started. Make sure to update the links and references to match your project's repository and documentation.