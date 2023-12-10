create
or replace table `sandbox.Refined.TenK_Legacy_T` as (
  select
    assignment_id,
    talent_id,
    talent_display_name,
    project_id,
    project_name,
    project_client,
    project_state,
    project_archived,
    assignment_starts_at,
    assignment_ends_at,
    assignment_billable_percent,
    talent_first_name,
    talent_last_name,
    talent_discipline,
    talent_role,
    talent_location,
    talent_tags,
    talent_billable,
    talent_billability_target,
    talent_archived,
    talent_deleted,
    talent_hire_date,
    talent_archived_at,
    talent_terminated_at,
    project_starts_at,
    project_ends_at,
    assignment_description,
    project_description_revised,
    project_tags,
    talent_email,
    assignment_fixed_hours,
    assignment_hours_per_day,
    IFNULL (assignment_status_effective_id, 306883) as assignment_status,
    talent_BU
    ,-- case
    --   when assignment_status_effective_id in (306886, 380443, 453408) then 'numerator'
    --   when assignment_status_effective_id in (306887) then 'denominator'
    --   else 'numerator'
    -- end as `assignment_type_name`
  from
    (
      select
        Assignments_id as `assignment_id`,
        user_id as `talent_id`,
        u.display_name as `talent_display_name`,
        p.Projects_id `project_id`,
        p.name `project_name`,
        p.client as `project_client`,
        p.project_state,
        p.archived `project_archived`,
        am.starts_at `assignment_starts_at`,
        am.ends_at `assignment_ends_at`,
        case
          when regexp_contains (
            am.description,
            (
              select
                string_agg (distinct label, '|')
              from
                `sandbox.Raw.TenK_status_options`
            )
          )
          and regexp_contains (am.description, '%') then cast(
            regexp_replace (
              regexp_extract (am.description, '[0-9]+%'),
              '%',
              ''
            ) as int
          ) / 100
          else am.percent
        end as `assignment_billable_percent`,
        u.first_name `talent_first_name`,
        u.last_name `talent_last_name`,
        u.discipline `talent_discipline`,
        u.role `talent_role`,
        u.location `talent_location`,
        u.tag `talent_tags`,
        u.tag_id `talent_tag_id`,
        u.billable `talent_billable`,
        u.billability_target / 100 `talent_billability_target`,
        u.archived `talent_archived`,
        u.deleted `talent_deleted`,
        u.hire_date `talent_hire_date`,
        u.archived_at `talent_archived_at`,
        u.termination_date `talent_terminated_at`,
        p.starts_at `project_starts_at`,
        p.ends_at `project_ends_at`,
        am.description `assignment_description`,
        regexp_replace (p.description, '\r|\n', '; ') `project_description_revised`,
        p.tags_value as `project_tags`,
        u.email `talent_email`,
        am.fixed_hours `assignment_fixed_hours`,
        am.hours_per_day `assignment_hours_per_day`,
        s.Status_id `assignment_status`,
        u.bu `talent_BU`,
        regexp_contains (am.description, '%') `% description`,
        case
          when regexp_contains (
            am.description,
            (
              select
                string_agg (distinct label, '|')
              from
                `sandbox.Raw.TenK_status_options`
            )
          )
          and regexp_contains (am.description, '%') then regexp_extract (
            am.description,
            (
              select
                string_agg (distinct label, '|')
              from
                `sandbox.Raw.TenK_status_options`
            )
          )
          else s.label
        end as `assignment_status_effective_label`,
        case
          when regexp_contains (
            am.description,
            (
              select
                string_agg (distinct label, '|')
              from
                `sandbox.Raw.TenK_status_options`
            )
          )
          and regexp_contains (am.description, '%') then (
            select
              Status_id
            from
              `sandbox.Raw.TenK_status_options` so
            where
              so.label = regexp_extract (
                am.description,
                (
                  select
                    string_agg (distinct label, '|')
                  from
                    `sandbox.Raw.TenK_status_options`
                )
              )
          )
          else s.status_id
        end as `assignment_status_effective_id`,
        null `assignment_non_billable_type` --TODO
,
        u.director `talent_director`,
        u.legal_name `talent_legal_name`,
        u.timezones `talent_timezones`,
        ab.type `assignment_type`,
        u.role `talent_rate_card_role`
      from
        `sandbox.Raw.TenK_Assignments` am
        left join `sandbox.Raw.TenK_Assignables` ab on am.assignable_id = ab.Assignables_id
        left join `sandbox.Raw.TenK_Users` u on am.user_id = u.Users_id
        left join `sandbox.Raw.TenK_Projects` p on am.assignable_id = p.projects_id
        left join `sandbox.Raw.TenK_status_options` s on am.status_option_id = s.Status_id
      where
        am.assignable_id not in (5450410, 5450411, 5450412, 5450433)
        and (
          (not regexp_contains (u.last_name, 'DEMO'))
          or u.last_name is null
        )
        and (not regexp_contains (p.name, 'SAMPLE'))
    )
  where
    (
      assignment_type is null
      or assignment_type = 'Project'
    )
    and project_id is not null
);