USE WATTapplication

/* Time Tracked Utilization by Day */

SELECT 
	CAST(worked.startedAtTime AS DATE) as workedDate,
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') AS INT)) AS [Minutes Tracked],
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') AS INT)) / 60.0 AS [Hours Tracked],
	(SUM(CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int))/60) / 8.0 as [Utilization]

FROM 
	WATT.worked 
	LEFT JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
--WHERE	CAST(worked.startedAtTime AS DATE)  = '2019-04-19'
GROUP BY
	CAST(worked.startedAtTime AS DATE)
ORDER BY 
	CAST(worked.startedAtTime AS DATE) DESC