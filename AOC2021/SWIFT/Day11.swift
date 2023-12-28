//
//  Day11.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 09/12/2021.
//
func day11() {
  var inputTest =
"""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

  var input =
"""
8448854321
4447645251
6542573645
4725275268
6442514153
4515734868
5513676158
3257376185
2172424467
6775163586
"""

  struct Cave: Hashable {
    var points: [[Int]] = []
    var stepCount = 0
    
    mutating func resetFlashed() -> Int {
      var flashCount = 0
      for row in 0..<points.count {
        for col in 0..<points[0].count {
          if points[row][col] > 9 {
            flashCount += 1
            points[row][col] = 0
          }
        }
      }
      return flashCount
    }
    
    mutating func inc(_ row: Int, _ col: Int) {
      guard col >= 0 && col < 10 && row >= 0 && row < 10 else { return }
      points[row][col] += 1
      if points[row][col] == 10 {
        for drow in -1...1 {
          for dcol in -1...1 {
            if !(drow == 0 && dcol == 0) {
              inc(row+drow, col+dcol)
            }
          }
        }
      }
    }

    mutating func incAll() {
      for row in 0..<points.count {
        for col in 0..<points[0].count {
          inc(row, col)
        }
      }
    }

    mutating func step() -> Int {
      stepCount += 1
      print("##############################")
      //show("START")
      incAll()
      //show("INCED")
      let flashes = resetFlashed()
      //show("DONE")
      return flashes
    }
    
    func show(_ message: String) {
      print("step = \(stepCount) - - - - - - - - - - - - - - - -")
      print(message)
      for row in points {
        print(row)
      }
    }
  }
  
  struct Point: Hashable {
    var col: Int
    var row: Int
  }
  
  var cave = Cave(points: input
                    .lines
                    .map{
    String($0)
      .trimmingCharacters(in: .whitespaces)
      .map{ Int(String($0))! }
  }
  )
  
  print("Day11")
  var keepCave = cave

  cave.show("BEGIN")
  var flash = 0
  for stepNum in 1...100 {
    flash += cave.step()
    if [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100].contains(stepNum) {
      cave.show("STEP")
    }
  }
  print("part one = \(flash)")

  cave = keepCave
  var stepNum = 0
  repeat {
    flash = cave.step()
    stepNum += 1
  } while (flash < 100)
  print("part two = \(stepNum)")
}
