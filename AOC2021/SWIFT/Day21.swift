//
//  Day21.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 22/12/2021.
//

let player1 = 8
let player2 = 6

func day21() {


  enum Game: Hashable {
    case playing(scores: [Int])
    case ended(winner: Int)

    // From the current position and score determine outcome:
    func turn(player: Int, score: Int) -> Game {
      let winningScore = 21
      switch self {
      case var .playing(scores):
        scores[player] += score
        if scores[player] >= winningScore {
          return .ended(winner: player)
        } else {
          return .playing(scores: scores)
        }
      case .ended: fatalError("Shouldn't have a turn if the game has ended!")
      }
    }

    // From the current position determine positions of all possible outcomes for given player:
    func turnOutcomes(player: Int) -> Multiset<Game> {
      var result: Multiset<Game> = []
      for roll1 in 1...3 {
        for roll2 in 1...3 {
          for roll3 in 1...3 {
            result.insert(turn(player: player, score: roll1+roll2+roll3))
          }
        }
      }
      return result
    }
  }

  var games: Multiset<Game>
  // Start with one game with no score
  = [ .playing(scores: [0,0]) ]
  
//  games = games.union()
  func turn() {
    
  }
  
  
  
}
