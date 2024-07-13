from threading import *
from time import *
from socket import *
import schedule
import threading
from pathlib import Path


class Process(Thread):

    def __init__(self, port, dsl):
        Thread.__init__(self)
        # Thread.daemon=True
        self.dsl = dsl
        self.port = port
        self.host = gethostname()
        self.start()

    def run(self):
        while (True):
            try:
                self.soc = socket(AF_INET, SOCK_STREAM)
                self.soc.connect((self.host, self.port))
                self.dsl.processcount = self.dsl.processcount + 1
                break
            except Exception as e:
                print("wating to connect to the port: ", self.port)
                # print("Error:",e)
            sleep(5)


class DistributedLocking(Thread):

    def __init__(self, pid):
        Thread.__init__(self)
        # Thread.daemon=True
        self.pid = pid
        self.processcount = 0
        self.timestamp = 0
        self.deliveryevents = {}
        self.eventbuffer = []
        self.respacknowledge = []
        self.event = "Update File"

    def setProcess1(self, process1):
        # print("Process counter:",self.processcount)
        self.process1 = process1

    def setProcess2(self, process2):
        # print("Process counter:",self.processcount)
        self.process2 = process2
        print("processes started at (", self.pid, ")")
        self.start()

    def compareTimestamp(self, processlogicaltime):
        if (processlogicaltime > self.timestamp):
            self.timestamp = processlogicaltime + 1
        else:
            self.timestamp = self.timestamp + 1

    def run(self):
        
        try:
                print(f"{self.pid} is requesting lock to P1")
                print(f"{self.pid} is requesting lock to P2")

                self.timestamp = self.timestamp + 1
                msg = self.pid + "," + self.event + "," + str(self.timestamp)
                self.process1.soc.sendall(msg.encode())

                pmsg1 = self.process1.soc.recv(1024)
                self.respacknowledge.append(pmsg1.decode('utf-8'))

                print(f"Received acknowledge from P1")

                self.timestamp = self.timestamp + 1
                msg = self.pid + "," + self.event + "," + str(self.timestamp)
                self.process2.soc.sendall(msg.encode())

                pmsg2 = self.process2.soc.recv(1024)
                self.respacknowledge.append(pmsg2.decode('utf-8'))
                print(f"Received acknowledge from P2")
                print(self.event)

                number= int(Path("Temp_File").read_text())
                number+= 1
                Path("Temp_File").write_text(f"{number}\n")
                print("Counter value updated to :", number)
                            
                print(f"Releasing lock by {self.pid}")
        except Exception as e:
            print(f"Error in acknowledging")

    def maintainRequestAndAcknowledge(self, socconn):
        try:
            while (True):
                msgdeliver = socconn.recv(1024)
                msg = msgdeliver.decode('utf-8').split(",")
                # pid, event, timestamp
                self.deliveryevents[msg[0] + "." + "Request"] = msgdeliver
                self.eventbuffer.append("Request")  # adding  events to eventbuffer
                self.compareTimestamp(int(msg[2]));
                mesg = self.pid + "." + "Request"
                socconn.sendall(mesg.encode())

                # while loop closing
        except Exception as e:
            print("maintain request and acknowledgement error:", e)


def mainThread():
    try:
        host = gethostname()
        port = 8883
        # -------process1 and process2 request accepting--------------
        # print("hostname:",host)
        # print("port:",port)
        conarg = []
        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen(3)
            while (True):
                conn, addr = s.accept()
                # print(conn)
                conarg.append([conn, addr]);
                # dsl.maintainRequestAndAcknowledge(conn)
                xt = Thread(target=dsl.maintainRequestAndAcknowledge, args=(conn,))
                xt.start()
                # print("Thread started")

    except Exception as e:
        print("Error in main program:", e)


if (__name__ == "__main__"):
    Path("Temp_File").write_text("0\n")
    dsl = DistributedLocking("process_3")
    x = Thread(target=mainThread, args=())
    x.start()

    p1 = Process(8881, dsl)
    p2 = Process(8882, dsl)
    while (True):
        if (dsl.processcount == 2):
            dsl.setProcess1(p1)
            dsl.setProcess2(p2)
            break
        sleep(5)
