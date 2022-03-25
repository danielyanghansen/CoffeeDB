 

# Delinnlevering 2: KaffeDB implementert i Python med bruk av sqlite3.

## Forfattere:
* Daniel Yang Hansen
* Patryk Kuklinski
* Erland Lie Amundgård

## Om oppgaven 
***Fra oppgavetekst:***\
Databaseapplikasjonen skal implementeres i Python basert på skjemaet fra første delinnlevering. De fem brukerhistoriene må være tilfredsstilt. Enkleste løsning er å lage et tekstbasert grensesnitt som kjører i et terminalvindu (eksempelvis cmd, bash, o.l.). Husk at poenget med oppgaven er å lage modeller, skrive SQL og gjøre databaseaksess fra Python. Følgende skal leveres:

* **a)** Python kildekode med SQL pakket i en zip-fil eller lignende. 
* **b)** Tekstlig beskrivelse som dokumenterer applikasjonen, levert som PDF. Dokumentasjonen må beskrive hvordan hver brukerhistorie er løst.
* **c)** Databasefilen til prosjektets SQLite-database. 
* **d)** De tekstlige resultatene fra brukerhistorienes spørringer.

Ettersom det er gjort noen små endringer i databasestrukturen siden deloppgave 1, skriver vi litt om dette i:

* **e)** Notat: Endringer fra forrige innlevering

Til slutt har vi en komplett utskrift av selve kjøringen i:

* **f)** Fullstendig output etter å ha kjørt KaffeDBUserStoryTests.py

# Svar deloppgave 2:
## a) Kildekode
Se vedlagt .zip-fil

## b) Hva applikasjonen inneholder
Applikasjonen inneholder følgende Python-filer:

* `KaffeDB.py`
* `KaffeDBTestInit.py`
* `KaffeDBUserStoryTests.py`

### KaffeDB:
Denne filen inneholder et bruker-objekt som instansieres når en bruker logger inn ved hjelp av en login-metode, og metoder for innsetting av data inn i de ulike tabellene
Hver innsettingsmetode er på samme format: koble til databasen, utføre en INSERT til tabellen metodenavnet referere til, committer og deretter stenger koblingen til databasen. Hvor nødvendig det er å stenge databasetilkoblingen og så koble opp til den igjen kan diskuteres. Siden vi jobber med sqlite på en lokal datamaskin, og at det bare er én som interagerer med databasen om gangen så har det kanskje ikke så mye å si. Når det kommer til web- eller klient/server applikasjoner er det kanskje greit å lukke koblingen rett etter den er brukt, for å ikke ta opp verdifull tilkoblingsplass

### KaffeDBTestInit:
Når denne filen kjøres vil innholdet i alle tabellene fjernes, auto-incrementen til nøkkeleverdiene settes tilbake til 1, og deretter fyller databasen med data i alle tabellene. Dataen generert er hovedsakelig bare for fyll, med unntak av noe informasjon som er nødvendig for å få noen resultater fra spørringene knyttet til flere av brukerhistoriene.

### KaffeDBUserStoryTests:
Denne filen er hvor brukerhistoriene blir testet. Måten de blir testet på er ved å utføre spørringene som er nødvendig for å få resultatene brukerhistoriene spør etter.
Før brukerhistorie-metodene blir kalt på vil alle tabellene og dens innhold printet ut til terminalen.

#### **Brukerhistorie 1:**
Brukerhistorien starter ved at man logger inn på en bruker (Her er brukeren Daniel Yang Hansen), som logges inn ved
```python
KaffeDB.login("danielyh@stud.ntnu.no", "passord123", UserState)
```
Med `login` som:
```python
def login(epost:str, passwd: str, UserState: User):
    try:
        con, cursor = open_connection()
        sql = """
        SELECT
            PK_BrukerID,
            Fornavn,
            Mellomnavn,
            Etternavn,
            Epost
        FROM Bruker
        WHERE 
            Epost = ? AND
            Passord = ?
        """
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
```
Vi simulerer dermed at brukeren ser listen av alle tilgjengelige kaffer, for så å legge på noen søkekrav:

