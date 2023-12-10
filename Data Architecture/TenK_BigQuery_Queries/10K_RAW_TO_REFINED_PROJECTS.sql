Create
or replace table `sandbox.Refined.TenK_projects` as
SELECT
    Projects_id as project_id,
    client as project_client,
    ends_at as project_ends_at,
    tags_value as project_tags,
    description as project_description_revised,
    starts_at as project_starts_at,
    archived as project_archived,
    name as project_name,
    project_state as project_state
FROM
    `sandbox.Raw.TenK_Projects`;