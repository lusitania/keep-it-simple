# Motivation
In a situation of rapidly changing folder contents it can become very
difficult to synchronise the contents to a backup location (ie. for migration
purposes) with system tools such as *rsync*. I've been in this situation in
2011 were *rsync* failed me because:

 - Building *rsync*'s job list took almost a week (no transfer done just yet)
 - After said week about 10% of the pool had already changed and as such was out of date
 - *tar*ing the folder with several million files inside took almost as long as *rsync*ing would have
 - source and backup contents shouldn't be more than a few hours "apart"

So instead of using a *block* procedure I devised an *online* scheme to
transfer files as they change and lazily work on the backlog of yet unchanged/
unsynced files. The original solution is closed source yet simple enough to
replicate in Python using ZeroMQ and python-inotify.

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

# Design
Since this is about keeping it simple (and avoiding spaghetti code like in my old 2011-approach) I need to do some upfront design to give the code a more intuitive feel. The UML can be visualised with [PlanUML Online Server](http://www.plantuml.com/plantuml/form), later there will be pictures.

## Overview
The application passes trough three stages: Initialisation, Transfer and Termination.

```
@startuml
start
:Init Phase;
:Transfer Phase;
note right
  long running activity,
  process requires signal to proceed
end note
:Termination Phase;
stop
@enduml
```

## Initialisation
```
@startuml
left to right direction
Source  <<Operator>>
Sink    <<Operator>>

rectangle "Init Phase" {
    :Prepare Service: as (PS)
    :Register with Service: as (RS)
    :Secure Channel: as (SC)
    :Ensure Readiness: as (ER)
    
    Source ..> Sink : exchange connection details
    
    Source -> (PS)
    (PS) -[hidden]-(RS)
    (RS) - Sink
    
    Source - (SC) : <<initiate>>
    (SC) <-- Sink : <<participate>>
    
    Source --> (ER) : <<participate>>
    (ER) - Sink : <<initiate>>
}
@enduml
```

### Case: Prepare Service
Flow of events:

    - The Source starts a CommandService.
    - The connection details (port) of the Source are printed to the console and must be used by the Sink to connect. (Discovery/exchange is not covered.)
    - The source awaits incoming connections from clients (Sink).

### Case: Register with Service
Flow of events:

    - The Sink connects to the CommandService of the Source with the connection details exchanged in *Prepare Service*.

```
@startuml
left to right direction

Source              <<Operator>>
Sink                <<Operator>>
"File Events" as Ev <<Operating System>>

rectangle "Transfer Phase" {
    :Commence Transfer: as (CT)
    :Transfer Report: as (TR)
    :Queue Report: as (QR)

    Source - (CT) : <<initiate>>
    Ev - (CT) : <<participate>>
    (CT) - Sink : <<participate>>

    (TR) - Sink : <<initiate>>
    Source - (TR) : <<participate>>

    Ev - (QR) : <<initiate>>
    Source - (QR) : <<participate>>
}
@enduml
```

```
@startuml
left to right direction

Source  <<Operator>>
Sink    <<Operator>>

rectangle "Termination Phase" {
    :Unregister from Service: as (US)
    :Service Termination: as (ST)

    Source - (US) : <<participate>>
    (US) - Sink : <<initiate>>

    (US) .> (ST) : <<include>>

    (ST) - Sink : <<participate>>
    Source - (ST) : <<initiate>>
}
@enduml
```