* Navn: 'Vinterkaffe 2022'
* BrenneriNavn: 'Trondheims-brenneriet Jacobsen & Svart'
* Region: 'Santa Ana'
* Land: 'El Salvador'
* Brenningsdato: '2022.01.20'
* Brenningsgrad: 'Lys'

Vi leter da etter kaffen med å spørre:
```SQL
SELECT
        Kaffe.PK_KaffeID,
        Kaffe.Navn,
        Kaffe.Beskrivelse,
        Kaffe.Kilopris,
        Kaffe.Kilopris_Valuta,
        Brenning.Brenningsgrad,
        Brenning.Brenningsdato,
        Brenneri.BrenneriNavn,
        Kaffeparti.Betalt_Kg_Pris_Gård_USD,
        Kaffeparti.Innhøstingsår,
        Kaffeparti.FK_Foredlingsmetode,
        Kaffegård.Navn as "Gårdsnavn",
        Kaffegård.MOH,
        Lokasjon.Region,
        Lokasjon.Land,
        Kaffebønne.Variant || ' ' || Kaffebønne.Artsnavn AS Første_Kaffebønne,
        COUNT(KaffepartiJunction.FK_Kaffebønne) as "Antall_Bønnetyper"
    FROM
        Kaffe
        INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
        INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
        INNER JOIN Kaffeparti on Kaffe.FK_KaffeParti = Kaffeparti.PK_KaffeParti
        INNER JOIN Kaffegård ON Kaffeparti.FK_GårdID = Kaffegård.PK_GårdID
        INNER JOIN Lokasjon ON Kaffegård.FK_Lokasjon = Lokasjon.PK_Lokasjon
        INNER JOIN KaffepartiJunction ON Kaffeparti.PK_KaffeParti = KaffepartiJunction.FK_KaffeParti 
        INNER JOIN Kaffebønne ON KaffepartiJunction.FK_Kaffebønne = Kaffebønne.PK_Kaffebønne

    WHERE
        Kaffe.Navn = 'Vinterkaffe 2022' AND
        Brenneri.BrenneriNavn = 'Trondheims-brenneriet Jacobsen & Svart' AND
        Lokasjon.Region = 'Santa Ana' AND
        Lokasjon.Land = 'El Salvador' AND
        Brenning.Brenningsdato = '2022.01.20' AND
        Brenning.Brenningsgrad = 'Lys' 
    GROUP BY Kaffe.PK_KaffeID 
```
...Hvor brukeren "velger" / "trykker på" den kaffen de vil gi tilbakemelding for, som gir tilbake en PK for kaffen.\
Vi kaller dermed på funksjonen `create_coffee_tasting`:
```python
pk_coffee = res[0] #PK
today = datetime.today().strftime('%Y.%m.%d') #Dato idag
KaffeDB.create_coffee_tasting("Wow – en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!", 10, today ,UserState.PK, pk_coffee)
```
Hvor selve funksjonen er definert som:
```python
def create_coffee_tasting(tasting_note: str, score: int, tasting_time: str ,FK_Bruker_ID: int , FK_KaffeID: int ):
    con, cursor = open_connection()
    values = [tasting_note, score, tasting_time, FK_Bruker_ID, FK_KaffeID]
    sql = """INSERT INTO Kaffesmaking (Brukerens_Smaksnotater, Poeng, Smaksdato, FK_BrukerID, FK_KaffeID) VALUES ( ?, ?, ?, ?, ?)""" 
    cursor.execute(sql,values) #hjelpemetode
    close_and_commit_connection(con) #hjelpemetode
    
    return True
```

