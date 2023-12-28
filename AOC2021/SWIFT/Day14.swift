//
//  Day13.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 09/12/2021.
//
func day14() {
  
  var polyInputTest = "NNCB"
  
  var inputTest =
  """
  CH -> B
  HH -> N
  CB -> H
  NH -> C
  HB -> C
  HC -> B
  HN -> C
  NN -> C
  BH -> H
  NC -> B
  NB -> B
  BN -> B
  BB -> N
  BC -> B
  CC -> N
  CN -> C
  """

var polyInput = "FSKBVOSKPCPPHVOPVFPC"
  
  var input =
"""
BV -> O
OS -> P
KP -> P
VK -> S
FS -> C
OK -> P
KC -> S
HV -> F
HC -> K
PF -> N
NK -> F
SC -> V
CO -> K
PO -> F
FB -> P
CN -> K
KF -> N
NH -> S
SF -> P
HP -> P
NP -> F
OV -> O
OP -> P
HH -> C
FP -> P
CS -> O
SK -> O
NS -> F
SN -> S
SP -> H
BH -> B
NO -> O
CB -> N
FO -> N
NC -> C
VF -> N
CK -> C
PC -> H
BP -> B
NF -> O
BB -> C
VN -> K
OH -> K
CH -> F
VB -> N
HO -> P
FH -> K
PK -> H
CC -> B
VH -> B
BF -> N
KS -> V
PV -> B
CP -> N
PB -> S
VP -> V
BO -> B
HS -> H
BS -> F
ON -> B
HB -> K
KH -> B
PP -> H
BN -> C
BC -> F
KV -> K
VO -> P
SO -> V
OF -> O
BK -> S
PH -> V
SV -> F
CV -> H
OB -> N
SS -> H
VV -> B
OO -> V
CF -> H
KB -> F
NV -> B
FV -> V
HK -> P
VS -> P
FF -> P
HN -> N
FN -> F
OC -> K
SH -> V
KO -> C
HF -> B
PN -> N
SB -> F
VC -> B
FK -> S
KK -> N
FC -> F
NN -> P
NB -> V
PS -> S
KN -> S
"""

  struct Rule: Hashable {
    var from: String
    var to: String
  }
  
  struct RuleSet {
    var rules: Set<Rule>
    
    func show() {
      print()
    }
    
    var count: Int { rules.count }
    
  }
  
  let polyBase = polyInputTest
  let base = inputTest
    .lines
    .map{
      String($0)
        .trimmingCharacters(in: .whitespaces)
        .replacingOccurrences(of: " -> ", with: ",")
        .split(separator: ",")
    }
    .map{
      Rule(from: String($0[0]), to: String($0[1]))
    }
  
  var rules: [String:Character] = [:]
  for rule in base {
    rules[rule.from] = rule.to.first!
  }

  func pairsOf(_ poly: String) -> [String] {
    var result: [String] = []
    var last: Character? = nil
    for char in poly {
      if let lastWas = last {
        result.append("\(lastWas)\(char)")
      }
      last = char
    }
    return result
  }

  func sub(_ poly: String) -> String {
    var gather: [Character] = []
    var last: Character? = nil
    for char in poly {
      guard last != nil else { last = char; continue }
      let pair = "\(last!)\(char)"
      gather.append(last!)
      let lookup = rules[pair]!
      gather.append(lookup)
      last = char
    }
    gather.append(last!)
    return String(gather)
  }
  
  print("Day14")
//  print("base=\(base)")

  var poly = polyBase

  let maxGen = 2
  
  for _ in 1...maxGen {
    poly = sub(poly)
  }
  //print(poly)
  
  let multiset = Multiset(poly.map{$0})
  print(multiset)
  
  let freq = Array(multiset.grouped())
    .map{ $0.count }
    .sorted()
  
  let resulta = freq.last! - freq.first!

  print("resulta=\(resulta)")

  var memoise: [Search:Int] = [:]

  struct Search: Hashable {
    var pair: String
    var char: Character
    var gen: Int
  }
  
  func f(_ search: Search, level: Int) -> Int {
    var result: Int
    if let previous = memoise[search] {
      result = previous
    } else {
      if search.gen == 0 {
        result =
        //(search.pair.first! == search.char ? 1 : 0) +
        (search.pair.last! == search.char ? 1 : 0) // Only second so no double counting!
      } else {
        let letterToInsert = rules[search.pair]!
        let left  = f(Search(pair: "\(search.pair.first!)\(letterToInsert)", char: search.char, gen: search.gen-1), level: level+1)
        let right = f(Search(pair: "\(letterToInsert)\(search.pair.last!)",  char: search.char, gen: search.gen-1), level: level+1)
        //let overlap = letterToInsert == search.char ? 1 : 0
        result = left + right //- overlap
      }
      memoise[search] = result
    }
    print(">"+String(repeating: ".", count: level)+"f(pair:\(search.pair) (so letter to insert is \(rules[search.pair]!)), char:\(search.char), gen:\(search.gen))=\(result)")
    return result
  }

  let pairs = rules.keys
  print(rules)
  let chars = Array(Set(pairs.reduce("", +).map{$0}))
  print(chars)
  //Load up memoise...
  for gen in 1...maxGen {
    for char in chars {
      for pair in pairs {
        let result = f(Search(pair: pair, char: char, gen: gen), level: 0)
        print("f(pair:\(pair) (so letter to insert is \(rules[pair]!)), char:\(char), gen:\(gen))=\(result)")
      }
    }
  }

  func f(poly: String, char: Character, gen: Int) -> Int {
    var result = poly.first! == char ? 1 : 0
    for pair in pairsOf(poly) {
      result += f(Search(pair: pair, char: char, gen: gen), level: 0)
    }
    //result -= poly.map{$0}.dropFirst().dropLast().filter{$0 == char}.count
    return result
  }

  print("chars=\(chars)")
  for gen in 0...maxGen {
    for char in chars {
      print("gen=\(gen) char=\(char), f=\(f(poly: poly, char: char, gen: gen))")
    }
  }

  //
  ////////////////////////////
  // repeats = 10
  //  ["V": 3149, "O": 2689, "K": 789, "C": 925, "B": 2400, "H": 1752, "N": 1966, "F": 1416, "S": 1414, "P": 2957]
  //  resulta=2360

  
  // ////////////////////////////
  // repeats = 20
  //  ["S": 1278331, "V": 3482505, "N": 2215039, "P": 2835263, "O": 3330370, "C": 837915, "B": 2133644, "K": 833033, "F": 1555258, "H": 1421587]
  //  resulta=2649472
  
  var resultb = base
  //print("resultb=\(resultb)")
}
