//
//  Day12.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 09/12/2021.
//

func day12() {
  var input =
"""
by-TW
start-TW
fw-end
QZ-end
JH-by
ka-start
ka-by
end-JH
QZ-cv
vg-TI
by-fw
QZ-by
JH-ka
JH-vg
vg-fw
TW-cv
QZ-vg
ka-TW
ka-QZ
JH-fw
vg-hu
cv-start
by-cv
ka-cv
"""

  var inputTest =
//"""
//start-A
//start-b
//A-c
//A-b
//b-d
//A-end
//b-end
//"""

//  """
//  dc-end
//  HN-start
//  start-kj
//  dc-start
//  dc-HN
//  LN-dc
//  HN-end
//  kj-sa
//  kj-HN
//  kj-dc
//  """

"""
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

  let base = input
    .lines
    .map{
      String($0)
      //        .trimmingCharacters(in: .whitespaces)
        .split(separator: "-")
    }
  
  var links: [String: [String]] = [:]

  func addLink(from: String, to: String) {
    if let _ = links[from] {
      links[from]!.append(to)
    } else {
      links[from] = [to]
    }
  }
  
  // Load links
  for link in base {
    let from = String(link[0])
    let to   = String(link[1])
    addLink(from: from, to: to)
    addLink(from: to, to: from)
  }

  typealias Path = [String]
  
  func isBig(_ name: String) -> Bool { name.first!.isUppercase }
  
  // Find all paths having come from somewhere
  func paths(from: Path, steps: Int, doubleSmall: Bool) -> [Path] {
    func spacer(_ char: String) -> String { String(repeating: char, count: steps) }
    //print(spacer(".")+"\(from)")
    if steps > 100 { return [from] }

    let last = from.last!
    if last == "end" { return [from] }
    if let nextPossible = links[last] {
      
      func hasVisited2SmallCaves() -> Bool {
        for (_, count) in Multiset(from.filter{ !isBig($0) }).grouped() {
          if count > 1 { return true }
        }
        return false
      }
      
      let possibles = nextPossible
        .filter{
          !from.contains($0) // Either we haven't been there before
          || isBig($0)       // Or it's a big character so we can visit again
          || (           // Or it's ok to visit a small cave again as long as no small cave has been visited twice:
            doubleSmall &&  // Only valid if this flag set
            ($0 != "start") && // Don't revisit start
            !hasVisited2SmallCaves() // Only allow if we haven;t double visited before
          )
        }
      var result: [Path] = []
      for possible in possibles {
        let newPaths = paths(from: from + [possible], steps: steps+1, doubleSmall: doubleSmall)
        result += newPaths
      }
      //print(spacer(">")+"\(result)")
      return result
    } else {
      return []
    }
    
  }

  print("Day12")
  print(base)
  print(links)
  print("------------- PATHS:")
  let pathsa = paths(from: ["start"],steps: 0, doubleSmall: false)
  for path in pathsa { print(path) }

  let pathsb = paths(from: ["start"],steps: 0, doubleSmall: true)
  for path in pathsb { print(path) }

  print(pathsa.count)
  print(pathsb.count)
}
