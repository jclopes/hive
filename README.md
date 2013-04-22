The Hive
========

Based on the board game "The Hive"
The aim of this project is to have a standard playground to develop and test A.I. to play the Hive game.

```
    / \ / \
   |   |   |
  / \ / \ / \
 |   |   |   |
  \ / \ / \ /
   |   |   |
    \ / \ /
```

Notation:
--------

 - Piece:
    * A piece is represented by 3 chars.
    * The first is the color and can be "black" or "white" {`b`|`w`}.
    * The second is the piece name {`A`|`B`|`G`|`Q`|`S`}.
    * The third is the piece number used to distinguish pieces of the same name {`1`|`2`|`3`}.
    * ex: `wG2` - represents the second played grasshopper played by the whites.

 - Move:
    * A move is represented by 3 sections.
    * The first section is the notation of the moving piece.
    * The second is the point of contact with the piece where the move stops.
    * The third is the notation of the piece refered by the contact point.
    * ex: `wG2/*bA1` - the second white grasshopper is positioned touching the first black ant on its left-upper side.

 - Point Of Contact:
    * `/*` - moving piece is place touching the target piece at its upper-left face
    * `|*` - moving piece is place touching the target piece at its left face
    * `\*` - moving piece is place touching the target piece at its lower-left face
    * `*\` - moving piece is place touching the target piece at its upper-right face
    * `*|` - moving piece is place touching the target piece at its right face
    * `*/` - moving piece is place touching the target piece at its lower-right face
    * `=*` - moving piece is place on top of the target piece

 - Starting Piece:
    The only exception to the previous notation is the starting piece of the first player. The first move of the first player is just the name of a piece since the placement of the 1st piece is always fixed.

Board:
-----

The board is a virtual concept since there is no board in the original board game.
The first player played piece is positioned at the cell 0,0 and the seccond player places its first piece at the cell 0,1 touching the first piece on its right side ("*|").
