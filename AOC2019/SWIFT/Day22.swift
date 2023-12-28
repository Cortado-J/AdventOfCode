//
//  Day22.swift
//  AdventOfCode2019
//
//  Created by Suhada on 23/12/2019.
//  Copyright © 2019 Suhada. All rights reserved.
//

enum Technique {
  case cut(cards: Int)
  case deal(increment: Int)
  case dealNew
  
  init(_ str: String) {
    let words = str.components(separatedBy: " ")
    switch (words[0],words[1]) {
    case ("cut", _): self = .cut(cards: Int(words[1])!)
    case ("deal", "with"): self = .deal(increment: Int(words[3])!)
    case ("deal", "into"): self = .dealNew
    default: fatalError("Unrecognised technique: \(str)")
    }
  }
  
  func endPosition(startPosition: Int, packSize: Int) -> Int {
    switch self {
    case .cut(let cards):        return (startPosition - cards + packSize) % packSize
    case .deal(let increment):   return (startPosition * increment) % packSize
    case .dealNew:               return packSize - startPosition - 1
    }
  }
  
  func startPosition(endPosition: Int, packSize: Int) -> Int {
    switch self {
    case .cut(let cards): return (endPosition + cards + packSize) % packSize
    case .deal(let increment):
      switch increment {
      case 1:          return endPosition
      case packSize-1: return packSize-endPosition-1
      default:         return ( (packSize - endPosition) * increment ) % packSize
      }
    case .dealNew:        return packSize - endPosition - 1
    }
  }
}

struct Day22 {
  
  let data = """
cut -1468
deal with increment 19
cut -7127
deal with increment 8
cut -8697
deal with increment 58
cut 4769
deal into new stack
cut 4921
deal with increment 16
cut -1538
deal with increment 55
cut 3387
deal with increment 41
cut 4127
deal with increment 26
cut 5512
deal with increment 21
deal into new stack
deal with increment 44
cut -7989
deal with increment 28
cut 569
deal into new stack
cut -9795
deal into new stack
cut -6877
deal with increment 60
cut -6500
deal with increment 37
cut -9849
deal with increment 66
cut -4821
deal with increment 50
deal into new stack
cut 9645
deal with increment 22
cut -6430
deal with increment 17
cut 658
deal with increment 67
cut -9951
deal into new stack
deal with increment 31
cut -2423
deal with increment 39
cut -5126
deal with increment 7
cut 432
deal with increment 8
cut 682
deal with increment 45
deal into new stack
deal with increment 41
cut -130
deal with increment 74
deal into new stack
cut -9207
deal into new stack
cut 7434
deal with increment 31
cut -5165
deal into new stack
cut 6209
deal with increment 25
cut 2734
deal with increment 53
deal into new stack
cut -1528
deal with increment 25
deal into new stack
deal with increment 68
cut 6458
deal into new stack
cut 1895
deal with increment 16
cut -6137
deal with increment 53
cut 2761
deal with increment 73
deal into new stack
cut 1217
deal with increment 69
deal into new stack
deal with increment 54
cut -6639
deal into new stack
cut -2891
deal with increment 10
cut -6297
deal with increment 31
cut 4591
deal with increment 35
cut -4035
deal with increment 65
cut -7504
deal into new stack
deal with increment 54
deal into new stack
cut 1313
"""
  
  let dataTestDealNew =
  """
  deal into new stack
  """
  
  let dataTestCut2 =
  """
  cut 2
  """
  
  let dataTestCut2Cut2 =
  """
  cut 2
  cut 2
  """
  
  let dataTestCutNeg2 =
  """
  cut -2
  """
  
  let dataTestInc3 =
  """
  deal with increment 3
  """
  
  let dataTestInc7 =
  """
  deal with increment 7
  """
  
  let dataTestInc9 =
  """
  deal with increment 9
  """
  
  let dataTest1 =
  """
deal with increment 7
deal into new stack
deal into new stack
"""
  
  let dataTest2 =
  """
cut 6
deal with increment 7
deal into new stack
"""
  
    let dataTestInc7Inc9 =
    """
  deal with increment 7
  deal with increment 9
  """

