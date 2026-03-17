+++
title = "CoreXY"
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
## Plan
After finally getting tired of the quirks of the Volcano I have decided to upgrade the hotend and the motion system that is on the Folgertech FT6. I am moving to a CoreXY motion system while also moving to the TriangleLabs Dragon hotend with a pancake stepper from LDO. In the process of moving to the CoreXY motion system I am also moving to using a couple beefy 0.9 degree steppers from LDO. All the new parts are listed at the bottom along with suppliers and prices.

The reason for switching to the CoreXY is for a few reasons:
- Weight reduction
  - I'll be dropping about 600 grams from the moving axis of the printer between ditching the extrusion, the large extruder motor, the axis motor, and the large carriage mount.
- Moving to a motion system that required fewer motors so I could run more expensive steppers.
- Joy of Designing something new.
 - With the Stay-at-home order I have been extremely bored and welcome the challenge.


## CoreXY Design
In the design of my new system I first had to identify the key constraints of CoreXY system to pay attention to. From research I've found the following:
  - Belts much be parallel along the rails
  - Idler mounts much be very rigid
  - Between the two options I went for a two level setup rather than crossing the belts

For this design I reconstructed the main parts of the printer in Fusion 360 and used that to size all of the parts and build the belt geometry. this gives me an accurate estimation of assembly, this method of design was very useful for estimation of 

In the past when I have done this kind of design work I have just designed the parts I need by pulling critical dimensions and designing around those. However given that a critical design feature is insuring that the belts are parallel, I designed the entire printer frame first and even put the bed at the appropriate level. This let me insert the new parts and evaluate fitment and how easy the parts were to work with before printing which is important in this case because while the printer is being upgraded, I can't print any new parts. If there are any issues with this install I would need reassemble the printer to reprint new parts.

As part of the redesign I wanted to reduce the amount of ghosting that I was seeing on parts while maintaining the print speed. With the current setup there are a couple different sources of ghosting. One is the jerk of the motion system combined with the weight of the moving axis. The other source seems to be that the x-axis pulley is not perfectly round. I have already described at a high level the measures I'm taking with weight reduction but to touch on it again, I am removing the extrusion, swapping the extruded stepper to a slim stepper, and removing the y-axis motor. 

I don't really understand why the extrusion was included initially because according to the simply supported beam formula below the maximum deflection is approximately 2.44e-5mm. I couldn't find a modulus of area for the MGH12 rail so I approximated the beam with a  rectangular profile which should be close enough.

$$ \delta_{max} = \frac{FL^3}{48EI}$$

The material specifications are:
- $E = 200 GPa$
- $I = bh^3/12$
- Force Calculations
  - BLTouch = 10 grams
  - BMG = 198 grams
  - Stepper = 150 grams
  - Cooler Mount = 9 grams
  - Mount = 46 grams
  - TOTAL = 413 grams or 4.05 Newtons



## New Parts
Name | Part Number | Price Each | Quantity | Source
---|---|----|---|---
Extruder Motor | LDO-42STH25-1404MAC |  16.99 | 1 | Filastruder
Motion Motor | LDO-42STH25-1404MAC |  16.99 | 2 | Filastruder
Gates Belt  | Gates-LL-2GT 6M | 17.67 | 1 | Aliexpress
Trianglelab BLTouch | BLTouch | 13.66 | 1 | Aliexpress
Trianglelab Pulleys | 2GT 20 teeth x5 | 6.99 | 1 | Aliexpress