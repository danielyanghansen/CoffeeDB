from contextlib import nullcontext
from inspect import _void
from multiprocessing.dummy.connection import Connection
from os import curdir
from select import select
#from tokenize import str
import sqlite3;
import KaffeDB;

def main():
    con = sqlite3.connect("./KaffeDB.db")
    cursor = con.cursor()

    ##Cleanup: Remove old data
    tables = ["Brenneri", "Brenning", "Bruker", "Foredlingsmetode", "Kaffe", "Kaffebønne", "Kaffegård", "Kaffeparti", "KaffepartiJunction", "Kaffesmaking", "Lokasjon"]
    cursor.execute("DELETE FROM sqlite_sequence") #reset all autoincrement
    con.commit()

    for table in tables:
        print("Wiping %s" %table)
        
        cursor.execute("DELETE FROM %s" %table)

        con.commit()
        print("Complete")
    con.close()


    # Brukere
    KaffeDB.create_user("Daniel", "Hansen", "danielyh@stud.ntnu.no", "passord123", "Yang") #PK 1
    KaffeDB.create_user("Erland", "Amundgaard", "erlandla@stud.ntnu.no", "passord321", "Lie") #PK 2
    KaffeDB.create_user("Ola", "Normann", "olanormanntest@stud.ntnu.no", "passord123", "") #PK 3
    KaffeDB.create_user("Kari", "Norkvinne", "karinorkvinnetest@stud.ntnu.no", "passord123", "") #PK 4

    # Lokasjon 
    KaffeDB.create_location("Trøndelag", "Norge") #PK 1
    KaffeDB.create_location("Troms og Finnmark", "Norge") #PK 2
    KaffeDB.create_location("Nordland", "Norge") #PK 3
    KaffeDB.create_location("Møre og Romsdal", "Norge") #PK 4
    KaffeDB.create_location("Vestland", "Norge") #PK 5
    KaffeDB.create_location("Rogaland", "Norge") #PK 6
    KaffeDB.create_location("Oslo og Innlandet", "Norge")
    KaffeDB.create_location("Agder", "Norge")
    KaffeDB.create_location("Viken", "Norge")
    KaffeDB.create_location("Sogn og Fjordane", "Norge")
    KaffeDB.create_location("Batman", "Tyrkia")
    KaffeDB.create_location("Bosphorus Strait", "Tyrkia") #PK 12
    KaffeDB.create_location("Santa Ana", "El Salvador")
    KaffeDB.create_location("Østprovinsen", "Rwanda") #PK 14
    KaffeDB.create_location("Kigali", "Rwanda") #PK 15
    KaffeDB.create_location("Nordprovinsen", "Rwanda") #16 
    KaffeDB.create_location("Sørprovinsen", "Rwanda") #17
    KaffeDB.create_location("Vestprovinsen", "Rwanda") #18
    KaffeDB.create_location("Caribbean", "Colombia") #19
    KaffeDB.create_location("Pacific", "Colombia") #20
    KaffeDB.create_location("Orinoco", "Colombia") #21 
    KaffeDB.create_location("Amazon", "Colombia") #22
    KaffeDB.create_location("Insular", "Colombia") #23

    # Gård 👩‍🌾
    KaffeDB.create_coffee_farm("Gård1", 200, 1) #PK 1
    KaffeDB.create_coffee_farm("Gård2", 1000, 4)
    KaffeDB.create_coffee_farm("Gård3", 500, 2)
    KaffeDB.create_coffee_farm("Gård4", 10, 11) #PK 4
    KaffeDB.create_coffee_farm("Nombre de Dios", 1500, 13) #On location 13: Santa Ana - El Salvador
    # Gårder fra Rwanda:
    KaffeDB.create_coffee_farm("Rwandan Bean Paradise", 700, 16) #PK 6
    KaffeDB.create_coffee_farm("Sorry I'm latte!", 1200, 18)
    KaffeDB.create_coffee_farm("Coffee beans must have low self-esteem because they're always bean roasted", 2000, 17)
    KaffeDB.create_coffee_farm("I think I put too many beans in my eyes. In Heinz sight, it was a poor decision", 250, 17)
    KaffeDB.create_coffee_farm("I've bean practicing jokes all day", 300, 15) #PK 10
    # Colombianske gårder:
    KaffeDB.create_coffee_farm("Café literamente", 500, 19) #PK 11
    KaffeDB.create_coffee_farm("Generic colombian coffee farm", 1100, 21)
    KaffeDB.create_coffee_farm("Paraíso de frijoles", 700, 22)
    KaffeDB.create_coffee_farm("Friojolitos", 300, 19)
    KaffeDB.create_coffee_farm("Café da las montañas colombianas", 2000, 21)
    KaffeDB.create_coffee_farm("Granja", 600, 23) #PK 16

    # Bønne
    KaffeDB.create_coffee_bean("Bourbon", "Arabica") #PK 1
    KaffeDB.create_coffee_bean("Bourbon", "Robusta")
    KaffeDB.create_coffee_bean("Bourbon", "Liberica")
    KaffeDB.create_coffee_bean("Kidney bean", "Arabica")
    KaffeDB.create_coffee_bean("Black bean", "Robusta")
    KaffeDB.create_coffee_bean("Monke", "Liberica") #PK 6
    KaffeDB.create_coffee_bean("Beanbaluba", "Arabica") #PK 1
    KaffeDB.create_coffee_bean("./bin", "Robusta")
    KaffeDB.create_coffee_bean("Celmanide", "Liberica")

    # Foredlingsmetode
    KaffeDB.create_processingmethod("Bærtørket", "They do be dry tho") #PK Bærtørket
    KaffeDB.create_processingmethod("Vasket", "They do be clean tho")
    KaffeDB.create_processingmethod("Honningmetoden", "En blanding mellom bærtørket og vasket")
    KaffeDB.create_processingmethod("Delvis_vasket", "Både tørt og vått B)") #PK Delvis_vasket

    # Brenneri 🏭
    KaffeDB.create_roastery("Polar Kaffe") #PK 1
    KaffeDB.create_roastery("Isbjørn")
    KaffeDB.create_roastery("Kafeteros")
    KaffeDB.create_roastery("Kaffebrenneriet") #PK 4
    KaffeDB.create_roastery("Maridalen Brenneri")
    KaffeDB.create_roastery("Solberg & Hansen")
    KaffeDB.create_roastery("Talormade")
    KaffeDB.create_roastery("Amundgård & Hansen & Kuklinski") #PK 8
    KaffeDB.create_roastery("Trondheims-brenneriet Jacobsen & Svart")

    # Brenning 🔥
    KaffeDB.create_roasting(1, "2022.01.01", "Mørk") #PK 1
    KaffeDB.create_roasting(2, "2022.01.01", "Lys")
    KaffeDB.create_roasting(3, "2022.01.02", "Middels")
    KaffeDB.create_roasting(4, "2021.01.01", "Mørk")
    KaffeDB.create_roasting(5, "2020.05.01", "Mørk") #PK 5
    KaffeDB.create_roasting(9, "2022.01.20", "Lys") #Brenning gjort av Jacobsen & Svart

    # Kaffeparti bag
    KaffeDB.create_coffee_batch(13.2 ,2015, 2, "Vasket") #PK 1
    KaffeDB.create_coffee_batch(4.6,1995,3, "Honningmetoden" )
    KaffeDB.create_coffee_batch(55.2, 2020,4, "Delvis_vasket") #PK 3
    KaffeDB.create_coffee_batch(8.0, 2021, 5, "Vasket") # " Kaffen ble høstet i 2021 og gården (Nombre de Dios) fikk utbetalt 8 USD per kg kaffe"
    # Partier fra Colobmia eller Rwanda
    KaffeDB.create_coffee_batch(13, 2021, 6, "Vasket")
    KaffeDB.create_coffee_batch(12, 2020, 8, "Vasket")
    KaffeDB.create_coffee_batch(10, 2021, 10, "Bærtørket")
    KaffeDB.create_coffee_batch(8, 2022, 16, "Vasket")
    KaffeDB.create_coffee_batch(10, 2021, 14, "Bærtørket")
    KaffeDB.create_coffee_batch(9, 2021, 11, "Delvis_vasket")

    #Binde bønner til parti
    beanlist1 = [1, 2, 3, 4]
    beanlist2 = [2, 4]
    beanlist3 = [4, 5, 6]
    KaffeDB.bind_beans_to_batch(1, beanlist1) #Ingen PK 
    KaffeDB.bind_beans_to_batch(2, beanlist2)
    KaffeDB.bind_beans_to_batch(3, beanlist3)
    KaffeDB.bind_beans_to_batch(4, [1]) #Only Bourbon Arabica is used

    # Kaffe ☕☕
    KaffeDB.create_coffee("NamNam Kaffe", "Smaker Nam", "15 USD", 1, 1) #PK 1
    KaffeDB.create_coffee("Kaffe best", "Smaker best", "19 USD", 2, 4)
    KaffeDB.create_coffee("DiggDigg Kaffe", "Smaker digg", "24.99 USD", 3, 5) #PK 3
    KaffeDB.create_coffee("Vinterkaffe 2022", "En velsmakende og kompleks kaffe for mørketiden", "600.0 NOK", 4, 6)

    # Kaffesmaking
    KaffeDB.create_coffee_tasting("Å digg", 9, "2022.03.19", 2, 1) #PK 1
    KaffeDB.create_coffee_tasting("Litt for bitter", 5, "2022.02.28", 1, 3)
    KaffeDB.create_coffee_tasting("Veldig god kaffe", 8, "2022.03.15", 2, 3)
    KaffeDB.create_coffee_tasting("Smakte jord", 1, "2022.01.12", 4, 2) #PK 4

if __name__ == "__main__":
    print("Starting setup...\n")
    main()
    print("\n...Setup complete\n")