//
//  Extensions.swift
//  AdventOfCode2019
//
//  Created by Adahus on 09/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

import Foundation

let show = false
func debug(_ message: String, show: Bool = true) { if show { print(message) } }

extension Int {
  // units = position 0, tens = position 1, etc
  func digit(_ position: Int) -> Int {
    return self / Int(pow(10,Double(position))) % 10
  }
}

extension Array {
  func chunked(into size: Int) -> [[Element]] {
    return stride(from: 0, to: count, by: size).map {
      Array(self[$0 ..< Swift.min($0 + size, count)])
    }
  }
}

func bearing(dy: Int, dx: Int) -> Double {
  if dx > 0 { return  90 - atan(Double(dy)/Double(dx))/(2 * .pi)*360 }
  if dx < 0 { return 270 - atan(Double(dy)/Double(dx))/(2 * .pi)*360 }
  // So dx == 0 and:
  if dy > 0 { return   0 }
  if dy < 0 { return 180 }
  // So dy == 0 and:
  fatalError("Must have either dx or dy as nonzero!")
}

extension Double {
  /// Rounds the double to decimal places value
  func rounded(toPlaces places:Int) -> Double {
    let divisor = pow(10.0, Double(places))
    return (self * divisor).rounded() / divisor
  }
}

//extension Array where Element: Equatable {
//  //  .#.#...#...   -->   #.#...#...
//  func leftTrimmed(_ compare: Element) -> Self {
//    var result = self
//    while let element = result.first, element == compare {
//      result.remove(at: 0)
//    }
//    return self
//  }
//
//  //  .#.#...#...   -->   .#.#...#
//  func rightTrimmed(_ compare: Element) -> Self {
//    var result = self
//    while let element = result.last, element == compare {
//      result.remove(at: result.count-1)
//    }
//    return self
//  }
//
//  //  .#.#...#...   -->   #.#...#
//  func trimmed(_ compare: Element) -> Self {
//    leftTrimmed(compare).rightTrimmed(compare)
//  }
//  
//  func leftBordered(_ element: Element, width: Int = 1) -> Self {
//    var result = self
//    if width > 0 {
//      for _ in (1...width) {
//        result.insert(element, at: 0)
//      }
//    }
//    return self
//  }
//
//  func rightBordered(_ element: Element, width: Int = 1) -> Self {
//    var result = self
//    if width > 0 {
//      for _ in (1...width) {
//        result.append(element)
//      }
//    }
//    return self
//  }
//
//  func bordered(_ element: Element, width: Int = 1) -> Self {
//    leftBordered(element, width: width)
//      .rightBordered(element, width: width)
//  }
//
//}
//
//extension Collection where Self.Iterator.Element: RandomAccessCollection {
//  func transposed() -> [[Self.Iterator.Element.Iterator.Element]] {
//    guard let firstRow = self.first else { return [] }
//    return firstRow.indices.map { index in
//      self.map{ $0[index] }
//    }
//  }
//}
//
//extension Array where Element == Array<PaintColour> {
//  //  ...........
//  //  ...........
//  //  .#.#...#...   -->   #.#...#
//  //  ...#####...         ..#####
//  //  ...........
//  func trimmed(_ colour: PaintColour) -> [[PaintColour]] {
//    guard count > 0 else { return self }
//    trimmed( Array(repeating: colour, count: self[0].count) )
//      .transposed()
//      .map{ $0.trimmed(colour) }
//      .transposed()
//  }
//  
//  //                  .........
//  //  #.#...#   -->   .#.#...#.
//  //  ..#####         ...#####.
//  //                  .........
//  func bordered(border: Int = 1) -> [[PaintColour]] {
//    map{ $0.bordered(colour) }
//      .transposed()
//      .map{ $0.trimmed(colour) }
//      .transposed()
//
//    return self
//  }
//}
