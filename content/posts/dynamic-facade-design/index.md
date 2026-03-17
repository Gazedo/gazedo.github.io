+++
title = "Dynamic Facade Design"
date = 2019-12-05

[taxonomies]
tags = []
categories = ["dynamic-facade"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
## Program Design
The program that I constructed for the controller is a function based monolithic architecture. Rather than using an object oriented approach I inherited the functional approach used in many of the samples that I took inspiration from. This approach was fine for the quick development cycle of this project but the code would need refactoring in order to expand it much further. The functions take from the unix style in that they do only one thing and try to do it well while also trying to keep the global variables to a minimum. Unfortunately, in order to simplify the motion control algorithm some control values were be defined globally.

In order to communicate, a very simple http server is setup which listens for messages along certain paths. The messages are processed through the ESPAsync library and passed to a variety of callbacks depending on the accessed URL which then passes the payload, if any, to that callback.

In addition to using this method in order to configure the device, the controller can save its current settings to the SPIFFS filesystem. This filesystem is persistent through reboots and thus retains settings. Some of these settings are transmitted back to the client application on boot. Other settings such as the configured position list are saved on the client device. An example of the custom position controller is shown below.

{{ figure(src="custom_position.jpg") }}

Once a destination is set the motion planner takes control as it is called on every update it returns the next desired position for each individual servo. This is a very simple step motion planner that takes advantage of the set acceleration already built into the servos. Once all the servos have reached their destination the run state variable is switched to false which tells the main program oscillation logic when to start timers if oscillation is turned on. An example of the oscillation program running is shown below.

<video controls src="fast_move.MP4"></video>
