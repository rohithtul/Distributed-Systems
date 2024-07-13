from threading import *
from time import *
from socket import *
import schedule
import threading

    
class  Process(Thread):

    def __init__(self,port,ltoa):
        Thread.__init__(self)
        #Thread.daemon=True
        self.ltoa=ltoa
        self.port=port
        self.host = gethostname()
        self.start()
        
    def run(self):
        while(True):
            try:        
                self.soc = socket(AF_INET, SOCK_STREAM)
                self.soc.connect((self.host,self.port))
                self.ltoa.processcount=self.ltoa.processcount+1  
                break
            except Exception as e:
                 print("wating to connect to the port: ",self.port)
                 #print("Error:",e)
            sleep(5)


class  VectorTotalOrderAlgorithm(Thread):
    
    def __init__(self,pid):
        Thread.__init__(self)
        #Thread.daemon=True
        self.pid=pid
        self.processcount=0                      
        self.timestamp=0  
        self.vectorclock=[0,0,0]                     
        self.deliveryevents = {}
        self.eventbuffer=[]
        self.respacknowledge=[]
        self.ProcessEvents=["Open File","Write Data","Close File"]
        

    def getVectorClock(self):
         return str(self.vectorclock[0])+","+str(self.vectorclock[1])+","+str(self.vectorclock[2])

    def compareAndUpdateLogicalClock(self,vectclock):
        self.timestamp=self.timestamp+1
        self.vectorclock[2]=self.timestamp
        for i in range(3):
          if(self.vectorclock[i]< vectclock[i]):
             self.vectorclock[i]= vectclock[i]
    
 
    def setProcess1(self,process1):
        #print("Process counter:",self.processcount)
        self.process1=process1

    def  setProcess2(self,process2):
        #print("Process counter:",self.processcount)
        self.process2=process2 
        print("processes started at (",self.pid ,")")
        self.start()

            
    def run(self):
        
        print("process event order starting")
        try:
          self.timestamp=self.vectorclock[2]    
          for event in self.ProcessEvents:
                  print(event)
                  self.timestamp=self.timestamp+1
                  self.vectorclock[2]=self.timestamp
                  
                  msg=self.pid+","+event+","+self.getVectorClock()
                  self.process1.soc.sendall(msg.encode())

                  pmsg1=self.process1.soc.recv(1024)
                  self.respacknowledge.append(pmsg1.decode('utf-8'))
                  print(f"Delivery of {self.pid} : {pmsg1.decode('utf-8')}, vc{[self.getVectorClock()]}")

                  self.timestamp=self.timestamp+1
                  self.vectorclock[2]=self.timestamp
                  msg=self.pid+","+event+","+self.getVectorClock()
                  self.process2.soc.sendall(msg.encode())

                  pmsg2=self.process2.soc.recv(1024)
                  self.respacknowledge.append(pmsg2.decode('utf-8'))

                  print(f"Delivery of {self.pid} : {pmsg2.decode('utf-8')}, vc{[self.getVectorClock()]}")          
                  self.timestamp=self.timestamp+1
                  self.vectorclock[2]=self.timestamp
                  
                  print(f"Delivery of {self.pid} : {self.pid}.{event[0]}, vc{[self.getVectorClock()]}")
        except Exception as e:
            print(f"Error in event multi casting:{e}")
        
    def maintainBufferAndAcknowledge(self,socconn):
            try:
                 while(True):
                      #print("maintainbuffer",socconn)
                      msgdeliver=socconn.recv(1024)
                      msg=msgdeliver.decode('utf-8').split(",")
                      #pid, event, vc[0], vc[1], vc[2]
                      updatevectclock=[int(msg[2]),int(msg[3]),int(msg[4])]
                      self.deliveryevents[msg[0]+"."+msg[1][0]]= msgdeliver 
                      self.eventbuffer.append(msg[1])    #adding  events to eventbuffer
                      self.compareAndUpdateLogicalClock(updatevectclock);
                      mesg=self.pid+"."+msg[1][0]
                      socconn.sendall(mesg.encode())
                                          
                      # while loop closing
            except Exception as e:
                  print("maintain buffer and acknowledgement error:",e)



def mainThread():
      try:
             host = gethostname()    
             port = 8883
             #-------process1 and process2 request accepting--------------
             #print("hostname:",host)
             #print("port:",port)
             conarg=[]
             with socket(AF_INET, SOCK_STREAM) as s:
                  s.bind((host, port))
                  s.listen(3)
                  while(True):
                     conn, addr = s.accept()
                     #print(conn)
                     conarg.append([conn,addr])
                     #ltoa.maintainBufferAndAcknowledge(conn)
                     xt = Thread(target=ltoa.maintainBufferAndAcknowledge, args=(conn,))
                     xt.start()
                     #print("Thread started")

      except Exception as e:
           print("Error in main program:",e)
 
    

if(__name__ == "__main__"): 
   ltoa=VectorTotalOrderAlgorithm("process_3")
   x = Thread(target=mainThread, args=())
   x.start()

   p1=Process(8881,ltoa)
   p2=Process(8882,ltoa)

   while(True):
      if(ltoa.processcount==2):
              ltoa.setProcess1(p1)
              ltoa.setProcess2(p2)
              break
      sleep(5)