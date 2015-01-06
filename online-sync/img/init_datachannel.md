![Data Channel](https://rawgit.com/lusitania/keep-it-simple/master/online-sync/img/init_datachannel.svg)

```
@startuml
hide footbox

box "Source Endpoint"
    participant "Source Control\nService" as SCS
    participant "Data Service" as DS
end box

box "Sink Endpoint"
    participant "Data Client" as DC
    participant "Source Controller" as SCL
end box

activate SCS
activate SCL
activate DS

DC <- SCL : start
activate DC

DS <- DC : connect

DC -> SCL : request registration
SCS <- SCL : {RegistrationRequest}

SCS -> DS : call for synchronisation
activate DS
DS -> DC : {Sychronisation}

SCS --> SCL : {RegistrationRequestAcknowledgement}
DC <- SCL : registration requested

DC --> SCL : confirm synchronisation
SCS <- SCL : {RegistrationSuccess}

DS -> DC : {Sychronisation}
SCS -> DS : stop synchronisation
deactivate DS

SCS --> SCL : {RegistrationSuccessAcknowledgement}
@enduml
```
