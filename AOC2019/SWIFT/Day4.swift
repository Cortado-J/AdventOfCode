//
//  Day4.swift
//  AdventOfCode2019
//
//  Created by Adahus on 04/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

struct Day4 {
  let minValue = 147981
  let maxValue = 691423

  func lengthsIn(_ string: String) -> Set<Int> {
    var result: Set<Int> = []
    var last: Character = "#"
    var length = 0
    for char in string {
      if last == "#" {
        length = 1
      } else {
        if char == last {
          length += 1
        } else {
          result.insert(length)
          length = 1
        }
      }
      last = char
    }
    if length > 0 {
      result.insert(length)
    }
    return result
  }
  
  func day4AandB() -> (Int,Int) {
    var countA = 0
    var countB = 0
    for value in (minValue...maxValue) {
      let d1 = (value / 100000) % 10
      let d2 = (value /  10000) % 10
      //      if d2 == 0 { print(value) }
      let d3 = (value /   1000) % 10
      let d4 = (value /    100) % 10
      let d5 = (value /     10) % 10
      let d6 = (value /      1) % 10
      let pair = (d1 == d2)
        || (d2 == d3)
        || (d3 == d4)
        || (d4 == d5)
        || (d5 == d6)
      if pair
        && d2 >= d1
        && d3 >= d2
        && d4 >= d3
        && d5 >= d4
        && d6 >= d5 {
        countA += 1
        if lengthsIn(String(value)).contains(2) {
          countB += 1
        }
      }
    }
    return (countA, countB)
  }

}
