//
//  RepairDroid.swift
//  AdventOfCode2019
//
//  Created by Adahus on 16/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

import Foundation

enum Sector {
  case unknown, empty, wall, oxygen
  
  func show() -> String {
    switch self {
    case .unknown: return "?"
    case .empty:   return " "
    case .wall:    return "#"
    case .oxygen:  return "o"
    }
  }
}

class Space {
  static let height = 200
  static let width  = 200
  static let startX = 100
  static let startY = 100

  var sectors: [[Sector]]
  
  init() {
    sectors = Array(repeating: Array(repeating: Sector.unknown, count: Space.width), count: Space.height)
  }
  
  init(space: Space) {
    sectors = space.sectors
  }
  
  func count(sector: Sector) -> Int {
    sectors.reduce(0) { $0 +
      $1.reduce(0) { $0 + ($1 == sector ? 1 : 0) }
    }
  }
  func get(_ position: Position) -> Sector { sectors[position.x][position.y] }
  func put(_ position: Position, sector: Sector) {
    sectors[position.x][position.y] = sector
  }
  
  func show(rowFrom: Int = 0, rowTo: Int = 0, colFrom: Int = 0, colTo: Int = 0) {
    let rowTo = rowTo == 0 ? sectors[0].count-1 : rowTo
    let colTo = colTo == 0 ? sectors.count-1 : colTo
    for y in (rowFrom...rowTo) {
      print("Row: \(y)\(y<100 ? " " : "") ", terminator: "")
      for x in (colFrom...colTo)  {
        print(sectors[x][y].show(), terminator: "")
      }
      print()
    }
  }
  
  func find(sector: Sector) -> Position? {
    for y in sectors[0].indices {
      for x in sectors.indices {
        if sectors[x][y] == sector { return Position(x: x, y: y) }
      }
    }
    return nil
  }

}

enum RepairDroidMove: Int {
  case north = 1
  case south = 2
  case west  = 3
  case east  = 4
  
  var reverse: RepairDroidMove {
    switch self {
    case .north: return .south
    case .south: return .north
    case .west:  return .east
    case .east:  return .west
    }
  }
  
  static let allMoves: [RepairDroidMove] = [.north, south, west, east]

}

extension Position {
  func move(by: RepairDroidMove) -> Position {
    switch by {
    case .north: return Position(x: x,   y: y-1)
    case .south: return Position(x: x,   y: y+1)
    case .west:  return Position(x: x-1, y: y  )
    case .east:  return Position(x: x+1, y: y  )
    }
  }
}

enum SearchResult {
  case foundOxygen(at: Position)
  case deadEnd
}

class Path {
  var droid: RepairDroid
  var currentPosition: Position /// Where the droid is
  var used: Set<Position> /// Positions used by this path (Doesn;t matter what order they were made in!)
  var movesToTry: Set<RepairDroidMove>

  static let maxLength = 500
  static var longestPathFound = 0
  static var shortestPathToOxygen = 9999999999
  static var oxygenPosition: Position? = nil

  // Creates a path for a droid at a given position
  // optionally base this path on a previous path
  init(for droid: RepairDroid, path: Path?) {
    self.droid = droid

    currentPosition = droid.position
    used = path?.used ?? []
    used.insert(droid.position)
    if used.count > Path.longestPathFound {
      print("Longer path found: \(used.count)")
      Path.longestPathFound = used.count
    }

    movesToTry = [.north, .south, .east, .west]
    for move in movesToTry {
      //Only try moves into the unknown
      if droid.space.get(currentPosition.move(by: move)) != .unknown {
        movesToTry.remove(move)
      }
    }
  }
  
