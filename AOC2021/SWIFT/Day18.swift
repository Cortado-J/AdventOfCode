//
//  Day18.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 18/12/2021.
//

func day18() {
  
  let inputTest =
  """
  [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
  [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
  [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
  [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
  [7,[5,[[3,8],[1,4]]]]
  [[2,[2,2]],[8,[8,1]]]
  [2,9]
  [1,[[[9,3],9],[[9,0],[0,7]]]]
  [[[5,[7,4]],7],1]
  [[[[4,2],2],6],[8,7]]
  """
  
  indirect enum Number {
    case regular(int: Int)
    case nested(pair: Pair)
    
    init(_ string: String) {
      var working = string
      
      func next() -> Character? {
        let first = working.first
        //        print(first ?? "Runout of chars!!")
        working = String(working.dropFirst())
        return first
      }
      
      func until(_ find: Character) -> String {
        var result = ""
        var bracketNest = 0
        while true {
          guard let char = next() else { fatalError("No more chars!") }
          if char == "[" { bracketNest += 1 }
          if bracketNest == 0 && char == find { return result }
          if char == "]" { bracketNest -= 1 }
          result.append(char)
        }
      }
      
      guard let char = next() else { fatalError("No more chars!") }
      if char == "[" {
        // It's a pair..
        let tillNextComma = until(",")
        let tillMatchingBracket = until("]")
        self = .nested(pair: Pair(left: Number(tillNextComma), right: Number(tillMatchingBracket)))
      } else {
        // It's a regular number..
        let number = Int(String(char))!
        self = .regular(int: number)
      }
    }
    
    func show() -> String {
      switch self {
      case let .regular(int): return String(int)
      case let .nested(pair): return "[\(pair.left.show()),\(pair.right.show())]"
      }
    }
    
    // regular number returns 0
    func deepest() -> Int {
      switch self {
      case .regular: return 0
      case .nested(let pair):
        return max(pair.left.deepest(), pair.right.deepest()) + 1
      }
    }
    
    // regular number returns nil
    // first pair returns 0
    // second nested pair level returns 1
    func deepestNestedPair() -> Int? {
      switch self {
      case .regular: return nil
      case .nested: return deepest() - 1
      }
    }
    
    func add(_ number: Number) -> Number {
      let result = Pair(left: self, right: number)
      return .nested(pair: result)
      //.reduced()
    }
  }
  
  class Pair {
    var left: Number
    var right: Number
    
    init(left: Number, right: Number) { self.left = left; self.right = right }
  }
  
  
  let x = Number("4")
  let y = Number("[4,5]")
  let z = Number("[[1,2],[4,5]]")
  let a = Number("[[[1,[1,[[1,2],2]]],2],[4,5]]")

  print(x.add(y).add(z).show())
  
  print("x", x.show(), x.deepest(), x.deepestNestedPair())
  print("y", y.show(), y.deepest(), y.deepestNestedPair())
  print("z", z.show(), z.deepest(), z.deepestNestedPair())
  print("a", a.show(), a.deepest(), a.deepestNestedPair())

}

