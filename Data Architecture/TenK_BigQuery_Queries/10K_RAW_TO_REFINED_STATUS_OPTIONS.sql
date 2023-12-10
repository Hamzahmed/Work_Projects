CREATE
OR REPLACE TABLE sandbox.Refined.TenK_status_options AS
SELECT
    Status_id as assignment_status_option_ID,
    label as assignment_status_label,
    Null as assignment_status_utilization,
    CAST(NULL AS STRING) AS assignment_status_calc
FROM
    `sandbox.Raw.TenK_status_options`;

UPDATE sandbox.Refined.TenK_status_options
SET
    assignment_status_calc = 'Ignore'
WHERE
    assignment_status_option_ID IN (306883.0, 306884.0, 360139.0);

UPDATE sandbox.Refined.TenK_status_options
SET
    assignment_status_calc = 'Numerator'
WHERE
    assignment_status_option_ID = 453408.0;

UPDATE sandbox.Refined.TenK_status_options
SET
    assignment_status_calc = 'Denominator'
WHERE
    assignment_status_option_ID = 306887.0;

UPDATE sandbox.Refined.TenK_status_options
SET
    assignment_status_calc = 'Numerator'
WHERE
    assignment_status_option_ID = 306886.0;