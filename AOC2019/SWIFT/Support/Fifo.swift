//
//  Fifo.swift
//  AdventOfCode2019
//
//  Created by Adahus on 09/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

class Fifo<T> {
  var values: [T] = []
  
  func put(_ value: T) {
    values.append(value)
  }
  
  func put(_ values: [T]) {
    values.forEach{ put($0) }
  }
  
  func get() -> T? {
    guard values.count > 0 else { return nil }
    let value = values[0]
    values.remove(at: 0)
    return value
  }

  func getAll() -> [T] {
    let valuesKeep = values
    values = []
    return valuesKeep
  }
}
