![Command Channel](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/init_commandchannel.svg)

```
@startuml
hide footbox
actor SourceOp <<Operator>>

box "Source Endpoint"
    participant "Flow Control" as FC
    participant "Data Service" as DS
end box

box "Sink Endpoint"
    participant "Remote Flow Control" as RFC
end box
actor SinkOp <<Operator>>

SourceOp -> SinkOp : notify ConnectionDetails

SourceOp -> FC : start()
    activate FC
    FC -> FC : bind socket

    FC -> DS : start()
    activate DS

SinkOp -> RFC : start()
    activate RFC
    RFC -> FC : connect

legend right
    start() provides ConnectionDetails
    previously exchanged by Operators
end legend
@enduml
```
