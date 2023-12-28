//
//  Day24.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 24/12/2021.
//

//inp a - Read an input value and write it to variable a.
//invinp a - Can't do!

//add a b - Add the value of a to the value of b, then store the result in variable a.
//func invadd(a: Int, b: Int) -> Int { a-b }

//mul a b - Multiply the value of a by the value of b, then store the result in variable a.
//func invmul(a: Int, b: Int) -> Int { a/b } // Must divide exactly!

//div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
//func invmul(a: Int, b: Int) -> Int { a/b } // Must divide exactly!

//mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
//eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.



var w = 0
var x = 0
var y = 0
var z = 0

func day24() {
  
  func reset() {
    w = 0
    x = 0
    y = 0
    z = 0
  }
  
  func f(input: Int, divver: Int, adder: Int, adder2: Int) {
    w = input //inp w
    x = 0 //mul x 0
    x = x + z //add x z
    x = x % 26 //mod x 26 (Watch out for negative x)
    z = z / divver //div z 1
    x = x + adder //add x 11
    x = x == w ? 1 : 0 //eql x w
    x = x == 0 ? 1 : 0 //eql x 0
    y = 0 //mul y 0
    y = y + 25 //add y 25
    y = y * x //mul y x
    y = y + 1 //add y 1
    z = z * y //mul z y
    y = 0 //mul y 0
    y = y + w //add y w
    y = y + adder2 //add y 6
    y = y * x //mul y x
    z = z + y //add z y
  }
  
  func f2(input: Int, divver: Int, adder: Int, adder2: Int) {
    if input == adder + z % 26 {
      z = z / divver
    } else {
      z = z / divver * 26 + input + adder2
    }
  }
  
//  [1, 11, 6],
//  [1, 11, 14],
//  [1, 15, 13],
//  [26, -14, 1],
//  [1, 10, 6],
//  [26, 0, 13],
//  [26, -6, 6],
//  [1, 13, 3],
//  [26, -3, 8],
//  [1, 13, 14],
//  [1, 15, 4],
//  [26, -2, 7],
//  [26, -9, 15],
//  [26, -2, 1],
//  
  func fAll(input: Int) -> Bool {
    let inputs = String(input).map{ Int(String($0))! }
    z = inputs[0] + 6
    if inputs[1]  !=  11 + z % 26 { z = z * 26 + inputs[1] + 14 }
    if inputs[2]  !=  15 + z % 26 { z = z * 26 + inputs[2] + 13 }
    if inputs[3]  == -14 + z % 26 { z = z / 26 } else { z = z + inputs[3] + 1 }
    if inputs[4]  !=  10 + z % 26 { z = z * 26 + inputs[4] + 6 }
    if inputs[5]  ==       z % 26 { z = z / 26 } else { z = z + inputs[5] + 13 }
    if inputs[6]  ==  -6 + z % 26 { z = z / 26 } else { z = z + inputs[6] + 6 }
    if inputs[7]  !=  13 + z % 26 { z = z * 26 + inputs[7] + 3 }
    if inputs[8]  ==  -3 + z % 26 { z = z / 26 } else { z = z + inputs[8] + 8 }
    if inputs[9]  !=  13 + z % 26 { z = z * 26 + inputs[9] + 14 }
    if inputs[10] !=  15 + z % 26 { z = z * 26 + inputs[10] + 4 }
    if inputs[11] ==  -2 + z % 26 { z = z / 26 } else { z = z + inputs[11] + 7 }
    if inputs[12] ==  -9 + z % 26 { z = z / 26 } else { z = z + inputs[12] + 15 }
    // for output 1 need inputs + 9 == z % 26 and 26 < z < 52 (e.g. input=1, z=36)
    if inputs[13] ==  -2 + z % 26 { z = z / 26 } else { z = z + inputs[13] + 1 }
    // for output 0 need input == z % 26 - 2 and z less than 26 (e.g. input=3, z=5)
    return z == 0
  }
    
  var divadds = [  // Tuples contain three values: divver, adder, addrer2
    (  1,  11,  6 ),
    (  1,  11, 14 ),
    (  1,  15, 13 ),
    ( 26, -14,  1 ),
    (  1,  10,  6 ),
    ( 26,   0, 13 ),
    ( 26,  -6,  6 ),
    (  1,  13,  3 ),
    ( 26,  -3,  8 ),
    (  1,  13, 14 ),
    (  1,  15,  4 ),
    ( 26,  -2,  7 ),
    ( 26,  -9, 15 ),
    ( 26,  -2,  1 )
  ]
  
  // Process the end of the number.
  func number14End(_ x: Int, zInput: Int, zAllowedAfterOneStep: Int) -> Int? {
    reset()
    z = zInput
    let valueAsString = String(x)
    let numberOfDigits = valueAsString.count
    for (index, digit) in valueAsString.map({ Int(String($0))! }).enumerated() {
      //print(index, digit, divadds[index])
      let (divver, adder, adder2) = divadds[ 14 - numberOfDigits + index ]
      f2(input: digit, divver: divver, adder: adder, adder2: adder2)

      // Check z after one step is valid!!
      if index == 0 && z != zAllowedAfterOneStep { return nil }
    }
    return z
  }

  struct ZEndAndEnd: Hashable {
    var zAtEnd: Int
    var numberEnd: String
    
    func asString() -> String {
      //"\(numberEnd)"
      "\(numberEnd)(z=\(zAtEnd)) "
    }
  }
  
  func validZAndStarts(zEndAndEndings: [ZEndAndEnd], zEnd: Int) -> [ZEndAndEnd] {
    var result: Set<ZEndAndEnd> = []
    for zTry in 0 ... zEnd {
      for start in 1...9 {
        for zEndAndEnd in zEndAndEndings {
          let numberToTry = Int(String(start) + zEndAndEnd.numberEnd)!
          if let getIt = number14End( numberToTry, zInput: zTry ,zAllowedAfterOneStep: zEndAndEnd.zAtEnd) {
            if getIt == 0 {
              result.insert( ZEndAndEnd(zAtEnd: zTry, numberEnd: String(numberToTry) ) )
            }
          }
        }
      }
    }
    return Array(result)
  }
  
  func tryWithPrefixAndZ(_ prefixLength: Int) -> [ZEndAndEnd] {
    var working = [ZEndAndEnd(zAtEnd: 0, numberEnd: "")]
    for step in 1...14 {
      let next = validZAndStarts(
        zEndAndEndings: working,
        zEnd:   step == 14 ? 0 : prefixLength
      )
      working = next
      print(step,
            next.count,
            working
              .sorted{ $0.numberEnd == $1.numberEnd ? $0.zAtEnd < $1.zAtEnd : $0.numberEnd < $1.numberEnd }
              .map{ $0.asString() }
              .prefix(20)
              .joined(separator: ", ")
      )
    }
    return working
  }
  
  func longHand() {
    var prefixLength = 100
    print(":=-=:")
    while true {
      print("Trying with prefixLength = \(prefixLength)")
      let result = tryWithPrefixAndZ(prefixLength)
      if result.count > 0 {
        print("ANSWER!!...\(result[0])")
        fatalError()
      }
      prefixLength += 40
    }
  }
  
  longHand()
  
  func shortHand() {
    for num in stride(from: 99999999999999, through: 0, by: -1) {
      if fAll(input: num) {
        print(num)
        fatalError("BINGO!!")
      }
      if num % 10000 == 0 { print(num) }
    }
  }
  
  //shortHand()
}
