![Overview](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/overview.svg)

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
