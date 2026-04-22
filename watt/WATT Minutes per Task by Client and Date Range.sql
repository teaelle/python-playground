USE WATTapplication

/* Minutes Spent per Task by Date Range */

SELECT 
	taskType.taskTypeName Task, 
	worked.clientCode Client,
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS 'Minutes'
	--SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
	INNER JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE  
	CAST(worked.startedAtTime AS DATE) BETWEEN '2019-11-01' AND '2019-11-07'
	--AND worked.clientCode = 'IBM0'
GROUP BY 
	taskType.taskTypeName,
	worked.clientCode
ORDER BY 
	Minutes DESC