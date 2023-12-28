//
//  Day16.swift
//  AdventOfCode2019
//
//  Created by Adahus on 16/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

struct Day16 {
      
  static func mult(position: Int, element: Int) -> Int {
    [0,1,0,-1][( (position+1) / (element+1) ) % 4]
  }
  
  static func step(_ input: String) -> String {
    let array =
      Array(input).map{Int(String($0))!}  /// Convert to Ints

    var output: [Int] = []
    for newPosition in array.indices {
      var sum = 0
      for oldPosition in array.indices {
        let multiplier = Day16.mult(position: oldPosition, element: newPosition)
        let bit = array[oldPosition] * multiplier
//        print("Value: \(array[oldPosition]) which is from Position: \(oldPosition) : Element: \(newPosition) creates multiplier \(multiplier) -> \(bit)")
        sum += bit
      }
      let lastDigit = (sum > 0) ? sum % 10 : (-sum) % 10
//      print("Sum is \(sum) which has last digit \(lastDigit)")
      output.append(lastDigit)
//      print("===========")
    }
    return String(output.flatMap{ String($0) })
  }

  func parta() -> [Int] {
    let data =
//    "12345678"
 "59781998462438675006185496762485925436970503472751174459080326994618036736403094024111488348676644802419244196591075975610084280308059415695059918368911890852851760032000543205724091764633390765212561307082338287866715489545069566330303873914343745198297391838950197434577938472242535458546669655890258618400619467693925185601880453581947475741536786956920286681271937042394272034410161080365044440682830248774547018223347551308590698989219880430394446893636437913072055636558787182933357009123440661477321673973877875974028654688639313502382365854245311641198762520478010015968789202270746880399268251176490599427469385384364675153461448007234636949"
    

    var working = data
    print(working)
    for step in (1 ... 100) {
      working = Day16.step(working)
      print(working)
    }
    
    return [99999]
  }
  
  func partb() -> [Int] {
    return [99999]
  }
}