Til slutt ser vi på alle smakingene som er gjort (i en ganske detaljert spørring), for å kunne sjekke at kaffesmakingen har blitt laget ordentlig
```SQL
SELECT
    Kaffesmaking.PK_Kaffesmaking,
    Kaffesmaking.Poeng,
    Kaffesmaking.Brukerens_Smaksnotater,
    Kaffesmaking.Smaksdato,
    Bruker.Epost AS Smakende_Bruker,
    Kaffe.PK_KaffeID,
    Kaffe.Navn,
    Kaffe.Beskrivelse,
    Kaffe.Kilopris,
    Brenning.Brenningsgrad,
    Brenning.Brenningsdato,
    Brenneri.BrenneriNavn,
    Kaffeparti.Betalt_Kg_Pris_Gård_USD,
    Kaffeparti.Innhøstingsår,
    Kaffeparti.FK_Foredlingsmetode,
    Kaffegård.Navn as "Gårdsnavn",
    Kaffegård.MOH,
    Lokasjon.Region,
    Lokasjon.Land,
    Kaffebønne.Variant || ' ' || Kaffebønne.Artsnavn AS Første_Kaffebønne,
    COUNT(KaffepartiJunction.FK_Kaffebønne) as "Antall_Bønnetyper"
FROM
    Kaffesmaking
    INNER JOIN Kaffe ON Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
    INNER JOIN Bruker ON Kaffesmaking.FK_BrukerID = Bruker.PK_BrukerID
    INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
    INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
    INNER JOIN Kaffeparti on Kaffe.FK_KaffeParti = Kaffeparti.PK_KaffeParti
    INNER JOIN Kaffegård ON Kaffeparti.FK_GårdID = Kaffegård.PK_GårdID
    INNER JOIN Lokasjon ON Kaffegård.FK_Lokasjon = Lokasjon.PK_Lokasjon
    INNER JOIN KaffepartiJunction ON Kaffeparti.PK_KaffeParti = KaffepartiJunction.FK_KaffeParti 
    INNER JOIN Kaffebønne ON KaffepartiJunction.FK_Kaffebønne = Kaffebønne.PK_Kaffebønne
GROUP BY Kaffesmaking.PK_Kaffesmaking
ORDER BY Kaffesmaking.Smaksdato DESC
```

#### **Brukerhistorie 2:**
Kobler til databasen og utfører følgende spørring:

```SQL
SELECT 
    Bruker.Fornavn,
    Bruker.Etternavn,
    COUNT (DISTINCT (Kaffesmaking.FK_KaffeID)) as 'Antall forskjellige Kaffer'
FROM
    Kaffesmaking
    INNER JOIN Bruker ON Kaffesmaking.FK_BrukerID = Bruker.PK_BrukerID
    INNER JOIN Kaffe ON Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
WHERE Kaffesmaking.Smaksdato LIKE '2022%'
GROUP BY Kaffesmaking.FK_BrukerID
ORDER BY COUNT(Kaffesmaking.FK_KaffeID) DESC;
```

#### **Brukerhistorie 3:**
Kobler til databasen, og utfører følgende spørring: 
``` SQL
SELECT
    Brenneri.BrenneriNavn,
    Kaffe.Navn AS 'Kaffe navn',
    Kaffe.Kilopris,
    AVG(Kaffesmaking.Poeng) AS 'Gjennomsnittlig score',
    (AVG(Kaffesmaking.Poeng)/Kaffe.Kilopris) AS 'Mest Verdi for Pengene'
FROM Kaffesmaking
    INNER JOIN Kaffe ON Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
    INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning =Brenning.PK_Kaffebrenning
    INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
GROUP BY (Kaffe.PK_KaffeID)
ORDER BY (AVG(Kaffesmaking.Poeng)/Kaffe.Kilopris) DESC;

```

#### **Brukerhistorie 4:**
Kobler til databasen, og utfører følgende spørring:
``` SQL
SELECT 
    Kaffe.Navn AS KaffeNavn, 
    Brenneri.BrenneriNavn
FROM Kaffesmaking
    INNER JOIN Kaffe ON Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
    INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
    INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
WHERE 
    Kaffesmaking.Brukerens_Smaksnotater LIKE '%floral%' OR
    Kaffe.Beskrivelse LIKE '%floral%'
```

#### **Brukerhistorie 5:**
Kobler til databasen, og utfører følgende spørring:
```SQL
SELECT
    Brenneri.BrenneriNavn,
    Kaffe.Navn AS KaffeNavn
FROM 
    Kaffe
    INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
    INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
    INNER JOIN Kaffeparti ON Kaffe.FK_Kaffeparti = Kaffeparti.PK_Kaffepar	
    INNER JOIN Kaffegård ON Kaffeparti.FK_GårdID = Kaffegård.PK_GårdID
    INNER JOIN Lokasjon ON Kaffegård.FK_Lokasjon = Lokasjon.PK_Lokasjon
WHERE
  	Kaffeparti.FK_Foredlingsmetode != 'Vasket' AND
    (Lokasjon.Land = 'Rwanda' OR Lokasjon.Land = 'Colombia')
```

