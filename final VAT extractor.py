import re
from bs4 import BeautifulSoup
from collections import Counter
import myModifier
import pandas as pd

verbose = True
increased_instances = True
check_for_publications = False
check_for_company_number = False

file_save_index = 0
if increased_instances:
    file_save_index += 1
if check_for_publications:
    file_save_index += 2
if check_for_company_number:
    file_save_index += 4

required_instances = 4
might_make_vat_wrong = []

if increased_instances:
    required_instances = 10
if check_for_publications:
    might_make_vat_wrong = ["library", "publication", "article", "book", "paper", "volume", "journal"]

def extractCodes(text_file: str, company_number: str) -> dict[str: int]:
    with open(f"company files/{text_file}", 'r', encoding="utf-8") as f:
        content = f.read()

    if verbose:
        print(f"{text_file}")
    if "Nu am găsit nici un rezultat pentru" in content:
        print("Degeaba1")
        print("\n\n")
        return {}
    if "Vezi rezultate pentru" in content:
        print("Degeaba2")
        print("\n\n")
        return {}
    
    soup = BeautifulSoup(content, "html.parser")
    
    # print(soup.get_text().lower().count("vat "))
    clean_text = soup.get_text(separator=" ", strip=True).lower()
    findings = re.finditer(r"vat\s", clean_text, flags=re.IGNORECASE)

    clear_codes = {}
    for finding in findings:
        canContainCode = clean_text[finding.start() : finding.end() + 150]
        found = ""
        # segments = re.split('[\s]+', canContainCode, re.M)
        for segment in canContainCode.split():
            if segment[0] != '\\' and (segment[2:-1].isnumeric() or segment[:-1].isnumeric()) and len(segment) > 2:
                found += segment
            
        if len(found) >= 9:
            found = re.sub(r'[^a-zA-Z0-9]', '', found)
            clear_codes.update({found: clear_codes.get(found, 0) + 1})

    # if text_file[0] == "m":
    #     with open("ceaidenumergi.txt", 'w', encoding="utf-8") as f:
    #         f.write(clean_text)
    pattern_with_letters = r"\b[A-Za-z](\s)*[A-Za-z](\d\s*){8}\d\b"
    pattern_without_letters = r"(?i)\b\d *\d *\d *\d *\d *\d *\d *\d *\d\b"
    
    map = {}
    perform_scan = True
    for item in might_make_vat_wrong:
        if item in text_file:
            perform_scan = False

    matches = re.finditer(pattern_without_letters, content)
    for m in matches:
        bad_match = False
        if perform_scan:
            area_around = content[max(0, m.start() - 200) : min(m.end() + 200, len(content))].lower()
            number_found = company_number in area_around if check_for_company_number else False

            # daca are numar langa, ignor. Daca nu are, caut
            if not number_found:
                for item in might_make_vat_wrong:
                    pattern = rf"\b{re.escape(item)}\b"
                    if re.search(pattern, area_around) is not None:
                        bad_match = True
                        break

        if not bad_match:
            map.update({m.end(): m.group()})

    matches = re.finditer(pattern_with_letters, content)
    for m in matches:
        bad_match = False
        if perform_scan:
            area_around = content[max(0, m.start() - 200) : min(m.end() + 200, len(content))].lower()
            number_found = company_number in area_around if check_for_company_number else False

            # daca are numar langa, ignor. Daca nu are, caut
            if not number_found:
                for item in might_make_vat_wrong:
                    pattern = rf"\b{re.escape(item)}\b"
                    if re.search(pattern, area_around) is not None:
                        bad_match = True
                        break

        if not bad_match:
            if m.group()[0:2].lower() in ["gb", "xi"]:
                map.update({m.end(): m.group().lower()})
    values = ["".join(x.split()) for x in map.values()]

    counter = Counter(values)
    counter_keys = sorted(counter, key=counter.get, reverse=True)

    could_be_vat = {}
    for e in counter_keys:
        if counter.get(e) < required_instances:
            break

        sum = int(e[-2:])
        for i in range(-9, -2):
            sum += (-i-1) * int(e[i])
        # print(sum, e, sum % 97)
        # 0 for the traditional method, 42 for the 9755 method
        if sum % 97 in [0, 42]: 
            could_be_vat.update({e: counter.get(e)})

    if verbose:
        print(f"Found after 'vat ': {clear_codes}")
        print(f"Could be vat: {could_be_vat}")
        print("\n\n")

    result = {}
    for code in clear_codes:
        for vat in could_be_vat:
            if code in vat:
                result.update({code: result.get(code, 0) + could_be_vat.get(vat)})

    result = dict(sorted(result.items(), key=lambda item: -item[1]))            
    return result

