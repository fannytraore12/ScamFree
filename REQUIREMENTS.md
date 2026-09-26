# ScamFree Data Pipeline: Requirements and Traceability

This document lists the requirements for ScamFree's email data pipeline
(`CSV_Parser.js` and `data_check.py`) and maps each requirement to the
automated test that verifies it.

## 1. Requirements

| ID | Requirement | Rationale |
|---|---|---|
| REQ-01 | The loader shall accept the labels "spam" and "ham", ignoring letter case and surrounding spaces, and map them to "Spam" and "Not Spam". | Source data is not consistently formatted. |
| REQ-02 | The loader shall reject any record whose label is not "spam" or "ham". | Unlabeled or mislabeled data would corrupt training. |
| REQ-03 | *(your turn: how subject and message are combined into one text)* | |
| REQ-04 | *(your turn: minimum and maximum text length, inclusive)* | |
| REQ-05 | *(your turn: the record limit)* | |
| REQ-06 | *(your turn: what must happen when the input file does not exist)* | |
| REQ-07 | *(your turn: the full dataset must contain both classes)* | |
| REQ-08 | *(your turn: minimum held-out accuracy of the classifier)* | |

## 2. Traceability matrix

Each requirement is verified by at least one automated test, run in CI on every push.

| Requirement | Verified by (test) | File |
|---|---|---|
| REQ-01 | `test_normalize_label_spam`, `test_normalize_label_ham_with_spaces_and_caps` | tests/test_data_check.py |
| REQ-02 | `test_normalize_label_rejects_unknown_values` | tests/test_data_check.py |
| REQ-03 | *(your turn)* | |
| REQ-04 | *(your turn)* | |
| REQ-05 | *(your turn: note there is one in each language)* | |
| REQ-06 | *(your turn: note there is one in each language)* | |
| REQ-07 | *(your turn)* | |
| REQ-08 | `held-out accuracy stays at or above 95%` | tests/scamfree.test.js |

## 3. Change history

| Date | Change |
|---|---|
| 2026-09-26 | Initial requirements and traceability matrix. |
