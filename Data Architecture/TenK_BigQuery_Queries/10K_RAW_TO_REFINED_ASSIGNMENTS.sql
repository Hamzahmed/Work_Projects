CREATE TABLE IF NOT EXISTS `sandbox.Refined.TenK_Assignments` (
  assignment_id int64
  ,assignment_talent_id int64
  ,assignment_starts_at date
  ,assignment_ends_at date
  ,assignment_allocation float64
  ,assignment_status_effective_id int64
  ,assignment_status_effective_label string
  ,assignment_non_billable_type string
  ,assignment_project_id int64
);

CREATE TEMP FUNCTION CUSTOM_DATE_DIFF(startDate DATE, endDate DATE, user_BU STRING) AS ((
  SELECT
    1 + DATE_DIFF(endDate, startDate, DAY) -
    2 * DATE_DIFF(endDate, startDate, WEEK) -
    IF(EXTRACT(DAYOFWEEK FROM startDate) = 1, 1, 0) -
    IF(EXTRACT(DAYOFWEEK FROM endDate) = 7, 1, 0) -
    COUNTIF((PARSE_DATE("%Y/%m/%d", Holiday_Dates) BETWEEN startDate AND endDate) AND user_BU = Business_Unit)
  FROM
    `sandbox.Raw.TenK_Holidays`
  WHERE
    PARSE_DATE("%Y/%m/%d", Holiday_Dates) BETWEEN startDate AND endDate
));

CREATE TEMP FUNCTION PARSE_DESCRIPTION(description STRING) AS (
  regexp_contains(description, (select string_agg(distinct label, '|') from `sandbox.Raw.TenK_status_options`)) and regexp_contains(description, '%')
);

CREATE TEMP FUNCTION EXTRACT_LABEL(description STRING) AS (
  regexp_extract(description, (select string_agg(distinct label, '|') from `sandbox.Raw.TenK_status_options`))
);

CREATE TEMP FUNCTION EXTRACT_STATUS(description STRING) AS (
  (select Status_id from `sandbox.Raw.TenK_status_options` so where so.label = regexp_extract(description, (select string_agg(distinct label, '|') from `sandbox.Raw.TenK_status_options`)))
);

merge into `sandbox.Refined.TenK_Assignments` ref
using (select 
  am.Assignments_id `assignment_id`
  ,am.user_id `assignment_talent_id`
  ,am.starts_at `assignment_starts_at`
  ,am.ends_at `assignment_ends_at`
  ,case 
    when am.allocation_mode = 'percent'
    then am.percent
    when am.allocation_mode = 'hours_per_day'
    then am.hours_per_day / 8
    when am.allocation_mode = 'fixed' and CUSTOM_DATE_DIFF(am.starts_at, am.ends_at, u.bu) = 0
    then am.fixed_hours / 8
    when am.allocation_mode = 'fixed' and CUSTOM_DATE_DIFF(am.starts_at, am.ends_at, u.bu) > 0
    then am.fixed_hours / (CUSTOM_DATE_DIFF(am.starts_at, am.ends_at, u.bu) * 8)
    end as assignment_allocation
  ,case when PARSE_DESCRIPTION(am.description)
    then EXTRACT_STATUS(am.description)
    else am.status_option_id
    end as `assignment_status_effective_id`
  ,case when PARSE_DESCRIPTION(am.description)
    then EXTRACT_LABEL(am.description)
    else s.label
    end as `assignment_status_effective_label`
  ,'' `assignment_non_billable_type` --TODO
  ,am.assignable_id `assignment_project_id`
from `sandbox.Raw.TenK_Assignments` am
left join `sandbox.Raw.TenK_Assignables` ab
on am.assignable_id = ab.Assignables_id
left join `sandbox.Raw.TenK_Users` u
on am.user_id = u.Users_id
left join `sandbox.Raw.TenK_status_options` s 
on am.status_option_id = s.Status_id
where TIMESTAMP_DIFF(CURRENT_TIMESTAMP, am.updated_at, hour) <= 1.5) raw
on ref.assignment_id = raw.assignment_id 
and ref.assignment_talent_id = raw.assignment_talent_id
when not matched then
insert (assignment_id 
  ,assignment_talent_id 
  ,assignment_starts_at 
  ,assignment_ends_at 
  ,assignment_allocation 
  ,assignment_status_effective_id
  ,assignment_status_effective_label
  ,assignment_non_billable_type 
  ,assignment_project_id)
  values (assignment_id 
  ,assignment_talent_id 
  ,assignment_starts_at 
  ,assignment_ends_at 
  ,assignment_allocation 
  ,assignment_status_effective_id
  ,assignment_status_effective_label
  ,assignment_non_billable_type
  ,assignment_project_id)
when matched then
update set 
  ref.assignment_starts_at = raw.assignment_starts_at
  ,ref.assignment_ends_at = raw.assignment_ends_at
  ,ref.assignment_allocation = raw.assignment_allocation
  ,ref.assignment_status_effective_id = raw.assignment_status_effective_id
  ,ref.assignment_status_effective_label = raw.assignment_status_effective_label
  ,ref.assignment_non_billable_type = raw.assignment_non_billable_type
  ,ref.assignment_project_id = raw.assignment_project_id;