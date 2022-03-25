BEGIN TRANSACTION; /*Bruker autogenererte/autoinkrementerte primærnøkler der det er mulig,
etter som vi ikke ser det relevant å basere det på allerede eksisterende systemer av unike nøkler*/
CREATE TABLE IF NOT EXISTS "Lokasjon" (
	"PK_Lokasjon"	INTEGER NOT NULL UNIQUE,
	"Region"	TEXT NOT NULL,
	"Land"	TEXT NOT NULL,
	PRIMARY KEY("PK_Lokasjon" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Kaffegård" (
	"PK_GårdID"	INTEGER NOT NULL UNIQUE,
	"Navn"	TEXT NOT NULL,
	"MOH"	INTEGER,
	"FK_Lokasjon"	INTEGER NOT NULL,
	PRIMARY KEY("PK_GårdID" AUTOINCREMENT)
	FOREIGN KEY("FK_Lokasjon") REFERENCES "Lokasjon"("PK_Lokasjon")
);
CREATE TABLE IF NOT EXISTS "Bruker" ( /*Forventer at ikke alle har mellomnavn, men ellers er alle andre felter hos en bruker obligatoriske */
	"PK_BrukerID"	INTEGER NOT NULL UNIQUE,
	"Fornavn"	TEXT NOT NULL,
	"Mellomnavn"	TEXT,
	"Etternavn"	TEXT NOT NULL,
	"Epost"	TEXT NOT NULL UNIQUE,
	"Passord"	TEXT NOT NULL,
	PRIMARY KEY("PK_BrukerID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Kaffebønne" (
	"PK_Kaffebønne"	INTEGER NOT NULL UNIQUE,
	"Variant"	TEXT NOT NULL,
	"Artsnavn"	TEXT NOT NULL,
	PRIMARY KEY("PK_Kaffebønne" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Foredlingsmetode" (
	"PK_ForedlingsmetodeNavn"	TEXT NOT NULL UNIQUE,
	"ForedlingsmetodeBeskrivelse"	TEXT NOT NULL,
	PRIMARY KEY("PK_ForedlingsmetodeNavn") /*Forventer aldri å ha to metoder med samme navn (som har ulik beskrivelse)*/
);
CREATE TABLE IF NOT EXISTS "Kaffeparti" (
	"PK_KaffeParti"	INTEGER NOT NULL UNIQUE,
	"Betalt_Kg_Pris_Gård_USD"	REAL NOT NULL,
	"Innhøstingsår"	INTEGER NOT NULL,
	"FK_GårdID"	INTEGER NOT NULL,
	"FK_Foredlingsmetode"	TEXT NOT NULL,
	FOREIGN KEY("FK_Foredlingsmetode") REFERENCES "Foredlingsmetode"("PK_ForedlingsmetodeNavn"),
	FOREIGN KEY("FK_GårdID") REFERENCES "Kaffegård"("PK_GårdID"),
	PRIMARY KEY("PK_KaffeParti" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "KaffepartiJunction" (
	"FK_KaffeParti"	INTEGER NOT NULL,
	"FK_Kaffebønne"	INTEGER NOT NULL,
	FOREIGN KEY("FK_Kaffebønne") REFERENCES "Kaffebønne"("PK_Kaffebønne"),
	FOREIGN KEY("FK_KaffeParti") REFERENCES "Kaffeparti"("PK_KaffeParti")
	/*Junction table burde ikke trenge Primary Key*/
);
CREATE TABLE IF NOT EXISTS "Brenneri" (
	"PK_BrenneriID"	INTEGER NOT NULL UNIQUE,
	"BrenneriNavn"	TEXT NOT NULL,
	PRIMARY KEY("PK_BrenneriID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Brenning" (
	"PK_Kaffebrenning"	INTEGER NOT NULL UNIQUE,
	"FK_BrenneriID"	INTEGER NOT NULL,
	"Brenningsdato"	TEXT NOT NULL,
	"Brenningsgrad"	TEXT NOT NULL,
	FOREIGN KEY("FK_BrenneriID") REFERENCES "Brenneri"("PK_BrenneriID"),
	PRIMARY KEY("PK_Kaffebrenning" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Kaffe" (
	"PK_KaffeID"	INTEGER NOT NULL UNIQUE,
	"Navn"	TEXT NOT NULL,
	"Beskrivelse"	TEXT, /*Tillater at det er tomme beskrivelser*/
	"Kilopris"	REAL NOT NULL,
	"Kilopris_Valuta"	TEXT NOT NULL,
	"FK_KaffeParti"	INTEGER NOT NULL,
	"FK_Kaffebrenning"	INTEGER NOT NULL,
	FOREIGN KEY("FK_Kaffebrenning") REFERENCES "Brenning"("PK_Kaffebrenning"),
	FOREIGN KEY("FK_KaffeParti") REFERENCES "Kaffeparti"("PK_KaffeParti"),
	PRIMARY KEY("PK_KaffeID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Kaffesmaking" (
	"PK_Kaffesmaking"	INTEGER NOT NULL UNIQUE,
	"Brukerens_Smaksnotater"	TEXT, /*Det skal være greit å ikke skrive noe kvalitativt, det holder med å gi en rating*/
	"Poeng"	INTEGER NOT NULL,
	"Smaksdato"	TEXT NOT NULL,
	"FK_BrukerID"	INTEGER NOT NULL,
	"FK_KaffeID"	INTEGER NOT NULL,
	FOREIGN KEY("FK_BrukerID") REFERENCES "Bruker"("PK_BrukerID"),
	FOREIGN KEY("FK_KaffeID") REFERENCES "Kaffe"("PK_KaffeID"),
	PRIMARY KEY("PK_Kaffesmaking" AUTOINCREMENT)
);
COMMIT;