## c) Databasefilen til prosjektets SQLite-database
    Se vedlagt .zip-fil
    Databasefilen heter `KaffeDB.db`
## d) Tekstlige resultater fra brukerhistoriene
### **Brukerhistorie 1:**

For å finne riktig kaffe:
```

 (4, 'Vinterkaffe 2022', 'En velsmakende og kompleks kaffe for mørketiden', 600.0, 'NOK', 'Lys', '2022.01.20', 'Trondheims-brenneriet Jacobsen & Svart', 8.0, 2021, 'Vasket', 'Nombre de Dios', 1500, 'Santa Ana', 'El Salvador', 'Bourbon Arabica', 1) 
```
Logg av selve smakingen:
```
Tastings:
(6, 10, 'Wow – en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!', '2022.03.25', 'danielyh@stud.ntnu.no', 4, 'Vinterkaffe 2022', 'En velsmakende og kompleks kaffe for mørketiden', 600.0, 'Lys', '2022.01.20', 'Trondheims-brenneriet Jacobsen & Svart', 8.0, 2021, 'Vasket', 'Nombre de Dios', 1500, 'Santa Ana', 'El Salvador', 'Bourbon Arabica', 1)

...
...
```



### **Brukerhistorie 2:**
Brukeres Navn og Antall unike kaffer de har smakt på i løpet av 2022, med flest smakinger først:

```
('Erland', 'Amundgaard', 3)
('Daniel', 'Hansen', 2)
('Kari', 'Norkvinne', 1)
```

### **Brukerhistorie 3:**
Brennerinavn, kaffenavn, pris, gjennomsnittscore, og gjennomsnittscore/pris (som resultatet er sortert etter):

```
('Polar Kaffe', 'NamNam Kaffe', 15.0, 9.0, 0.6)
('Maridalen Brenneri', 'DiggDigg Kaffe', 24.99, 6.5, 0.2601040416166467)
('Isbjørn', 'Flower Power', 20.0, 2.0, 0.1)
('Kaffebrenneriet', 'Kaffe best', 19.0, 1.0, 0.05263157894736842)
('Trondheims-brenneriet Jacobsen & Svart', 'Vinterkaffe 2022', 600.0, 10.0, 0.016666666666666666)
```

### **Brukerhistorie 4:**
Alle kaffer som er beskrevet som 'floral' av enten et brenneri eller av en bruker:

```
('Flower Power', 'Isbjørn')
('Suavemente coffee', 'Kafeteros')
```

### **Brukerhistorie 5:**
Alle kaffer fra Rwanda eller Colombia som ikke er vasket:

```
('Polar Kaffe', 'Rwandan Gold')
('Kafeteros', 'Suavemente coffee')
```

## e) Notat: Endringer fra forrige innlevering
Vi fant ut at det var noen feil i forrige SQL-skript, i hovedsak mangel på referanser innad fremmednøkler (som gjør det vanskelig å kontrollere korrekt radinnsetting, og å gjennomføre CASCADING DELETE). Cascading så isåfall tas hensyn til i selve SQL spørringen. 
I kaffe-tabellen så vi det som hensiktsmessig å endre på Kilopris-feltet. Feltet var opprinnelig et felt av type text, som inneholdt både selve kiloprisen, og hvilken valuta den hører til. (F.eks. “150 NOK”). Nå har vi splittet det opp til to felt: Kilopris av typen Real, og Kilopris_Valuta av typen Text. Ingen av de kan være null.

### f) Fullstendig output etter å ha kjørt KaffeDBUserStoryTests.py


