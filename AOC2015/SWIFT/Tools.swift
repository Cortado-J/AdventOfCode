//
//  Tools.swift
//  AdvenOfCode2015
//
//  Created by Justin Roughley on 29/12/2021.
//
import CryptoKit
import Foundation

extension StringProtocol {
  subscript(offset: Int) -> Character { self[index(startIndex, offsetBy: offset)] }
  subscript(range: Range<Int>) -> SubSequence {
    let startIndex = index(self.startIndex, offsetBy: range.lowerBound)
    return self[startIndex..<index(startIndex, offsetBy: range.count)]
  }
  subscript(range: ClosedRange<Int>) -> SubSequence {
    let startIndex = index(self.startIndex, offsetBy: range.lowerBound)
    return self[startIndex..<index(startIndex, offsetBy: range.count)]
  }
  subscript(range: PartialRangeFrom<Int>) -> SubSequence { self[index(startIndex, offsetBy: range.lowerBound)...] }
  subscript(range: PartialRangeThrough<Int>) -> SubSequence { self[...index(startIndex, offsetBy: range.upperBound)] }
  subscript(range: PartialRangeUpTo<Int>) -> SubSequence { self[..<index(startIndex, offsetBy: range.upperBound)] }
}

extension String {
  func getbit(_ bit: Int) -> Int {
    self[bit] == "1" ? 1 : 0
  }
}

extension Array where Element == String {
  func stats(_ bit: Int) -> (Int, Int) {
    var bit0 = 0
    var bit1 = 0
    for e in self {
      if e.getbit(bit) == 0 { bit0 += 1 }
      if e.getbit(bit) == 1 { bit1 += 1 }
    }
    return (bit0, bit1)
  }
}

extension Array {
  mutating func filterInPlace(isIncluded: (Element) throws -> Bool) rethrows {
    var writeIndex = self.startIndex
    for readIndex in self.indices {
      let element = self[readIndex]
      let include = try isIncluded(element)
      if include {
        if writeIndex != readIndex {
          self[writeIndex] = element
        }
        writeIndex = self.index(after: writeIndex)
      }
    }
    self.removeLast(self.distance(from: writeIndex, to: self.endIndex))
  }
}

extension String {
  func binaryAsInt() -> Int {
    var result = 0
    var multiplier = 1
    for bit in stride(from: count-1, through: 0, by: -1) {
      result += getbit(bit) * multiplier
      multiplier *= 2
    }
    return result
  }
}

enum KeepBit { case greater, lesser }


extension StringProtocol {
  var lines: [SubSequence] { split(whereSeparator: \.isNewline) }
}

extension String {
  var MD5: String {
    let computed = Insecure.MD5.hash(data: self.data(using: .utf8)!)
    return computed.map { String(format: "%02hhx", $0) }.joined()
  }
}

extension Character {
  func nextUnicode() -> Character {
    Character(UnicodeScalar(UnicodeScalar(String(self))!.value + 1)!)
  }
}

extension StringProtocol {
  func index<S: StringProtocol>(of string: S, options: String.CompareOptions = []) -> Index? {
    range(of: string, options: options)?.lowerBound
  }
  func endIndex<S: StringProtocol>(of string: S, options: String.CompareOptions = []) -> Index? {
    range(of: string, options: options)?.upperBound
  }
  func indices<S: StringProtocol>(of string: S, options: String.CompareOptions = []) -> [Index] {
    ranges(of: string, options: options).map(\.lowerBound)
  }
  func ranges<S: StringProtocol>(of string: S, options: String.CompareOptions = []) -> [Range<Index>] {
    var result: [Range<Index>] = []
    var startIndex = self.startIndex
    while startIndex < endIndex,
          let range = self[startIndex...]
            .range(of: string, options: options) {
      result.append(range)
      startIndex = range.lowerBound < range.upperBound ? range.upperBound :
      index(range.lowerBound, offsetBy: 1, limitedBy: endIndex) ?? endIndex
    }
    return result
  }
}

extension RangeReplaceableCollection {
  func rotatedLeft(positions: Int = 1) -> SubSequence {
    let index = self.index(startIndex, offsetBy: positions, limitedBy: endIndex) ?? endIndex
    return self[index...] + self[..<index]
  }
  mutating func rotateLeft(positions: Int = 1) {
    let index = self.index(startIndex, offsetBy: positions, limitedBy: endIndex) ?? endIndex
    let slice = self[..<index]
    removeSubrange(..<index)
    insert(contentsOf: slice, at: endIndex)
  }
}

extension RangeReplaceableCollection {
  func rotatedRight(positions: Int = 1) -> SubSequence {
    let index = self.index(endIndex, offsetBy: -positions, limitedBy: startIndex) ?? startIndex
    return self[index...] + self[..<index]
  }
  mutating func rotateRight(positions: Int = 1) {
    let index = self.index(endIndex, offsetBy: -positions, limitedBy: startIndex) ?? startIndex
    let slice = self[index...]
    removeSubrange(index...)
    insert(contentsOf: slice, at: startIndex)
  }
}

extension Array where Element == (String, Int) {
  func asMultiset() -> Multiset<String> {
    Multiset( Dictionary(uniqueKeysWithValues: self) )
  }
}

precedencegroup PowerPrecedence { higherThan: MultiplicationPrecedence }
infix operator ^^ : PowerPrecedence
func ^^ (radix: Int, power: Int) -> Int {
  return Int(pow(Double(radix), Double(power)))
}

extension Int {
  /// Returns the digits of the number in the given base.
  /// The array of digits is ordered from most to least significant.
  func digits(base: Int = 10) -> [Int] {
    if self < base {
      return [self]
    }
    var n = self
    var d: [Int] = []
    while n > 0 {
      d.insert(n % base, at: 0)
      n /= base
    }
    return d
  }
  
  func digit(_ digit: Int, base: Int = 10) -> Int {
    let d = digits(base: base)
    guard digit < d.count else { return 0 }
    return digits(base: base)[digit]
  }
}

extension Set {
  var powerSet: [[Element]] {
    guard !isEmpty else { return [[]] }
    let head = randomElement()!
    var tail = self
    tail.remove(head)
    return tail.powerSet.flatMap { [$0, [head] + $0] }
  }
}

