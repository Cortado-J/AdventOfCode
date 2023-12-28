//
//  Combination.swift
//  AdventOfCode2019
//
//  Created by Suhada on 25/12/2019.
//  Copyright © 2019 Suhada. All rights reserved.
//

func powersetFrom<T>(_ elements: Set<T>) -> Set<Set<T>> {
  guard elements.count > 0 else { return [[]] }
  var powerset: Set<Set<T>> = [[]]
  for element in elements {
    for subset in powerset {
      powerset.insert(subset.union([element]))
    }
  }
  return powerset
}
