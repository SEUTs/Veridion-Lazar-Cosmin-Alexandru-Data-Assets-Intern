import json

with open("results7.json", 'r') as f:
    dataset = json.load(f)
with open("results0.json", 'r') as f:
    ala_cu_greseli = json.load(f)

corecte = 0
evitate = 0

print("ACESTEA SUNT REZULTATELE CORECTE")
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
print(f"{corecte} VAT-uri corecte")
print(f"{evitate} VAT-uri gresite identificate")