DROP VIEW "main"."V_Full_Tasting_Description";
CREATE VIEW [V_Full_Tasting_Description] AS
SELECT
	Kaffesmaking.Poeng,
	Kaffesmaking.Brukerens_Smaksnotater,
	Kaffesmaking.Smaksdato,
	Bruker.Epost AS Smakende_Bruker,
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
;
DROP VIEW "main"."V_Full_Coffee_Description";
CREATE VIEW [V_Full_Coffee_Description] AS
SELECT
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
	Kaffe 
	INNER JOIN Brenning ON Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
	INNER JOIN Brenneri ON Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
	INNER JOIN Kaffeparti on Kaffe.FK_KaffeParti = Kaffeparti.PK_KaffeParti
	INNER JOIN Kaffegård ON Kaffeparti.FK_GårdID = Kaffegård.PK_GårdID
	INNER JOIN Lokasjon ON Kaffegård.FK_Lokasjon = Lokasjon.PK_Lokasjon
	INNER JOIN KaffepartiJunction ON Kaffeparti.PK_KaffeParti = KaffepartiJunction.FK_KaffeParti 
	INNER JOIN Kaffebønne ON KaffepartiJunction.FK_Kaffebønne = Kaffebønne.PK_Kaffebønne
GROUP BY PK_KaffeParti
;
DROP VIEW "main"."V_Coffe_By_Average_Score";
CREATE VIEW [V_Coffe_By_Average_Score] AS
SELECT
	Kaffesmaking.FK_KaffeID,
	AVG(Kaffesmaking.Poeng) as "gjsn_poeng",
	Kaffe.PK_KaffeID,
	Kaffe.Navn
FROM 
	Kaffesmaking
	INNER JOIN Kaffe on Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
GROUP BY Kaffesmaking.FK_KaffeID
ORDER BY "gjsn_poeng" DESC
;
DROP VIEW "main"."V_Roastery_By_Average_Score";
CREATE VIEW [V_Roastery_By_Average_Score] AS
SELECT
	Brenneri.PK_BrenneriID,
	Brenneri.BrenneriNavn,
	AVG(Kaffesmaking.Poeng) as "gjsn_poeng"
FROM 
	Kaffesmaking
	INNER JOIN Kaffe on Kaffesmaking.FK_KaffeID = Kaffe.PK_KaffeID
	INNER JOIN Brenning on Kaffe.FK_Kaffebrenning = Brenning.PK_Kaffebrenning
	INNER JOIN Brenneri on Brenning.FK_BrenneriID = Brenneri.PK_BrenneriID
GROUP BY Brenneri.PK_BrenneriID
ORDER BY "gjsn_poeng" DESC
;