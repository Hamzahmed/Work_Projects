--enable change tracking on database level
ALTER DATABASE [Eagle-next-dev] 
SET CHANGE_TRACKING = ON  
(CHANGE_RETENTION = 2 DAYS, AUTO_CLEANUP = ON);
GO

--enable change tracking on table level

ALTER TABLE [Finance].[RevenuePeriod]
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON)
GO

-- ALTER TABLE [Finance].[RevenuePeriod]
-- DISABLE CHANGE_TRACKING; 

-- select CHANGE_TRACKING_CURRENT_VERSION() 'Current Version';
-- GO

-- SELECT
--  *
-- FROM
--  CHANGETABLE(CHANGES [Finance].[RevenuePeriod], null) as CT;
-- GO


