import re
import os

def validate_identifiers(src_file="a2l_Validation.a2l"):
    print(f"Reading {src_file} from workspace...")

    if not os.path.exists(src_file):
        print("ERROR: File not found")
        print("RESULT=FAIL")
        return 1

    with open(src_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Loaded {src_file} with {len(lines)} lines")

    pattern = re.compile(r".*_uc[12]_([A-Za-z0-9]{4}).*")

    identifiers = []
    invalid_identifiers = []

    for line in lines:
        match = pattern.search(line)
        if match:
            identifier = match.group(1).strip()
            identifiers.append(identifier)
            print(f"Found identifier: {identifier}")

    print(f"Collected identifiers: {identifiers}")

    for ident in identifiers:
        if re.fullmatch(r"[A-Z]\d{3}", ident):
            print(f"VALID: {ident}")
        else:
            print(f"INVALID: {ident} (expected: 1 capital letter + 3 digits)")
            invalid_identifiers.append(ident)

    if invalid_identifiers:
        print(f"Invalid identifiers: {', '.join(invalid_identifiers)}")
        print("Validation failed")
        print("RESULT=FAIL")
        return 1

    print(f"Validation passed. '{src_file}' ready for SVN upload.")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    validate_identifiers()
