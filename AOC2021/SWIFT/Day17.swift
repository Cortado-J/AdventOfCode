//
//  Day17.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 09/12/2021.
//
func day17() {
  print("Day17")
  
    let minx =  150, maxx = 193
    let miny = -136, maxy = -86

  //Test
  //  let minx =  20, maxx = 30
  //  let miny = -10, maxy = -5
  
  func shoot(setvx: Int, setvy: Int) -> Int? {
    //    print("==================================================")
    //    print("shoot(setvx: \(setvx), setvy: \(setvy))")
    var x = 0
    var y = 0
    var vx = setvx
    var vy = setvy
    var step = 0
    var highesty = miny-1
    
    while true {
      step += 1
      x += vx
      y += vy
      highesty = max(y, highesty)
      if vx > 0 { vx -= 1 }
      if vx < 0 { vx += 1 }
      vy -= 1
      //print("...step=\(step): x=\(x) y=\(y) vx=\(vx) vy=\(vy)")
      if (x >=  minx) && (x <= maxx) && (y >=  miny) && (y <= maxy) {
//        print("In area and highest y was \(highesty)")
        return highesty
      }
      if y < miny { return nil }
    }
    
  }

  var maxHighest = minx-1000

  var count = 0
  
  for x in stride(from: 1, through: maxx, by: 1) {
    for y in stride(from: -miny, through: miny, by: -1) {
      if let answer = shoot(setvx: x,setvy: y) {
        count += 1
        print("x=\(x), y=\(y) gives: \(answer)")
        if answer > maxHighest {
          maxHighest = answer
          print("HIGHER:", answer)
        }
      }
    }
  }
  
  print("Max Highest=\(maxHighest)")
  print("Number of solutions=\(count)")

}
