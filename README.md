Distributed Systems - Project 1

DESCRIPTION:
As part of Distributed Systems Project 1, we have implemented file operations includes upload, download, rename and delete operations which are based on message oriented, client-server communication and a computation service using remote procedure call (RPC) based communication.
Question 1:
 We have implemented all the programs using python. For Question 1, we have implemented a single threaded server which connects with the help of sockets. A socket is bound to a port number so that the TCP layer can identify the application that data is destined to be sent to. Single threaded means we open a single connection and server can respond to only single client at a time. In this program we have implemented four basic operations Download, Delete, Rename and Upload. We have used a connection-oriented protocol in which the client and server first establishes a network connection, negotiates the operation to be performed and carry out the file transfer in the same connection. 
Question 2:
In Question 2, we have implemented a multi-threaded server which connects with sockets and multithread. In multi-threaded server, server socket can respond to multiple clients at a time. The multithread is executed with the help of locking mechanism. In distributed systems, a locking mechanism is helpful when two or more than two clients are trying to access the same file, only one can access it. Each request is working on its own thread. Whenever multiple threads act on the same resource, then threads are locked to work first in first out. Distributed locks are helpful to improve the efficiency of services or implement the absolute mutual exclusion of accesses. Mainly, locking mechanism used in deleting and renaming process. The main challenge we faced in converting single thread server to multi thread server is to add threads and lock mechanism to single socket thread program. We also faced difficulty in debugging the code as we also had to maintain concurrency. When one of the clients is renaming one of the files another client will not be able to change or modify the file. We have also tested several test cases by involving both the clients. Example: one client deleted the file from the server, another client cannot download or rename the same file.
Question 3 and 4: 
In Question 3 and 4, we have implemented synchronous and asynchronous Remote Procedure Call (RPC). Remote Procedure Call (RPC) is a technique for building distributed systems. Basically, it allows a program on one machine to call a subroutine on another machine without knowing that it is remote. RPC is not a transport protocol: rather, it is a method of using existing communications features in a transparent way.
ISSUES:
The major issues found in implementing asynchronous RPC, as I need to implement without using modules. First thing needs to understand how the code should be written that can perform RPC process efficiently.
 The challenges faced in converting single threaded to multithreaded is that to understand how the process should for more than one client and the server should be in loop that can give responses according to the client input.
The purpose of a lock is to ensure that among several nodes that might try to do the same piece of work, only one does it (at least only one at a time). That work might be to write some data to a shared storage system, to perform some computation, to call some external API

Distributed Systems - Project 2
DESCRIPTION:
As part of Distributed Systems Project 2, we have developed an n-node distributed 
system that supports totally ordered events and a distributed locking scheme. We 
created totally ordered events through the totally ordered multicast and vector clocks. A 
distributed locking scheme is needed to prevent concurrent access to the shared file.
The distributed system uses a logical clock to timestamp messages sent/received 
between nodes.
Assignment 1: Total Order Multicasting Using Lamport’s Algorithm
For Assignment 1, we have implemented a Total order multicasting using Lamport's
algorithm which monitors the events of file open, write & close. In this network we have 
3 nodes, each node multicasts the message before performing any event and process 
which has lower number has priority and it get acknowledged first. Also, we are 
multicasting the acknowledgements to all the nodes. We are maintaining buffer of all 
the pending requests and orders are preserved. Timestamps are also validated and 
updated according to each event. So, the total order of events using timestamp are 
obtained.
From this assignment, we have learned how a total order multicasting using Lamport’s 
algorithm works and understood the main drawback of this algorithm which is receiving 
many acknowledgements and messages from the processes when any event is 
scheduled.
The main challenge we faced in this assignment is to maintain total order between the 
processes and to maintain buffers for storing the acknowledgements received from the 
processes.
Assignment 2: Vector Clock
A vector clock is a data structure used for determining the partial ordering of events in a 
distributed system and detecting causality violations. Just as in Lamport timestamps, 
inter- process messages contain the state of the sending process’s logical lock. A vector 
clock of a system of N processes is an array/vector of N logical clocks, one clock per 
process; a local “largest possible values” copy of the global clock-array is kept in each 
process.
We are running three individual processes in three different nodes(machines). Each 
process has three events (“Open File”, “Write Data”, “Close File”) and whenever one 
event is read in a process, it increments its logical clock by one and then multicasts its 
message to the remaining two processes by incrementing the clock value to again 1.
• Initially all vector clocks are zero. 
• Each time a process experiences an internal event, it increments its own logical 
clock in the vector by one. 
• Each time a process sends a message, it increments its own logical clock in the 
vector by one.
• Each time a process receives a message, it increments its own logical clock in the 
vector by one and updates each element in its vector by taking the maximum of 
the value in its own vector clock and the value in the vector received message.
From this assignment, we have learned how a vector clock is implemented and by using 
vector clock how the total number of messages or acknowledgements can be reduced. 
The main issue we faced is in implementing or maintaining the vector clock in each 
process.
Assignment 3: Distributed Locking
In Distributed Locking, to get access to a shared resource the process should send the 
lock request to all the other processes and wait till it receives the positive 
acknowledgements from all the other processes to be able to lock the shared resource. 
We have created a temporary file by assuming it as a shared resource. Whenever any 
process gets the lock, it will increment the counter value by 1 and then releases the 
lock. When one process gets the lock, other processes will wait until the lock is released. 
Once the lock is released, the process who wants to acquire the lock will send the 
requests to the other two processes and wait till it gets the positive acknowledgements.
From this assignment, we have learned how the distributed locking mechanism can be 
helpful while accessing the shared resources and what are the drawbacks of using this 
mechanism. 
The main challenge we faced in this assignment was to obtain the locks and, we made
sure that when one node is executing the other two processes need to wait to perform 
their operation.
