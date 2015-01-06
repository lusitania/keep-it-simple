# Motivation
In a situation of rapidly changing folder contents it can become very
difficult to synchronise the contents to a backup location (ie. for migration
purposes) with system tools such as *rsync*. I've been in this situation in
2011 were *rsync* failed me because:

 - Building *rsync*'s job list took almost a week (no transfer done just yet)
 - After said week about 10% of the pool had already changed and as such was out of date
 - *tar*ing the folder with several million files inside took almost as long as *rsync*ing would have
 - source and backup contents shouldn't be more than a few hours "apart"

So instead of using a *block* procedure I devised an *online* replication
scheme to transfer files as they change and lazily work on the backlog of yet
unchanged/unsynced files. The original solution is closed source yet simple
enough to replicate in Python using ZeroMQ and python-inotify.

osync essentially integrates to other *simpletons*, namely filesystem-watcher
and queuing. Have a peek if you want to learn more about INotify and ZeroMQ.

# Instructions
TBD

# Discussion
TBD

 - It delivers whole messages exactly as they were sent
 - ZeroMQ guarantees to deliver all the parts (one or more) for a message, or none of them.
 - prevent slow joiner syndrome, where the subscriber loses messages as it connects to the server's socket
 - A message (single or multipart) must fit in memory.
 - high water mark

# Roadmap
 1. One-on-one synchronisation
 1. One-to-many synchronisation and service discovery
 1. Secure channel in application

# Design
Since this is about keeping it simple (and avoiding spaghetti code like in my old 2011-approach) I need to do some upfront design to give the code a more intuitive feel. The UML can be visualised with [PlanUML Online Server](http://www.plantuml.com/plantuml/form), later there will be pictures.

## Overview
The application passes trough three stages: Initialisation, Transfer and Termination.

![Overview](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/overview.svg)

Flow of events:

 1. In an *Initialisation Phase* two Endpoints connect and prepare for data transfer
 1. In a *Transfer Phase* the Source Endpoint sends the files notifies from the FileEvents to the Sink Endpoint
 1. In a *Termination Phase* an Endpoint send termination request which closes down the connection in mutual agreement

## Initialisation Phase

### Init CommandChannel
Participating actors: SourceOperator (SourceOp), SinkOperator (SinkOp)

Flow of events:

 1. The SourceOp starts the SourceControlService of SourceEndpoint with defined ConnetionDetails
    1. The SourceEndpoint binds a socket to the committed ConnetionDetails
    1. The SourceControlService starts the DataService
 1. The SinkOp starts the SourceController with ConnetionDetails given from the SourceOp
    1. The SourceController connects to the SourceControlService

Entry condition:

 - (Non-system) Two ports are already SSH forwarded between Source and Sink.

![Command Channel](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/init_commandchannel.svg)

### Init DataChannel

Flow of events:

 1. DataClient connects to the DataService
 1. DataClient issues a registration request to the SourceController 
 1. The SourceController sends RegistrationRequest command to the SourceControlService
    1. The SourceControlService calls the DataService to issue Synchronisation messages
    1. DataService sends SynchronisationMessages to the DataClient
    1. SourceControlService responds with a RegistrationRequestAcknowledgement
 1. The SourceController notifies the DataClient the synchronisation is underway
 1. The DataClient receives the Synchronisation messages and notifies the SourceController of successful registration
 1. SourceController sends RegistrationSuccess command to the SourceControlService
    1. The SourceControlService notifies the DataService to stop sending SynchronisationMessages
    1. The SourceControlService sends RegistrationSuccessAcknowledgement

Entry condition:

 - SourceController is connected with SourceControlService

Exit condition:

 - DataClient is ready to reliably receive messages from DataService

![Data Channel](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/init_datachannel.svg)

## Transfer Phase

### Transfer Data
Participating actors: SinkOp << Operator >>, SourceOp << Operator >>, INotify << File System >>

Flow of events:

 1. FileEventQueue registers to INotify events from a particular root path in the local file system
 1. DataService polls FileEventQueue indefinitely and for every polled entry it
    1. Retrieves the file content
    1. Wraps file content and relative path (without root path component) into a FileData message
    1. Sends the FileData message to the DataClient

Entry conditions:

 - DataClient is ready to receive (successful synchronisation with DataService)

Exit conditions:

 - An operator signals either DataService or DataClient to terminate transfer

Quality requirements:

 - DataService may buffer polled entries until a certain threshold was met
 - FileData messages and thereby file contents fit into memory and must not be split

### Too many INotify events (extension to Transfer Data)
Participating actors: INotify << File System >>, FindTouch << Operator >>

Flow of events: 

 1. Warn the operator to throttle change events if event queue reaches warning threshold
 1. Go to Termination phase if event queue reaches critical threshold

Entry condition:

 - The OS internal INotify event queue closes in on its maximum (high water mark). Events come in faster than they can be send to the client.

Quality requirements:

 - Warning threshold should be high enough to seldom trigger the event but low enough to allow the operator to respond.
 - Critical threshold must be higher than warning and at most 100% of the queue

## Termination Phase

TBD

# Contributions

 - [tobibe](https://github.com/tobibe) (Requirements elicitation, Protocol design)
