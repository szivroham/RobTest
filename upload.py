import sqlite3, json, os, base64

class DBConnection:
	def __entry__(self):
		self.conn = sqlite3.connect("ROB_2016.s3db")
		return conn.cursor()
		
	def __exit__(self):
		self.conn.commit()
		self.conn.close()

class Upload:
	def getTestFiles(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("""
			SELECT UT.UploadTestId,UT.File_URL,UT.FileName,UT.Extension,UT.Step_ExecutionId 
			FROM Uploads_Test AS UT 
			LEFT JOIN Step_Execution AS SE ON SE.Id=UT.Step_ExecutionId 
			WHERE SE.ExecutionId=? 
			AND StepId=?""",
			[kwargs['exeId'],kwargs['stepId']])
		result=c.fetchall()
		conn.commit()
		return result
		
	def saveTestFile(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("""
			INSERT INTO Uploads_Test 
			(Step_ExecutionId,File_URL,FileName,Extension) 
			VALUES (?,?,?,?)""",
			[kwargs['stepexeId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		conn.commit()
		c.execute("""
			SELECT * FROM Uploads_Test 
			WHERE Step_ExecutionId=? 
			AND File_URL=? 
			AND FileName=? 
			AND Extension=?""",
			[kwargs['stepexeId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		result = c.fetchone()
		conn.commit()
		return result
	
	def getTestFileURL(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT File_URL FROM Uploads_Test WHERE UploadTestId=?",[kwargs['fileId']])
		name=c.fetchone()
		conn.commit()
		return name[0]
	
	def deleteFileTest(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Uploads_Test WHERE UploadTestId=?",[kwargs['fileId']])
		conn.commit()
		return "success"
	
	def saveObjectFile(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Uploads_Object (ObjectId,File_URL,FileName,Extension) VALUES (?,?,?,?)",[kwargs['objectId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		conn.commit()
		c.execute("SELECT * FROM Uploads_Object WHERE ObjectId=? AND File_URL=? AND FileName=? AND Extension=?",[kwargs['objectId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		result = c.fetchone()
		conn.commit()
		return result
	
	def getObjectFileURL(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT File_URL FROM Uploads_Object WHERE UploadObjectId=?",[kwargs['fileId']])
		name=c.fetchone()
		conn.commit()
		return name[0]
		
	def deleteFileObject(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Uploads_Object WHERE UploadObjectId=?",[kwargs['fileId']])
		conn.commit()
		return "success"
	
	def nameExists(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		if kwargs['mode'] == "test":
			c.execute("SELECT * FROM Uploads_Test WHERE File_URL=?",[kwargs['path']])
			result=c.fetchone()
			conn.commit()
			if result == None:
				return kwargs['name']
			else:
				name=kwargs['name'].rsplit('.', 1)[0]+"-Copy"+kwargs['name'].rsplit('.', 1)[1]
				return UP.nameExists(path=os.path.join(kwargs['folder'], name),mode=kwargs['mode'],name=name,folder=kwargs['folder'])
		if kwargs['mode'] == "object":
			c.execute("SELECT * FROM Uploads_Object WHERE File_URL=?",[kwargs['path']])
			result=c.fetchone()
			conn.commit()
			if result == None:
				return kwargs['name']
			else:
				name=kwargs['name'].rsplit('.', 1)[0]+"-Copy."+kwargs['name'].rsplit('.', 1)[1]
				return UP.nameExists(path=os.path.join(kwargs['folder'], name),mode=kwargs['mode'],name=name,folder=kwargs['folder'])
		if kwargs['mode'] == "set":
			c.execute("SELECT * FROM Uploads_Set WHERE File_URL=?",[kwargs['path']])
			result=c.fetchone()
			conn.commit()
			if result == None:
				return kwargs['name']
			else:
				name=kwargs['name'].rsplit('.', 1)[0]+"-Copy."+kwargs['name'].rsplit('.', 1)[1]
				return UP.nameExists(path=os.path.join(kwargs['folder'], name),mode=kwargs['mode'],name=name,folder=kwargs['folder'])
		if kwargs['mode'] == "exe":
			c.execute("SELECT * FROM Uploads_Execution WHERE File_URL=?",[kwargs['path']])
			result=c.fetchone()
			conn.commit()
			if result == None:
				return kwargs['name']
			else:
				name=kwargs['name'].rsplit('.', 1)[0]+"-Copy."+kwargs['name'].rsplit('.', 1)[1]
				return UP.nameExists(path=os.path.join(kwargs['folder'], name),mode=kwargs['mode'],name=name,folder=kwargs['folder'])
		if kwargs['mode'] == "case":
			c.execute("SELECT * FROM Uploads_Case WHERE File_URL=?",[kwargs['path']])
			result=c.fetchone()
			conn.commit()
			if result == None:
				return kwargs['name']
			else:
				name=kwargs['name'].rsplit('.', 1)[0]+"-Copy."+kwargs['name'].rsplit('.', 1)[1]
				return UP.nameExists(path=os.path.join(kwargs['folder'], name),mode=kwargs['mode'],name=name,folder=kwargs['folder'])
		if kwargs['mode'] == "action" or kwargs['mode'] == "result":
			c.execute("SELECT * FROM Uploads_Step WHERE File_URL=?",[kwargs['path']])
			result=c.fetchone()
			conn.commit()
			if result == None:
				return kwargs['name']
			else:
				name=kwargs['name'].rsplit('.', 1)[0]+"-Copy."+kwargs['name'].rsplit('.', 1)[1]
				return UP.nameExists(path=os.path.join(kwargs['folder'], name),mode=kwargs['mode'],name=name,folder=kwargs['folder'])
		if kwargs['mode'] == "step":
			c.execute("SELECT * FROM Uploads_Step WHERE File_URL=?",[kwargs['path']])
			result=c.fetchone()
			conn.commit()
			if result == None:
				return kwargs['name']
			else:
				name=kwargs['name'].rsplit('.', 1)[0]+"-Copy."+kwargs['name'].rsplit('.', 1)[1]
				return UP.nameExists(path=os.path.join(kwargs['folder'], name),mode=kwargs['mode'],name=name,folder=kwargs['folder'])
		if kwargs['mode'] == "templates":
			c.execute("SELECT * FROM Uploads_Template WHERE File_URL=?",[kwargs['path']])
			result=c.fetchone()
			conn.commit()
			if result == None:
				return kwargs['name']
			else:
				name=kwargs['name'].rsplit('.', 1)[0]+"-Copy."+kwargs['name'].rsplit('.', 1)[1]
				return UP.nameExists(path=os.path.join(kwargs['folder'], name),mode=kwargs['mode'],name=name,folder=kwargs['folder'])
	
	def saveSetFile(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Uploads_Set (SetId,File_URL,FileName,Extension) VALUES (?,?,?,?)",[kwargs['setId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		conn.commit()
		c.execute("SELECT * FROM Uploads_Set WHERE SetId=? AND File_URL=? AND FileName=? AND Extension=?",[kwargs['setId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		result = c.fetchone()
		conn.commit()
		return result
	
	def getSetFileURL(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT File_URL FROM Uploads_Set WHERE UploadSetId=?",[kwargs['fileId']])
		name=c.fetchone()
		conn.commit()
		return name[0]
		
	def deleteFileSet(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Uploads_Set WHERE UploadSetId=?",[kwargs['fileId']])
		conn.commit()
		return "success"
	
	def saveExeFile(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Uploads_Execution (ExecutionId,File_URL,FileName,Extension) VALUES (?,?,?,?)",[kwargs['exeId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		conn.commit()
		c.execute("SELECT * FROM Uploads_Execution WHERE ExecutionId=? AND File_URL=? AND FileName=? AND Extension=?",[kwargs['exeId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		result = c.fetchone()
		conn.commit()
		return result
	
	def getExeFileURL(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT File_URL FROM Uploads_Execution WHERE UploadExeId=?",[kwargs['fileId']])
		name=c.fetchone()
		conn.commit()
		return name[0]
		
	def deleteFileExe(self,**kwargs):
		with DBConnection as cursor:
			cursor.execute("DELETE FROM Uploads_Execution WHERE UploadExeId=?",[kwargs['fileId']])
		return "success"
	
	def saveCaseFile(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Uploads_Case (CaseId,File_URL,FileName,Extension) VALUES (?,?,?,?)",[kwargs['caseId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		conn.commit()
		c.execute("SELECT * FROM Uploads_Case WHERE CaseId=? AND File_URL=? AND FileName=? AND Extension=?",[kwargs['caseId'],kwargs['url'],kwargs['filename'],kwargs['extension']])
		result = c.fetchone()
		conn.commit()
		return result
	
	def getCaseFileURL(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT File_URL FROM Uploads_Case WHERE UploadCaseId=?",[kwargs['fileId']])
		name=c.fetchone()
		conn.commit()
		return name[0]
		
	def deleteFileCase(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Uploads_Case WHERE UploadCaseId=?",[kwargs['fileId']])
		conn.commit()
		return "success"
		
	def saveStepFile(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Uploads_Step (File_URL,FileName,Extension,Status) VALUES (?,?,?,?)",[kwargs['url'],kwargs['filename'],kwargs['extension'],kwargs['status']])
		conn.commit()
		c.execute("SELECT * FROM Uploads_Step WHERE File_URL=? AND FileName=? AND Extension=? AND Status=?",[kwargs['url'],kwargs['filename'],kwargs['extension'],kwargs['status']])
		result = c.fetchone()
		conn.commit()
		return result
	
	def getStepFileURL(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT File_URL FROM Uploads_Step WHERE UploadStepId=?",[kwargs['fileId']])
		name=c.fetchone()
		conn.commit()
		return name[0]
		
	def deleteFileStep(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Uploads_Step WHERE UploadStepId=?",[kwargs['fileId']])
		conn.commit()
		return "success"
	
	def deleteFileStepUrl(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Uploads_Step WHERE File_URL=?",[kwargs['url']])
		conn.commit()
		return "success"
		
	def saveTemplatesFile(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("INSERT INTO Uploads_Template (File_URL,FileName,Extension,Status) VALUES (?,?,?,?)",[kwargs['url'],kwargs['filename'],kwargs['extension'],kwargs['status']])
		conn.commit()
		c.execute("SELECT * FROM Uploads_Template WHERE File_URL=? AND FileName=? AND Extension=? AND Status=?",[kwargs['url'],kwargs['filename'],kwargs['extension'],kwargs['status']])
		result = c.fetchone()
		conn.commit()
		return result
	
	def getTemplateFileURL(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT File_URL FROM Uploads_Template WHERE UploadTemplateId=?",[kwargs['fileId']])
		name=c.fetchone()
		conn.commit()
		return name[0]
		
	def getTemplateFile(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Uploads_Template WHERE UploadTemplateId=?",[kwargs['fileId']])
		name=c.fetchone()
		conn.commit()
		return name
	
	def getTemplates(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Uploads_Template")
		name=c.fetchall()
		conn.commit()
		return name
	
	def deleteFileTemplate(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Uploads_Template WHERE UploadTemplateId=?",[kwargs['fileId']])
		conn.commit()
		return "success"
	
	def deleteFileTemplateUrl(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("DELETE FROM Uploads_Template WHERE File_URL=?",[kwargs['url']])
		conn.commit()
		return "success"
		
	def deleteAllTemplates(self,**kwargs):
		conn= sqlite3.connect("ROB_2016.s3db")
		c = conn.cursor()
		c.execute("SELECT * FROM Uploads_Template WHERE Status!=0")
		result=c.fetchall()
		conn.commit()
		for k in result:
			c.execute("DELETE FROM Uploads_Template WHERE UploadTemplateId=?",[k[0]])
			conn.commit()
		return result
	
UP = Upload()