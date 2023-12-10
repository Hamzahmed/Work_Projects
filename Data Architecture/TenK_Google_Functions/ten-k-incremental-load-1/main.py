from google.cloud import bigquery
from flask import escape

def merge_assignments(request):
    # Create a BigQuery client
    client = bigquery.Client()

    # Define the query
    query = """
    MERGE `Raw.TenK_Assignments` AS target
    USING (
      SELECT
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
      FROM `Landing.TenK_Assignments`
    ) AS source
    ON target.Assignments_id = source.Assignments_id
    WHEN MATCHED THEN
      UPDATE SET
        target.fixed_hours = source.fixed_hours,
        target.data_retrieval_time = source.data_retrieval_time,
        target.description = source.description,
        target.resource_request_id = source.resource_request_id,
        target.status_option_id = source.status_option_id,
        target.assignable_id = source.assignable_id,
        target.hours_per_day = source.hours_per_day,
        target.note = source.note,
        target.bill_rate_id = source.bill_rate_id,
        target.all_day_assignment = source.all_day_assignment,
        target.updated_at = source.updated_at,
        target.created_at = source.created_at,
        target.percent = source.percent,
        target.starts_at = source.starts_at,
        target.bill_rate = source.bill_rate,
        target.user_id = source.user_id,
        target.status = source.status,
        target.ends_at = source.ends_at,
        target.repetition_id = source.repetition_id,
        target.allocation_mode = source.allocation_mode
    WHEN NOT MATCHED BY TARGET THEN
      INSERT (
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
      VALUES (
        source.fixed_hours,
        source.Assignments_id,
        source.data_retrieval_time,
        source.description,
        source.resource_request_id,
        source.status_option_id,
        source.assignable_id,
        source.hours_per_day,
        source.note,
        source.bill_rate_id,
        source.all_day_assignment,
        source.updated_at,
        source.created_at,
        source.percent,
        source.starts_at,
        source.bill_rate,
        source.user_id,
        source.status,
        source.ends_at,
        source.repetition_id,
        source.allocation_mode
      )
    WHEN NOT MATCHED BY SOURCE THEN
      DELETE;
    """

    # Run the query
    job = client.query(query)

    # Wait for the query to complete
    job.result()

    return 'Query executed successfully.'

