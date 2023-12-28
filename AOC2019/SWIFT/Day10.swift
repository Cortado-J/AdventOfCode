//
//  Day10.swift
//  AdventOfCode2019
//
//  Created by Adahus on 09/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//
import Foundation

struct Position: Equatable, Hashable {
  var x: Int
  var y: Int
}

struct Day10 {

  var data = [
  "#....#.....#...#.#.....#.#..#....#",
  "#..#..##...#......#.....#..###.#.#",
  "#......#.#.#.....##....#.#.....#..",
  "..#.#...#.......#.##..#...........",
  ".##..#...##......##.#.#...........",
  ".....#.#..##...#..##.....#...#.##.",
  "....#.##.##.#....###.#........####",
  "..#....#..####........##.........#",
  "..#...#......#.#..#..#.#.##......#",
  ".............#.#....##.......#...#",
  ".#.#..##.#.#.#.#.......#.....#....",
  ".....##.###..#.....#.#..###.....##",
  ".....#...#.#.#......#.#....##.....",
  "##.#.....#...#....#...#..#....#.#.",
  "..#.............###.#.##....#.#...",
  "..##.#.........#.##.####.........#",
  "##.#...###....#..#...###..##..#..#",
  ".........#.#.....#........#.......",
  "#.......#..#.#.#..##.....#.#.....#",
  "..#....#....#.#.##......#..#.###..",
  "......##.##.##...#...##.#...###...",
  ".#.....#...#........#....#.###....",
  ".#.#.#..#............#..........#.",
  "..##.....#....#....##..#.#.......#",
  "..##.....#.#......................",
  ".#..#...#....#.#.....#.........#..",
  "........#.............#.#.........",
  "#...#.#......#.##....#...#.#.#...#",
  ".#.....#.#.....#.....#.#.##......#",
  "..##....#.....#.....#....#.##..#..",
  "#..###.#.#....#......#...#........",
  "..#......#..#....##...#.#.#...#..#",
  ".#.##.#.#.....#..#..#........##...",
  "....#...##.##.##......#..#..##...."]
  
  let dataTest = [
".#..#",
".....",
"#####",
"....#",
"...##"
  ]

  let dataTest2 = [
  "......#.#.",
  "#..#.#....",
  "..#######.",
  ".#.#.###..",
  ".#..#.....",
  "..#....#.#",
  "#..#....#.",
  ".##.#..###",
  "##...#..#.",
  ".#....####"]
  
  let data3 = [
  ".#..##.###...#######",
  "##.############..##.",
  ".#.######.########.#",
  ".###.#######.####.#.",
  "#####.##.#.##.###.##",
  "..#####..#.#########",
  "####################",
  "#.####....###.#.#.##",
  "##.#################",
  "#####.##.###..####..",
  "..######..##.#######",
  "####.##.####...##..#",
  ".#####..#.######.###",
  "##...#.##########...",
  "#.##########.#######",
  ".####.#.###.###.#.##",
  "....##.##.###..#####",
  ".#.#.###########.###",
  "#.#.#.#####.####.###",
  "###.##.####.##.#..##"]

  let dataVap = [
  ".#....#####...#..",
  "##...##.#####..##",
  "##...#...#.#####.",
  "..#.....X...###..",
  "..#.#.....#....##"]
  
  func partaandb() -> [Int] {
    let lines = data
//      let lines = dataTest

      .map{ $0.map{$0 == "#" } }
    
    let width = lines[0].count
    let height = lines.count
    
    var moons: [Position] = []
    
    for x in (0..<width) {
      for y in (0..<height) {
        if lines[y][x] {
          moons.append( Position(x: x, y: y) )
        }
      }
    }
    print(moons)
    

    let views = 0
    
    func canSee(a: Position, b: Position) -> Bool {
      for c in moons {
        if c != a && c != b {
          let ay = c.y - a.y
          let ax = c.x - a.x
          let by = c.y - b.y
          let bx = c.x - b.x

          if (ay > 0 && by < 0)
            || (ay < 0 && by > 0) {
            let slopea = Double(ax) / Double(ay)
            let slopeb = Double(bx) / Double(by)
            if  abs(slopea - slopeb) < 0.000000001 {
              return false
            }
          }
          if (ax > 0 && bx < 0)
            || (ax < 0 && bx > 0) {
            let slopea = Double(ay) / Double(ax)
            let slopeb = Double(by) / Double(bx)
            if  abs(slopea - slopeb) < 0.000000001 {
              return false
            }
          }
        }
      }
      return true
    }

    var maxi = 0
    var bestmoonopt: Position? = nil

    for moona in moons {
      var count = 0
      //print("----------------\(moona)")
      for moonb in moons {
        if moona != moonb {
          if canSee(a: moona, b: moonb) {
            //print("\(moona) can see \(moonb)")
            count += 1
          }
        }
      }
      if count > maxi {
        bestmoonopt = moona
        maxi = count
      }
    }
    
    let bestmoon = bestmoonopt!
    
    print(bestmoon)
    
    var moonsOtherThanBest = moons
    moonsOtherThanBest.removeAll{
      $0 == bestmoon
    }

    let bearings = moonsOtherThanBest.map{ (moon) -> (Position, Double, Int) in
      let dy: Int = moon.y - bestmoon.y
      let dx: Int = moon.x - bestmoon.x
      return (moon,
              bearing(dy: -dy, dx: dx).rounded(toPlaces: 10),  /// Note we use -dy because we want the bearings to be such that a bearing of 0 is up which is y descending
              abs(dx) + abs(dy) /// Manhattan distance is fine because we will only sort in groups of the same bearing
      )
    }
    
    let bearingList = Array(Set(bearings.map{ $0.1 })).sorted()
    
    var moonsOnBearing = bearingList.map{ bearing in
      bearings
        .filter{ $0.1 == bearing }
        .sorted{ $0.2 < $1.2 }
        .map{ $0.0 }
    }
    
    /// So now we have an array of arrays in bearing order (from 0...359)
    /// And each array in the array is sorted into manhattan distance order so the nearest ones are first
    /// Manhattan distance is fine because we will only sort in groups of the same bearing
    
    print(moonsOnBearing)
    
    var index = 0
    var count = 0
    while true {
      if moonsOnBearing[index].count > 0 {
        /// There's a moon left on this bearing:
        count += 1
        if count == 200 { break }
        var current = moonsOnBearing[index]
        print("Vaporised: \(count): \(current[0])")
        current.remove(at: 0)
        moonsOnBearing[index] = current
      }
      index += 1
      /// Check for loopback to start
      if index >= moonsOnBearing.count { index = 0 }
    }
    print("= = = = = = =")
    print(count,moonsOnBearing[index])
    print("= = = = = = =")

    let moon200 = moonsOnBearing[index][0]
    let partbResult = moon200.x * 100 + moon200.y
    
    return [maxi,partbResult]
  }

}
