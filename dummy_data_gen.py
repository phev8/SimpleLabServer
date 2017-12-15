import sqlite3
from time import sleep
from datetime import datetime
import random

DB_con = sqlite3.connect("EBS 20M.db3")
DB_cursor = DB_con.cursor()

val_range_min = 500
val_range_max = 1500
index = 400
while True:
    try:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        val_range_min += random.randint(-100, 100)
        val_range_max += random.randint(-100, 100)
        value = random.randint(val_range_min, val_range_max)

        DB_cursor.execute("INSERT INTO Messwerten VALUES (?, 4, 3, ?, 0, ?, 0, null)", (index, time, value))

        # Save (commit) the changes
        DB_con.commit()
        sleep(2.5)
        index += 1
    except KeyboardInterrupt:
        DB_con.close()

