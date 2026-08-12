"""
Problem Statement
You are given a chess game recorded as a sequence of moves in standard algebraic notation (SAN). Design and implement a system that validates whether the game is legal — that is, every move is legal given the position that precedes it, starting from the standard initial position.
Your program should process the moves in order and either confirm the game is fully valid, or report the first illegal move (its index and the reason it is illegal).
You do not need to determine the game's outcome (win/draw). You only need to validate the legality of each move as it is played.
Understanding the Notation (SAN)
Each move describes what piece moves where. The square is written as a file (column, a–h) followed by a rank (row, 1–8). So e4 means the square in column e, row 4.
Pieces are identified by an uppercase letter; a pawn has no letter.
Symbol
Piece
K
King
Q
Queen
R
Rook
B
Bishop
N
Knight (N, because K is taken)
(none)
Pawn

Move examples:
Notation
Meaning
e4
Pawn moves to e4
Nf3
Knight moves to f3
Bb5
Bishop moves to b5
Qd8
Queen moves to d8
Ra1
Rook moves to a1
Kf1
King moves to f1

Captures are written with an x before the destination square:
Notation
Meaning
Nxe5
Knight captures the piece on e5
exd5
Pawn on the e-file captures on d5 (pawns use their starting file as the prefix)
Qxf7
Queen captures on f7

Castling uses a fixed symbol (letter O), regardless of colour:
Notation
Meaning
O-O
Kingside castle
O-O-O
Queenside castle

Promotion appends = and the new piece when a pawn reaches the last rank:
Notation
Meaning
e8=Q
Pawn advances to e8 and promotes to a Queen
bxa1=N
Pawn captures on a1 and promotes to a Knight

Check / checkmate may be suffixed but do not change what the move does — you may parse and ignore them if you wish:
Notation
Meaning
Qh5+
Move gives check
Qh7#
Move gives checkmate

Disambiguation — when two identical pieces can reach the same square, the origin file or rank is inserted:
Notation
Meaning
Nbd2
The knight on the b-file moves to d2 (the other knight could also reach d2)
R1a3
The rook on rank 1 moves to a3


Input
A list of moves in SAN, alternating White and Black:

Reading a few of these: e4 (White pawn to e4), e5 (Black pawn to e5), Nf3 (White knight to f3), Bb5 (White bishop to b5), O-O (White castles kingside), exd4 (Black e-file pawn captures on d4).
Output
If all moves are legal: VALID
If a move is illegal: the 0-based index of the first illegal move and a reason, e.g.:
 INVALID at index 6: king would pass through check while castling
Example — invalid game:
Input:  ["e4", "e5", "Ke2", "Nf6", "O-O"]
Output: INVALID at index 4: king has already moved, castling not allowed
"""



"""
Valid Case: 
Input: ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "O-O", "Nf6", "d4", "exd4"]
Output: Valid

Invalid Case: 
Input: ["e4", "e5", "Ke2", "Nf6", "O-O"]
Output: INVALID at index 4: king has already moved, castling not allowed


Rules:
1. symbols:
K King
Q Queen
R Rook
B Bishop
N Knight (N, because K is taken)
(none) Pawn

2. 
x -> Captures
O-O -> Castling
  -> Promotion
  -> checkmate
  -> Disambiguation
  
 
  
"""
