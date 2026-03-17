+++
title = "Brainstorm"
date = 2020-09-12

[taxonomies]
tags = []
categories = ["autolevel", "brainstorm"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
## Existing System
The existing system in the RV is very simple. It is a system of 4 switches, 3 actuate the cylinders up and down and the last turns on or off the pump. The cylinders are located at the front, one on the rear left and the last on the rear right. The standard method of leveling the RV is to actuate the front first to bring the front up slightly above the rear and then use the last two in order to bring the rear up to meet the front while staying level side to side.

## Hardware to Add
To implement the system the minimum amount of feedback I need from the physical world is a couple of control inputs, the direction of gravity, and a voltage converter. Optionally the extension of the cylinders could enable a more advanced system.

Going with the minimum required would result in a simple add in box that could be installed in the dash. The box would contain an imu, the main processor, and would lead to a few buttons. I think having 4 buttons would be optimal for the system, one to activate the system initially, one to activate the front to back leveling routine, another to activate the side to side routine, and the last to 'safe' or deactivate the system. The last button would retract the cylinders for the maximum amount of time expected for a retract operation from the greatest extension limit. Until the cylinders are allowed to retract for the full time the system will safe the ignition and not allow the engine to be started.

Adding the cylinder extension meters would allow the system to release the safe earlier by watching the cylinders and releasing the system when the cylinders are fully retracted. The other aspect of the meter would be to watch for a cylinder failure to retract.

## Operation of system.
When the RV is stopped, the auto leveling system is enabled and the following list is followed:
1. The front to back routine is run until the system stops actuating the front cylinder.
2. The side to side routine is run until the system stops actuating the cylinders. 
3. Activate the front to back again to ensure the rv is leveled front to back.
4. Go outside and check that the cylinders are touching the ground.
   
When ready to leave the system is retracted just by holding the Safe button until the red led turns off.

## Software Framework
I have yet to have a good project to use Zephyr with but this seems like an ideal candidate. I don't know yet exactly which IMU or Board I'm going to use so I need something easily transferable, I would like something based on a growing industry standard, and finally easily updatable. Zephyr ticks all of these boxes and also has the option of working through Platformio in VS Code.