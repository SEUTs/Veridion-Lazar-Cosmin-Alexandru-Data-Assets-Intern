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