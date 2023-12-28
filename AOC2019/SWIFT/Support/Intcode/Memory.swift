//
//  Memory.swift
//  AdventOfCode2019
//
//  Created by Adahus on 09/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

class Memory {
  var memory: [Int]
  var relativeBase: Int
  
  init(initial: [Int], extraSpaceSize: Int = 10000) {
    memory = initial + Array(repeating: 0, count: extraSpaceSize)
    relativeBase = 0
  }
  
  func checkInRange(_ address: Int) {
    guard address >= 0 && address < memory.count  else { fatalError("Error: Address [\(address)] outside of valid memory range [0..<\(memory.count)].") }
  }
  
  // Simple read and write
  func read(_ address: Int) -> Int {
    checkInRange(address)
    return memory[address]
  }
  
  func write(to address: Int, value: Int) {
    checkInRange(address)
    memory[address] = value
  }
  
  // ParameterMode read and write
  func read(from address: Int, mode: ParameterMode) -> Int {
    switch mode {
    case .position:  return read(read(address))
    case .immediate: return read(address)
    case .relative:  return read(relativeBase + read(address))
    }
  }
  
  func write(to address: Int, mode: ParameterMode, value: Int) {
    switch mode {
    case .position:  write(to: read(address), value: value)
    case .immediate: fatalError("Immediate write is invalid!")
    case .relative:  write(to: relativeBase + read(address), value: value)
    }
  }
  
  // Parameter read and write
  func readParameter(base: Int, offset: Int, mode: ParameterMode) -> Int {
    read(from: base+offset, mode: mode)
  }
  
  func writeParameter(base: Int, offset: Int, mode: ParameterMode, value: Int) {
    write(to: base+offset, mode: mode, value: value)
  }
  
  func patch(address: Int, values: [Int] ) {
    for (offset, value) in values.enumerated() {
      write(to: address+offset, value: value)
    }
  }
  
  func patch(address: Int, value: Int ) {
    write(to: address, value: value)
  }
  
  func patch(_ values: [(address: Int, value: Int)]) {
    for (address, value) in values {
      write(to: address, value: value)
    }
  }
  
}
