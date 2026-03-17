+++
title = "Brushed Motor Positioning"
date = 2020-07-06

[taxonomies]
tags = []
categories = ["brushed-motor-encoder"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
## Cheap Positioning an a Brushed Motor
There are several methods of measuring the rotational rate of a motor which require external hardware and a few that use internal characteristic of the motor. The method that I'm going to go over is not something I have ever had the chance to use in a project but should be useful depending on situation. When a brushed motor spins, the brushes move between the armatures in order to deliver current to the magnets. When the brushes are between the armatures, the voltage spikes on the motor's power delivery lines. This is because the lines act kind of like an inductor but it could also be because the motor pulls the voltage down and with the cessation of the load the voltage is allowed to climb back up. 
{{ figure(src="Electric_motor_cycle_1.png", alt="Breakdown of Electric Motor") }}

By establishing a low-pass filter on the motor lines these commutation spikes can be measured and used to calculate the speed at which the motor is rotating. The number of commutation spikes per rotation is equal to double the number of poles in the motor.
