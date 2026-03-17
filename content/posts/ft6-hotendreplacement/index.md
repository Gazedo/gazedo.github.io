+++
title = "HotendReplacement"
date = 2020-08-20

[taxonomies]
tags = ["3d printing", "3d design"]
categories = ["ft6"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
Almost immediately after initially building the printer, the hotend failed. Even before the failure the extruder kept skipping and the hotend wouldn't expel material smoothly. I decided it was time for an upgrade rather than a simple repair. On the market there were several options but I decided to stick with a genuine part and stay away from copies. My options were bondtech bmg with an e3d hotend or an e3d titan aero. I did not have good experiences with the e3d titan aero on my smaller i3 style printer so I decided to go with the bmg and e3d pairing. Given that the printer is gigantic, I went for the e3d volcano hotend which advertises the ability to print at a higher rate than a normal v6.

With this combination I had to figure out a new way to mount the hotend to the printer. Initially I tried to run the volcano in bowden mode with the extruder mounted on the frame, but I couldn't get the volcano to stop oozing in this configuration. When I decided to move to direct drive I had to design my own carriage mount as my current one did not have the option for direct mounting of the extruder. Below is an image of the mount that I ended up with. 

{{ figure(src="imageUrl", alt="Description") }}


It is designed to bolt up to the stock belt carrier while providing an optional accessory mounting for either a dial gauge or a bltouch. The main feature of the mount is the compatibility with a petsfang cooler which I wanted to keep since I didn't want to design a new cooler and go through the air flow analysis.

It has been awhile since I designed this mount and it has served well, it had a couple of dimensional issues that were close so I just sanded away the extra material. It was still a tight fit but I eventually got it together. Since it was together I didn't fiddle with it until I decided to rework it.

For the replacement I wanted a few features:
  - Lighter weight
  - More rigid
  - BLTouch mount
  - Maximizes space for printing
  - Simplistic cooler

Along with the hotend rebuild I decided I wanted to massively reduce the weight of the movement axis and to do this I went CoreXY. The next post will detail the changes from the stock system.