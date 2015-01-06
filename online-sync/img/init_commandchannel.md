![Command Channel](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/init_commandchannel.svg)

```
@startuml
hide footbox
actor SourceOp <<Operator>>

box "Source Endpoint"
    participant "Source Control\nService" as SCS
    participant "Data Service" as DS
end box

box "Sink Endpoint"
    participant "Source Controller" as SCL
end box
actor SinkOp <<Operator>>

SourceOp -> SinkOp : notify ConnectionDetails

SourceOp -> SCS : start()
    activate SCS
    SCS -> SCS : bind socket

    SCS -> DS : start()
    activate DS

SinkOp -> SCL : start()
    activate SCL
    SCL -> SCS : connect

legend right
    start() provides ConnectionDetails
    previously exchanged by Operators
end legend
@enduml
```
