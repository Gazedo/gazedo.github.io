+++
title = "Dynamic Facade Future"
date = 2020-07-21

[taxonomies]
tags = ["esp8266", "future"]
categories = ["dynamic-facade"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
## Future
This program has the capability to be greatly expanded but that expansion would likely need almost a complete rewrite in order to reorganize the code into modular classes. Some of the possible upgrades I've considered are below:

- Expand command input to
  - Also listen to openhab or google home or others
  - Allow input based on light level through either a photoresistor or a solar panel
  - Allow input based on generic mqtt server
  - Configure neural net based on seasonal changes for optimal temperature sustainment
    - IE in the summer open the blinds if the house is warm at night to allow more heat out but close the blinds during the day to block heat input
  - Configurable open/closing based on time and calendar
- Expand power supply option to include LiPo or LiIon with management
- Expand motor option to add back in stepper control