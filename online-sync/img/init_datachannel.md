![Data Channel](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/init_datachannel.svg)

```
@startuml
hide footbox

box "Source Endpoint"
    participant "Flow Control" as FC
    participant "Data Service" as DS
end box

box "Sink Endpoint"
    participant "Data Client" as DC
    participant "Remote Flow Control" as RFC
end box

activate FC
activate RFC
activate DS

DC <- RFC : start
activate DC

DS <- DC : connect

DC -> RFC : request registration
FC <- RFC : {RegistrationRequest}

FC -> DS : call for synchronisation
activate DS
DS -> DC : {Sychronisation}

FC --> RFC : {RegistrationRequestAcknowledgement}
DC <- RFC : registration requested

DC --> RFC : confirm synchronisation
FC <- RFC : {RegistrationSuccess}

DS -> DC : {Sychronisation}
FC -> DS : stop synchronisation
deactivate DS

FC --> RFC : {RegistrationSuccessAcknowledgement}
@enduml
```
