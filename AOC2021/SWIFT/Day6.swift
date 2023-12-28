//
//  Day6.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 09/12/2021.
//

func day6() {
  var shoal =
  //"3,4,3,1,2"
  "5,1,4,1,5,1,1,5,4,4,4,4,5,1,2,2,1,3,4,1,1,5,1,5,2,2,2,2,1,4,2,4,3,3,3,3,1,1,1,4,3,4,3,1,2,1,5,1,1,4,3,3,1,5,3,4,1,1,3,5,2,4,1,5,3,3,5,4,2,2,3,2,1,1,4,1,2,4,4,2,1,4,3,3,4,4,5,3,4,5,1,1,3,2,5,1,5,1,1,5,2,1,1,4,3,2,5,2,1,1,4,1,5,5,3,4,1,5,4,5,3,1,1,1,4,5,3,1,1,1,5,3,3,5,1,4,1,1,3,2,4,1,3,1,4,5,5,1,4,4,4,2,2,5,5,5,5,5,1,2,3,1,1,2,2,2,2,4,4,1,5,4,5,2,1,2,5,4,4,3,2,1,5,1,4,5,1,4,3,4,1,3,1,5,5,3,1,1,5,1,1,1,2,1,2,2,1,4,3,2,4,4,4,3,1,1,1,5,5,5,3,2,5,2,1,1,5,4,1,2,1,1,1,1,1,2,1,1,4,2,1,3,4,2,3,1,2,2,3,3,4,3,5,4,1,3,1,1,1,2,5,2,4,5,2,3,3,2,1,2,1,1,2,5,3,1,5,2,2,5,1,3,3,2,5,1,3,1,1,3,1,1,2,2,2,3,1,1,4,2"
    .split(separator: ",")
    .map{ Int($0)! }
    
  print("Day6")
  print(shoal)

  var frequencies = Array(repeating: 0, count: 10)
  for (element, count) in Multiset(shoal).grouped() {
    frequencies[element] = count
  }
  
  print(frequencies)
  
  for day in 1...256 {
    var freqNew = Array(repeating: 0, count: 10)
    for (index, freq) in frequencies.enumerated() {
      switch index {
      case 0:
        freqNew[6] += freq
        freqNew[8] += freq
      default:
        freqNew[index-1] += freq
      }
    }
    frequencies = freqNew
    print(freqNew)
  }
  print(frequencies.reduce(0,+))
}
