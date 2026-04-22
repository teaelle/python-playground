

SELECT 
'Main Work' ,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
WHERE CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)
AND worked.taskTypeId IN (1,2,3,4,5,6,14,15,16,17)
UNION
SELECT 
'NULL Work' ,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
WHERE CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)
AND worked.taskTypeId IN (7,8,12,13,9)
UNION
SELECT 
'Project Work' ,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
WHERE CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)
AND worked.taskTypeId IN (10,11,18)
UNION
SELECT 
'All Work' ,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
WHERE CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)


/*
SELECT * FROM watt.taskType

Main Work: (1,2,3,4,5,6,14,15,16,17)
NULL Work: (7,8,12,13,9)
Project Work: (10,11,18)


*/