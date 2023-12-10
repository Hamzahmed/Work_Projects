CREATE TABLE
  IF NOT EXISTS `sandbox.Raw.TenK_status_options` LIKE `sandbox.Landing.TenK_status_options`;

merge into `sandbox.Raw.TenK_status_options` raw using (
  select
    *
  from
    `sandbox.Landing.TenK_status_options`
) land on raw.Status_id = land.Status_id when not matched then insert (
  data_retrieval_time,
  Status_id,
  deleted_at,
  created_at,
  stage,
  `order`,
  color,
  updated_at,
  label
)
values
  (
    data_retrieval_time,
    Status_id,
    deleted_at,
    created_at,
    stage,
    `order`,
    color,
    updated_at,
    label
  ) when matched then
update
set
  raw.data_retrieval_time = land.data_retrieval_time,
  raw.Status_id = land.Status_id,
  raw.deleted_at = land.deleted_at,
  raw.created_at = land.created_at,
  raw.stage = land.stage,
  raw.order = land.order,
  raw.color = land.color,
  raw.updated_at = land.updated_at,
  raw.label = land.label;