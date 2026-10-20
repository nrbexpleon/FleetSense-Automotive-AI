from .models import SignalDefinition

def default_catalogue()->list[SignalDefinition]:
    return [SignalDefinition("Powertrain.Motor.Temperature","degC",-40,200,5000,True),SignalDefinition("Powertrain.Motor.Vibration","g",0,20,5000,True),SignalDefinition("Battery.StateOfCharge","%",0,100,10000,False),SignalDefinition("Network.ServiceLatency","ms",0,5000,5000,False)]
