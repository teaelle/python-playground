USE WATTapplication

SELECT * FROM WATT.worked WHERE CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE) ORDER BY workedItemId DESC


/****************RESEARCH***************************************

SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE '2019-09-09'
SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE '2019-05-02%'

*****************CALL REPORTS****************************************
SELECT *
FROM 
	watt.V_trackingReports
WHERE  CAST(dateWorked AS DATE) BETWEEN '2019-11-01' AND '2019-11-07'
AND taskTypeName = 'Call'
ORDER BY dateWorked
*****************inq REPORTS****************************************
SELECT DISTINCT taskTypeName, CODE, dateWorked, analystNameForDisplay
FROM 
	watt.V_trackingReports
WHERE  CAST(dateWorked AS DATE) BETWEEN '2019-11-01' AND '2019-11-07'
AND taskTypeName = 'Data Inquiries'
ORDER BY dateWorked
*****************TRACKING UTILIZATION**************************
SELECT 
CAST(worked.startedAtTime AS DATE) dateWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
GROUP BY CAST(worked.startedAtTime AS DATE)
ORDER BY CAST(worked.startedAtTime AS DATE) DESC

*****************WORK TRACKED BY TASK************************
SELECT 
taskType.taskTypeName,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
INNER JOIN WATT.taskType ON worked.taskTypeId = taskType.taskTypeId
WHERE CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)
GROUP BY taskType.taskTypeName
ORDER BY totalMinutesWorked DESC

*****************WORK TRACKED BY CLIENT************************
SELECT 
worked.clientCode,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
WHERE  CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)
GROUP BY worked.clientCode
ORDER BY totalMinutesWorked DESC

*****************UPDATE START DATETIME**************************
UPDATE watt.worked
SET startedAtTime = '2019-10-22 14:47:00'
WHERE workedItemId = 2608

*****************UPDATE END DATETIME****************************
UPDATE watt.worked
SET endedAtTime = '2019-10-30 15:42:00'
WHERE workedItemId = 2752

*****************UPDATE TASK TYPE*******************************
UPDATE watt.worked
SET taskTypeId =  11
WHERE workedItemId = 1864

SELECT * FROM watt.taskType

*****************UPDATE CLIENT CODE*****************************
UPDATE watt.worked
SET clientCode =  'NEST'
WHERE workedItemId = 2145

UPDATE watt.worked
SET clientCode =  'WP00'
WHERE clientCode =  'WP'

*****************UPDATE NOTE*****************************
UPDATE watt.worked
SET workedItemNote =  'QA'
WHERE workedItemId = 2122

*****************DELETE TASK************************************
DELETE watt.worked WHERE workedItemId IN (2753)


*****************ADD NEW TASK************************************
INSERT INTO watt.worked (taskTypeId,clientCode,workedItemNote,startedAtTime,endedAtTime)
VALUES
(14,'IBM0','','2019-09-10 08:20:00','2019-09-10 09:02:00')
*/
