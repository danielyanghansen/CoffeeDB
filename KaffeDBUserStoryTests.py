import KaffeDB
import sqlite3
import time
import logging
from datetime import datetime

def displayAllTables():
    con = sqlite3.connect("./KaffeDB.db")
    cursor = con.cursor()

    ##Cleanup: Remove old data
    tables = ["Brenneri", "Brenning", "Bruker", "Foredlingsmetode", "Kaffe", "Kaffebønne", "Kaffegård", "Kaffeparti", "KaffepartiJunction", "Kaffesmaking", "Lokasjon"]
    print("=========Showing the contents of all tables:=========\n\n")
    for table in tables:
        print("Table %s:" %table)
        logging.info("Table %s:" %table)
        
        cursor.execute("SELECT * FROM %s" %table)
        tableinfo = cursor.fetchall()
        for field in tableinfo:
            print(field)
            logging.info(field)
        
        con.commit()
        print("\n")
    con.close()

def userStory1(UserState: KaffeDB.User):
    """"
    En bruker smaker kaffen Vinterkaffe 2022 fra Trondheims-brenneriet
    Jacobsen & Svart (brent 20.01.2022), gir den 10 poeng og skriver «Wow
    – en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!». Kaffen er lysbrent, bærtørket Bourbon (c. arabica), kommer fra gården
    Nombre de Dios (1500 moh.) i Santa Ana, El Salvador, har en kilopris
    på 600 kr og er ifølge brenneriet «En velsmakende og kompleks kaffe for
    mørketiden». Kaffen ble høstet i 2021 og gården fikk utbetalt 8 USD
    per kg kaffe. Input fra brukerens side er brenneri, kaffenavn, poeng og
    smaksnotat.
    """
    print("User story 1:")
    print("These are all the coffees:")
    
    con = sqlite3.connect("./KaffeDB.db")
    cursor = con.cursor()
    
    cursor.execute("""SELECT * FROM V_Full_Coffee_Description""")
    res = cursor.fetchall()
    for field in res:
        print(field)
        
    print("""
          Trying again with restrictions: 
            Navn: 'Vinterkaffe 2022'
            BrenneriNavn: 'Trondheims-brenneriet Jacobsen & Svart'
            Region: 'Santa Ana'
            Land: 'El Salvador'
            Brenningsdato: '2022.01.20'
            Brenningsgrad: 'lys'
        Which should be sufficient 
            
          """)
    sql = """
            SELECT * FROM V_Full_Coffee_Description 
                WHERE
                    Navn = 'Vinterkaffe 2022' AND
                    BrenneriNavn = 'Trondheims-brenneriet Jacobsen & Svart' AND
                    Region = 'Santa Ana' AND
                    Land = 'El Salvador' AND
                    Brenningsdato = '2022.01.20' AND
                    Brenningsgrad = 'Lys'       
            """
    print("Running: \n", sql)
    cursor.execute(sql)
    res = cursor.fetchone()
    con.close()
    
    pk_coffee = res[0]
    today = datetime.today().strftime('%Y.%m.%d')
    print("Found the coffee:\n", res, "\n")
    print("Creating tasting with description")
    KaffeDB.create_coffee_tasting("Wow – en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!", 10, today ,UserState.PK, pk_coffee)
    
    con2 = sqlite3.connect("./KaffeDB.db")
    cursor2 = con2.cursor()
    
    cursor2.execute("""SELECT * FROM V_Full_Tasting_Description ORDER BY Smaksdato Desc""")
    res2 = cursor2.fetchall()
    print("Tastings:")
    for field in res2:
        print(field)
        
    con2.close()    
        
    print("User story 1 complete")
    
def userStory2():
    print("User story 2:")
    """
    En bruker skal kunne få skrevet ut en liste over hvilke brukere som
    har smakt flest unike kaffer så langt i år, sortert synkende. Listen skal
    inneholde brukernes fulle navn og antallet kaffer de har smakt.
    """
    # TODO

def userStory3():
    print("User story 3:")
    """
    En skal kunne se hvilke kaffer som gir forbrukeren mest for pengene
    ifølge KaffeDBs brukere (høyeste gjennomsnittsscore kontra pris), sortert synkende. 
    Listen skal inneholde brennerinavn, kaffenavn, pris og
    gjennomsnittsscore for hver kaffe.
    """
    # TODO

def userStory4():
    print("User story 4:")
    """
    En bruker søker etter kaffer som er blitt beskrevet med ordet «floral»,
    enten av brukere eller brennerier. Brukeren skal få tilbake en liste med
    brennerinavn og kaffenavn.
    """

    con = sqlite3.connect("./KaffeDB.db")
    cursor = con.cursor()

    query = """
            SELECT Kaffe.Navn AS KaffeNavn, Brenneri.BrenneriNavn
            FROM Kaffesmaking
            INNER JOIN Kaffe ON Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
            INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
            INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
            WHERE 
                Kaffesmaking.Brukerens_Smaksnotater LIKE '%floral%' OR
                Kaffe.Beskrivelse LIKE '%floral'
            """
    print("\nQuery:" + query)

    print("""These are all the names of the coffees and 
roasteries where either the description of a coffee or a 
tasting note of a coffee describes it as 'floral':""")

    cursor.execute(query)

    coffees_with_matching_note_or_desc = cursor.fetchall()
    for coffee in coffees_with_matching_note_or_desc:
        print(coffee)

    con.close()

def userStory5():
    print("User story 5:")
    """
    En annen bruker er lei av å bli skuffet av vaskede kaffer og deres tidvis kjedelige smak, 
    og ønsker derfor å søke etter kaffer fra Rwanda
    og Colombia som ikke er vaskede. Systemet returnerer en liste over
    brennerinavn og kaffenavn.
    """

    con = sqlite3.connect("./KaffeDB.db")
    cursor = con.cursor()

    query = """
                SELECT Brenneri.BrenneriNavn, Kaffe.Navn AS KaffeNavn
                FROM Kaffe
                INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
                INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
                INNER JOIN Kaffeparti ON Kaffe.FK_Kaffeparti = Kaffeparti.PK_Kaffeparti
                INNER JOIN Kaffegård ON Kaffeparti.FK_GårdID = Kaffegård.PK_GårdID
                INNER JOIN Lokasjon ON Kaffegård.FK_Lokasjon = Lokasjon.PK_Lokasjon
                WHERE
                    Kaffeparti.FK_Foredlingsmetode != 'Vasket' AND
                    (Lokasjon.Land = 'Rwanda' OR 
                    Lokasjon.Land = 'Colombia')
            """

    print("\nQuery:" + query)

    print("""
These are all the roasteries and coffees where the 
farm is either from Rwanda or Colombia while the 
coffee also wasn't processed using the washing method:""")

    cursor.execute(query)

    coffeeFromColombiaRwandaNoWashed = cursor.fetchall()
    for coffee in coffeeFromColombiaRwandaNoWashed:
        print(coffee)

    con.close()

def main():
    UserState = KaffeDB.User(0, "", "", "", "")
    
    displayAllTables()
    time.sleep(1.0)
    
    print("Login into danielyh@stud.ntnu.no (Daniel Yang Hansen)")
    time.sleep(0.5)
    KaffeDB.login("danielyh@stud.ntnu.no", "passord123", UserState)
    
    #userStory1(UserState)

    time.sleep(0.2)

    #userStory2()

    time.sleep(0.2)

    #userStory3()    

    time.sleep(0.2)

    userStory4()    

    time.sleep(0.2)

    userStory5()    
    
    
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("LOG START")
    
    print("Starting user story tests:\n\n")
    main()
    
    logging.info("LOG END")
    