  func search() -> SearchResult {
    while !movesToTry.isEmpty {
      /// Remove the direction so we don;t try it again
      let tryMove = movesToTry.removeFirst()
      
      /// Try to get the droid to move:
      let result = droid.step(input: tryMove.rawValue) /// N.B. this updates space and position of droid but also returned what happened
      switch result {
      case 0:
        ///  0: The repair droid hit a wall. Its position has not changed.
        continue /// Try another direction
        
      case 1,2:
        ///  1: The repair droid has moved one step in the requested direction.

        if result == 2 {
          /// We've found oxygen - we won't stop as we need to know the whole map but we must record the oxygen location and path length:
          Path.oxygenPosition = droid.position
          if used.count < Path.shortestPathToOxygen {
            print("Shorter path to oxygen found: \(used.count)")
            Path.shortestPathToOxygen = used.count
          }
        }
        ///  We'd like to create a new path but first let's check if the path is over it's length limit"
        if used.count > Path.maxLength {
          fatalError("Maximim path length (\(Path.maxLength)) exceeded!!")
//           Alternatively could turn back....
//                    /// We hit a deadend so we need to move the droid back to it's previous position:
//                    let resultOfReverse = droid.step(input: tryMove.reverse.rawValue)
//                    guard resultOfReverse == 1 else { fatalError("Unexpected result from reverse of move!") }
//                    continue /// Try another direction
        }
        /// So create a new path from that new point
        let path = Path(for: droid, path: self)
        /// Search form that new point recursively
        switch path.search() {
          /// The only outcomes of a search are finding oxygen or a deadend:
        case .foundOxygen(let at):
          /// We're no longer doing this in the result but at a class level
          fatalError("Not doing any more!")
          return .foundOxygen(at: at)  /// i.e pass back to the parent path
        case .deadEnd:
          /// We hit a deadend so we need to move the droid back to it's previous position:
          let resultOfReverse = droid.step(input: tryMove.reverse.rawValue)
          guard resultOfReverse == 1 else { fatalError("Unexpected result from reverse of move!") }
          continue /// Try another direction
        }
        
      default:
        fatalError("Unknown return from droid!")
      }
    }
    return .deadEnd
  }
  
}

struct RepairDroid {
  var brain: IntCode
  var space: Space
  var position: Position {
    didSet {
      print("DROID: moves to: (\(position.x),\(position.y))")
    }
  }
  
  init() {
    brain = IntCode(program: repairDroid)
    space = Space()
    position = Position(x: Space.startX, y: Space.startY)
    print("DROID: starts at: (\(position.x),\(position.y))")
  }
  
  ///  Input:
  ///  1: north
  ///  2: south
  ///  3: west
  ///  4: east
  ///
  ///  Returns:
  ///  0: The repair droid hit a wall. Its position has not changed.
  ///  1: The repair droid has moved one step in the requested direction.
  ///  2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
  mutating func step(input: Int) -> Int {
    let direction = RepairDroidMove(rawValue: input)!
    let result = brain.run(input: [input]) /// Don't yield because we need an outputs
    switch result.count {
    case 0: fatalError("Should not end!!")
      
    case 1:  /// result will be [result of droid move]
      switch result[0] {
      case 0:
        ///  0: The repair droid hit a wall. Its position has not changed.
        /// Record that there's a wall
        space.put(position.move(by: direction), sector: .wall)
        /// But do not change the position
        
      case 1:
        ///  1: The repair droid has moved one step in the requested direction.
        /// Move to the new position
        position = position.move(by: direction)
        /// And record that this sector is empty
        space.put(position, sector: .empty)
        
      case 2:
        ///  2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
        /// Move to the new position
        position = position.move(by: direction)
        /// And record that this sector has oxygen
        space.put(position, sector: .oxygen)
        
      default:
        fatalError("Unknown return from droid!")
      }
    default:
      fatalError("Expected one output from droid!")
    }
    return result[0]
  }
  
  func getSector() -> Sector {
    space.get(position)
  }
  
  func stats() -> [Int] {
    let path = Path(for: self, path: nil)
    /// This search is to find the shortest path to the oxygen
    /// It also continues searching until all searchable sectors have been discovered
    let _ = path.search()
    print("Shortest path to oxygen = \(Path.shortestPathToOxygen)")
    print("Longest path = \(Path.longestPathFound)")

    space.show(rowFrom: 78, rowTo: 120, colFrom: 78, colTo: 120)
    let spaceToFill = Space(space: space) /// Make a copy of the space ready for filling
    var filled: Set<Position> = [Path.oxygenPosition!] /// Start with just the original oxygen producer
    var hours = 0
    while spaceToFill.count(sector: .empty) > 0 {
      hours += 1
      var newFilled = filled
      filled.forEach{ base in
        RepairDroidMove.allMoves.forEach{ move in
          let adjacent = base.move(by: move)
          if spaceToFill.get(adjacent) == .empty {
            spaceToFill.put(adjacent, sector: .oxygen) /// Fill empty corridor with oxygen
            newFilled.insert(adjacent)
          }
        }
      }
      filled = newFilled
    }
    print("Hours till full = \(hours)")
    return [Path.shortestPathToOxygen, hours]
  }
  
