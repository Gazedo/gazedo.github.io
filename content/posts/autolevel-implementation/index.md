+++
title = "Implementation"
date = 2021-07-23

[taxonomies]
tags = ["esp32", "freertos", "cpp"]
categories = ["autolevel"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
## Program Architecture

{{ figure(src="LevelingSystemFlow.png", alt="Flow chart of system") }}
In order for holding the buttons to do the appropriate actions the controller needs a state machine to detect when the button is being held so as to communicate to the threads handling the motion that they should do stuff.
The nonvolatile data issue is solved by using a configuration file saved in the SPIFFS subsystem of the target esp32. The file also supports a version number so as to tell if the file is compatible before attempting to import attributes. Without a version number the program can segfault while trying to import a non-existant setting. The file is saved in a json format whihc is both easy to parse and fairly easy to read.

## Threads

The program is set to run with 4 threads. The following is a list of the threads and their responsibilities:

* Limit Checker
* Button Watcher
* Led Controller
* IMU Reader

There is another thread that runs in diagnosis mode that outputs current status of the system including the internal state machine, the IMU output, and the button state. Each thread runs with about 4kb of stack space and all are pinned to core 1 except the imu task which is allowed to run on either core.

## Testing

Unfortunately testing on the actual system is not possible. Therefore to test I  made a test rig which shows outputs on LED's and provides buttons to interact with the controller. While testing I had the diagnostic output displaying on a laptop.