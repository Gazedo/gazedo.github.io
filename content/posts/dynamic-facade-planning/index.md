+++
title = "Dynamic Facade Planning"
date = 2019-12-04

[taxonomies]
tags = ["esp8266", "project planning", "brainstorming"]
categories = ["dynamic-facade"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
# Project Planning and Process

Originally the project was laid out as follows:

- Single stepper motor which moved the vertical blinds through a system of 3d printed gears.
- Esp8266 in order to move the stepper simply back and forth in a set time period.
- Code written in using the Arduino sdk in order to take advantage of the stepper libraries. 

I prototyped a board using a drv8826 driver module with a spare 200 step/rotation stepper that I had left over from a 3d printer upgrade. Once I had some physical hardware I got that rotating using an example and started to suggest possible upgrades. The upgrades I suggested were:

- Individual control of blinds using cheap sg90 servo motors from amazon.
- Remote control of orientation.

My girlfriend and her group were pleased with the progress and due to the difficulty of printing enough gears to actuate the blinds, readily agreed to the idea of using sg90 servos. The remote orientation control was met with a little resistance as they really wanted to keep the ability to have automatic rotations. So I proposed doing a staged development cycle where the first set of goals included:

- Stage 1
  - Remote start/stop of set automatic movement for all blinds
  - Control of all 8 servos individually
  - Android app for remote control
Stage 2
  - Remote calibration procedure
  - Remote position seeking
Stage 3
  - Adjustable speed and acceleration for movement profiles
  - Programmable positions in app.
Stage 4
  - Individually timed movements for each blind

By proceeding in this staged fashion, they would be sure to meet the minimal requirements of the project. Due to time constraints, stage 4 was never finished.
