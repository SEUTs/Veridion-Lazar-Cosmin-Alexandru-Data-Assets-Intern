import re

def modify(q: str) -> str:
    mappings = {
        '*': "&ast;",
        '\"': "&quot;",
        '/': "&sol;",
        '\\': "&bsol;",
        '<': "&lt;",
        '>': "&gt;",
        ':': "&colon;",
        '|': "&verbar;",
        '?': "&quest;"
    }
    modified_company_name = q
    for char in mappings:
        modified_company_name = modified_company_name.replace(char, mappings.get(char))
    return modified_company_name

ignored_suffixes = ["Co.", "Company", "Corp.", "Corporation", "Inc.", "Incorporated", "Limited", "Ltd.", "Ltd", "L.t.d.", "PLC", "Public Limited Company", "LLC", "L.L.C.", "Limited Liability Company", "LLP", "L.L.P.", "Limited Liability Partnership", "LP", "L.P.", "Limited Partnership", "PC", "P.C.", "Professional Corporation", "PLLC", "P.L.L.C.", "Professional Limited Liability Company", "PA", "P.A.", "Professional Association", "BC", "B.C.", "Benefit Corporation", "L3C", "Low-Profit Limited Liability Company", "Unlimited", "Ultd.", "Unltd.", "IBC", "International Business Company", "NV", "N.V.", "Naamloze Vennootschap", "BV", "B.V.", "Besloten Vennootschap", "GmbH", "Gesellschaft mit beschränkter Haftung", "AG", "Aktiengesellschaft", "SA", "S.A.", "Sociedad Anónima", "Société Anonyme", "Società Anonima", "SRL", "S.R.L.", "Società a responsabilità limitata", "Sociedad de Responsabilidad Limitada", "Société à Responsabilité Limitée", "SE", "Societas Europaea", "KK", "K.K.", "Kabushiki Kaisha", "GK", "Godo Kaisha", "AS", "A/S", "Aksjeselskap", "Aktieselskab", "AB", "Aktiebolag", "Oy", "Osakeyhtiö", "Sp. z o.o.", "Spółka z ograniczoną odpowiedzialnością", "S.A.S.", "Société par Actions Simplifiée", "OOO", "Obshchestvo s Ogranichennoy Otvetstvennostyu", "Pty Ltd", "Proprietary Limited", "Bhd", "Berhad", "Sdn Bhd", "Sendirian Berhad", "CIC", "Community Interest Company", "CIO", "Charitable Incorporated Organisation", "SC", "S.C.", "Societate Comercială", "Trust", "Association", "Club", "Foundation", "Society", "Syndicate", "Union"]
ignored_suffixes = [x.lower() for x in ignored_suffixes]
ignored_suffixes.sort(key=lambda s: -len(s))

def remove_suffixes(q: str) -> str:
    restart = True
    while restart:
        q = q.strip()
        restart = False
        for suffix in ignored_suffixes:
            # print(q + "|" + q[-len(suffix):].lower() + "|" + suffix + "|" + f"{q[-len(suffix):].lower() == suffix}")
            if len(q) > len(suffix) and q[-len(suffix):].lower() == suffix:
                q = q[:-len(suffix)]
                restart = True
    return q.strip()

if __name__ == "__main__":
    print(ignored_suffixes)