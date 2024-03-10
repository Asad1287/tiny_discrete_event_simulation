import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, service_monitors, queue_monitors, wait_monitors):
        """
        Initializes the plotter with monitors.
        
        :param service_monitors: Dict of service monitors
        :param queue_monitors: Dict of queue length monitors
        :param wait_monitors: Dict of waiting time monitors
        """
        self.service_monitors = service_monitors
        self.queue_monitors = queue_monitors
        self.wait_monitors = wait_monitors
    
    def plot_service_times(self):
        """Plots the average service time for each resource."""
        resources = list(self.service_monitors.keys())
        avg_times = [monitor.mean() for monitor in self.service_monitors.values()]
        
        plt.figure(figsize=(10, 6))
        plt.bar(resources, avg_times, color='skyblue')
        plt.xlabel('Resources')
        plt.ylabel('Average Service Time (minutes)')
        plt.title('Average Service Time by Resource')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_waiting_times(self):
        """Plots the average and max waiting time for each resource."""
        resources = list(self.wait_monitors.keys())
        avg_wait_times = [monitor.mean() for monitor in self.wait_monitors.values()]
        max_wait_times = [monitor.max() for monitor in self.wait_monitors.values()]

        x = range(len(resources))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots(figsize=(12, 6))
        rects1 = ax.bar(x - width/2, avg_wait_times, width, label='Avg Waiting Time')
        rects2 = ax.bar(x + width/2, max_wait_times, width, label='Max Waiting Time')

        ax.set_xlabel('Resources')
        ax.set_ylabel('Waiting Time (minutes)')
        ax.set_title('Waiting Times by Resource')
        ax.set_xticks(x)
        ax.set_xticklabels(resources)
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_queue_lengths(self):
        """Plots the average queue length for each resource."""
        resources = list(self.queue_monitors.keys())
        avg_queue_lengths = [monitor.mean() for monitor in self.queue_monitors.values()]

        plt.figure(figsize=(10, 6))
        plt.bar(resources, avg_queue_lengths, color='lightgreen')
        plt.xlabel('Resources')
        plt.ylabel('Average Queue Length')
        plt.title('Average Queue Length by Resource')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    def plot_queue_length_over_time(self, queue_length_data, resource_name):
        """
        Plots the queue length over time for a given resource.
        
        :param queue_length_data: List of tuples (timestamp, queue_length)
        :param resource_name: Name of the resource
        """
        # Assuming queue_length_data is structured like: [('10:00', 2), ('10:05', 5), ...]
        times, lengths = zip(*queue_length_data)  # Unpack the list of tuples

        # Convert string times to datetime objects for plotting
        times = [datetime.strptime(time, '%H:%M') for time in times]

        plt.figure(figsize=(10, 6))
        plt.plot(times, lengths, marker='o', linestyle='-')

        # Formatting the plot
        plt.title(f'Queue Length Over Time for {resource_name}')
        plt.xlabel('Time')
        plt.ylabel('Queue Length')
        plt.xticks(rotation=45)

        # Use DateFormatter to handle datetime x-axis labels
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))  # Adjust interval as needed

        plt.grid(True)
        plt.tight_layout()
        plt.show()
