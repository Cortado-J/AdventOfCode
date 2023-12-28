//
//  Day13.swift
//  AdventOfCode2019
//
//  Created by Adahus on 13/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

struct Day13 {
  
  func parta() -> [Int] {
    var game = Game()
    while game.step(input: []) {
    }
    return [game.screen.count(tile: .block)]
  }
  
  func partb() -> [Int] {
    var game = Game()
    game.brain.memory.patch(address: 0, value: 2)
    while game.step(input: [game.joystick.rawValue]) {
      game.screen.show()
      print("Score = \(game.score)")
      
      if game.screen.count(tile: .block) == 0 { break }

      guard let ball   = game.screen.find(tile: .ball)   else { fatalError("Ball not found") }
      guard let paddle = game.screen.find(tile: .paddle) else { fatalError("Paddle not found") }
      if ball.x < paddle.x {
        game.joystick = .left
      } else {
        if ball.x > paddle.x {
          game.joystick = .right
        } else {
          game.joystick = .neutral
        }
      }
    }
    return [game.score]
  }
}
