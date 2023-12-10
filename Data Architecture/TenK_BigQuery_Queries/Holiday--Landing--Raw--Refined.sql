create or replace table 
`sandbox.Raw.TenK_Holidays`
as select * from `sandbox.Landing.TenK_Holidays`;


create or replace table 
`sandbox.Refined.TenK_Holidays`
as select * from `sandbox.Raw.TenK_Holidays`;