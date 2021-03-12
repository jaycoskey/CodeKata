== ChessKata ==

I originally imagined a Code Kata as an exercise that took at most a few hours. Implement an algorithm or use a particular metaprogramming technique, etc. Then I later thought that they could be longer---even longer than a day. But the scope should be small enough that, if the Code Kata were repeated, it could eventually be completed within a day. With this in mind, the initial iteration should be less than a week.

* Day 1:
  * See how far I could get towards implementation of a chess program. Might later continue on to additional days.
  * Small amount of testing.
* Day 2:
  * Complete-ish design of class APIs.
  * Some testing for each main class.
* Day 3:
  * Some user interactivity.
* Day 4:
  * Two-player game from console. Some feature might be omitted (e.g., castling, Pawn promotion, some forms of stalemate).
  * Some testing for each of the pure functions.
* Day 5:
  * Complete rules.
* Day 6:
  * Undo feature.

=== Priorities and non-goals ===
* Project non-goals
  * GUI
  * AI

* Day 1
  * Day 1 priorities    
    * Explore design decisions.
    * End with something that compiles.
    * Avoid a class hierarchy of Pieces. (Option: Use a type enum instead)
    * Game rules (e.g., move rules for each piece) should be made concise through supporting definitions.
    * Some testing ... but not much.
    * Initially: Use a sparse array of pieces at their (x,y) board locations is OK.
      * Optional: Consider using integer indexing of board pieces (e.g., 0..63).
    * Add TODO statements to highlight actions adjacent to existing functionality.
  * Day 1 non-goals    
    * A project plan---except to the extent that this file counts as one.
    * Thorough testing.
    * Text interface (not a day-one feature)
    * GUI (not a day-two feature)
    * An undo feature (should be an eventual goal if project is continued) 
    * Exact interfaces and implementations. (TODO: Complete class APIs, encapsulating data with privacy)
      * The small use of smart points need expansion.
      * The interfaces c 
    * Not all unfinished features need TODO statements.