def getCodesAndConfidence(codes: dict[str: int]) -> tuple[list[str], float, int]:
    """ Returns a tuple containing the most common code
    (with and without country if found), the confidence
    score and the total number of codes found.
    
    Ex: (["232128892", "GB232128892"], 0.9545)
    
    If the number of instances required is not met, the output is (["", ""], 0, instances)
    """
    if len(codes) == 0:
        return (["", ""], 0, 0)
    
    digits_only = [re.sub(r'[^0-9]', '', code) for code in codes]
    total = sum(codes.values())
    digits_only_code = list(codes.keys())[0]
    country_code = ""
    # print(counter.total())
    for code in codes:
        if not code[0].isnumeric() and code[2:] == digits_only_code:
            country_code = code
    confidence_score = round(codes.get(digits_only_code) / total, 4)

    if codes.get(digits_only_code) > required_instances:
        return ([digits_only_code, country_code], confidence_score, total)
    return (["", ""], 0, total)

def extractForCompanies(company_names: list[str], company_numbers: list[str]) -> dict[str, tuple[list[str], float, int]]:
    result = {}
    print(len(company_names))
    for i in range(len(company_names)):
        if len(company_numbers) != len(company_names):
            codes = extractCodes(f"{company_names[i]}.html", "")
        else:
            codes = extractCodes(f"{company_names[i]}.html", company_numbers[i])
        print(i)

        output = getCodesAndConfidence(codes)
        result.update({company_names[i]: output})
    return result

import json
from pathlib import Path

if __name__ == "__main__":
    
# Specify the folder path
    folder_path = Path("company files")
    file_names = set([file.name[:-5] for file in folder_path.iterdir() if file.is_file()])

    company_names = []
    company_numbers = []
    # A fost prea mare sa il urc pe github. Este 7 part 7 din septembrie 2026.
    df = pd.read_csv("Companies House initial dataset.csv", low_memory=False)
    search_range = [0, 824]
    names = df.iloc[search_range[0]:search_range[1], 0]
    numbers = df.iloc[search_range[0]:search_range[1], 1]

    skipped = 0
    for i in range(len(names)):
        name = names[i]
        number = numbers[i]
        suffixless_name = myModifier.remove_suffixes(name)
        # if suffixless_name == "THE SOCIETY OF HOMEOPATHS":
        #     break
        if suffixless_name in file_names:
            company_names.append(suffixless_name)
            company_numbers.append(number)
        elif name in file_names:
            company_names.append(name)
            company_numbers.append(number)
        else:
            print("SKIPPED" + name)
            skipped += 1
    print(skipped)
    # print(company_names)

    # for number in numbers:
    #     company_numbers.append(number)

    to_search = [myModifier.modify(q) for q in company_names]
    
    result = extractForCompanies(to_search, company_numbers)
    with open(f"results{file_save_index}.json", 'w') as f:
        f.write(json.dumps(result, indent=4))

    for company in result:
        if result.get(company)[2] != 0:
            print(result.get(company), company)


# codes = extractCodes("the social group limited.txt")
# # for index, element in enumerate(found, start=1):
# #     print(f"Element #{index}: |{element}|")
# result = getCodesAndConfidence(codes)
# print(result)