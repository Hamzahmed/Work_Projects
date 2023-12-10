CREATE
OR REPLACE TABLE `sandbox.Refined.TenK_placeholders` AS
SELECT
    p.Placeholders_id AS placeholders_id,
    p.title AS placeholders_title,
    p.role AS placeholders_role,
    p.discipline AS placeholders_discipline,
    p.GL_Business_Unit as placeholders_BU,
    p.Director as placeholders_director
FROM
    `sandbox.Raw.TenK_placeholders` AS p