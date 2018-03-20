import argparse
import tornado.web
import os
import json
import sqlite3

DB_con = None
DB_cursor = None


class SensorDataHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        window_size = self.get_argument("window", 1)

        measurements = DB_cursor.execute("SELECT * FROM Messwerten ORDER BY Zeit DESC LIMIT " + str(window_size)).fetchall()
        measurements.reverse()

        self.write(json.dumps(measurements))
        return


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
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path_dir}),
        (r"/api/measurement", SensorDataHandler),
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
