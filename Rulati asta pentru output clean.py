import json

# rezultatele gresite de mine si verificate prin HMRC sunt mai jos, in comentariu

with open("results7.json", 'r') as f:
    dataset = json.load(f)
with open("results0.json", 'r') as f:
    ala_cu_greseli = json.load(f)

corecte = 0
evitate = 0

print("ACESTEA SUNT REZULTATELE SALVATE CA FIIND CORECTE")
print(f"[[VAT 123, VAT GB123], certainty, instances] name")
for company in dataset:
    if dataset[company][0][0] != "":
        print(dataset[company], company)
        corecte += 1

print()
print("ACESTEA SUNT REZULTATELE INCORECTE CARE AU FOST FILTRATE")
for company in ala_cu_greseli:
    if dataset[company][0][0] == "" and ala_cu_greseli[company][0][0] != "":
        print(ala_cu_greseli[company], company)
        evitate += 1

print(f"{len(dataset)} de companii analizate")
print(f"{corecte} VAT-uri presupus corecte")
print(f"{evitate} VAT-uri presupus gresite")

print()
print("  In realitate:\n36/61 adevarat pozitive\n25/61 fals pozitive\n6/10 adevarat negative\n4/10 fals negative\n750/821 neidentificate")

"""
CORRECT NUMBERS MARKED AS WRONG:
[['653544628', ''], 1.0, 7] THE SOCIETY OF EDITORS
[['gb934179605', ''], 1.0, 6] THE SOFT WATER COMPANY (GB) LIMITED
[['674986271', ''], 1.0, 8] THE SOLDIERS, SAILORS, AIRMEN AND FAMILIES ASSOCIATION
[['gb325118430', ''], 1.0, 12] THE SOMERTON LIBRARY TRUST

WRONG NUMBERS MARKED AS CORRECT: 
[['592950700', ''], 1.0, 37] THE SOCIETY FOR THE EDUCATION OF THE DEAF
[['414350488', ''], 1.0, 14] THE SOCIETY OF ANTIQUARIES OF NEWCASTLE UPON TYN
[['659770483', ''], 1.0, 12] THE SOCIETY OF LOCAL AUTHORITY CHIEF EXECUTIVES
[['gb887474853', ''], 0.375, 48] THE SOCIETY OF MASTER SADDLERS (U.K.) LIMITED
[['488024668', ''], 1.0, 15] THE SOCIETY OF SPORTS THERAPISTS
[['293967539', ''], 1.0, 12] THE SOCIETY OF TEACHERS OF THE ALEXANDER TECHNIQUE
[['281765280', ''], 1.0, 29] THE SOFA SHOP INC LTD
[['gb154407423', ''], 1.0, 13] THE SOHAL REPAIRS LTD
DIMARK LTD si [['gb835713423', ''], 1.0, 15] THE SOHO SANDWICH COMPANY LTD (aceeasi adresa)
GEO-4D LIMITED si [['gb169044203', ''], 1.0, 20] THE SOLID BAR COMPANY LTD (aceeasi adresa)
[['496785415', ''], 1.0, 12] THE SOLITAIRE ASSET HOLDINGS LIMITED
OCMIS LTD si [['gb406792245', ''], 1.0, 20] THE SOMERSET CIDER BRANDY COMPANY LIMITED (vecini directi)
[['496785415', ''], 1.0, 12] THE SOMERSET COUNTY FEDERATION OF WOMEN'S INSTITUTES
[['gb371399079', ''], 1.0, 26] THE SOMERSET GAS CO. LIMITED
[['509397560', ''], 0.5769, 26] THE SOMERSET TOILETRY COMPANY LIMITED
[['134683994', ''], 1.0, 14] THE SOMERSETSHIRE COAL CANAL SOCIETY
KENT AUTO PANELS LTD si [['gb336047511', ''], 1.0, 57] THE SONGWRITING ACADEMY LIMITED (vecini directi))
97 FOXES LIMITED si [['gb189479925', ''], 0.5781, 128] THE SOUND BARN LIMITED (aceeasi adresa)
Fals pozitive

[['gb409020437', ''], 1.0, 20] THE SOCIAL GIRL LTD
[['gb292102037', ''], 0.5797, 138] THE SOCIETY OF WILL WRITERS (SERVICES) LIMITED
[['gb902151866', ''], 0.3333, 42] THE SOFTWARE FOR HEALTH FOUNDATION LIMITED
[['gb312372047', ''], 1.0, 61] THE SOFTWARE FOUNDRY LIMITED
Expirate

OPERAMATICS LIMITED si [['gb225431338', ''], 0.5849, 106] THE SOLAR BUREAU LTD (aceeasi adresa)
CAPITAL CONVERSIONS & CONSTRUCTION LTD si [['gb225628213', ''], 1.0, 72] THE SOLUTION ORGANISATION LIMITED (acelasi adresa)
DBR CONSULTANCY (DORSET) LTD si [['gb241232257', ''], 1.0, 76] THE SOLUTIONS CENTRE LIMITED (acelasi adresa)
Fals si expirat

Unde scrie Nume1 si [cod] Nume2, Nume1 = companie corecta, Nume2 = compania pentru care a detectat codul meu"""