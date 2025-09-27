#!/usr/bin/env python3
"""
password_strength.py
Assess password strength and give suggestions.

Usage:
  python password_strength.py        # prompts for a password (hidden)
  python password_strength.py -p "MyPass123!"   # evaluate single password
  python password_strength.py -f list.txt       # evaluate each line in file
"""

import re
import string
from collections import Counter
import argparse
import getpass

COMMON_PASSWORDS = {
    "password","123456","12345678","qwerty","abc123","111111","1234567890",
    "1234567","iloveyou","admin","welcome","letmein","monkey","dragon"
}

def score_length(pw: str) -> int:
    l = len(pw)
    if l >= 12:
        return 40
    if l >= 9:
        return 30
    if l >= 7:
        return 20
    if l >= 5:
        return 10
    return 0

def has_upper(pw: str) -> bool:
    return any(c.isupper() for c in pw)

def has_lower(pw: str) -> bool:
    return any(c.islower() for c in pw)

def has_digit(pw: str) -> bool:
    return any(c.isdigit() for c in pw)

def has_special(pw: str) -> bool:
    return any(c in string.punctuation for c in pw)

def is_common_password(pw: str) -> bool:
    return pw.lower() in COMMON_PASSWORDS

def is_sequential(pw: str) -> bool:
    # remove non-alnum and check for any length-4 sequential substring
    s = ''.join(ch for ch in pw.lower() if ch.isalnum())
    if len(s) < 4:
        return False
    for i in range(len(s) - 3):
        sub = s[i:i+4]
        # check ascending
        if all(ord(sub[j+1]) - ord(sub[j]) == 1 for j in range(3)):
            return True
        # check descending
        if all(ord(sub[j]) - ord(sub[j+1]) == 1 for j in range(3)):
            return True
    return False

def is_repeated(pw: str) -> bool:
    if not pw:
        return False
    cnt = Counter(pw)
    most = cnt.most_common(1)[0][1]
    return (most / len(pw)) > 0.5

def assess_password(pw: str) -> dict:
    if not pw:
        return {"score": 0, "category": "Very Weak", "reason": "empty password", "suggestions": ["Enter a password."]}

    if is_common_password(pw):
        return {"score": 0, "category": "Very Weak", "reason": "common password", "suggestions": [
            "Don't use common passwords (e.g. 'password', '123456').",
            "Use a long passphrase with mixed characters."
        ]}

    raw = 0
    raw += score_length(pw)
    raw += 15 if has_upper(pw) else 0
    raw += 15 if has_lower(pw) else 0
    raw += 15 if has_digit(pw) else 0
    raw += 15 if has_special(pw) else 0

    penalties = 0
    if is_sequential(pw):
        penalties += 20
    if is_repeated(pw):
        penalties += 20

    final = max(0, raw - penalties)
    final = min(final, 100)

    if final >= 80:
        cat = "Strong"
    elif final >= 60:
        cat = "Good"
    elif final >= 40:
        cat = "Weak"
    else:
        cat = "Very Weak"

    suggestions = []
    if len(pw) < 12:
        suggestions.append("Increase length to 12+ characters (or use a 4+ word passphrase).")
    if not has_upper(pw):
        suggestions.append("Add uppercase letters (A-Z).")
    if not has_lower(pw):
        suggestions.append("Add lowercase letters (a-z).")
    if not has_digit(pw):
        suggestions.append("Add digits (0-9).")
    if not has_special(pw):
        suggestions.append("Add special characters (e.g. !@#$%).")
    if is_sequential(pw):
        suggestions.append("Avoid sequential patterns like 'abcd' or '1234'.")
    if is_repeated(pw):
        suggestions.append("Avoid repeated characters like 'aaaaaa' or '111111'.")
    suggestions.append("Use a unique password per site; consider a password manager.")

    details = {
        "length_score": score_length(pw),
        "has_upper": has_upper(pw),
        "has_lower": has_lower(pw),
        "has_digit": has_digit(pw),
        "has_special": has_special(pw),
        "raw_score": raw,
        "penalties": penalties
    }

    return {"score": final, "category": cat, "reason": "OK", "suggestions": suggestions, "details": details}

def pretty_print(result: dict, pw: str = None):
    print("Password:", ("(hidden)" if pw else ""))
    print("Score:", result["score"], "/100")
    print("Category:", result["category"])
    if result.get("details"):
        d = result["details"]
        print("Breakdown -> length_score:", d["length_score"],
              " upper:", d["has_upper"], " lower:", d["has_lower"],
              " digits:", d["has_digit"], " special:", d["has_special"])
        print("Raw score:", d["raw_score"], " Penalties:", d["penalties"])
    if result.get("suggestions"):
        print("\nSuggestions:")
        for s in result["suggestions"]:
            print(" -", s)
    print("-" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password strength checker")
    parser.add_argument("-p", "--password", help="Password to check (use carefully!)")
    parser.add_argument("-f", "--file", help="File with one password per line")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as fh:
                for line in fh:
                    pw = line.rstrip("\n")
                    res = assess_password(pw)
                    print("Password (from file):", pw)
                    pretty_print(res, pw)
        except Exception as e:
            print("Error reading file:", e)
    else:
        if args.password:
            pw = args.password
        else:
            # hidden input
            pw = getpass.getpass("Enter password to evaluate: ")
        res = assess_password(pw)
        pretty_print(res, pw)
