# transmission-simulator
A simulation of an Automatic Transmission Controller.

## Overview
The idea of this project is to simulate an internal combustion engine and automatic transmission, using certain engine characteristics and inputs to drive the simulation. The state of the drive train in a vehicle equiped with an automatic transmission can be simulated from the trottle and brake inputs from the driver and the feedback from the current state of various components of the vehicle. 

To model the engine itself, a torque map is needed to simulate the physical torque output based on throttle position and current RPM. Low throttle positions result in relatively high torque at low engine speeds which tapers off as engine speed increases. This tapering characteristic diminishes as throttle position is increased, resulting in steadily increasing torque curves for higher RPMs as the thottle position reaches 100%. See the screenshot below.
![Alt text](torque_map.jpg?raw=true "Engine Torque Output")

Engine output to the transmission is controlled by the torque converter. Described simply, a torque converter resembles two fans encased together inside a housing filled with liquid. As the fan connected to the engine spins (the impeller), the liquid inside the housing causes the opposing fan connected to the transmission to spin (the turbine). Torque is transferred through this liquid (and sometimes multiplied, depending on the speed ratio between the fans) to the transmission and the final drive and the wheels.

When the vehicle is at rest, the turbine is in a stalled state. But as the throttle is increased and engine output torque increases, the resulting torque on the turbine overcomes the static load of the vehicle; the turbine will begin to spin. Combined with the gearing in the transmission and that of the final drive gearing, the vehicle will begin to move. Eventually, as the road speed approaches the engine speed, both the impeller and turbine will spin at the same rate (some torque converters employ a lock-up clutch at this point to prevent losses).

This entire system then fluctuates as the throttle and brake inputs change, affecting the dynamic state of the vehicle as a whole.

## Current Status
### Engine
The engine idles well enough. Loading of the torque map currently only linearly interpolates for RPM. Interpolation of throttle position from the text file would be nice.

### Torque Converter
Still needs a good transfer function for transmitting torque from impeller to turbine. The feed back from the transmission doesn't seem right either.

### Transmission
Needs a shift schedule and a shift controller, but this can wait until the engine revs properly with throttle inputs.

### Vehicle Dynamics
Vehicle load and road speed calculations need some work. This is probably the source of all the engine woes, since these values ultimately determine the engine speed via feedback.

