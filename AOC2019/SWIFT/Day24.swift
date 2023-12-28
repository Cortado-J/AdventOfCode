//
//  Day24.swift
//  AdventOfCode2019
//
//  Created by Suhada on 24/12/2019.
//  Copyright © 2019 Suhada. All rights reserved.
//

struct World: Hashable {
  var spaces: [[Bool]]

  init(spaces: [[Bool]]) {
    self.spaces = spaces
  }

  init() {
    spaces = (0...4).map{ _ in (0...4).map{ _ in false } }
  }
  
  /// Allows x, y to be outside range
  func get(x: Int, y: Int) -> Bool {
    guard x >= 0 && x < spaces.count else { return false }
    guard y >= 0 && y < spaces[0].count else { return false }
    return spaces[x][y]
  }
  
  func neighbours(x: Int, y: Int) -> Int {
    (  get(x: x+1, y: y  ) ? 1 : 0) +
      (get(x: x-1, y: y  ) ? 1 : 0) +
      (get(x: x  , y: y+1) ? 1 : 0) +
      (get(x: x  , y: y-1) ? 1 : 0)
  }
  
  func gen() -> World {
    World(spaces: spaces.indices.map{ x in
      spaces[0].indices.map { y in
        let current = get(x: x, y: y)
        let neigh = neighbours(x: x, y: y)
        // if x == 2 && y == 2 { return false }  This was tried in case centre cell was ignored!!
        if current { if neigh != 1 { return false }
        } else {     if neigh == 1 || neigh == 2 { return true }
        }
        return current
      }
      }
    )
  }
  
  func bugs() -> Int {
    var result = 0
    spaces.forEach { row in
      row.forEach { cell in
        if cell { result += 1 }
      }
    }
    return result
  }

  func biodiversity() -> Int {
    var result = 0
    var mult = 1
    spaces.forEach { row in
      row.forEach { cell in
        if cell { result += mult }
        mult *= 2
      }
    }
    return result
  }
  
  func show() {
    spaces.forEach { row in
      row.forEach { cell in
        print(cell ? "#" : ".", terminator: "")
      }
      print()
    }
    print("------------------------------")
  }
  
}

struct NestedWorld {
  var worlds: [World]
  
  init(worlds: [World]) {
    self.worlds = worlds
  }

  /// Allows x, y to be outside range
  func get(level: Int, x: Int, y: Int) -> Bool {
    guard level >= 0 else { return false } /// Nothing adjacent to top level!
    guard level < worlds.count else { return false } /// Nothing after top level! (Important that extra levels added as necessary)
    guard !(x == 2 && y == 2) else { return false } /// Nothing in the middle (other routines will deal with recursion)
    return worlds[level].get(x: x, y: y)
  }

  func count(level: Int, points: [(x: Int, y: Int)]) -> Int {
    points.reduce(0){ $0 + (get(level: level, x: $1.x, y: $1.y) ? 1 : 0) }
  }

  func neighbours(level: Int, x: Int, y: Int) -> Int {
    var result = worlds[level].neighbours(x: x, y: y)
    switch (x,y) {
    // Neighbours in next level in
    case (1,2): result += count(level: level+1, points: [(0,0),(0,1),(0,2),(0,3),(0,4)])
    case (3,2): result += count(level: level+1, points: [(4,0),(4,1),(4,2),(4,3),(4,4)])
    case (2,1): result += count(level: level+1, points: [(0,0),(1,0),(2,0),(3,0),(4,0)])
    case (2,3): result += count(level: level+1, points: [(0,4),(1,4),(2,4),(3,4),(4,4)])

      // Neighbours in next level out
      // Note that these are only done if level is 0 or greater because level 0 does not have a "next level out"
    case (0,0): if level >= 0 { result += count(level: level-1, points: [(1,2),(2,1)]) }
    case (0,4): if level >= 0 { result += count(level: level-1, points: [(1,2),(2,3)]) }
    case (4,0): if level >= 0 { result += count(level: level-1, points: [(2,1),(3,2)]) }
    case (4,4): if level >= 0 { result += count(level: level-1, points: [(2,3),(3,2)]) }

    case (0,_): if level >= 0 { result += count(level: level-1, points: [(1,2)]) }
    case (4,_): if level >= 0 { result += count(level: level-1, points: [(3,2)]) }
    case (_,0): if level >= 0 { result += count(level: level-1, points: [(2,1)]) }
    case (_,4): if level >= 0 { result += count(level: level-1, points: [(2,3)]) }

    default: break
    }
    return result
  }
  
