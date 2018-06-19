import argparse
import tornado.web
import os
import json
import sqlite3
from datetime import datetime
from video_generator import create_signal_plot_video

DB_con = None
DB_cursor = None


class GetVideoListHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        file_list = os.listdir(static_path_dir)
        file_list.sort()

        video_list = []
        for f in file_list:
            if f.split('.')[-1] != 'mp4' or len(f.split('_')) != 3:
                continue
            else:
                video_list.append(
                    {
                        "link": "static/" + f,
                        "start": f.split('_')[1],
                        "end": f.split('.')[0].split('_')[2]
                    }
                )

        video_list.reverse()

        self.write(json.dumps(video_list))


class DeleteVideoHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self, *args, **kwargs):
        filename = self.get_argument("filename")

        try:
            os.remove(os.path.join(PATH, filename))
        except OSError:
            pass


class SignalPlotGeneratorHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        min_time = self.get_argument("from")
        max_time = self.get_argument("to")
        window_size = int(self.get_argument("window"))

        min_time = datetime.strptime(min_time, "%Y-%m-%d %H:%M:%S").timestamp()
        max_time = datetime.strptime(max_time, "%Y-%m-%d %H:%M:%S").timestamp()
        min_time = datetime.utcfromtimestamp(min_time)
        max_time = datetime.utcfromtimestamp(max_time)

        video_name = create_signal_plot_video(DB_cursor, min_time, max_time, window_size, 1.0/24)

        self.write(json.dumps({
            "link": "static/" + video_name,
            "start": video_name.split('_')[1],
            "end": video_name.split('.')[0].split('_')[2],
        }))


class SensorDownloadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        min_time = self.get_argument("from")
        max_time = self.get_argument("to")

        min_time = datetime.strptime(min_time, "%Y-%m-%d %H:%M:%S").timestamp()
        max_time = datetime.strptime(max_time, "%Y-%m-%d %H:%M:%S").timestamp()
        min_time = datetime.utcfromtimestamp(min_time)
        max_time = datetime.utcfromtimestamp(max_time)
        print(min_time, max_time)

        measurements = DB_cursor.execute("SELECT * FROM Messwerten WHERE Zeit BETWEEN ? AND ? ORDER BY Zeit DESC", (min_time, max_time)).fetchall()
        measurements.reverse()
        self.write(json.dumps(measurements))
        return


class SensorDataHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        window_size = self.get_argument("window", 1)

        measurements = DB_cursor.execute("SELECT * FROM Messwerten ORDER BY Zeit DESC LIMIT " + str(window_size)).fetchall()
        measurements.reverse()
        print(measurements)

        self.write(json.dumps(measurements))
        return

class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--webport', metavar='PORT', type=int, default=8888,
                        help='API port.')
    parser.add_argument('-d', '--db_path', metavar='DBPATH', type=str, default="EBS 20M.db3",
                        help='Path to the sensor DB.')

    args = parser.parse_args()

    DB_con = sqlite3.connect(args.db_path)
    DB_cursor = DB_con.cursor()

    settings = {
        # "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "xsrf_cookies": False,
    }

    PATH = os.path.dirname(os.path.realpath(__file__))
    static_path_dir = os.path.join(PATH, 'static')

    app = tornado.web.Application([
        (r'/static/(.*)', MyStaticFileHandler, {'path': static_path_dir}),
        (r"/api/measurement", SensorDataHandler),
        (r"/api/measurement-in-range", SensorDownloadHandler),
        (r"/api/plot-video-generator", SignalPlotGeneratorHandler),
        (r"/api/videos", GetVideoListHandler),
        (r"/api/delete-video", DeleteVideoHandler),
        #(r"/api/sensors", SensorListHandler),
        #(r"/api/sensorselection", SensorSelectionHandler),
        # (r"/api/ir", SensorDataHandler, {'proxyport': args.proxyport }),
        # (r"/api/us", SensorDataHandler, {'proxyport': args.proxyport }),

    ], **settings)
    app.listen(args.webport)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
