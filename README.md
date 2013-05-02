The Hive
========

Implementation of the board game "Hive" from gen42 [http://www.gen42.com/hive].
The aim of this project is to have a standard playground to develop and test
A.I. to play the Hive game.

Board:
-----

The board is a virtual concept since there is no board in the original board
game but as pieces are placed next to each other an hexagonal structure forms.
The internal representation of the hexagonal board is a 2 dimentional matrix.

```
  / \ / \ / \
 |0,0|1,0|2,0|
  \ / \ / \ / \
   |0,1|1,1|2,1|
  / \ / \ / \ /
 |0,2|1,2|2,2|
  \ / \ / \ /
```

Notation:
--------

To represent each move of the game I created a human readable notation that
can be easily parsed by a machine.

 - __Piece__:
    A piece is represented by 3 chars.
    * The first is the color and can be "black" or "white" {`b`|`w`}.
    * The second is the piece name {`A`|`B`|`G`|`Q`|`S`}.
    * The third is the piece number used to distinguish pieces of the same
        name {`1`|`2`|`3`}.
    * ex: `wG2` - represents the second played grasshopper played by the
        whites.

 - __Move__:
    A move can be a placement of a piece from the player set into the board or
    moving a piece from its current position to a new position. Both of this
    actions are represented in the same way.
    A move representation has 3 sections:
        (action piece)+(point of contact)+(target piece)
    * The first section is the notation of the action piece.
    * The second is the point of contact with the piece where the move stops.
    * The third is the notation of the piece refered by the contact point.
    * ex: `wG2/*bA1` - the second white grasshopper is positioned touching the
        first black ant on its left-upper side.

 - __Point Of Contact__:
    To represent how the pieces are placed next to each other we refer to wich
    face of the target piece the action piece will be touching by the end of
    the action.
    * `/*` - NW (north-west) active piece is place touching the target piece
        at its upper-left face.
    * `|*` - W (west) active piece is place touching the target piece at its
        left face.
    * `\*` - SW (south-west) active piece is place touching the target piece
        at its lower-left face.
    * `*\` - NE (noth-east) active piece is place touching the target piece at
        its upper-right face.
    * `*|` - E (east) active piece is place touching the target piece at its
        right face.
    * `*/` - SE (south-east) active piece is place touching the target piece
        at its lower-right face.
    * `=*` - O (origin/over) active piece is place on top of the target piece.

 - __Starting Piece__:
    The only exception to the previous notation is the starting piece of the
    first player. The first move of the first player is just the name of a
    piece since the placement of the 1st piece is always fixed.
