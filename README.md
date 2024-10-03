# UPDATE LOG

## EXCEL-MATCH 1.0.0 (2024-10-03)

### Major Features

- Supports one-to-one, one-to-many, and many-to-many matching.
- Supports uploading xlsx, xls and csv file types.
- Only the same type of table structure is supported.
- Only inner joins are implemented for table joins.
- Provides error alerts for file type errors, table structure inconsistencies, non-existent columns, and match failures.
- Chinese and English documents are supported.

### Bug Fixes

- **Form Validation:** 
  - Fixed the ability to upload non-excel type files. 
  - Fixed the issue where a request could be sent with an incomplete form.

- **Exception handling:**
  - Fixed an issue where back-end exception handling was unclear.

- **File type support:**

  - Fixed csv file saving bug.

  - The fix supports xlsx and xls saving methods.