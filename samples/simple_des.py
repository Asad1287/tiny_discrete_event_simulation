from datetime import timedelta
from tinydes.core.SimulationEnviroment import SimulationEnvironment
from tinydes.core.Simulation import Simulation
simulation_duration = timedelta(hours=1)
env = SimulationEnvironment(simulation_duration)
env.run_simulation()
env.print_statistics()