CREATE TABLE partitioned_accounting
WITH (
      format = 'Parquet',
      write_compression = 'GZIP',
      external_location = "*s3-bucket*"",
      partitioned_by = ARRAY['year'],
      bucketed_by = ARRAY['policy_id'], 
      bucket_count = 95
      )
AS SELECT
*,
date_format(Coalesce(
        try(cast(date_parse(time_stamp, '%Y-%m-%d %H:%i:%S') as date)),
        try(cast(date_parse(time_stamp, '%Y-%m-%d %H:%i:%S.%f') as date))
        ),'%Y') AS year
FROM accounting;