  func gen() -> NestedWorld {
    var nestedWorld = self
//    if nestedWorld.worlds.last!.bugs() > 0 {
//      /// There's at least one bug in the last level so add an extra blank level on the end in case any new bugs need making there:
//      nestedWorld.worlds.append( World(spaces: nestedWorld.worlds[0].spaces.map{ $0.map{ _ in false } } ) )
//    }
    return NestedWorld(worlds:
      nestedWorld.worlds.indices.map{ level in
        //print("level=\(level)---------------------------------")
        return World(spaces:
          nestedWorld.worlds[level].spaces.indices.map{ y in
            nestedWorld.worlds[level].spaces[0].indices.map{ x in
              if x == 2 && y == 2 { return false }
              let current = nestedWorld.get(level: level, x: x, y: y)
              let neigh = nestedWorld.neighbours(level: level, x: x, y: y)
              //print("level=\(level), x=\(x), y=\(y), current=\(current), neigh=\(neigh)")
              if current { if neigh != 1 { return false }
              } else {     if neigh == 1 || neigh == 2 { return true }
              }
              return current
            }
          }
        )
      }
    )


  }
  
  func bugs() -> Int {
    var result = 0
    worlds.forEach { world in
      world.spaces.forEach { row in
        row.forEach { cell in
          result += (cell ? 1 : 0)
        }
      }
    }
    return result
  }
  
  func show() {
    var rows = worlds[0].spaces.map{ _ in "" } // Construct rows to be built on.
    worlds.forEach{ world in
      world.spaces.enumerated().forEach{ (index, row) in
        row.forEach{ cell in
          rows[index] += cell ? "#" : "."
        }
        rows[index] += " "
      }
    }
    rows.forEach{ row in print(row) }
    print()
  }

}

struct Day24 {
  let data = [
    "####.",
    ".###.",
    ".#..#",
    "##.##",
    "###.."
  ]
  
  let dataTest = [
    "....#",
    "#..#.",
    "#..##",
    "..#..",
    "#...."
  ]

  func parta() -> [Int] {
    var world = World(spaces: data.map { row in row.map{ char in char == "#" } } )
    var history: [World] = []
    var gen = 0
    print("Generation: \(gen)")
    world.show()
    var first: Int? = nil
    repeat {
      history.append(world)
      world = world.gen()
      gen += 1
      print("Generation: \(gen)")
      world.show()
      first = history.firstIndex(of: world)
    } while first == nil
    print("#####################################################")
    print("Gen \(first) is same as Gen \(history.count)")
    world.show()
    print("#####################################################")
    return [world.biodiversity()]
    // Tried 18371095 but was the answer to someone else's puzzle!!
    // Tried 18842609 but was the answer to someone else's puzzle!!
  }
  
  func partb() -> [Int] {
    let needed = 300
    let generations = 200
    var nestedWorld = NestedWorld(worlds: Array(repeating: World(), count: needed))
    nestedWorld.worlds[needed / 2] = World(spaces: data.map { row in row.map{ char in char == "#" } } )
    nestedWorld.show()
    for _ in (1...generations) {
      nestedWorld = nestedWorld.gen()
      nestedWorld.show()
    }
    return [nestedWorld.bugs()]
  }
  
}
