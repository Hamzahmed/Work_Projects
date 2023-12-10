CREATE
OR REPLACE TABLE sandbox.Refined.TenK_Users AS (
    SELECT
        Users_id as talent_id,
        data_retrieval_time,
        archived_at as talent_archived_at,
        last_name as talent_last_name,
        archived as talent_archived,
        location as talent_location,
        termination_date as talent_terminated_at,
        hire_date as talent_hire_date,
        display_name as talent_display_name,
        email as talent_email,
        billable as talent_billable,
        billability_target as talent_billability_target,
        first_name as talent_first_name,
        deleted as talent_deleted,
        role as talent_role,
        discipline as talent_discipline,
        director AS talent_director,
        BU as talent_BU,
        legal_name as talent_legal_name,
        timezones as talent_timezones,
        tag as talent_tags,
    FROM
        `sandbox.Raw.TenK_Users`
);