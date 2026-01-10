Feature: TicTacToe Memory Challenge Gameplay
  As a child player
  I want to play tic-tac-toe with a memory twist
  So that I can have fun while training my memory

  Scenario: Start new game on easy difficulty
    Given a new game is started
    And difficulty is set to "easy"
    Then the countdown should be 10 seconds
    And the board should be visible
    And it should be the player's turn

  Scenario: Player makes a valid move
    Given a new game is started
    When the player places a mark at position 4
    Then position 4 should contain the player's mark
    And it should be the computer's turn

  Scenario: Win detection works correctly
    Given a new game is started
    And the player has marks at positions 0, 1, 2
    Then the player should win
    And win streak should increase by 1

  Scenario: Difficulty affects countdown time
    Given a new game is started
    When difficulty is set to "hard"
    Then the countdown should be 1 second
