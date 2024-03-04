# Thanks to mac4n6 for the groundwork https://www.mac4n6.com/blog/2018/8/5/knowledge-is-power-using-the-knowledgecdb-database-on-macos-and-ios-to-determine-precise-user-and-application-usage
#    although the queries seem to need to be changed for Mac OS 13 (instead of 10)
import sqlite3
import os
from collections import Counter
home_directory = os.path.expanduser("~")
db_path = os.path.join(home_directory, "Library/Application Support/Knowledge/knowledgeC.db")
con = sqlite3.connect(db_path)

con.row_factory = sqlite3.Row
cur = con.cursor()
q = """
SELECT
datetime(ZOBJECT.ZCREATIONDATE+978307200,'UNIXEPOCH', 'LOCALTIME') as "ENTRY CREATION", 
CASE ZOBJECT.ZSTARTDAYOFWEEK 
    WHEN "1" THEN "Sunday"
    WHEN "2" THEN "Monday"
    WHEN "3" THEN "Tuesday"
    WHEN "4" THEN "Wednesday"
    WHEN "5" THEN "Thursday"
    WHEN "6" THEN "Friday"
    WHEN "7" THEN "Saturday"
END "DAY OF WEEK",
ZOBJECT.ZSECONDSFROMGMT/3600 AS "GMT OFFSET",
datetime(ZOBJECT.ZSTARTDATE+978307200,'UNIXEPOCH', 'LOCALTIME') as "START", 
datetime(ZOBJECT.ZENDDATE+978307200,'UNIXEPOCH', 'LOCALTIME') as "END",
(ZOBJECT.ZENDDATE-ZOBJECT.ZSTARTDATE) as "USAGE IN SECONDS",
ZOBJECT.ZSTREAMNAME,
ZOBJECT.ZVALUESTRING
FROM ZOBJECT
WHERE ZSTREAMNAME IS "/app/usage"
ORDER BY ZSTREAMNAME
"""
res = cur.execute(q)
# one = res.fetchone()
# print(one.keys())
# print(one[:])
results = res.fetchall()
print(results[0].keys())
counter = Counter()
for row in results:
    print(row[:])
    counter[row['DAY OF WEEK']] += row['USAGE IN SECONDS']
for day in counter:
    seconds = counter[day]
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Total usage on {day}: {hours}h {minutes}m {seconds}s")