  var repairDroid = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1001,1034,0,1039,1001,1036,0,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,102,1,1034,1039,1001,1036,0,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,1001,1035,0,1040,101,0,1038,1043,101,0,1037,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,1001,1037,0,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,37,1032,1006,1032,165,1008,1040,5,1032,1006,1032,165,1102,1,2,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,64,1044,1106,0,224,1101,0,0,1044,1105,1,224,1006,1044,247,1002,1039,1,1034,101,0,1040,1035,102,1,1041,1036,102,1,1043,1038,101,0,1042,1037,4,1044,1106,0,0,13,40,97,1,18,1,79,93,56,16,38,41,78,11,78,25,46,84,31,38,76,17,96,5,78,50,8,67,77,54,42,82,39,2,8,5,11,85,37,93,37,7,97,12,94,2,44,70,74,78,34,45,94,75,19,8,84,72,2,9,69,74,6,11,75,79,42,35,86,83,23,82,88,40,81,70,8,58,46,57,77,65,76,68,79,61,24,80,61,88,70,42,32,71,16,23,99,77,73,57,45,99,39,29,97,4,90,76,3,5,86,11,95,94,90,59,13,37,94,29,57,42,99,4,45,96,22,74,33,73,70,24,96,4,82,10,3,79,37,81,97,72,42,66,3,27,98,4,73,49,55,86,12,41,65,38,21,66,27,80,87,53,86,26,85,80,42,26,92,17,79,76,58,69,2,71,7,88,12,61,73,16,67,48,83,87,8,21,72,67,50,70,7,71,9,53,46,81,99,47,3,70,11,23,68,22,86,43,32,92,30,78,94,61,81,32,60,89,97,58,23,27,52,99,85,90,41,20,11,87,73,57,83,30,79,2,58,93,32,81,16,86,35,87,38,73,88,11,6,65,32,20,81,87,89,12,11,66,42,84,12,79,14,23,72,37,85,95,15,48,80,92,59,56,7,95,85,21,82,53,93,45,73,29,79,6,17,68,79,34,72,47,39,81,93,63,83,51,67,99,1,74,56,89,47,86,95,51,94,46,3,95,18,81,20,85,19,90,60,24,65,65,46,91,17,82,37,87,21,83,80,22,28,75,17,68,72,40,67,82,19,9,79,42,86,55,93,91,41,76,55,22,74,61,91,42,96,73,11,1,79,60,85,82,40,76,88,84,2,14,97,89,29,69,39,43,65,19,58,97,68,45,50,2,91,54,52,93,82,61,76,22,15,77,63,76,60,81,42,89,77,45,80,3,92,17,10,98,16,92,38,71,2,46,81,81,11,7,43,82,68,82,93,25,44,87,60,49,48,7,47,82,82,26,65,93,50,75,57,92,57,78,11,39,99,2,93,42,69,6,66,60,96,79,50,20,75,84,48,98,57,5,93,98,62,78,85,53,85,32,37,90,90,30,43,74,57,81,19,35,19,94,50,65,60,98,65,46,86,75,68,16,31,83,75,56,93,35,42,89,32,69,35,2,60,82,58,53,1,87,18,66,82,41,73,73,7,99,91,89,48,83,20,81,31,66,17,93,23,41,86,65,57,72,13,13,82,94,79,77,54,89,90,62,95,35,74,82,37,43,33,66,77,3,86,26,87,35,69,19,24,85,62,18,9,72,42,69,25,95,57,34,41,82,36,90,24,36,27,67,49,30,70,75,82,44,33,67,70,35,36,69,33,85,10,87,50,72,8,74,97,18,95,25,97,5,84,16,65,60,89,15,86,81,9,75,73,58,72,39,91,10,55,3,11,86,96,18,98,97,28,22,98,49,89,19,84,18,98,34,92,67,37,80,17,8,65,72,2,91,95,55,76,19,30,78,40,96,78,34,91,99,23,14,71,38,37,71,59,93,78,83,61,24,31,97,25,85,8,16,84,15,65,77,14,96,98,6,89,33,98,59,4,84,66,18,74,48,12,41,86,31,45,33,74,97,86,55,85,16,34,54,91,77,3,19,65,70,18,90,41,98,25,55,22,95,15,92,14,67,20,88,5,51,69,92,33,69,75,56,36,91,3,80,13,78,36,88,50,88,79,65,24,66,5,99,45,98,88,66,30,92,98,84,5,90,13,67,95,96,33,77,30,80,39,99,81,95,55,86,0,0,21,21,1,10,1,0,0,0,0,0,0]
}
