"""
pytest unit tests for data_check.py.

Rules pytest follows:
  - any function whose name starts with test_ is a test
  - a plain `assert` is the check
  - `with pytest.raises(SomeError):` checks that an error IS raised
  - adding `tmp_path` as a parameter gives you a temporary folder
    (a pathlib.Path) where you can write small fake CSV files

Run from the ScamFree folder with:  python -m pytest -v
"""

import pytest
from data_check import normalize_label, build_text, is_valid, load_emails, label_counts


# ---------- EXAMPLE (done for you) ----------
def test_normalize_label_spam():
    assert normalize_label("spam") == "Spam"


# ---------- YOUR TURN: write one test per line below ----------

# 1. normalize_label(" HAM ") returns "Not Spam"  (case + spaces ignored)
def test_normalize_label_ham_with_spaces_and_capital():
    assert normalize_label(" HAM ") == "Not Spam"

# 2. normalize_label returns None for "other", "" and None
def test_normalize_label_rejects_unknown_values():
    assert normalize_label("other") is None
    assert normalize_label("") is None
    assert normalize_label(None) is None

# 3. build_text("Hello", "world") returns "Hello world"
def test_build_text():
    assert build_text("Hello", "world") == "Hello world"

# 4. build_text("", "just body") returns "just body"  (no leading space)
def test_build_text_with_space():
    assert build_text("", "just body") =="just body"

# 5. is_valid accepts the boundaries: text of length 3 and of length 2000
#    Tip: "a" * 3 makes a 3-character string
def test_is_valid_accepts_boundary_lengths():
    assert is_valid("a" *3, "Spam") == True
    assert is_valid("a"*2000, "Spam") == True
    

# 6. is_valid rejects length 2, length 2001, and a valid text with label None
def test_is_valid_rejects_boundary_lengths():
    assert is_valid("a" *2, "Spam") == False
    assert is_valid("a"*2001, "Spam") ==False
    assert is_valid("hello", None) == False
# 7. load_emails respects the limit.
#    Write a tiny CSV into tmp_path with 5 valid rows, call load_emails(path, limit=2),
#    and assert you get exactly 2 records back.
#    Tip:
#      path = tmp_path / "mini.csv"
#      path.write_text("Spam/Ham,Subject,Message\nspam,Win,Claim your prize now\n...")
def test_load_emails_respects_limit(tmp_path):
    path = tmp_path / "mini.csv"
    path.write_text(
        "Spam/Ham,Subject,Message\n"
        "spam,Win,Claim your prize now\n"
        "ham,Lunch,Are we still meeting at noon\n"
        "spam,Urgent,Verify your account today\n"
        "ham,Notes,Here are the lecture notes\n"
        "spam,Offer,Free gift card inside\n"
    )

    # Act: load it, but only allow 2 records
    emails = load_emails(path, limit=2)

    # Assert: we got exactly 2 back
    assert len(emails) == 2
# 8. load_emails skips invalid rows.
#    Tiny CSV with 1 valid row, 1 row with a bad label, 1 row with text "hi" -> 1 record.
# 8. load_emails skips invalid rows
def test_load_emails_skips_invalid_rows(tmp_path):
    path = tmp_path / "mini.csv"
    path.write_text(
        "Spam/Ham,Subject,Message\n"
        "spam,Win,Claim your prize now\n"      # valid
        "maybe,Hi,This label is not real\n"    # bad label -> skipped
        "ham,,hi\n"                            # text "hi" is too short -> skipped
    )

    emails = load_emails(path)

    assert len(emails) == 1
# 9. load_emails raises FileNotFoundError for a missing file.
#    Tip:
#      with pytest.raises(FileNotFoundError):
#          load_emails("does-not-exist.csv")
def test_load_email_raiseError():
    with pytest.raises(FileNotFoundError):
        load_emails("does-not-exist.cvs")



# 10. (integration) On the real "123.csv": every record passes is_valid,
#     and label_counts shows BOTH "Spam" and "Not Spam".
# 10. (integration) On the real "123.csv": every record passes is_valid,
#     and label_counts shows BOTH "Spam" and "Not Spam".
def test_real_dataset_is_clean_and_has_both_labels():
    # Act: load the real dataset
    emails = load_emails("123.csv")

    # Assert 1: we actually got data
    assert len(emails) > 0

    # Assert 2: every record passes is_valid
    for email in emails:
        assert is_valid(email["text"], email["label"])

    # Assert 3: both labels are present
    counts = label_counts(emails)
    assert "Spam" in counts
    # ...your turn: one more line for "Not Spam"