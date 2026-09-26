"""
data_check.py - Python data validation for ScamFree's email dataset (123.csv).

It mirrors what CSV_Parser.js does in JavaScript, so both halves of the
project agree on what a "valid" email record is.

CSV columns used: "Spam/Ham", "Subject", "Message"

Fill in each TODO. Run the tests with:  python -m pytest -v
"""

import csv

MIN_LEN = 3
MAX_LEN = 2000


def normalize_label(raw):
    """Turn a raw label into "Spam", "Not Spam" or None.

    Should ignore capital letters and surrounding spaces:
      "spam" -> "Spam",  " HAM " -> "Not Spam",  "other" -> None,  "" -> None
    Tip: raw might also be None, so handle that too.
    """
    if raw is None:
        return None
    cleaned = raw.strip().lower()

    if cleaned == "spam":
        return "Spam"
    elif cleaned == "ham":
        return "Not Spam"
    else:
        return None
        


def build_text(subject, message):
    """Join subject and message with one space, then strip the ends.

      ("Hello", "world") -> "Hello world"
      ("", "just body")   -> "just body"
    Tip: treat None the same as "".
    """
    if subject is None:
        subject = ""
    if message is None:
        message = ""
    return (subject + " " + message).strip()


def is_valid(text, label, min_len=MIN_LEN, max_len=MAX_LEN):
    """True only if label is not None AND min_len <= len(text) <= max_len.

    Both limits are inclusive: length 3 and length 2000 are valid,
    length 2 and length 2001 are not.
    """
    if label is None:
        return False
    if not(min_len <= len(text) <= max_len):
        return False
    return True


def load_emails(path, limit=7000):
    """Read the CSV and return a list of {"text": ..., "label": ...} dicts.

    - Use csv.DictReader and the three helpers above.
    - Skip rows that are not valid.
    - Stop once `limit` valid records are collected.
    - If the file does not exist, let FileNotFoundError be raised
      (this is the bug the JavaScript loader had - Python gets it right
      by default, as long as you don't catch the error).
    Tip: open the file with encoding="utf-8", errors="ignore".
    """
    emails = []

    with open(path, encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = normalize_label(row.get("Spam/Ham"))
            text = build_text(row.get("Subject"), row.get("Message"))
            if not is_valid(text,label):
                continue
            emails.append({"text": text, "label": label})
            if len(emails) >= limit:
                break
        return emails
                            




def label_counts(emails):
    """Return how many of each label there are, e.g. {"Spam": 950, "Not Spam": 6050}."""
    counts = {}
    for email in emails:
         label = email["label"]
         counts[label] = counts.get(label, 0) + 1
    return counts

