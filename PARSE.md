# Prase

## Frame
- fork_type if tapered prased set it to Tapered text choice and if tapered doesnt exists, set it to straight text choice
- bb_type parse the shelltype to match the textchoices
- bb_width parse the number which has the string mm appended to it
- fork_brake_drilled if it says fork drilled in the string. set it to a boolean. if both are in the same sentence then set to true
- frame_brake_drilled if it says frame drilled in the string. set it to a boolean. if both are in the same sentence then set to true
- seatpost_size take the number either 31.6mm or 27.2mm or 30.9mm
- max_tire_clearance_mm prase the number from clearance or max clearance

## BottomBracket
- bb_type match with shell tpye
- spindle_interface_mm parse to match 
- spindle_length_mm if there a jis or iso interface then the length of the spindle should be in the specs or spec_notes. if the interface isnt tapered then set it to null
- bb_width if not in the spec or spec_notes, its in the name
- colors parse them

## crankset
- spindle_interface_mm parse to match 
- spindle_length_mm if there a jis or iso interface then the length of the spindle should be in the specs or spec_notes. if the interface isnt tapered then set it to null
- arm_length match with choices

## Hubs
- the position of the hub is in the name of the component
- hole_count is drilling
- fixed/fixed, fixed/single, fixed/free label it flip flop but for special cases it will specifc an amount of spoke holes like 36h singleside fixed meaning its not flip flop for that amount of holes
- spacing for rear and front will be 100 or 120
- if theres is no option for choosing one of the option variant then set it to none so it wont display on the frontend
- check in spec and spec_notes for missing data

