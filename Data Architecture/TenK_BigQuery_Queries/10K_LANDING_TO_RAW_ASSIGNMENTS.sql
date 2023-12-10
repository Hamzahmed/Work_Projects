CREATE TABLE
  IF NOT EXISTS `sandbox.Raw.TenK_Assignments` LIKE `sandbox.Landing.TenK_Assignments`;

merge into `sandbox.Raw.TenK_Assignments` raw using (
  select
    *
  from
    `sandbox.Landing.TenK_Assignments`
) land on raw.Assignments_id = land.Assignments_id when not matched then insert (
  fixed_hours,
  Assignments_id,
  data_retrieval_time,
  description,
  resource_request_id,
  status_option_id,
  assignable_id,
  hours_per_day,
  note,
  bill_rate_id,
  all_day_assignment,
  updated_at,
  created_at,
  percent,
  starts_at,
  bill_rate,
  user_id,
  status,
  ends_at,
  repetition_id,
  allocation_mode
)
values
  (
    fixed_hours,
    Assignments_id,
    data_retrieval_time,
    description,
    resource_request_id,
    status_option_id,
    assignable_id,
    hours_per_day,
    note,
    bill_rate_id,
    all_day_assignment,
    updated_at,
    created_at,
    percent,
    starts_at,
    bill_rate,
    user_id,
    status,
    ends_at,
    repetition_id,
    allocation_mode
  ) when matched then
update
set
  raw.fixed_hours = land.fixed_hours,
  raw.Assignments_id = land.Assignments_id,
  raw.data_retrieval_time = land.data_retrieval_time,
  raw.description = land.description,
  raw.resource_request_id = land.resource_request_id,
  raw.status_option_id = IFNULL (
    land.status_option_id,
    IF (land.bill_rate > 0, 306883, 306886)
  ),
  raw.assignable_id = land.assignable_id,
  raw.hours_per_day = land.hours_per_day,
  raw.note = land.note,
  raw.bill_rate_id = land.bill_rate_id,
  raw.all_day_assignment = land.all_day_assignment,
  raw.updated_at = land.updated_at,
  raw.created_at = land.created_at,
  raw.percent = land.percent,
  raw.starts_at = land.starts_at,
  raw.bill_rate = land.bill_rate,
  raw.user_id = land.user_id,
  raw.status = land.status,
  raw.ends_at = land.ends_at,
  raw.repetition_id = land.repetition_id,
  raw.allocation_mode = land.allocation_mode