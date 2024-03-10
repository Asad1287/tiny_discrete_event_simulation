env = HospitalSimulationEnvironment('sim.yaml')
env.run_simulation()
env.print_statistics()
plotter = Plotter(env.service_monitors, env.queue_monitors, env.wait_monitors)

# To plot the service times, waiting times, and queue lengths
plotter.plot_service_times()
plotter.plot_queue_lengths()
