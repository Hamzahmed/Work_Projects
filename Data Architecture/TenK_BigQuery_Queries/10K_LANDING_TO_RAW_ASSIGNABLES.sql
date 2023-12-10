create table
  if not exists `sandbox.Raw.TenK_Assignables` like `sandbox.Landing.TenK_Assignables`;

merge into `sandbox.Raw.TenK_Assignables` raw using (
  select
    *
  from
    `sandbox.Landing.TenK_Assignables`
) land on raw.Assignables_id = land.Assignables_id when not matched then insert (
  phase_name,
  client,
  owner_name,
  owner_id,
  data_retrieval_time,
  parent_id,
  settings,
  starts_at,
  secureurl,
  project_code,
  updated_at,
  Assignables_id,
  thumbnail,
  timeentry_lockout,
  deleted_at,
  description,
  project_state_id,
  name,
  ends_at,
  secureurl_expiration,
  guid,
  type,
  created_at
)
values
  (
    phase_name,
    client,
    owner_name,
    owner_id,
    data_retrieval_time,
    parent_id,
    settings,
    starts_at,
    secureurl,
    project_code,
    updated_at,
    Assignables_id,
    thumbnail,
    timeentry_lockout,
    deleted_at,
    description,
    project_state_id,
    name,
    ends_at,
    secureurl_expiration,
    guid,
    type,
    created_at
  ) when matched then
update
set
  raw.phase_name = land.phase_name,
  raw.client = land.client,
  raw.owner_name = land.owner_name,
  raw.owner_id = land.owner_id,
  raw.data_retrieval_time = land.data_retrieval_time,
  raw.parent_id = land.parent_id,
  raw.settings = land.settings,
  raw.starts_at = land.starts_at,
  raw.secureurl = land.secureurl,
  raw.project_code = land.project_code,
  raw.updated_at = land.updated_at,
  raw.Assignables_id = land.Assignables_id,
  raw.thumbnail = land.thumbnail,
  raw.timeentry_lockout = land.timeentry_lockout,
  raw.deleted_at = land.deleted_at,
  raw.description = land.description,
  raw.project_state_id = land.project_state_id,
  raw.name = land.name,
  raw.ends_at = land.ends_at,
  raw.secureurl_expiration = land.secureurl_expiration,
  raw.guid = land.guid,
  raw.type = land.type,
  raw.created_at = land.created_at;