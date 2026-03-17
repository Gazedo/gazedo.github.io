+++
title = "Algorithm"
description = "Figuring out how the code works in order to simplify the leveling routines."
date = 2020-09-13

[taxonomies]
tags = ["esp32", "freertos", "cpp"]
categories = ["autolevel"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
## The Problem

In order for the auto-leveling routines to work, the program needs to know the error it must correct. The error is calculated by taking the input from an IMU (likely MPU6050 in this case) and subtracting a set point in order to allow for calibration after installation. Initially I was planing on calculating out the vector angles so the math would be easy to expand into directly calculating the ideal cylinder lengths if I eventually added in cylinder extension sensors. I was looking up methods to find the vector angle using matrix operations and infinite series when I realized I didn't need to, the driver in Zephyr directly gives X, Y, and Z accelerations so I just need to minimize the error in X and Y directions. This will not be expandable directly to cylinder extensions but if the system works well enough then there is no reason to expand the math to do that.

As an example of my planned operation lets say the IMU gives the sensor readings:
accel -5.882554 -6.485893  4.415782 m/s/s

This means that the front to back routine needs to run until -5.882554 is closer to 0 and the side to side needs to try to zero out -6.485892 assuming the set point is 0,0,9.80665 m/s/s. There is also the cause where the imu needs to check and make sure it at rest in which case the magnitude of the vectors should total up to gravity or 9.80665m/s/s or at least close to it within a configurable deadband.

## Actuating the System

Finding out the directions required to move is good but the system also needs to take input from buttons in order to know when to safe the system, when to activate the pump, and when to move the cylinders. To do this I'll be using the gpio system to bind the 4 buttons to functions to control the program execution. 

For anything to happen the main switch must be actuated which will enable the hydraulic motor to be turned on when a cylinder is being moved down. Without this switch the system will do nothing as a safety measure. The system will also wait 1 second to do anything after a button is pressed in order to ensure there wasn't a mistaken push. While the system is operating the corresponding button must be held for the entirety of the operation. IE after the system is switched on with the enable switch the front to back switch must be held for the entirety of the front to back leveling operation. Same for the side to side and safe switches.

