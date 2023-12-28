//
//  Day7.swift
//  AdventOfCode2019
//
//  Created by Adahus on 07/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

struct Day7 {

   let amplifierControl = [3,8,1001,8,10,8,105,1,0,0,21,30,51,76,101,118,199,280,361,442,99999,3,9,102,5,9,9,4,9,99,3,9,102,4,9,9,1001,9,3,9,102,2,9,9,101,2,9,9,4,9,99,3,9,1002,9,3,9,1001,9,4,9,102,5,9,9,101,3,9,9,1002,9,3,9,4,9,99,3,9,101,5,9,9,102,4,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,4,9,99,3,9,1002,9,2,9,1001,9,3,9,102,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,99]
  
  let amplifierControlTest = [
    3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
  ]

  let amplifierControlTestLoop = [
    3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
  ]

  let amplifierControlTestLoop2 = [
    3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
  ]
  
  func permutations<T>(_ a: [T], _ n: Int) -> [[T]] {
    var gather: [[T]] = []
    if n == 0 {
      gather.append(a)
    } else {
      var a = a
      gather += permutations(a, n - 1)
      for i in 0..<n {
        a.swapAt(i, n)
        gather += permutations(a, n - 1)
        a.swapAt(i, n)
      }
    }
    return gather
  }

  func amplify(signal: Int, phase: Int) -> Int {
    let program = IntCode(program: amplifierControl)
    return program.run(input: [phase, signal], yieldWhenOutputAvailable: true).first!
  }
  
  func amplify(signal: Int, phases: [Int]) -> Int {
    var signal = signal
    phases.forEach{ phase in
      signal = amplify(signal: signal, phase: phase)
    }
    return signal
  }
  
  func amplifyLoop(signal: Int, phases: [Int]) -> Int {
    let amps = (0...4).map{ _ in IntCode(program: amplifierControl) }
    var signal = signal
    var first = true
    debug("======================")
    debug("=== Phases: \(phases)")

    var loopCount = 1
    mainLoop:
    while true {
      debug("=== Loop: \(loopCount)")
      for ampIndex in (0...4) {
        debug("=== Amp: \(ampIndex) with signal in: \(signal)")
        let input = first ? [phases[ampIndex], signal] : [signal]
        let output = amps[ampIndex].run(input: input, yieldWhenOutputAvailable: true)
        switch output.count {
        case 0:
          /// No outputs so must be an end to the program!
          break mainLoop
        case 1:
          /// We have one output so we can return it
          signal = output.first!
        default:
          fatalError("Multiple outputs - probably an error!!!")
        }
        debug("--- Loop: \(loopCount)   Signal Out: \(signal)")
      }
      first = false
      loopCount += 1
      if loopCount == 6 {
        var x = 1
        x = x + 1
      }
    }
    return signal
  }

  func maxAmplify(signal: Int, phases: [Int]) -> Int {
    var maximum = Int.min
    for permutation in permutations(phases,phases.count-1) {
      let signal = amplify(signal: 0, phases: permutation)
      maximum = max(maximum, signal)
    }
    return maximum
  }

  func maxAmplifyLoop(signal: Int, phases: [Int]) -> Int {
    var maximum = Int.min
    for permutation in permutations(phases,phases.count-1) {
      let signal = amplifyLoop(signal: 0, phases: permutation)
      maximum = max(maximum, signal)
    }
    return maximum
  }

  func day7a() -> Int {
    return maxAmplify(signal: 0, phases: [0,1,2,3,4])
  }
    
  func day7b() -> Int {
    return maxAmplifyLoop(signal: 0, phases: [5,6,7,8,9])
  }

}