  let dataTest3 =
  """
deal with increment 7
deal with increment 9
cut -2
"""
  
  let dataTest4 =
  """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""
  
  
  func dataInc(_ n: Int) -> String { "deal with increment \(n)" }
  func dataCut(_ n: Int) -> String { "cut \(n)"                 }
  func dataNew()         -> String { "deal into new stack"      }
  
  static func transform(n: Int, by: [Technique], packSize: Int) -> Int {
    by.reduce(n) { $1.endPosition(startPosition: $0, packSize: packSize) }
  }
  
  static func transform(n: Int, by: String, packSize: Int) -> Int {
    let techs = by
      .split{ $0.isNewline }
      .map{ Technique(String($0)) }
    return transform(n: n, by: techs, packSize: packSize)
    //    var current = n
    //    for trans in techs {
    //      current = trans.endPosition(startPosition: current, packSize: packSize)
    //    }
    //    //print(current)
    //    return current
  }
  
  static func backTransform(n: Int, by: [Technique], packSize: Int) -> Int {
    by.reversed()
      .reduce(n) {
      $1.startPosition(endPosition: $0, packSize: packSize)
    }
  }
  
  static func backTransform(n: Int, by: String, packSize: Int) -> Int {
    let techs = by
      .split{ $0.isNewline }
      .map{ Technique(String($0)) }
    return backTransform(n: n, by: techs, packSize: packSize)
//    var current = n
//    for trans in techs.reversed() {
//      current = trans.startPosition(endPosition: current, packSize: packSize)
//    }
//    return current
  }
  
  func parta() -> [Int] {
    let result = Day22.transform(n: 2019, by: data, packSize: 10007)
    return [result]
  }
  
  func partb() -> [Int] {
    return [88888]
  }
  
  func tests() {
    let packSize = 10
    
    func testAll(_ data: String) {
      let result = (0..<packSize).map{ Day22.transform(n: $0, by: data, packSize: packSize) }
      print("forward:  positions of 0 to \(packSize-1) are: '\(result)'")
      let order = (0..<packSize).map{
        result.firstIndex(of: $0)!
      }
      print("          order is:                 '\(order)'")
    }
    
    
    func backTestAll(_ data: String) {
      let result = (0..<packSize).map{ Day22.backTransform(n: $0, by: data, packSize: packSize) }
      print("backward: order is                : '\(result)'")
      print("          positions of 0 to \(packSize-1) are: '\((0..<packSize).map{result.firstIndex(of: $0)! })'")
    }
    
    func forwardAndBack(_ title: String, _ data: String) {
      print("---\(title)")
      testAll(data)
      backTestAll(data)
    }
    
    forwardAndBack("DealNew",  dataNew()  )
    for j in (1..<packSize) {
      forwardAndBack("Cut\(j)", dataCut(j) )
    }
    for j in (1..<packSize) {
      forwardAndBack("CutNeg\(j)", dataCut(-j) )
    }
    for j in (1..<packSize) {
      guard coprime(j, packSize) else {
        print("Skipping \(j) because \(j) and \(packSize) are not coprime.")
        continue
      }
//      guard j != 1 && j != packSize-1 else {
//        print("Skipping \(j) because 'Increment \(j)' not implemented.")
//        continue
//      }
      forwardAndBack("Inc\(j)", dataInc(j) )
    }
    forwardAndBack("Cut2Cut2", dataTestCut2Cut2 )
    forwardAndBack("Inc7,Inc9", dataTestInc7Inc9  )
    
    forwardAndBack("Inc3",     """
    deal with increment 3
    """  )

    forwardAndBack("Inc3,Inc3",     """
    deal with increment 3
    deal with increment 3
    """  )
    
    forwardAndBack("Test1 = Inc7,New,New", dataTest1      )
    forwardAndBack("Test2 = Cut6,Inc7,New", dataTest2     )
    forwardAndBack("Test3 = Inc7,Inc9,CutNeg2", dataTest3 )
    forwardAndBack("Test4 = New,CutNeg2,Inc7,Cut8,CutNeg4,Inc7,Cut3,Inc9,Inc3,CutNeg1", dataTest4)
  }
    
}
