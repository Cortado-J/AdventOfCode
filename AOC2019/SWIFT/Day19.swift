//
//  Day19.swift
//  AdventOfCode2019
//
//  Created by Adahus on 19/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

struct Day19 {

  var drone: IntCode
    
  init() {
    drone = IntCode(program: program)
  }
  
  mutating func pullTest(_ x: Int, _ y: Int) -> Bool {
    let row =
    ["#.......................................",
     ".#......................................",
     "..##....................................",
     "...###..................................",
     "....###.................................",
     ".....####...............................",
     "......#####.............................",
     "......######............................",
     ".......#######..........................",
     "........########........................",
     ".........#########......................",
     "..........#########.....................",
     "...........##########...................",
     "...........############.................",
     "............############................",
     ".............#############..............",
     "..............##############............",
     "...............###############..........",
     "................###############.........",
     "................#################.......",
     ".................########OOOOOOOOOO.....",
     "..................#######OOOOOOOOOO#....",
     "...................######OOOOOOOOOO###..",
     "....................#####OOOOOOOOOO#####",
     ".....................####OOOOOOOOOO#####",
     ".....................####OOOOOOOOOO#####",
     "......................###OOOOOOOOOO#####",
     ".......................##OOOOOOOOOO#####",
     "........................#OOOOOOOOOO#####",
     ".........................OOOOOOOOOO#####",
     "..........................##############",
     "..........................##############",
     "...........................#############",
     "............................############",
     ".............................###########"][y]
      
    return row[row.index(row.startIndex, offsetBy: x)] != "."
  }

  mutating func pull(_ x: Int, _ y: Int) -> Bool {
    drone = IntCode(program: program) /// Reset
    return drone.run(input: [x,y])[0] == 1
  }

  mutating func partA() -> [Int] {
    var count = 0
    for x in (0..<50) {
      for y in (0..<50) {
        if pull(x,y) {
          print("*", terminator: "")
          count += 1
        } else {
          print(".", terminator: "")
        }
      }
      print()
    }
    return [count]
  }
  
  mutating func partB() -> [Int] {
    var tractor: [(Int, Int)] = Array(repeating: (0,0), count: 2000) // Left x and right x of the tractor for each y
    
    func findTractor(y: Int, lastStart: Int?, lastEnd: Int?) {
      if y < 10 {
        tractor[y] = (0,1) //Fake pull for early ones
      } else {
        
        //look for first pull on row
        var x = lastStart ?? 0
        while !pull(x,y) {
          x += 1
        }
        let start = x
        //look for first last pull
        x = lastEnd ?? start
        while pull(x,y) {
          x += 1
        }
        let end = x-1
        tractor[y] = (start,end)
      }
      print("Y=\(y), startX=\(tractor[y].0), endX=\(tractor[y].1)")
    }

    for y in (0...99) {
      findTractor(y: y, lastStart: nil, lastEnd: nil)
    }
    var y = 99
    while tractor[y].0 + 99 > tractor[y-99].1 {
      let lastTractor = tractor[y]
      y += 1
      findTractor(y: y, lastStart: lastTractor.0-2, lastEnd: lastTractor.1-2)
    }
    let lowY = y-99
    let lowX = tractor[y-99].1 - 99
    print("lowY =\(lowY), lowX=\(lowX)")
    
    func around(_ midY: Int) {
      for y in (midY-2...midY+2) {
        print("Y=\(y), startX=\(tractor[y].0), endX=\(tractor[y].1)")
      }
    }
    print("=============================")
    around(lowY)
    print("=============================")
    around(lowY+99)
    print("=============================")

    return([lowX*10000 + lowY])
    
    //    =============================
    //    lowY =1322, lowX=975
    //    =============================
    //    Y=1320, startX=906, endX=1072
    //    Y=1321, startX=907, endX=1073
    //    Y=1322, startX=907, endX=1074  so right hand end is 1074 so 99 to left is 975
    //    Y=1323, startX=908, endX=1074
    //    Y=1324, startX=909, endX=1075
    //    =============================
    //    Y=1419, startX=974, endX=1152
    //    Y=1420, startX=975, endX=1153
    //    Y=1421, startX=975, endX=1154 99 on from above is 1421
    //    =============================
  }
  
  //  9071322 is wrong
  //  9751323 is wrong
  //  9751322 is wrong
  // 13220975 is wrong

  let program = [109,424,203,1,21102,1,11,0,1106,0,282,21101,0,18,0,1105,1,259,1201,1,0,221,203,1,21101,31,0,0,1105,1,282,21102,38,1,0,1105,1,259,21001,23,0,2,21201,1,0,3,21101,1,0,1,21102,57,1,0,1106,0,303,2102,1,1,222,21001,221,0,3,20102,1,221,2,21101,259,0,1,21102,80,1,0,1106,0,225,21101,0,167,2,21101,0,91,0,1105,1,303,2102,1,1,223,20102,1,222,4,21102,1,259,3,21102,1,225,2,21102,225,1,1,21102,1,118,0,1106,0,225,21001,222,0,3,21102,1,93,2,21101,0,133,0,1105,1,303,21202,1,-1,1,22001,223,1,1,21101,148,0,0,1105,1,259,2101,0,1,223,21001,221,0,4,20102,1,222,3,21102,21,1,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,1,195,0,106,0,108,20207,1,223,2,21001,23,0,1,21101,-1,0,3,21102,214,1,0,1106,0,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,1202,-4,1,249,21202,-3,1,1,21202,-2,1,2,21201,-1,0,3,21101,0,250,0,1105,1,225,22101,0,1,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22101,0,-2,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22102,1,-2,3,21102,343,1,0,1105,1,303,1106,0,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21102,384,1,0,1106,0,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,22102,1,1,-4,109,-5,2105,1,0]
}

