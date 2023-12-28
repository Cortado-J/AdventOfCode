//
//  Day11.swift
//  AdventOfCode2019
//
//  Created by Adahus on 11/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//


struct Day11 {
    
  func parta() -> [Int] {
    var robot = Robot()
    while robot.step() {
    }
    return [robot.painted.count]
  }
  
  func partb() -> [Int] {
    var robot = Robot()
    robot.hull.put(robot.position, colour: .white)
    while robot.step() {
    }
    robot.hull.squares.forEach{ row in
      print(row.map{ square in
        square == .black ? "." : "#"
      })
    }
    return [robot.painted.count]
  }
}
