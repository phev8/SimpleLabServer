import requests
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from datetime import datetime

api_addr = "http://localhost:8888/api/measurement"

fig = plt.figure()
plot_data, = plt.plot([], [], '-x')
plt.pause(0.01)

while True:
    try:
        response = requests.get(api_addr, { "window": 60 })
        measurements = response.json()

        times = []
        values = []

        last_time = None
        for i, m in enumerate(measurements):
            m_time = datetime.strptime(m[3][:19], "%Y-%m-%d %H:%M:%S")

            # Use only the data of the last experiment in the visualization
            if last_time is not None:
                diff = m_time.timestamp() - last_time
                if diff > 10:
                    times = []
                    values = []

            last_time = m_time.timestamp()

            times.append(m_time)
            values.append(m[5])

        plot_data.set_data(times, values)
        if len(times) <= 0:
            continue
        plt.xlim([times[0], times[-1]])
        plt.ylim([0, 2000])
        fig.autofmt_xdate()
        plt.pause(2.5)

    except KeyboardInterrupt:
        break
