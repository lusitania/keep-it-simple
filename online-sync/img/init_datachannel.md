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
actor SinkOp <<Operator>>

activate SCS
activate SCL
activate DS

SinkOp -> DC : start()
    activate DC
    DS <- DC : connect

    DC -> SCL : request registration
    SCS <- SCL : {RegistrationRequest}

    SCS -> DS : call for synchronisation
    DS -> DC : {Sychronisation}

    SCS --> SCL : {RegistrationRequestAcknowledgement}
    DC <- SCL : registration requested

    ...

    DC --> SCL : confirm synchronisation
    SCS <- SCL : {RegistrationSuccess}

    DS -> DC : {Sychronisation}
    SCS -> DS : stop synchronisation

    SCS --> SCL : {RegistrationSuccessAcknowledgement}
@enduml
```
