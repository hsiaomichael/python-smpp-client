

import sys,string,struct
import PCA_GenLib
import PCA_Parser
import PCA_XMLParser


##############################################################################
###    Message Handler   	
##############################################################################
class Handler(PCA_Parser.ContentHandler):	
	
	
	command_status_ESME_ROK = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00) 
	command_status_ESME_RINVMSGLEN = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01) 
	command_status_ESME_RINVCMDLEN = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x02) 
	command_status_ESME_RINVCMDID = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x03) 
	command_status_ESME_RINVBNDSTS = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x04) 
	command_status_ESME_RALYBND = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x05) 
	command_status_ESME_ESME_RINVPRTFLG = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x06) 
	
	command_status_ESME_RSYSERR = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x08) 
	command_status_ESME_RINVMSGLEN = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x09) 
	
	command_status_ESME_RINVSRCADR = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x0a) 
	command_status_ESME_RINVDSTADR = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x0b) 
	
	command_status_ESME_RINVPASWD = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x0e) 
	command_status_ESME_ESME_RINVSYSID = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x0f) 
	command_status_ESME_RSUBMITFAIL = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x45) 
	
	
	 
	
	Command_Status_Message = {}
	Command_Status_Message[command_status_ESME_ROK] = 'No Error - ESME_ROK'
	Command_Status_Message[command_status_ESME_RINVMSGLEN] = 'Message Length is invalid - ESME_RINVMSGLEN'
	Command_Status_Message[command_status_ESME_RINVCMDLEN] = 'Command Length is invalid - ESME_RINVCMDLEN'
	Command_Status_Message[command_status_ESME_RINVCMDID] = 'Invalid Command ID - ESME_RINVCMDID'
	Command_Status_Message[command_status_ESME_RINVBNDSTS] = 'Incorrect BIND Status for given command - ESME_RINVBNDSTS'
	Command_Status_Message[command_status_ESME_RALYBND] = 'ESME Already in Bound State - ESME_RALYBND'
	Command_Status_Message[command_status_ESME_ESME_RINVPRTFLG] = 'Invalid Priority Flag - ESME_ESME_RINVPRTFLG'
	
	Command_Status_Message[command_status_ESME_RSYSERR] = 'System Error - ESME_RSYSERR'
	
	Command_Status_Message[command_status_ESME_RINVSRCADR] = 'Invalid Source Address - ESME_RINVSRCADR'
	Command_Status_Message[command_status_ESME_RINVDSTADR] = 'Invalid Dest Addr - command_status_ESME_RINVDSTADR'
	Command_Status_Message[command_status_ESME_RINVPASWD] = 'Invalid Password - ESME_RINVPASWD'
	Command_Status_Message[command_status_ESME_ESME_RINVSYSID] = 'Invalid System ID - ESME_RINVSYSID'
	
	Command_Status_Message[command_status_ESME_RSUBMITFAIL] = 'submit_sm or submit_multi failed - ESME_RSUBMITFAIL'

	
 	def __init__(self):
		PCA_Parser.ContentHandler.__init__(self)
		self.Message = ''
		
		
	def startDocument(self):
	       self.ExtraSocketData = ''
	       self.status_code = 'na'
	

 	
 	def startElement(self, name, attrs):
		
        	try:
        		
        		Msg = "startElement Init "
			PCA_GenLib.WriteLog(Msg,9)
			
			Msg = "%s=<%s>" % (name ,attrs)
			PCA_GenLib.WriteLog(Msg,2)
			
			if name == "command status":	
				try:
					data = self.Command_Status_Message[attrs]
				except:
					data = 'Unknow Error'
				self.status_code = hex(struct.unpack("!i",attrs)[0])
				self.Message = data
			
			#self.Message = "<%s>=<%s>,%s" % (name,attrs,self.Message)
			
			Msg = "startElement OK"
			PCA_GenLib.WriteLog(Msg,9)
        		
        	
        	except:
        		Msg = "startElement Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise


	def endDocument(self,Message):
        	try:
        		
        		x=1
        		
        	
        	except:
        		Msg = "startElement Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise

      	
   	
	def getHandlerResponse(self):	
		try:
			Msg = "getHandlerResponse Init "
			PCA_GenLib.WriteLog(Msg,9)
			
			Msg = "data=<%s>" % self.Message
			PCA_GenLib.WriteLog(Msg,3)
			
			Msg = "getHandlerResponse OK"
			PCA_GenLib.WriteLog(Msg,9)
			
			
			return self.Message
			
		except:
			Msg = "getHandlerResponse  error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise								
							
	def getCommandStatus(self):	
		try:
			
			
			return  self.status_code 
			
		except:
			Msg = "getCommandStatus  error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise								
					

						

#########################################################################
# 
#
#########################################################################
class Parser(PCA_Parser.Parser):
	
	
	
	bind_receiver = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
	bind_receiver_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x01)
	bind_transmitter = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x02)
	bind_transmitter_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x02)
	outbind = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x0b) 
	unbind = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x06) 
	unbind_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x06) 
	submit_sm = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x04) 
	submit_sm_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x04) 
	deliver_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x05) 
	deliver_sm_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x05) 
	
	query_sm = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x03) 
	query_sm_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x03) 
	cancel_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x08) 
	cancel_sm_resp =chr(0x80)+chr(0x0)+chr(0x00)+chr(0x08) 
	replace_sm =  chr(0x00)+chr(0x0)+chr(0x00)+chr(0x07) 
	replace_sm_resp=  chr(0x80)+chr(0x0)+chr(0x00)+chr(0x07) 
	enquire_link =  chr(0x00)+chr(0x0)+chr(0x00)+chr(0x0a) 
	enquire_link_resp =  chr(0x80)+chr(0x0)+chr(0x00)+chr(0x0a) 
 	generic_nack =  chr(0x80)+chr(0x00)+chr(0x00)+chr(0x00) 
	
	command_id_dict = {}
 	command_id_dict[bind_receiver] = 'bind_receiver'
 	command_id_dict[bind_receiver_resp] = 'bind_receiver_resp'
 	command_id_dict[bind_transmitter] = 'bind_transmitter'
 	command_id_dict[bind_transmitter_resp] = 'bind_transmitter_resp'
 	command_id_dict[submit_sm] = 'submit_sm'
 	command_id_dict[submit_sm_resp] = 'submit_sm_resp'
 	command_id_dict[query_sm] = 'query_sm'
 	command_id_dict[query_sm_resp] = 'query_sm_resp'
 	
 	command_id_dict[deliver_sm] = 'deliver_sm'
 	command_id_dict[deliver_sm_resp] = 'deliver_sm_resp'
 	command_id_dict[enquire_link] = 'enquire_link'
 	command_id_dict[enquire_link_resp] = 'enquire_link_resp'
 	

 	message_state_enroute =  chr(0x01)
 	message_state_delivered =  chr(0x02)
 	message_state_expired =  chr(0x03)
 	message_state_deleted =  chr(0x04)
 	message_state_undeliverable =  chr(0x05)
 	message_state_accepted =  chr(0x06)
 	message_state_unknown =  chr(0x07)
 	message_state_rejected =  chr(0x08)

	message_state_dict = {}
 	message_state_dict[message_state_enroute] = 'enroute'
 	message_state_dict[message_state_delivered] = 'delivered'
 	message_state_dict[message_state_expired] = 'expired'
 	message_state_dict[message_state_deleted] = 'deleted'
 	message_state_dict[message_state_undeliverable] = 'undeliverable'
 	message_state_dict[message_state_accepted] = 'accepted'
 	message_state_dict[message_state_unknown] = 'unknown'
 	message_state_dict[message_state_rejected] = 'rejected'
 	
 	message_error_code_no_error =  0
 	message_error_code_undef_subscriber_at_msc =  5
 	message_error_code_call_barred =  13
 	message_error_code_abscent_subscriber =  60
 	message_error_code_abscent_subscriber_gprs_detached =  67
	message_error_code = {}
	message_error_code[message_error_code_no_error] = "no error"
	message_error_code[message_error_code_undef_subscriber_at_msc] = "undef_subscriber_at_msc"
	message_error_code[message_error_code_call_barred] = "call barred"
	message_error_code[message_error_code_abscent_subscriber] = "abscent subscriber"
	message_error_code[message_error_code_abscent_subscriber_gprs_detached] = "abscent subscriber gprs detached"
 	
			
	def set_handler(self,name,attrs,content):			
		self._cont_handler.startElement(name, attrs)        		
		self._cont_handler.characters(content)
        	self._cont_handler.endElement(name)
	
	def parse(self, source):
		try:
			Msg = "parser init"
			PCA_GenLib.WriteLog(Msg,9)	
			
			#Msg = "orig data =\n%s" % PCA_GenLib.HexDump(orig_data)
			#PCA_GenLib.WriteLog(Msg,0)	
			
			
			data = source[0:4]
			name = "command length"	
			attrs = struct.unpack("!i",data)[0]
			content = attrs
			self.set_handler(name,attrs,content)
			
			data = source[4:8]
			name = "command id"	
			attrs = self.command_id_dict[data]
       			command_id = attrs
			content = attrs
			self.set_handler(name,attrs,content)
			
			data = source[8:12]
			name = "command status"	
			
			attrs = data
			content = attrs
			self.set_handler(name,attrs,content)
			
			data = source[12:16]
			name = "sequence number"	
			attrs = struct.unpack("!i",data)[0]
			content = attrs
			self.set_handler(name,attrs,content)
			

			data = source[16:]
			name = "PDU Body"	
			attrs = data
			content = attrs
			self.set_handler(name,attrs,content)
			Msg = "Body =\n%s" % PCA_GenLib.HexDump(data)
			PCA_GenLib.WriteLog(Msg,2)	

       			if (command_id == "query_sm_resp"):
				try:
                        		message_state = self.message_state_dict[data[-2]]
				except:
                        		message_state = "unknown message state"
					Msg = "Body =\n%s" % PCA_GenLib.HexDump(data)
					PCA_GenLib.WriteLog(Msg,0)	

				try:
                        		#error_code = self.message_error_code[ord(data[-1])]
                        		error_code = self.message_error_code[ord(data[-1])]
				except:
                        		error_code = "unknown error code "
					Msg = "Body =\n%s" % PCA_GenLib.HexDump(data)
					PCA_GenLib.WriteLog(Msg,0)	

				Msg = "QuerySM Response : message_state = <%s>,error_code=<%s>" % (message_state,error_code)
				PCA_GenLib.WriteLog(Msg,2)	
				print Msg

       			elif (command_id == "submit_sm_resp"):
				#Msg = "Body =\n%s" % PCA_GenLib.HexDump(data)
				Msg = "msg id =<%s>" % data 
				PCA_GenLib.WriteLog(Msg,1)	
				print Msg
			
			self._cont_handler.endDocument(source)
        		
			Msg = "parser OK"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser  :<%s>,<%s>,name=<%s>" % (sys.exc_type,sys.exc_value,name)
			PCA_GenLib.WriteLog(Msg,0)
			
			
			raise
	        		
	    
	  	     
