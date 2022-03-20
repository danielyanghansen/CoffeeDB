from multiprocessing.dummy.connection import Connection

#from tokenize import str
import sqlite3


class User:
    def __init__(self, PK, first_name, middle_name, last_name, email):
        self.PK = PK
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        
        #default not logged in
        self.loginStatus = False
        
    def fullinfo(self):
        print("PK: {key}\nFull Name: {first} {second} {last}\nEmail: {mail}".format(key = self.PK, first = self.first_name, second=self.middle_name, last=self.last_name, mail=self.email ))
        
    def printMyTastings(self):
        return
 
 
    

#==============HELPER METHODS==============
def open_connection():
    con = sqlite3.connect("./KaffeDB.db")
    cursor = con.cursor()
    return con, cursor

def close_and_commit_connection(con :Connection):
    if (con):
        con.commit()
        con.close()

#con.execute("...") to get stuff
#con.close after
#Example safe syntax: cursor.execute("SELECT * FROM person WHERE navn = :navn", {"navn" = navn})

def check_available_email(email:str) -> bool:
    """
    Checks if there exists no email in the database with the given string.

    Parameter:
        email (str): the email addresse you want to check.

    Returns:
        True if no email of the given string exists, false otherwise.
    """
    con, cursor = open_connection()
    values = [email]
    sql = "SELECT Epost FROM Bruker WHERE (Epost = ?)"
       
    cursor.execute(sql, values)
    epost = cursor.fetchone()
    close_and_commit_connection(con)
    if (epost == None):
        return True
    return False

def create_user(first_name: str, last_name: str, email: str, password: str, middle_name:str=None):
    """
    Creates a user in the user table Bruker.
    
    Parameeters:
        first_name (str): the first name of the user.
        last_name (str): the last name of the user.
        email (str): the email address of the user.
        password (str): the password.
        middle_name (str) (OPTIONAL): the middle name of the user.

    Returns:
        [True if successful?] //TODO
    """
    
    values = [first_name, middle_name, last_name, email, password]
    sql = """ INSERT INTO Bruker (Fornavn, Mellomnavn, Etternavn, Epost, Passord) VALUES (?, ?, ?, ?, ?) """
    con, cursor = open_connection()
    cursor.execute(sql, values)
    close_and_commit_connection(con)

    return True

def create_location(region: str, country: str):
    """
    Creates a location in the location table Lokasjon.
    
    Parameters:
        region (str): the region 
        country (str): the country
        
    Returns:
        True if successfully created.
    """
    
    values = [region, country]
    sql = """ INSERT INTO Lokasjon (Region, Land) VALUES (?, ?) """
    con, cursor = open_connection()
    cursor.execute(sql, values)
    close_and_commit_connection(con)
    
    return True

def create_coffee_farm(name: str, moh: int, FK_location: int):
    values = [name, moh, FK_location]
    sql = """ INSERT INTO Kaffegård (Navn, MOH, FK_Lokasjon) VALUES (?, ?, ?) """
    con, cursor = open_connection()
    cursor.execute(sql, values)
    close_and_commit_connection(con)

    return True

def create_processingmethod(name: str, description: str):
    values = [name, description]
    sql = """ INSERT INTO Foredlingsmetode (PK_ForedlingsmetodeNavn, ForedlingsmetodeBeskrivelse) VALUES (?, ?) """
    con, cursor = open_connection()
    cursor.execute(sql, values)
    close_and_commit_connection(con)

    return True        

def create_coffee_batch(paid_usd: float, harvest_year: int, FK_farm: int, FK_processing_method: str):
    values = [paid_usd, harvest_year, FK_farm, FK_processing_method]
    sql = """ INSERT INTO Kaffeparti (Betalt_Kg_Pris_Gård_USD, Innhøstingsår, FK_GårdID, FK_Foredlingsmetode) VALUES (?, ?, ?, ?) """
    con, cursor = open_connection()
    cursor.execute(sql, values)
    close_and_commit_connection(con)
    
    return True

