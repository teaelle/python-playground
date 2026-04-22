/* 
*************
RUN ONLY ONCE
*************
*/

CREATE DATABASE WATTapplication;

USE WATTapplication

CREATE SCHEMA WATT;

CREATE TABLE WATT.taskType (
	taskTypeId INT PRIMARY KEY NOT NULL IDENTITY(1,1),
	taskTypeName VARCHAR(50),
	taskTypeHexColor VARCHAR(6)
)

--DROP TABLE WATT.taskType
--TRUNCATE TABLE watt.taskType
INSERT INTO WATT.taskType (taskTypeName,taskTypeHexColor)
VALUES
('Files','00C389'),
('Data Inquiries','FFB81C'),
('Email','00A0D2'),
('Call','DDD0CF'),
('Review','D9E6DC'),
('Misc. Client Work','D8DBD8'),
('Meeting','D8D7DF'),
('Break','D9E6DC'),
('Training/Shadowing','702082'),
('Chat/Questions','EFEEDE'),
('Misc. Non-Client','C8D7DF'),
('Fallouts','D8DBD8'),
('JIRA','D8DBD8'),
('CDSR','D8DBD8'),
('DRR','D8DBD8'),
('SQL/Reporting','C70039'),
('Project/Documentation','C110A0'),
('Project/Coding','C8D7DF'),
('Project/Misc','D8DBD8'),
('Leveling(PS,Read)','D8DBD8'),
('Non-Work,IT/Comp','D8DBD8');


--DROP TABLE WATT.worked
--TRUNCATE TABLE watt.worked
CREATE TABLE watt.worked (
	workedItemId INT PRIMARY KEY NOT NULL IDENTITY(1,1),
	taskTypeId INT,
	clientCode VARCHAR(10),
	workedItemNote VARCHAR(100), 
	startedAtTime SMALLDATETIME,
	endedAtTime SMALLDATETIME,
	FOREIGN KEY (taskTypeId) REFERENCES WATT.taskType (taskTypeId)
)

--DROP TABLE WATT.settings
CREATE TABLE WATT.settings (
	username VARCHAR(10) PRIMARY KEY, 
	backgroundColor VARCHAR(10),
)

SELECT * FROM WATT.taskType;

SELECT * FROM WATT.worked;


CREATE TABLE watt.clientCodeList (
	clientCodeOption VARCHAR(4)
)

INSERT INTO watt.clientCodeList 
VALUES
('4460'),
('4420'),
('watt')


/* STORED PROCEDURE  */

/*DURATION TRIGGER*/


/* VIEW: INQ / FALLOUT REVIEW REPORT TEMPLATE */
--DROP VIEW watt.V_TrackingReports
CREATE VIEW watt.V_TrackingReports AS
SELECT 
	taskType.taskTypeName,
	worked.clientCode AS CODE, 
	CAST(worked.startedAtTime AS DATE) AS dateWorked,
	FORMAT(worked.startedAtTime, 'hh:mm tt', 'en-US') AS StartTimeForDisplay,
	FORMAT(worked.endedAtTime, 'hh:mm tt', 'en-US') AS EndTimeForDisplay,
	CASE 
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 5
			THEN '5 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 10
			THEN '10 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)  <= 15
			THEN '15 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)  <= 20
			THEN '20 min'
		WHEN (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 25
			THEN '25 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 30
			THEN '30 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 45
			THEN '45 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 60
			THEN '60 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 75
			THEN '75 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 90
			THEN '90 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 120
			THEN '120 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) < 150
			THEN '150 min'
		WHEN  endedAtTime IS NULL 
			THEN CONCAT((CAST(FORMAT(GETDATE() - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(GETDATE() - startedAtTime, 'mm', 'en-US') as int),'+' )
		ELSE 
			'unknown'
	END AS timeWorkedForDisplay,
	'Tamilyn Peck' AS analystNameForDisplay
FROM 
	WATT.worked 
	INNER JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE 
	taskType.taskTypeName IN ('Data Inquiries','Call')
	--AND CAST(worked.startedAtTime AS DATE) BETWEEN '2019-04-26' AND '2019-05-02'

/* VIEW: Durations Report */
--DROP VIEW watt.V_trackingReport
CREATE VIEW watt.V_trackingReport AS
SELECT 
	worked.clientCode AS CODE, 
	CAST(worked.startedAtTime AS DATE) AS dateWorked,
	FORMAT(worked.startedAtTime, 'hh:mm tt', 'en-US') AS StartTimeForDisplay,
	FORMAT(worked.endedAtTime, 'hh:mm tt', 'en-US') AS EndTimeForDisplay,
	CASE 
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 5
			THEN '5 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 10
			THEN '10 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)  <= 15
			THEN '15 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)  <= 20
			THEN '20 min'
		WHEN (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 25
			THEN '25 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 30
			THEN '30 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 45
			THEN '45 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 60
			THEN '60 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 75
			THEN '75 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 90
			THEN '90 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 120
			THEN '120 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) < 150
			THEN '150 min'
		WHEN  endedAtTime IS NULL 
			THEN CONCAT((CAST(FORMAT(GETDATE() - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(GETDATE() - startedAtTime, 'mm', 'en-US') as int),'+' )
		ELSE 
			'unknown'
	END AS timeWorkedForDisplay,
	'Tamilyn Peck' AS analystNameForDisplay,
	FORMAT(endedAtTime - startedAtTime, 'HH:mm:ss', 'en-US') as realDurantionInTime,
	(CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) as realDurationInMinutes
FROM 
	WATT.worked 
	INNER JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId