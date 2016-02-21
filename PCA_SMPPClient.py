#!/opt/Python-2.3/python

import sys
sys.path.insert(0,"/opt/Python-2.3/build/lib.hp-ux-B.11.00-9000/869-2.3")
import struct,time
import PCA_GenLib
import PCA_XMLParser
import PCA_ClientSocket


import PCA_SMPPMessage
import PCA_SMPPParser

				
########################################################		
## SMPP Client       				      ##
##						      ##
########################################################

class SMPPConnector(PCA_ClientSocket.Connector):

	def readSMPPMessage(self):
		try:
			Msg = "SMPPConnector init."
			PCA_GenLib.WriteLog(Msg,9)	
				
			response_data = None	
            		ResponseLen = self.readDataFromSocket(Length=4,TimeOut = 3.0,ReadAttempts = 1)
			
			if ResponseLen != None:
				msg_command_length = struct.unpack("!i",ResponseLen)[0]
			
				Msg = "SMPP PDU Header <command_length> = <%d>" % msg_command_length			
				PCA_GenLib.WriteLog(Msg,2)
			
				Msg = "read %d bytes data from socket" % (msg_command_length)
				PCA_GenLib.WriteLog(Msg,2)
		
				Message = self.readDataFromSocket(msg_command_length-4,TimeOut = 3.0,ReadAttempts = 1)	
				response_data = ResponseLen+Message
			
			Msg = "SMPPConnector OK"
			PCA_GenLib.WriteLog(Msg,9)
			
			return response_data
            		
		except:
			Msg = "SMPPConnector error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise		
			
	
	

########################################################		
## SMPP Client Class				      ##
##						      ##
########################################################
class SMPPClient:
	bind_receiver_pdu = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
	bind_receiver_resp_pdu = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x01)
	
	bind_transmitter_pdu = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x02)
	bind_transmitter_resp_pdu = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x02)
	
	submit_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x04) 
	deliver_sm_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x04) 		
	def __init__(self,XMLCFG):		
		try:	
			Msg = "Init SMPPClient ..."
			PCA_GenLib.WriteLog(Msg,9)	
			
			self.SMPPConnection = SMPPConnector(XMLCFG)
			self.SMPPConnection.connect()
			
			self.parser = PCA_SMPPParser.Parser()
			self.handler = PCA_SMPPParser.Handler()
			self.parser.setContentHandler(self.handler)
			
			Msg = "Init SMPPClient OK"
			PCA_GenLib.WriteLog(Msg,9)			
			
		except :
			Msg = "SMPPClient Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise
	
						
	def bind_transmitter(self,UID,PASSWD,TYPE):
		try:	
			Msg = "bind_transmitter init"
			PCA_GenLib.WriteLog(Msg,9)
			
			system_id = UID+chr(0x00)
			password = PASSWD+chr(0x00)
		
		
			system_type =TYPE+chr(0x00)
			
			
			
			#interface_version = chr(0x1)
			
			#addr_ton = chr(0x30)
			#addr_npi = chr(0x30)
			
			interface_version = chr(0x34)
			
			addr_ton = chr(0x01)
			addr_npi = chr(0x01)
			
			address_range = chr(0x01)+chr(0x00)
			#facilities_mask = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)
			
			
			self.SMPPWriter = PCA_SMPPMessage.SMPP_PDU_Writer(100) 	
			self.SMPPWriter.ConstructHeader(self.bind_transmitter_pdu)
		
			SMPP_PDU = self.SMPPWriter.ConstructParameter(system_id,password,system_type,interface_version,addr_ton,addr_npi,address_range)
			
			
 			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "-----------         Request          --------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			PCA_GenLib.WriteLog(Msg,0)
			self.parser.parse(SMPP_PDU)
			resp_data = self.handler.getHandlerResponse()
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
					
			#Msg = "send=\n%s" % PCA_GenLib.HexDump(SMPP_PDU)
			#PCA_GenLib.WriteLog(Msg,0)	
 			
 			self.SMPPConnection.sendDataToSocket(SMPP_PDU,TimeOutSeconds=0.5,WriteAttempts=1)			
 			Message =  self.SMPPConnection.readSMPPMessage()
 			
			#Msg = "recv=\n%s" % PCA_GenLib.HexDump(Message)
			#PCA_GenLib.WriteLog(Msg,0)
			
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "-----------         Response         --------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			self.parser.parse(Message)
			resp_data = self.handler.getHandlerResponse()
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			
									
 			status = struct.unpack("!i",Message[8:12])[0]
			if (status == 0):			
				Msg = "Status=<success>"
				PCA_GenLib.WriteLog(Msg,0)
				if self.bind_transmitter_resp_pdu == Message[4:8] :	
				
					Msg = "bind_transmitter Success"
					PCA_GenLib.WriteLog(Msg,0)
					
					Msg = "data=<%s>" % Message[16:]
					PCA_GenLib.WriteLog(Msg,0)
				else:
					Msg = "recv=\n%s" % PCA_GenLib.HexDump(Message[4:8])
					PCA_GenLib.WriteLog(Msg,0)
					Msg = "not a bind transmitter response"
					PCA_GenLib.WriteLog(Msg,0)
			else:
				Msg = "bind_transmitter Fail"
				PCA_GenLib.WriteLog(Msg,0)
				raise "bind Transmitter error"
				
			
			Msg = "bind Ok ..."
			PCA_GenLib.WriteLog(Msg,9)
			
			return 
		except :
			Msg = "bind_transmitter error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise	
			
			
						
	def bind_receiver(self,UID,PASSWD,TYPE):
		try:	
			Msg = "bind_receiver init"
			PCA_GenLib.WriteLog(Msg,9)
			
			system_id = UID+chr(0x00)
			password = PASSWD+chr(0x00)
		
		
			system_type =TYPE+chr(0x00)
			#interface_version = chr(0x1)
			
			#addr_ton = chr(0x30)
			#addr_npi = chr(0x30)
			
			interface_version = chr(0x34)
			
			addr_ton = chr(0x01)
			addr_npi = chr(0x01)
			
			address_range = chr(0x01)+chr(0x00)
			#facilities_mask = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)
			
			
			self.SMPPWriter = PCA_SMPPMessage.SMPP_PDU_Writer(100) 	
			
			self.SMPPWriter.ConstructHeader(self.bind_receiver_pdu)
		
			SMPP_PDU = self.SMPPWriter.ConstructParameter(system_id,password,system_type,interface_version,addr_ton,addr_npi,address_range)
			
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "-----------         Request          --------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			self.parser.parse(SMPP_PDU)
			resp_data = self.handler.getHandlerResponse()
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
		
			
			#Msg = "send=\n%s" % PCA_GenLib.HexDump(SMPP_PDU)
			#PCA_GenLib.WriteLog(Msg,0)	
 			
 			self.SMPPConnection.sendDataToSocket(SMPP_PDU,TimeOutSeconds=0.5,WriteAttempts=1)			
 			Message =  self.SMPPConnection.readSMPPMessage()
 			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "-----------         Response          --------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			self.parser.parse(Message)
			resp_data = self.handler.getHandlerResponse()
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			#Msg = "recv=\n%s" % PCA_GenLib.HexDump(Message)
			#PCA_GenLib.WriteLog(Msg,0)					
 				
			status = struct.unpack("!i",Message[8:12])[0]
			if (status == 0):
				if self.bind_receiver_resp_pdu == Message[4:8] :	
				
					Msg = "bind_receiver Success"
					PCA_GenLib.WriteLog(Msg,0)
					
					
					while 1:
						Msg = "wating message ................"
						PCA_GenLib.WriteLog(Msg,2)
						Message =  self.SMPPConnection.readSMPPMessage()
 						if Message != None:
							Msg = "recv=\n%s" % PCA_GenLib.HexDump(Message)
							PCA_GenLib.WriteLog(Msg,0)
							
							parser = PCA_SMPPParser.Parser()
							handler = PCA_SMPPParser.Handler()
							parser.setContentHandler(handler)
							Msg = "---------------------------------------------------------"
							PCA_GenLib.WriteLog(Msg,0)
							Msg = "-----------         Response          --------------------"
							PCA_GenLib.WriteLog(Msg,0)
							Msg = "---------------------------------------------------------"
							PCA_GenLib.WriteLog(Msg,0)
			
							parser.parse(Message)
							resp_data = handler.getHandlerResponse()
							if resp_data == "deliver_sm":
								self.SMPPWriter = PCA_SMPPMessage.SMPP_PDU_Writer(100) 	
			
								self.SMPPWriter.ConstructHeader(self.deliver_sm_resp)
								message_id = chr(0x00)
								SMPP_PDU = self.SMPPWriter.ConstructParameter(message_id)
			
								Msg = "---------------------------------------------------------"
								PCA_GenLib.WriteLog(Msg,0)
								Msg = "-----------         Request Response --------------------"
								PCA_GenLib.WriteLog(Msg,0)
								Msg = "---------------------------------------------------------"
								PCA_GenLib.WriteLog(Msg,0)
								self.parser.parse(SMPP_PDU)
								resp_data = self.handler.getHandlerResponse()
								Msg = "---------------------------------------------------------"
								PCA_GenLib.WriteLog(Msg,0)
								self.SMPPConnection.sendDataToSocket(SMPP_PDU,TimeOutSeconds=0.5,WriteAttempts=1)
								
								
							
							
							
				else:
					Msg = "recv=\n%s" % PCA_GenLib.HexDump(Message[4:8])
					PCA_GenLib.WriteLog(Msg,0)
					Msg = "not a bind receiver response"
					PCA_GenLib.WriteLog(Msg,0)
			else:
				Msg = "bind_transmitter Fail"
				PCA_GenLib.WriteLog(Msg,0)
				raise "bind Transmitter error"
				
			
			Msg = "bind Ok ..."
			PCA_GenLib.WriteLog(Msg,9)
			
			return 
		except :
			Msg = "bind_receiver error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise				
	
	def SubmitSM(self,SourceAddr,DestAddr,Text):
		try:	
			Msg = "SubmitSM ..."
			PCA_GenLib.WriteLog(Msg,9)
			
			
			# Src address english word TON,NPI = 5,0
			A_TON = chr(0x01)   
			A_NPI = chr(0x01)  
			
			
			B_TON = chr(0x1)  # FET
			B_NPI = chr(0x1)  # FET
			
			#TON = chr(0x05)  # CHT
			#NPI = chr(0x00)  # CHT
			#Textformat = chr(0x08) # Chinese
			Textformat = chr(0x00) # English
 			
 			
 			
 			
 			#[service_type][source_addr_ton][source_addr_npi][source_addr][dest_addr_ton][dest_addr_npi][dest_addr]
               		# var 6           int 1           int 1            var 21            int 1           int 1            var 21  
                	# 0x00                                                                          
                
                	#[esm_class][protocol_id][priority_flag]                                                                      
                	# int 1         int 1       int 	
                	#                 0x0       0x0         
                                                                                                     
                	#[schedule_delivery_time][validity_period][registered_delivery][replace_if_present_flag]                                                                                     
                	#    c-oct 17             var 17            int 1                    int 1      
                	#   0x00                  0x00              0x00                                 
                                                                                                
                                                                                                
                	#[data_coding][sm_default_msg_id][sm_length][short_message]                                                                                 
                	#  int 1              int          int 2       4k           
                	#  0xff              0x00                       
		
		
			self.SMPPWriter.ConstructHeader(self.submit_sm)
		
			#service_type = "VMA"+chr(0x00)
			service_type = chr(0x00)
			source_addr_ton = A_TON
			source_addr_npi = A_NPI
			#source_addr_ton = chr(0x05)
			#source_addr_npi = chr(0x00)  
			source_addr = SourceAddr+chr(0x00)
			#dest_addr_ton = chr(0x01)
			#dest_addr_npi = chr(0x01)	
			dest_addr_ton = B_TON
			dest_addr_npi = B_NPI
			dest_address = DestAddr+chr(0x00)
			esm_class = chr(0x00)
			protocol_id = chr(0x00)		
			priority_flag = chr(0x00)		
			schedule_delivery_time = chr(0x00)
			validity_period = chr(0x00)
			registered_delivery = chr(0x00)
			replace_if_present_flag = chr(0x00)
			#data_coding = chr(0x08)
			data_coding = Textformat
			sm_default_msg_id = chr(0x00)
			#MsgTxt = chr(0x4e)+chr(0x4b)+chr(0x5f)+chr(0x8c)
			short_message = Text
		
			sm_length =  chr(len(short_message))
		
		
			parm1 = service_type + source_addr_ton + source_addr_npi + source_addr
			parm2 = dest_addr_ton + dest_addr_npi + dest_address + esm_class + protocol_id + priority_flag
			parm3 = schedule_delivery_time + validity_period + registered_delivery
			#parm4 = sm_default_msg_id + sm_length + short_message
			parm4 =  replace_if_present_flag+ data_coding +sm_default_msg_id+sm_length + short_message
		
			SMPP_PDU = self.SMPPWriter.ConstructParameter(parm1,parm2,parm3,parm4)
 			
 			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "-----------         Request          --------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "recv=\n%s" % PCA_GenLib.HexDump(SMPP_PDU)
			PCA_GenLib.WriteLog(Msg,0)
			
			self.parser.parse(SMPP_PDU)
			resp_data = self.handler.getHandlerResponse()
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			
			
			
 			self.SMPPConnection.sendDataToSocket(SMPP_PDU,TimeOutSeconds=0.5,WriteAttempts=1)			
 			Message =  self.SMPPConnection.readSMPPMessage()
 			
			
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "-----------         Response         --------------------"
			PCA_GenLib.WriteLog(Msg,0)
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			self.parser.parse(Message)
			resp_data = self.handler.getHandlerResponse()
			Msg = "---------------------------------------------------------"
			PCA_GenLib.WriteLog(Msg,0)
			
			
 				
			#status =  self.SMPP_CMD.SMPPResponse(Message[0:4],Message[4:])
			#if (status == 0):
				#Msg = "Send A=<%s> , b=<%s> ,Status=<%s> , success" % (SourceAddr,DestAddr,status)
			#else:
				#Msg = "Send A=<%s> , b=<%s> ,Status=<%s> , error " % (SourceAddr,DestAddr,status)
			
			#PCA_GenLib.WriteLog(Msg,0)	
			
			Msg = "SubmitSM Ok ..."
			PCA_GenLib.WriteLog(Msg,9)
			
			return 
		except :
			Msg = "SubmitSM error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise				
				
					
	def unbind(self):
		try:	
			Msg = "unbind init..."
			PCA_GenLib.WriteLog(Msg,9)
		
			
			
			
			unbind = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x06) 
			self.SMPPWriter.ConstructHeader(unbind)		
		
			SMPP_PDU = self.SMPPWriter.ConstructParameter()		
			
			self.SMPPConnection.sendDataToSocket(SMPP_PDU,TimeOutSeconds=0.5,WriteAttempts=1)				
 			Message = self.SMPPConnection.readSMPPMessage()				
			status = struct.unpack("!i",Message[8:12])[0]
			if (status == 0):
				Msg = "unbind Success"
				PCA_GenLib.WriteLog(Msg,0)
					
			else:
				Msg = "unbind Fail"
				PCA_GenLib.WriteLog(Msg,0)
				raise "unbind Fail"
				
			Msg = "unbind Ok ..."
			PCA_GenLib.WriteLog(Msg,9)
			self.SMPPConnection.Close()
			return 
		except :
			Msg = "unbind error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise				


################################################################################################## 	  	
#####################            main program                        ############################
##################################################################################################   	
if __name__ == '__main__':
  
  try:	
  
	def TestSMPPClient(XMLCFG,SourceAddr,DestAddr,Text):
		try:
		
			print 'Start Program ...'
			PCA_GenLib.DBXMLCFGInit(XMLCFG)	
			
			try:			
				SMPP = SMPPClient(XMLCFG)
			
				system_id = 'pavel'			
				system_type = '1'
				Password = 'wpsd'
				
				SMPP.bind_transmitter(system_id,Password,system_type)
				
				
				#SMPP.bind_receiver(system_id,Password,system_type)
				
				SMPP.SubmitSM(SourceAddr,DestAddr,Text)
				
				SMPP.unbind()
			
				
			finally:			
				PCA_GenLib.CloseLog()

		except:
 	  		print 'PCA_SMPPClient.py uncaught ! < ',sys.exc_type,sys.exc_value,' >'
 	  		raise
  	####################################################################################
  	NumOfArg = len(sys.argv)
  	if NumOfArg < 4:
  		print "number of arg = <%s>\n" % NumOfArg
  		print "Usage : %s [A-Party] [B-Party] [Message Text] \n" % sys.argv[0]
  		raise "wrong argument"
  		
	(SourceAddr,DestAddr,Text) = (sys.argv[2],sys.argv[2],sys.argv[3])
  	print "Open cfg file"
	XMLCFG =  open("PCA_SMPPClient.cfg","r").read()
	
  	TestSMPPClient(XMLCFG,SourceAddr,DestAddr,Text)
 	
  except:
  	
 	#print "Msg = : <%s>,<%s>" % (sys.exc_type,sys.exc_value)
 	#import traceback
	#traceback.print_exc()
  	sys.exit()
 

