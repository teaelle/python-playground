USE WATTapplication

/* Minutes Spent per Client by Date Range */

SELECT 
	worked.clientCode,
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
--WHERE  CAST(worked.startedAtTime AS DATE) BETWEEN '2019-04-26' AND '2019-05-02'
WHERE  
	CAST(worked.startedAtTime AS DATE) BETWEEN '2019-11-01' AND '2019-11-07'
GROUP BY
	worked.clientCode
ORDER BY 
	totalMinutesWorked DESC
