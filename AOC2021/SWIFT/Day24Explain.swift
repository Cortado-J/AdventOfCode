////
////  Day24.swift
////  AdventOfCode2021
////
////  Created by Justin Roughley on 24/12/2021.
////
//
//var w = 0
//var x = 0
//var y = 0
//var z = 0
//
//func day24() {
//  
//  func reset() {
//    w = 0
//    x = 0
//    y = 0
//    z = 0
//  }
//  
//  func f(input: Int, divver: Int, adder: Int, adder2: Int) {
//    w = input //inp w
//    x = 0 //mul x 0
//    x = x + z //add x z
//    x = x % 26 //mod x 26 (Watch out for negative)
//    z = z / divver //div z 1
//    x = x + adder //add x 11
//    x = x == w ? 1 : 0 //eql x w
//    x = x == 0 ? 1 : 0 //eql x 0
//    y = 0 //mul y 0
//    y = y + 25 //add y 25
//    y = y * x //mul y x
//    y = y + 1 //add y 1
//    z = z * y //mul z y
//    y = 0 //mul y 0
//    y = y + w //add y w
//    y = y + adder2 //add y 6
//    y = y * x //mul y x
//    z = z + y //add z y
//  }
//  
//  func f2(input: Int, divver: Int, adder: Int, adder2: Int) {
//    if input == adder + z % 26 {
//      z = z / divver
//    } else {
//      z = z / divver * 26 + input + adder2
//    }
//  }
//  
//  func f2z(z: Int, input: Int, divver: Int, adder: Int, adder2: Int) -> Int? {
//    if z < 0 { return nil }
//    if input == adder + z % 26 {
//      return z / divver
//    } else {
//      return (z / divver) * 26 + input + adder2
//    }
//  }
//  
//  //func f2(input: Int, divver: Int, adder: Int, adder2: Int) {
//  //  w = input
//  //
//  //  if input == adder + z % 26 {
//  //    //    x = 0
//  //    //    y = 0
//  //    z = z / divver
//  //  } else {
//  //    //    x = 1
//  //    //    y = input + adder2
//  //    z = z / divver * 26 + input + adder2
//  //  }
//  //
//  //}
//  
//  // w: input
//  // x: adder + z % 26
//  // y:
//  // z:
//  
//  
//  // Changes to w:
//  //   w = input
//  
//  // Changes to x:
//  //   x = adder + z % 26
//  //   x = 0
//  //   x = 1
//  
//  // Changes to y:
//  //   y = 0
//  //   y = input + adder2
//  
//  // Changes to z:
//  //   z = z / divver
//  //   z = z * 26 + input + adder2
//  
//  //func f2(input: Int, divver: Int, adder: Int, adder2: Int) {
//  //  z = z / divver
//  //  if input != (z % 26 + adder) {
//  //    z = z * 26 + (input + adder2)
//  //  }
//  //}
//  
//  var divadds = [  // Tuples contain three values: divver, adder, addrer2
//    (  1,  11,  6 ),
//    (  1,  11, 14 ),
//    (  1,  15, 13 ),
//    ( 26, -14,  1 ),
//    (  1,  10,  6 ),
//    ( 26,   0, 13 ),
//    ( 26,  -6,  6 ),
//    (  1,  13,  3 ),
//    ( 26,  -3,  8 ),
//    (  1,  13, 14 ),
//    (  1,  15,  4 ),
//    ( 26,  -2,  7 ),
//    ( 26,  -9, 15 ),
//    ( 26,  -2,  1 )
//  ]
//  
//  func number14(_ x: Int) -> (Int, Int, Int, Int) {
//    reset()
//    for (index, digit) in String(x).map({ Int(String($0))! }).enumerated() {
//      //print(index, digit, divadds[index])
//      let (divver, adder, adder2) = divadds[index]
//      f(input: digit, divver: divver, adder: adder, adder2: adder2)
//    }
//    return( (w,x,y,z) )
//  }
//  
//  // Process the end of the number.
//  func number14End(_ x: Int, zInput: Int, zAllowedAfterOneStep: Int) -> Int? {
//    reset()
//    z = zInput
//    let valueAsString = String(x)
//    let numberOfDigits = valueAsString.count
//    for (index, digit) in valueAsString.map({ Int(String($0))! }).enumerated() {
//      //print(index, digit, divadds[index])
//      let (divver, adder, adder2) = divadds[14-numberOfDigits+index]
//      f2(input: digit, divver: divver, adder: adder, adder2: adder2)
//      
//      // Check z after one step is valid!!
//      if index == 0 && z != zAllowedAfterOneStep { return nil }
//    }
//    return z
//  }
//  
//  //  func validStarts(givenEndings: [String], zStart: Int, zEnd: Int) -> [String] {
//  //    var result: Set<Int> = []
//  //    for zTry in zStart ... zEnd {
//  //      for start in 1...9 {
//  //        for ending in givenEndings {
//  //          let numberToTry = Int(String(start) + ending)!
//  //          if number14End( numberToTry, zInput: zTry ) == 0 {
//  //            result.insert(numberToTry)
//  //          }
//  //        }
//  //      }
//  //    }
//  //    return Array(result).map{ String($0) }
//  //  }
//  //
//  //  func tryWithPrefix(_ prefixLength: Int) -> [String] {
//  //    var working = [""]
//  //    for step in 1...14 {
//  //      let next = validStarts(
//  //        givenEndings: working,
//  //        zStart: step == 14 ? 0 : -1 * prefixLength,
//  //        zEnd:   step == 14 ? 0 :  1 * prefixLength
//  //      )
//  //      working = next
//  //        .sorted(by: >)
//  //        .prefix(prefixLength)
//  //        .map{ String($0) }
//  //      print(step, next.count, working)
//  //    }
//  //    return working
//  //  }
//  //
//  //  var prefixLength = 40
//  //  while true {
//  //    print("Trying with prefixLength = \(prefixLength)")
//  //    let result = tryWithPrefix(prefixLength)
//  //    if result.count > 0 {
//  //      print("ANSWER!!...\(result[0])")
//  //    }
//  //    prefixLength += 40
//  //  }
//  
//  struct ZEndAndEnd: Hashable {
//    var zAtEnd: Int
//    var numberEnd: String
//    
//    func asString() -> String {
//      //"\(numberEnd)"
//      "\(numberEnd)(z=\(zAtEnd)) "
//    }
//  }
//  
//  func validZAndStarts(zEndAndEndings: [ZEndAndEnd], zEnd: Int) -> [ZEndAndEnd] {
//    var result: Set<ZEndAndEnd> = []
//    for zTry in 0 ... zEnd {
//      for start in 1...9 {
//        for zEndAndEnd in zEndAndEndings {
//          let numberToTry = Int(String(start) + zEndAndEnd.numberEnd)!
//          if number14End( numberToTry, zInput: zTry ,zAllowedAfterOneStep: zEndAndEnd.zAtEnd) == 0 {
//            result.insert( ZEndAndEnd(zAtEnd: zTry, numberEnd: String(numberToTry) ) )
//          }
//        }
//      }
//    }
//    return Array(result)
//  }
//  
//  func tryWithPrefixAndZ(_ prefixLength: Int) -> [ZEndAndEnd] {
//    var working = [ZEndAndEnd(zAtEnd: 0, numberEnd: "")]
//    for step in 1...14 {
//      let next = validZAndStarts(
//        zEndAndEndings: working,
//        zEnd:   step == 14 ? 0 :  1 * prefixLength
//      )
//      working = next
//      print(step,
//            next.count,
//            working
//              .sorted{ $0.numberEnd == $1.numberEnd ? $0.zAtEnd < $1.zAtEnd : $0.numberEnd < $1.numberEnd }
//              .map{ $0.asString() }
//              .prefix(20)
//              .joined(separator: ", ")
//      )
//    }
//    return working
//  }
//  
//  var prefixLength = 100
//  print(":=-=:")
//  while true {
//    print("Trying with prefixLength = \(prefixLength)")
//    let result = tryWithPrefixAndZ(prefixLength)
//    if result.count > 0 {
//      print("ANSWER!!...\(result[0])")
//      fatalError()
//    }
//    prefixLength += 40
//  }
//  
//  //  func randVal() -> Int {
//  //    Int.random(in: -30 ... 30)
//  //  }
//  //
//  //  struct Input {
//  //    var iw: Int
//  //    var ix: Int
//  //    var iy: Int
//  //    var iz: Int
//  //    var input: Int
//  //    var divver: Int
//  //    var adder: Int
//  //    var adder2: Int
//  //
//  //    static func random() -> Input {
//  //      Input(
//  //        iw: Int.random(in: -100 ... 100),
//  //        ix: Int.random(in: -100 ... 100),
//  //        iy: Int.random(in: -100 ... 100),
//  //        iz: Int.random(in: -100 ... 100),
//  //        input: Int.random(in: 1 ... 9),
//  //        divver: Int.random(in: 1 ... 2) == 1 ? Int.random(in: 1 ... 100) : Int.random(in: -100 ... -1),
//  //        adder: Int.random(in: -100 ... 100),
//  //        adder2: Int.random(in: -100 ... 100)
//  //      )
//  //    }
//  //
//  //    func setGlobal() {
//  //      w = iw; x = ix; y = iy; z = iz
//  //    }
//  
//  //  print(":=-=:")
//  // Test that f is same as f2
//  //  for _ in 1...10000 {
//  //    let rand = Input.random()
//  //    rand.setGlobal() // Set up w,x,y,z from rand
//  //    f(input: rand.input, divver: rand.divver, adder: rand.adder, adder2: rand.adder2)
//  //    let fResult = (w, x, y, z)
//  //    rand.setGlobal() // Set up w,x,y,z from rand
//  //    f2(input: rand.input, divver: rand.divver, adder: rand.adder, adder2: rand.adder2)
//  //    let f2Result = (w, x, y, z)
//  //    if fResult.3 != f2Result.3 {
//  //      print("------------------------------------")
//  //      print("inputs  =(\(rand))")
//  //      print("fResult =(\(fResult))")
//  //      print("f2Result=(\(f2Result))")
//  //    }
//  //  }
//  
//  //  for n in stride(from: 99999999999999, through: 0, by: -1) {
//  //    let (w,x,y,z) = number14(n)
//  //    let valid = z == 0
//  //    print(n, valid)
//  //    if valid { break }
//  //  }
//  
//  
//  // w,x and y are all ignored by the function
//  // So we can work backwards as follows:
//  // Find what numbers in last        position lead to z = 0
//  // Find what numbers in second last position lead to z = 0
//  // etc
//  
//  
//}
