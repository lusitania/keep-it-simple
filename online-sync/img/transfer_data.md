![Transfer Data](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/transfer_data.svg)

```
@startuml
hide footbox

actor SourceOp <<Operator>>
actor INotify <<FileSystem>>
database "Source Folder" as SoF

box "Source Endpoint"
    boundary "File Events" as FE
    participant "Data Service" as DS
    participant "File Data\nMessage" as FD
end box

box "Sink Endpoint"
    participant "Data Client" as DC
end box

database "Sink Folder" as SiF

activate DS
activate DC

SourceOp -> DS : tell location of SourceFolder

FE <- DS : start on SourceFolder
activate FE
INotify <- FE : register to changes in SourceFolder

FE <- DS : poll for events
FE --> DS : set of events
activate DS
    loop for each event
    create FD
    DS -> FD : create from event
    activate FD
        FD -> SoF : content and stat of file
        FD <-- SoF
        FD -> FD : path offset\nrelative to\nSourceFolder
        DS <-- FD

        DS -> DC : {FileData}
    destroy FD

    DC -> SiF : create file\nfrom {FileData}
    end
deactivate DS

@enduml
```