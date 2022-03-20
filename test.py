from contextlib import nullcontext
from inspect import _void
from select import select
#from tokenize import str
import sqlite3;
import KaffeDB

print("Hello")

con = sqlite3.connect("./KaffeDB.db")
cursor = con.cursor()

"""

args = ("Batman", "Tyrkia")

malargs = ("');DROP TABLE Lokasjon;--", "B")

qry = "INSERT INTO Lokasjon (Region, Land) VALUES ( ?,  ? )"

cursor.execute(qry, args)
"""


KaffeDB.create_coffee_farm("TestFarm1234", 1234, 1)

con.commit()
con.close()