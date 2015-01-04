![Command Channel](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/init_commandchannel.svg)

```
@startuml
actor SourceOp <<Operator>>

box "Source Endpoint"
    participant "Source Control\nService" as SCS
    participant "Data Service" as DS
end box

box "Sink Endpoint"
    participant "Source Controller" as SCL
end box
actor SinkOp <<Operator>>

SourceOp -> SCS : start
    activate SCS
    SCS -> SCS : bind socket

    SCS -> DS : start
    activate DS

SinkOp -> SCL : start
    activate SCL
    SCL -> SCS : connect
@enduml
```
