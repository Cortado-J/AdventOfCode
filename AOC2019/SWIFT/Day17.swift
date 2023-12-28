//
//  Day17.swift
//  AdventOfCode2019
//
//  Created by Adahus on 17/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

extension Int {
  var asArray: [Int] { [self] }
}

struct Day17 {
  
  func parta() -> [Int] {
    var ascii = Ascii()
    return ascii
      .intersections()
      .reduce(0) {
        $0 + ($1.0 * $1.1)
    }
    .asArray
  }
  
  func partb() -> [Int] {
    var ascii = Ascii()
    ascii.explore()
    return [88888]
  }
  
}
