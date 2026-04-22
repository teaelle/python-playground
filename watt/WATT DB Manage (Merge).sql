USE WATTapplication

/*************
ARCHIVE DATA
*************/
--DROP TABLE WATT.archivedWork
CREATE TABLE watt.archivedWork (
	archivedWorkId INT PRIMARY KEY IDENTITY(1,1),
	taskTypeName VARCHAR(20),
	clientCode VARCHAR(4),
	workedItemNote VARCHAR(100), 
	startedAtTime SMALLDATETIME,
	endedAtTime SMALLDATETIME,
	duration TIME
)

select * from watt.archivedWork

MERGE INTO WATT.archivedWork AS target
USING 
	(SELECT 
		taskTypeName, clientCode, workedItemNote, startedAtTime, endedAtTime, endedAtTime 
	FROM watt.worked 
	INNER JOIN watt.taskType 
		ON worked.taskTypeId = taskType.taskTypeId) 
	AS source (taskTypeName,clientCode,workedItemNote,startedAtTime,endedAtTime,duration)
	ON (target.taskTypeName = source.taskTypeName
		AND target.clientCode = source.clientCode
		AND target.workedItemNote = source.workedItemNote
		AND target.startedAtTime = source.startedAtTime)

WHEN NOT MATCHED THEN
	INSERT (taskTypeName,clientCode,workedItemNote,startedAtTime,endedAtTime,duration)
	VALUES (source.taskTypeName,source.clientCode,source.workedItemNote,source.startedAtTime,source.endedAtTime,source.duration);

/* RESET DATA */
--TRUNCATE TABLE watt.worked