The Hive
========

Based on the board game "The Hive"

 / \ / \
|   |   |
 \ / \ /
  |   |
   \ /

Notation:
--------

 - Pice:
    * A pice is represented by 3 chars.
    * The first is the color and can be "black" or "white" {'b'|'w'}.
    * The second is the pice name {'A'|'B'|'G'|'Q'|'S'}.
    * The third is the pice number used to distinguish pices of the same name {'1'|'2'|'3'}.
    * ex: "wG2" - represents the second played grasshopper played by the whites.

 - Move:
    * A move is represented by 3 sections.
    * The first is the notation of the moving pice.
    * The second is the point of contact with the pice where the move stops.
    * The third is the notation of the pice refered by the contact point.
    * ex: "wG2/*bA1" - the second white grasshopper is positioned touching the first black ant on its left-upper side.

 - Point Of Contact:
    * /* - moving pice is place touching the target pice at its upper-left face
    * |* - moving pice is place touching the target pice at its left face
    * \* - moving pice is place touching the target pice at its lower-left face
    * *\ - moving pice is place touching the target pice at its upper-right face
    * *| - moving pice is place touching the target pice at its right face
    * */ - moving pice is place touching the target pice at its lower-right face
    * =* - moving pice is place on top of the target pice


Board:
-----

The board is a virtual concept since there is no board in the original board game.
The first player played pice is positioned at the cell 0 and the seccond player places its first pice at the cell 1 touching the first pice on its right side ("*|").
