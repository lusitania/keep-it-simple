![Initialisation](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/initialisation.svg)

```
@startuml
left to right direction
SourceOp  <<Operator>>
SinkOp    <<Operator>>

rectangle "Init Phase" {
    :Init CommandChannel: as (ICC)
    :Init DataChannel: as (IDC)

    SourceOp ..> SinkOp : exchange ConnectionDetails

    SourceOp - (ICC) : <<initiate>>
    (ICC) - SinkOp : <<participate>>

    SinkOp -l- (IDC)
}
@enduml
```
