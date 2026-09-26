# ScamFree Data Pipeline: Requirements and Traceability

This document lists the requirements for ScamFree's email data pipeline
(`CSV_Parser.js` and `data_check.py`) and maps each requirement to the
automated test that verifies it.

## 1. Requirements

| ID | Requirement | Rationale |
|---|---|---|
| REQ-01 | The loader shall accept the labels "spam" and "ham", ignoring letter case and surrounding spaces, and map them to "Spam" and "Not Spam". | Source data is not consistently formatted. |
| REQ-02 | The loader shall reject any record whose label is not "spam" or "ham". | Unlabeled or mislabeled data would corrupt training. |
| REQ-03 The loader shall combine each record's subject and message into one text, separated by a single space, with leading and trailing whitespace removed.| |
| REQ-04 | The loader shall keep only records whose text is between 3 and 2000 characters long, inclusive.| |
| REQ-05 | The loader shall stop after collecting a configurable maximum number of valid records (default: 7000).| |
| REQ-06 | The loader shall report an error when the input file does not exist (FileNotFoundError in Python, a rejected promise in JavaScript) instead of hanging.| |
| REQ-07 | The full dataset shall contain valid records of both classes, "Spam" and "Not Spam".| |
| REQ-08 |The trained classifier shall achieve at least 95% accuracy on held-out test data| |

## 2. Traceability matrix

Each requirement is verified by at least one automated test, run in CI on every push.

| Requirement | Verified by (test) | File |
|---|---|---|
| REQ-01 | `test_normalize_label_spam`, `test_normalize_label_ham_with_spaces_and_capital` | tests/test_data_check.py |
| REQ-02 | `test_normalize_label_rejects_unknown_values`, `test_load_emails_skips_invalid_rows` | tests/test_data_check.py |
| REQ-03 | `test_build_text`, `test_build_text_with_space` | tests/test_data_check.py |
| REQ-04 | `test_is_valid_accepts_boundary_lengths`, `test_is_valid_rejects_boundary_lengths`, `test_load_emails_skips_invalid_rows` | tests/test_data_check.py |
| REQ-04 | `filters out texts that are too short or too long` | tests/scamfree.test.js |
| REQ-05 | `test_load_emails_respects_limit` | tests/test_data_check.py |
| REQ-05 | `respects the record limit` | tests/scamfree.test.js |
| REQ-06 | `test_load_email_raiseError` | tests/test_data_check.py |
| REQ-06 | `rejects when the file does not exist` | tests/scamfree.test.js |
| REQ-07 | `test_real_dataset_is_clean_and_has_both_labels` | tests/test_data_check.py |
| REQ-07 | `dataset contains both spam and non-spam examples` | tests/scamfree.test.js |
| REQ-08 | `held-out accuracy stays at or above 95%` | tests/scamfree.test.js |

## 3. Change history

| Date | Change |
|---|---|
| 2026-09-26 | Initial requirements and traceability matrix. |
