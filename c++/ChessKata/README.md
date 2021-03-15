## ChessKata

I originally imagined a Code Kata as an exercise that took at most a few hours. Implement an algorithm or use a particular metaprogramming technique, etc. Then I later thought that they could be longer---even longer than a day. But the scope should be small enough that, if the Code Kata were repeated, it could eventually be completed within a day. With this in mind, the initial iteration should be less than a week.

* Day 1:
  * See how far I could get towards implementation of a chess program in one day. Unsure whether I'll continue.
  * Display of board, and partial implementation of classes: Game, Board, Player, Piece, Move, and several enums.
  * Small amount of testing.
* Day 2:
  * Some user interactivity (move entry and execution) without Pawns. (Moved up from Day 3)
  * Improved naming and encapsulation.
  * No additional testing.
* Day 3 (projected)
  * Pawn movement.
  * Zobrist hashing, to detect board layout repetition.
  * Stalemate detection.
  * Complete-ish design of class APIs. (Deferred from Day 2)
  * Some testing for each main class.  (Deferred from Day 2)
* Day 4 (projected)
  * Two-player game from console.
  * Some feature might be omitted (e.g., castling, Pawn promotion, some forms of stalemate).
* Day 5 (projected)
  * Complete rules.
* Day 6 (projected)
  * Undo feature.

### Priorities and non-goals
* Project non-goals
  * GUI
  * AI

* Day 1
  * Day 1 priorities
    * Explore design decisions.
    * Sketch out the main classes, ending with something that compiles.
    * Avoid a class hierarchy of Pieces. (Option: Use a type enum instead)
    * Allow for future support of hexagonal boards by encapsulating board geometry.
    * Game rules (at least per-piece move rules) should be made concise through supporting definitions.
    * Initially: Use a sparse array of pieces at their (x,y) board locations is OK.
      * Optional: Consider using integer indexing of board pieces (e.g., 0..63).
    * Some testing.
    * Add TODO statements to highlight actions adjacent to existing functionality.
  * Day 1 non-goals
    * A project plan---except to the extent that this file counts as one.
    * GUI
    * An undo feature (should be an eventual goal if project is continued)
    * Finalized interfaces and implementations. (TODO: Complete class APIs, encapsulating data with privacy)
    * Thorough testing.
    * Detailed feature or task backlog.
