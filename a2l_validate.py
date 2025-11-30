import re
import sys
import os

def validate_identifiers(src_file="a2l_Validation.a2l"):
    print(f"Reading {src_file} from workspace...")

    # Check file presence
    if not os.path.exists(src_file):
        print(f"ERROR: File not found: {src_file}")
        sys.exit(1)

    # Load file content
    with open(src_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Loaded {src_file} with {len(lines)} lines")

    # Pattern: capture 4 alphanumeric chars after _uc1_ or _uc2_
    pattern = re.compile(r".*_uc[12]_([A-Za-z0-9]{4}).*")

    identifiers = []
    invalid_identifiers = []

    # Extract identifiers
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
            print(f"INVALID: {ident}  (expected: 1 capital letter + 3 digits)")
            invalid_identifiers.append(ident)

    if invalid_identifiers:
        print(f"Invalid identifiers: {', '.join(invalid_identifiers)}")
        print("Validation failed. Will skip SVN upload.")
        sys.exit(2)

    print(f"Validation passed. '{src_file}' ready for SVN upload.")
    return 0


if __name__ == "__main__":
    sys.exit(validate_identifiers())