def create_roastery(name: str):
    con, cursor = open_connection()
    values = [name]
    sql = """ INSERT INTO Brenneri (BrenneriNavn) VALUES (?) """
    cursor.execute(sql,values)
    close_and_commit_connection(con)

    return True

def create_roasting(FK_roastery: int, roast_date: str, roast_deg: str):
    con, cursor = open_connection()
    values = [FK_roastery, roast_date, roast_deg]
    sql = """INSERT INTO Brenning (FK_BrenneriID, Brenningsdato, Brenningsgrad) VALUES (?, ?, ?)"""
    cursor.execute(sql, values)
    close_and_commit_connection(con)

    return True

def create_coffee_bean(variant: str, species: str):
    """
    Creates a coffee bean in the table Kaffebønne.
    
    Parameeters:
        variant (str): the variant of the bean.
        species (str): the species of the bean.

    Returns:
        [True if successful?] //
    """
    con, cursor = open_connection()
    values = [variant, species]
    sql = """INSERT INTO Kaffebønne (Variant, Artsnavn) VALUES (?, ?)"""
    cursor.execute(sql, values)
    close_and_commit_connection(con)
        
    return True
    
def create_coffee_tasting(tasting_note: str, score: int, tasting_time: str ,FK_Bruker_ID: int , FK_KaffeID: int ):
    con, cursor = open_connection()
    values = [tasting_note, score, tasting_time, FK_Bruker_ID, FK_KaffeID]
    sql = """ INSERT INTO Kaffesmaking (Brukerens_Smaksnotater, Poeng, Smaksdato, FK_BrukerID, FK_KaffeID) VALUES ( ?, ?, ?, ?, ?) """ 
    cursor.execute(sql,values)
    close_and_commit_connection(con)
    
    return True

def bind_beans_to_batch(FK_Batch, list_FK_bean):
    con, cursor = open_connection()
    for FK_bean in list_FK_bean:
        sql = """INSERT INTO KaffePartiJunction (FK_KaffeParti, FK_Kaffebønne) VALUES ( ? , ? )"""
        values = [FK_Batch, FK_bean]
        cursor.execute(sql, values)
    close_and_commit_connection(con)
    return True

def create_coffee(name:str, description : str, kg_price: str, FK_CoffeeBatchID : int, FK_Coffeeroasting: int):
    con, cursor = open_connection()
    values = [name, description, kg_price, FK_CoffeeBatchID, FK_Coffeeroasting]
    sql = """ INSERT INTO Kaffe (Navn, Beskrivelse, Kilopris, FK_KaffeParti, FK_Kaffebrenning) VALUES (?, ?, ?, ?, ?) """
    cursor.execute(sql,values)
    close_and_commit_connection(con)
    
    return True
     

def test():
    con, cursor = open_connection()
    #cursor = open_connection()
    print("cursor working")
    cursor.execute("""INSERT INTO Kaffegård (Navn, MOH, FK_Lokasjon)
                VALUES ('TestNavn', '150', '12123')""")
    close_and_commit_connection(con)
    
def login(epost:str, passwd: str, UserState: User):
    try:
        con, cursor = open_connection()
        sql = """SELECT PK_BrukerID, Fornavn, Mellomnavn, Etternavn, Epost from Bruker WHERE Epost = ? AND Passord = ?"""
        cursor.execute(sql, [epost, passwd])
        user = cursor.fetchone()
        
        con.close()
        
        UserState.PK = user[0]
        UserState.first_name = user[1]
        UserState.middle_name = user[2]
        UserState.last_name = user[3]
        UserState.email = user[4]
        return True
    except:
       print("Error While Logging In...\n")
       return False
    

def main():
    print("Welcome to KaffeDB")
    access_string = ""
    while (access_string != "l" or access_string != "r" or access_string != "a" or access_string != "e"):
        access_string = input("""
            Here are are your options:
            l:    login
            r:    register new user
            a:    access public info about Coffee
            e:    exit
            """)
        
    
    s = ""
    while (s != exit):
        s = input("\n")

if __name__ == "__main__":
    main()