```                                        
    
=========Showing the contents of all tables:=========


Table Brenneri:
(1, 'Polar Kaffe')
(2, 'Isbjørn')
(3, 'Kafeteros')
(4, 'Kaffebrenneriet')
(5, 'Maridalen Brenneri')
(6, 'Solberg & Hansen')
(7, 'Talormade')
(8, 'Amundgård & Hansen & Kuklinski')
(9, 'Trondheims-brenneriet Jacobsen & Svart')


Table Brenning:
(1, 1, '2022.01.01', 'Mørk')
(2, 2, '2022.01.01', 'Lys')
(3, 3, '2022.01.02', 'Middels')
(4, 4, '2021.01.01', 'Mørk')
(5, 5, '2020.05.01', 'Mørk')
(6, 9, '2022.01.20', 'Lys')


Table Bruker:
(1, 'Daniel', 'Yang', 'Hansen', 'danielyh@stud.ntnu.no', 'passord123')
(2, 'Erland', 'Lie', 'Amundgaard', 'erlandla@stud.ntnu.no', 'passord321')
(3, 'Ola', '', 'Normann', 'olanormanntest@stud.ntnu.no', 'passord123')
(4, 'Kari', '', 'Norkvinne', 'karinorkvinnetest@stud.ntnu.no', 'passord123')


Table Foredlingsmetode:
('Bærtørket', 'They do be dry tho')
('Vasket', 'They do be clean tho')
('Honningmetoden', 'En blanding mellom bærtørket og vasket')
('Delvis_vasket', 'Både tørt og vått B)')


Table Kaffe:
(1, 'NamNam Kaffe', 'Smaker Nam', 15.0, 'USD', 1, 1)
(2, 'Kaffe best', 'Smaker best', 19.0, 'USD', 2, 4)
(3, 'DiggDigg Kaffe', 'Smaker digg', 24.99, 'USD', 3, 5)
(4, 'Vinterkaffe 2022', 'En velsmakende og kompleks kaffe for mørketiden', 600.0, 'NOK', 4, 6)
(5, 'Flower Power', 'A coffee with an amazing floral smell, while also tasting like fantastic coffee', 20.0, 'GBP', 4, 2)
(6, 'Rwandan Gold', 'A taste of gold from Rwanda. Now with washed beans', 61919.1, 'USD', 6, 3)
(7, 'Rwandan Gold', 'A taste of gold from Rwanda. Dried beans with the utmost care', 61919.1, 'USD', 7, 1)
(8, 'Suavemente coffee', 'Suavemente, bésame Que quiero sentir tus labios Besándome otra vez', 1500.0, 'USD', 9, 3)


Table Kaffebønne:
(1, 'Bourbon', 'Arabica')
(2, 'Bourbon', 'Robusta')
(3, 'Bourbon', 'Liberica')
(4, 'Kidney bean', 'Arabica')
(5, 'Black bean', 'Robusta')
(6, 'Monke', 'Liberica')
(7, 'Beanbaluba', 'Arabica')
(8, './bin', 'Robusta')
(9, 'Celmanide', 'Liberica')


Table Kaffegård:
(1, 'Gård1', 200, 1)
(2, 'Gård2', 1000, 4)
(3, 'Gård3', 500, 2)
(4, 'Gård4', 10, 11)
(5, 'Nombre de Dios', 1500, 13)
(6, 'Rwandan Bean Paradise', 700, 16)
(7, "Sorry I'm latte!", 1200, 18)
(8, "Coffee beans must have low self-esteem because they're always bean roasted", 2000, 17)
(9, 'I think I put too many beans in my eyes. In Heinz sight, it was a poor decision', 250, 17)
(10, "I've bean practicing jokes all day", 300, 15)
(11, 'Café literamente', 500, 19)
(12, 'Generic colombian coffee farm', 1100, 21)
(13, 'Paraíso de frijoles', 700, 22)
(14, 'Friojolitos', 300, 19)
(15, 'Café da las montañas colombianas', 2000, 21)
(16, 'Granja', 600, 23)


Table Kaffeparti:
(1, 13.2, 2015, 2, 'Vasket')
(2, 4.6, 1995, 3, 'Honningmetoden')
(3, 55.2, 2020, 4, 'Delvis_vasket')
(4, 8.0, 2021, 5, 'Vasket')
(5, 13.0, 2021, 6, 'Vasket')
(6, 12.0, 2020, 8, 'Vasket')
(7, 10.0, 2021, 10, 'Bærtørket')
(8, 8.0, 2022, 16, 'Vasket')
(9, 10.0, 2021, 14, 'Bærtørket')
(10, 9.0, 2021, 11, 'Delvis_vasket')


Table KaffepartiJunction:
(1, 1)
(1, 2)
(1, 3)
(1, 4)
(2, 2)
(2, 4)
(3, 4)
(3, 5)
(3, 6)
(4, 1)


Table Kaffesmaking:
(1, 'Å digg', 9, '2022.03.19', 2, 1)
(2, 'Litt for bitter', 5, '2022.02.28', 1, 3)
(3, 'Veldig god kaffe', 8, '2022.03.15', 2, 3)
(4, 'Smakte jord', 1, '2022.01.12', 4, 2)
(5, 'Det var kanskje en floral lukt, men smakte jord!', 2, '2022.03.15', 2, 5)
(6, 'Artig overraskelse med en såpass floral smak, det var interessant og ganske godt!', 6, '2022.03.15', 3, 8)


Table Lokasjon:
(1, 'Trøndelag', 'Norge')
(2, 'Troms og Finnmark', 'Norge')
(3, 'Nordland', 'Norge')
(4, 'Møre og Romsdal', 'Norge')
(5, 'Vestland', 'Norge')
(6, 'Rogaland', 'Norge')
(7, 'Oslo og Innlandet', 'Norge')
(8, 'Agder', 'Norge')
(9, 'Viken', 'Norge')
(10, 'Sogn og Fjordane', 'Norge')
(11, 'Batman', 'Tyrkia')
(12, 'Bosphorus Strait', 'Tyrkia')
(13, 'Santa Ana', 'El Salvador')
(14, 'Østprovinsen', 'Rwanda')
(15, 'Kigali', 'Rwanda')
(16, 'Nordprovinsen', 'Rwanda')
(17, 'Sørprovinsen', 'Rwanda')
(18, 'Vestprovinsen', 'Rwanda')
(19, 'Caribbean', 'Colombia')
(20, 'Pacific', 'Colombia')
(21, 'Orinoco', 'Colombia')
(22, 'Amazon', 'Colombia')
(23, 'Insular', 'Colombia')


Login into danielyh@stud.ntnu.no (Daniel Yang Hansen)
User story 1:
These are all the coffees:
(1, 'NamNam Kaffe', 'Smaker Nam', 15.0, 'USD', 'Mørk', '2022.01.01', 'Polar Kaffe', 13.2, 2015, 'Vasket', 'Gård2', 1000, 'Møre og Romsdal', 'Norge', 'Bourbon Arabica', 4)
(2, 'Kaffe best', 'Smaker best', 19.0, 'USD', 'Mørk', '2021.01.01', 'Kaffebrenneriet', 4.6, 1995, 'Honningmetoden', 'Gård3', 500, 'Troms og Finnmark', 'Norge', 'Bourbon Robusta', 2)
(3, 'DiggDigg Kaffe', 'Smaker digg', 24.99, 'USD', 'Mørk', '2020.05.01', 'Maridalen Brenneri', 55.2, 2020, 'Delvis_vasket', 'Gård4', 10, 'Batman', 'Tyrkia', 'Kidney bean Arabica', 3)
(4, 'Vinterkaffe 2022', 'En velsmakende og kompleks kaffe for mørketiden', 600.0, 'NOK', 'Lys', '2022.01.20', 'Trondheims-brenneriet Jacobsen & Svart', 8.0, 2021, 'Vasket', 'Nombre de Dios', 1500, 'Santa Ana', 'El Salvador', 'Bourbon Arabica', 1)
(5, 'Flower Power', 'A coffee with an amazing floral smell, while also tasting like fantastic coffee', 20.0, 'GBP', 'Lys', '2022.01.01', 'Isbjørn', 8.0, 2021, 'Vasket', 'Nombre de Dios', 1500, 'Santa Ana', 'El Salvador', 'Bourbon Arabica', 1)

        Assuming that the user has identified the correct coffee to select
        Trying again with restrictions: 
            Navn: 'Vinterkaffe 2022'
            BrenneriNavn: 'Trondheims-brenneriet Jacobsen & Svart'
            Region: 'Santa Ana'
            Land: 'El Salvador'
            Brenningsdato: '2022.01.20'
            Brenningsgrad: 'Lys'
        Which should be sufficient 
            
          
Running: 
 
    SELECT
        Kaffe.PK_KaffeID,
        Kaffe.Navn,
        Kaffe.Beskrivelse,
        Kaffe.Kilopris,
        Kaffe.Kilopris_Valuta,
        Brenning.Brenningsgrad,
        Brenning.Brenningsdato,
        Brenneri.BrenneriNavn,
        Kaffeparti.Betalt_Kg_Pris_Gård_USD,
        Kaffeparti.Innhøstingsår,
        Kaffeparti.FK_Foredlingsmetode,
        Kaffegård.Navn as "Gårdsnavn",
        Kaffegård.MOH,
        Lokasjon.Region,
        Lokasjon.Land,
        Kaffebønne.Variant || ' ' || Kaffebønne.Artsnavn AS Første_Kaffebønne,
        COUNT(KaffepartiJunction.FK_Kaffebønne) as "Antall_Bønnetyper"
    FROM
        Kaffe
        INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
        INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
        INNER JOIN Kaffeparti on Kaffe.FK_KaffeParti = Kaffeparti.PK_KaffeParti
        INNER JOIN Kaffegård ON Kaffeparti.FK_GårdID = Kaffegård.PK_GårdID
        INNER JOIN Lokasjon ON Kaffegård.FK_Lokasjon = Lokasjon.PK_Lokasjon
        INNER JOIN KaffepartiJunction ON Kaffeparti.PK_KaffeParti = KaffepartiJunction.FK_KaffeParti 
        INNER JOIN Kaffebønne ON KaffepartiJunction.FK_Kaffebønne = Kaffebønne.PK_Kaffebønne

    WHERE
        Kaffe.Navn = 'Vinterkaffe 2022' AND
        Brenneri.BrenneriNavn = 'Trondheims-brenneriet Jacobsen & Svart' AND
        Lokasjon.Region = 'Santa Ana' AND
        Lokasjon.Land = 'El Salvador' AND
        Brenning.Brenningsdato = '2022.01.20' AND
        Brenning.Brenningsgrad = 'Lys' 
    GROUP BY Kaffe.PK_KaffeID 

        
Found the coffee:
 (4, 'Vinterkaffe 2022', 'En velsmakende og kompleks kaffe for mørketiden', 600.0, 'NOK', 'Lys', '2022.01.20', 'Trondheims-brenneriet Jacobsen & Svart', 8.0, 2021, 'Vasket', 'Nombre de Dios', 1500, 'Santa Ana', 'El Salvador', 'Bourbon Arabica', 1) 

Creating tasting with description
Tastings:
(7, 10, 'Wow – en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!', '2022.03.25', 'danielyh@stud.ntnu.no', 4, 'Vinterkaffe 2022', 'En velsmakende og kompleks kaffe for mørketiden', 600.0, 'Lys', '2022.01.20', 'Trondheims-brenneriet Jacobsen & Svart', 8.0, 2021, 'Vasket', 'Nombre de Dios', 1500, 'Santa Ana', 'El Salvador', 'Bourbon Arabica', 1)
(1, 9, 'Å digg', '2022.03.19', 'erlandla@stud.ntnu.no', 1, 'NamNam Kaffe', 'Smaker Nam', 15.0, 'Mørk', '2022.01.01', 'Polar Kaffe', 13.2, 2015, 'Vasket', 'Gård2', 1000, 'Møre og Romsdal', 'Norge', 'Bourbon Arabica', 4)
(3, 8, 'Veldig god kaffe', '2022.03.15', 'erlandla@stud.ntnu.no', 3, 'DiggDigg Kaffe', 'Smaker digg', 24.99, 'Mørk', '2020.05.01', 'Maridalen Brenneri', 55.2, 2020, 'Delvis_vasket', 'Gård4', 10, 'Batman', 'Tyrkia', 'Kidney bean Arabica', 3)
(5, 2, 'Det var kanskje en floral lukt, men smakte jord!', '2022.03.15', 'erlandla@stud.ntnu.no', 5, 'Flower Power', 'A coffee with an amazing floral smell, while also tasting like fantastic coffee', 20.0, 'Lys', '2022.01.01', 'Isbjørn', 8.0, 2021, 'Vasket', 'Nombre de Dios', 1500, 'Santa Ana', 'El Salvador', 'Bourbon Arabica', 1)
(2, 5, 'Litt for bitter', '2022.02.28', 'danielyh@stud.ntnu.no', 3, 'DiggDigg Kaffe', 'Smaker digg', 24.99, 'Mørk', '2020.05.01', 'Maridalen Brenneri', 55.2, 2020, 'Delvis_vasket', 'Gård4', 10, 'Batman', 'Tyrkia', 'Kidney bean Arabica', 3)
(4, 1, 'Smakte jord', '2022.01.12', 'karinorkvinnetest@stud.ntnu.no', 2, 'Kaffe best', 'Smaker best', 19.0, 'Mørk', '2021.01.01', 'Kaffebrenneriet', 4.6, 1995, 'Honningmetoden', 'Gård3', 500, 'Troms og Finnmark', 'Norge', 'Bourbon Robusta', 2)
User story 1 complete
User story 2:

Query: 
    SELECT 
        Bruker.Fornavn , 
        Bruker.Etternavn, 
        COUNT(DISTINCT(Kaffesmaking.FK_KaffeID)) as 'Antall forskjellige Kaffer'
    FROM 
        Kaffesmaking
        INNER JOIN Bruker ON Kaffesmaking.FK_BrukerID = Bruker.PK_BrukerID 
        INNER JOIN Kaffe ON Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID 
    WHERE 
        Kaffesmaking.Smaksdato LIKE '2022%' 
    GROUP BY
        Kaffesmaking.FK_BrukerID
    ORDER BY
        COUNT(Kaffesmaking.FK_KaffeID) DESC;

    
List of users that have tasted distinct Coffee, sorted from most to least 
('Erland', 'Amundgaard', 3)
('Daniel', 'Hansen', 2)
('Kari', 'Norkvinne', 1)
('Ola', 'Normann', 1)
User story 3:

Query:
    SELECT 
        Brenneri.BrenneriNavn, 
        Kaffe.Navn AS 'Kaffe navn', 
        Kaffe.Kilopris, 
        AVG(Kaffesmaking.Poeng) AS 'Gjennomsnittlig score',
        (AVG(Kaffesmaking.Poeng)/Kaffe.Kilopris) AS 'Mest Verdi for Pengene'
    FROM Kaffesmaking
        INNER JOIN Kaffe ON Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
        INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
        INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
    GROUP BY (Kaffe.PK_KaffeID)
    ORDER BY (AVG(Kaffesmaking.Poeng)/Kaffe.Kilopris) DESC;
    
List of roasteries, coffees, price, average score from tastings, and average score from tastings divided by the coffees price, sorted 
('Polar Kaffe', 'NamNam Kaffe', 15.0, 9.0, 0.6)
('Maridalen Brenneri', 'DiggDigg Kaffe', 24.99, 6.5, 0.2601040416166467)
('Isbjørn', 'Flower Power', 20.0, 2.0, 0.1)
('Kaffebrenneriet', 'Kaffe best', 19.0, 1.0, 0.05263157894736842)
('Trondheims-brenneriet Jacobsen & Svart', 'Vinterkaffe 2022', 600.0, 10.0, 0.016666666666666666)
('Kafeteros', 'Suavemente coffee', 1500.0, 6.0, 0.004)
User story 4:

Query:
            SELECT Kaffe.Navn AS KaffeNavn, Brenneri.BrenneriNavn
            FROM Kaffesmaking
            INNER JOIN Kaffe ON Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
            INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
            INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
            WHERE 
                Kaffesmaking.Brukerens_Smaksnotater LIKE '%floral%' OR
                Kaffe.Beskrivelse LIKE '%floral%';
            
These are all the names of the coffees and 
roasteries where either the description of a coffee or a 
tasting note of a coffee describes it as 'floral':
('Flower Power', 'Isbjørn')
('Suavemente coffee', 'Kafeteros')
User story 5:

Query:
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
                    Lokasjon.Land = 'Colombia');
            

These are all the roasteries and coffees where the 
farm is either from Rwanda or Colombia while the 
coffee also wasn't processed using the washing method:
('Polar Kaffe', 'Rwandan Gold')
('Kafeteros', 'Suavemente coffee')
```
