//
//  GCD_LCM.swift
//  AdventOfCode2019
//
//  Created by Adahus on 12/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

func gcdIterativeEuklid(_ m: Int, _ n: Int) -> Int {
  var a: Int = 0
  var b: Int = max(m, n)
  var r: Int = min(m, n)
  
  while r != 0 {
    a = b
    b = r
    r = a % b
  }
  return b
}

func gcd(_ m: Int, _ n: Int) -> Int { gcdIterativeEuklid(m,n) }

func gcd(_ a: [Int]) -> Int {
  guard a.count > 0 else { fatalError("Need some numbers!!") }
  if a.count == 1 { return a.first! }
  return a.dropFirst().reduce(a.first!){ gcd($0, $1) }
}

func coprime(_ m: Int, _ n: Int) -> Bool { gcd(m,n) == 1 }

func lcm(_ m: Int, _ n: Int) -> Int {
  guard (m & n) != 0 else { fatalError("lcm division by zero") }
  return m / gcd(m, n) * n
}

func lcm(_ a: [Int]) -> Int {
  guard a.count > 0 else { fatalError("Need some numbers!!") }
  if a.count == 1 { return a.first! }
  return a.dropFirst().reduce(a.first!){ lcm($0, $1) }
}
