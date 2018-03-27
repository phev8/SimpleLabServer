import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

from datetime import datetime


def get_windows(start, end, window_method):
    window_size = float(window_method.split("-")[1]) / 1000.0
    step_size = float(window_method.split("-")[2]) / 1000.0

    current_window = (start, start + window_size / 2, start + window_size)
    windows = [current_window]

    while current_window[2] < end:
        current_window = (current_window[0] + step_size, current_window[1] + step_size, current_window[2] + step_size)
        windows.append(current_window)

    return windows


def get_data(DB_cursor, min_time, max_time):
    measurements = DB_cursor.execute("SELECT * FROM Messwerten WHERE Zeit BETWEEN ? AND ? ORDER BY Zeit ASC",
                                     (min_time, max_time)).fetchall()

    data = []
    for m in measurements:
        data.append([
            datetime.strptime(m[3], "%Y-%m-%d %H:%M:%S").timestamp(),
            m[5]
        ])

    return data


def create_signal_plot_video(DB_cursor, start_time, end_time, window_size, window_step):
    output_file = os.path.join("static", "measurement_" +
                               datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d-%H-%M-%S") + "_" +
                               datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d-%H-%M-%S") + ".mp4")

    window_method = "SW-" + str(int(window_size * 1000)) + "-" + str(int(window_step * 1000))

    start_time_timestamp = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timestamp()
    signal_min = start_time_timestamp - window_size / 2
    signal_max = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timestamp() + window_size / 2
    windows = get_windows(signal_min, signal_max, window_method)
    windows = pd.DataFrame(windows[:-1], columns=['t_start', 't_mid', 't_end'])

    raw_signal = get_data(DB_cursor, start_time, end_time)

    raw_df = pd.DataFrame(raw_signal,
                          columns=['timestamp', 'values'])
    raw_df.set_index('timestamp', inplace=True)

    signals = ['values']

    print( "--> create signal video ", output_file)
    FFMpegWriter = manimation.writers['ffmpeg']
    title = 'Experiment ' + start_time + ' - ' + end_time
    metadata = dict(title=title, artist='Peter Hevesi',
            comment='DFKI')

    writer = FFMpegWriter(fps=1.0/window_step, metadata=metadata, bitrate=-1, codec="libx264", extra_args=['-pix_fmt', 'yuv420p'])

    #fig = plt.figure()
    fig, ax = plt.subplots(figsize=(12, 4), dpi=300)
    for index, signal_name in enumerate(signals):
        plt.plot(raw_df.index - start_time_timestamp,  raw_df[signal_name])

    plt.title(title)
    plt.legend(signals)

    plt.grid()
    plt.tight_layout()


    #ax = plt.gca()
    vl = ax.axvline(0, color="k")  # the vert line
    plt.show()

    last_status = 0
    with writer.saving(fig, output_file, 100):

        for wnd in windows.itertuples():
            print(wnd)
            plt.xlim(wnd.t_start - start_time_timestamp, wnd.t_end - start_time_timestamp)
            current_time = wnd.t_mid
            vl.set_xdata(current_time - start_time_timestamp)
            plt.draw()
            writer.grab_frame()

            # current_values = raw_df[(raw_df.index >= wnd.t_start) & (raw_df.index <= wnd.t_end)]

    print( "<-- ready.")
    plt.close()
    return os.path.basename(output_file)