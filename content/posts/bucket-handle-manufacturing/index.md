+++
title = "Testing and Manufacturing"
date = 2020-06-03

[taxonomies]
tags = ["3d printing", "testing"]
categories = ["bucket-handle"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
+++
## Testing
Going back to the main features that I wanted to design for: 

1. Ergonomics
2. Durability
3. Cost
4. Ease of Maintenance

I tried to think of some tests to confirm I had reached my goals. Using the superfluous prototypes I set about trying to confirm that I had reached desired durability level required to meet my desired goals. To that end I decided to preform the following tests:
- Gave a couple to my dog to test how long they would to take to rip apart and how they ripped apart.
- Submerged the one with the thinnest walls in some gasoline.
- Hit one that had the same structure I was planning to use with a hammer.

For the dog test, they only lasted 10-15 minutes before my dog was ripping chunks off. Reassuringly, they didn't rip solely along the layer lines anymore. This showed me that I was printing at a temperature that generated enough layer adhesion that the it rivaled the rest of the material in toughness.

By submerging the material in gasoline I was confirming the TPU's claimed material resistances. According to a generic tpu it can resist solvents like gas, the color is uv resistant, and shouldn't get stained. I did not have enough time to test the last two claims but since the first proved true for this blend, I thought it was acceptable to assume the other two will hold true as well.

After those admittedly unscientific tests were accomplished I considered the handles "good enough" and sent a set to my family for a test session over time.

## Manufacturing
Make the handles was not as easy as just slicing and sending them to the printer. I seemed to have accidentally deleted my profile for printing TPU and had to retune. I ended up doing them in a batch print all at once which ended up being almost a 9 hour print for 5 handles. The handles that I sent off to my family ended up being only prototype quality with significant layer lines and retraction issues between the models. For final design handles that I will be selling, I need to either print sequentially or fix the retraction which I suspect would require replacing the print head. The volcano that is currently on the printer oozes way too much to be usable for fine detail work.
{{ figure(src="IMG_4347.jpg", alt="Layer lines and ghosting on text") }}

I'm not sure I can fix this with the current hotend but I'll be trying slightly more retraction, less acceleration, and a lower temperature. Hopefully the combination of temperature and retraction will help the tiny pimples and the layer line issue. Lowering the acceleration should reduce the ghosting. The acceleration change will have to wait until I find the funds to do another upgrade round on the printer though.
