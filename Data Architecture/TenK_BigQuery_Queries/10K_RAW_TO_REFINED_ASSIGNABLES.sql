CREATE
OR REPLACE TABLE sandbox.Refined.TenK_Assignments_Refined AS
SELECT
  *,
  CAST(NULL AS FLOAT64) AS assignment_allocation
FROM
  `sandbox.Raw.TenK_Assignments`;

UPDATE sandbox.Refined.TenK_Assignments_Refined
SET
  assignment_allocation = CAST(percent AS FLOAT64)
WHERE
  allocation_mode = 'percent';

UPDATE sandbox.Refined.TenK_Assignments_Refined
SET
  assignment_allocation = CAST(CAST(hours_per_day AS FLOAT64) / 8 AS FLOAT64)
WHERE
  allocation_mode = 'hours_per_day';

CREATE TEMP FUNCTION CUSTOM_DATE_DIFF (startDate DATE, endDate DATE) AS (
  (
    SELECT
      1 + DATE_DIFF (endDate, startDate, DAY) -
    2 * DATE_DIFF (endDate, startDate, WEEK) - IF (
        EXTRACT(
          DAYOFWEEK
          FROM
            startDate
        ) = 1,
        1,
        0
      ) - IF (
        EXTRACT(
          DAYOFWEEK
          FROM
            endDate
        ) = 7,
        1,
        0
      ) - COUNTIF (
        PARSE_DATE ("%Y/%m/%d", Holiday_Dates) BETWEEN startDate AND endDate
      )
    FROM
      `sandbox.Raw.TenK_Holidays`
    WHERE
      PARSE_DATE ("%Y/%m/%d", Holiday_Dates) BETWEEN startDate AND endDate
  )
);

UPDATE sandbox.Refined.TenK_Assignments_Refined
SET
  assignment_allocation = IF (
    allocation_mode = "fixed"
    AND CUSTOM_DATE_DIFF (starts_at, ends_at) > 0,
    fixed_hours / (CUSTOM_DATE_DIFF (starts_at, ends_at) * 8),
    0
  )
WHERE
  assignment_allocation IS NULL;