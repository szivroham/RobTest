import sqlite3

class Database:
	def login_querry(self, **kwargs):
		
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT COUNT(*) FROM Users WHERE UserName = ? AND UserPassword= ?",[kwargs['title'],kwargs['pw']])
		result=c.fetchone()
		return result[0]
		
	def get_execution(self,**kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT Name FROM Execution")
		result=c.fetchone()
	#-----case page-----	
	def get_case(self):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT CaseId,Title FROM Cases")
		result=c.fetchall()
		return result
	
	def save_case(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Cases (Title,Priority,Data) VALUES (?,?,?)",[kwargs['title'],kwargs['priority'],kwargs['data']])
		conn.commit()
		c.execute("SELECT CaseId FROM Cases WHERE Title=? AND Priority=? AND Data=?",[kwargs['title'],kwargs['priority'],kwargs['data']])
		CaseID=c.fetchone()
		return CaseID[0]
		
	def save_steps(self, **kwargs):
		step=[]
		actions=kwargs['action'];
		results=kwargs['result'];
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		for k,l in zip(actions,results):
			c.execute("INSERT INTO Steps (Action,Result) VALUES (?,?)",[k,l])
			conn.commit()
			c.execute("SELECT StepId FROM Steps WHERE Action=? AND Result=?",[k,l])
			stepID=c.fetchone()
			#print(stepID)
			step.append(stepID[0])
		for k in step:
			c.execute("INSERT INTO Case_Step (CaseId,StepId) VALUES (?,?)",[kwargs['id'],k])
			conn.commit()
	
	def get_case_parameters(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Cases WHERE CaseId=?",[kwargs['id']])
		result=c.fetchall()
		return result
	
	def get_step_parameters(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT StepId FROM Case_Step WHERE CaseId=?",[kwargs['id']])
		result=c.fetchall()
		case_parameter = []
		for k in result:
			c.execute("SELECT * FROM Steps WHERE StepId=?",[k[0]])
			case_parameter.append(c.fetchone())
		print(result)
		return case_parameter
	
	def deleteCase(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Cases WHERE CaseId=?",[kwargs['id']])
		conn.commit()
		c.execute("SELECT StepId FROM Case_Step WHERE CaseId=?",[kwargs['id']])
		result=c.fetchall()
		conn.commit()
		c.execute("DELETE FROM Case_Step WHERE CaseId=?",[kwargs['id']])
		conn.commit()
		for k in result:
			c.execute("DELETE FROM Steps WHERE StepId=?",[k[0]])
			conn.commit()
	
	def updateCase(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("UPDATE Cases SET Title=?,Priority=?,Data=? WHERE CaseId=?",[kwargs['title'],kwargs['priority'],kwargs['data'],kwargs['caseId']])
		conn.commit()
	
	def updateStep(self, **kwargs):
		step=[]
		actions=kwargs['action'];
		results=kwargs['result'];
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Case_Step WHERE CaseId=?",[kwargs['caseId']])
		stepID=c.fetchall()
	
	#-----object-----
	def get_object(self, active=None, owner=None, search=None, **kwargs):
		args = []
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT ObjectId,ObjectName FROM Objects",args)
		result=c.fetchall()
		return result
	
	def save_object(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Objects (ObjectName,ObjectHardware,ObjectDesc) VALUES (?,?,?)",[kwargs['name'],kwargs['hardware'],kwargs['desc']])
		conn.commit()
		c.execute("SELECT ObjectId FROM Objects WHERE ObjectName=? AND ObjectHardware=? AND ObjectDesc=?",[kwargs['name'],kwargs['hardware'],kwargs['desc']])
		CaseID=c.fetchone()
		return CaseID[0]
	
	def get_object_parameters(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Objects WHERE ObjectId=?",[kwargs['id']])
		result=c.fetchall()
		return result
	
	def deleteObject(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Objects WHERE ObjectId=?",[kwargs['id']])
		conn.commit()
	
	#-----set-----
	def get_set(self, active=None, owner=None, search=None):
		args = []
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT SetId,SetName FROM Sets",args)
		result=c.fetchall()
		return result
	
	def save_set(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Sets (SetName,SetDate,SetPriority) VALUES (?,?,?)",[kwargs['name'],kwargs['date'],kwargs['priority']])
		conn.commit()
		c.execute("SELECT SetId FROM Sets WHERE SetName=?",[kwargs['name']])
		CaseID=c.fetchone()
		return CaseID[0]
	
	def saveSetCase(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		for k in kwargs['ID']:
			c.execute("INSERT INTO Set_Case (SetId,CaseId) VALUES (?,?)",[kwargs['setID'],k])
			conn.commit()
	
	def get_set_parameters(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Sets WHERE SetId=?",[kwargs['id']])
		result=c.fetchall()
		return result
	
	def getSetCases(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT CaseId FROM Set_Case WHERE SetId=?",[kwargs['id']])
		result=c.fetchall()
		conn.commit()
		cases = []
		for k in result:
			c.execute("SELECT * FROM Cases WHERE CaseId=?",[k[0]])
			cases.append(c.fetchone())
		return cases
	
	def deleteSet(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Sets WHERE SetId=?",[kwargs['id']])
		conn.commit()
	
	#-----execution-----
	def getExecution(self, active=None, owner=None, search=None):
		args=[]
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT ExecutionId,ExeName FROM Execution",args)
		result=c.fetchall()
		return result
		
	def saveExe(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		#c.execute("INSERT INTO Execution (ExeName,ExeDate) VALUES (?,?)",[kwargs['name'],kwargs['date']])
		c.execute("INSERT INTO Execution (ExeName) VALUES (?)",[kwargs['name']])
		conn.commit()
		c.execute("SELECT ExecutionId FROM Execution WHERE ExeName=?",[kwargs['name']])
		ExeID=c.fetchone()
		conn.commit()
		c.execute("INSERT INTO Exe_Object (ExecutionId,ObjectId) VALUES (?,?)",[ExeID[0],kwargs['testObject']])
		conn.commit()
		return ExeID[0]
	
	def saveCaseExe(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		print(kwargs['ID'])
		for k in kwargs['ID']:
			print(k)
			c.execute("SELECT Title FROM Cases WHERE CaseId=?",[k])
			CaseTitle=c.fetchone()
			c.execute("INSERT INTO Case_Execution (ExecutionId,CaseId,Result,title) VALUES (?,?,?,?)",[kwargs['exeID'],k,"NOTRUN",CaseTitle[0]])
			conn.commit()
			c.execute("SELECT Id FROM Case_Execution WHERE ExecutionId=? AND CaseId=? AND title=?",[kwargs['exeID'],k,CaseTitle[0]])
			ID=c.fetchone()
			c.execute("SELECT StepId FROM Case_Step WHERE CaseId=?",[k])
			StepId=c.fetchall()
			print(ID)
			print(StepId)
			for l in StepId:
				c.execute("INSERT INTO Step_Execution (StepId,ExecutionId,Case_ExecutionId,Result) VALUES (?,?,?,?)",[l[0],kwargs['exeID'],ID[0],"NOTRUN"])
				conn.commit()
		return
		
	def getExeParameters(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Execution WHERE ExecutionId=?",[kwargs['id']])
		result=c.fetchall()
		return result
	
	def getExeObject(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT ObjectId FROM Exe_Object WHERE ExecutionId=?",[kwargs['id']])
		ObjectId=c.fetchone()
		conn.commit()
		c.execute("SELECT * FROM Objects WHERE ObjectId=?",[ObjectId[0]])
		Object=c.fetchone()
		return Object
	
	def getExeCases(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Case_Execution WHERE ExecutionId=?",[kwargs['id']])
		result=c.fetchall()
		conn.commit()
		cases = []
		for k in result:
			c.execute("SELECT * FROM Cases WHERE CaseId=?",[k[2]])
			cases.append(c.fetchone()+(k[3],))
		return cases
	
	def getExeFromCases(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Case_Execution WHERE ExecutionId=?",[kwargs['id']])
		result=c.fetchall()
		conn.commit()
		return result
	
	def deleteExe(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Execution WHERE ExecutionId=?",[kwargs['id']])
		conn.commit()
		c.execute("DELETE FROM Case_Execution WHERE ExecutionId=?",[kwargs['id']])
		conn.commit()
		c.execute("DELETE FROM Exe_Object WHERE ExecutionId=?",[kwargs['id']])
		conn.commit()
	
	def getStatusFromStepExe(self, **kwargs):
		conn = sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT Id FROM Case_Execution WHERE ExecutionId=? AND CaseId=?",[kwargs['exeId'],kwargs['caseId']])
		caseExeId=c.fetchall()
		conn.commit()
		print(caseExeId)
		c.execute("SELECT Result,Comment FROM Step_Execution WHERE Case_ExecutionId=?",[caseExeId[0][0]])
		result=c.fetchall()
		conn.commit()
		print(result)
		return result
	
	#-----test-----
	def saveSetStatus(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("UPDATE Step_Execution SET Result=? WHERE StepId=? AND ExecutionId=?",[kwargs['status'],kwargs['stepId'],kwargs['caseExeId']])
		conn.commit()
	
	def saveCaseStatus(self, **kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT Id FROM Case_Execution WHERE ExecutionId=? AND CaseId=?",[kwargs['exeId'],kwargs['caseId']])
		caseExeId=c.fetchall()
		conn.commit()
		c.execute("SELECT Result FROM Step_Execution WHERE ExecutionId=? AND Case_ExecutionId=?",[kwargs['exeId'],caseExeId[0][0]])
		Results=c.fetchall()
		conn.commit()
		print('result:')
		print(Results)
		for k in Results:
			if k[0] == "FAILED":
				c.execute("UPDATE Case_Execution SET Result=? WHERE ExecutionId=? AND CaseId=?",["FAILED",kwargs['exeId'],kwargs['caseId']])
				conn.commit()
				return "FAILED"
			if k[0] == "NOTRUN":
				c.execute("UPDATE Case_Execution SET Result=? WHERE ExecutionId=? AND CaseId=?",["NOTRUN",kwargs['exeId'],kwargs['caseId']])
				conn.commit()
				return "NOTRUN"
			if k[0] == "NOTIMP":
				c.execute("UPDATE Case_Execution SET Result=? WHERE ExecutionId=? AND CaseId=?",["NOTIMP",kwargs['exeId'],kwargs['caseId']])
				conn.commit()
				return "NOTIMP"
		c.execute("UPDATE Case_Execution SET Result=? WHERE ExecutionId=? AND CaseId=?",["RUN",kwargs['exeId'],kwargs['caseId']])
		conn.commit()
		return "RUN"
		
DB = Database()