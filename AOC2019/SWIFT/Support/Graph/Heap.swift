//
//  Heap.swift
//  AdventOfCode2019
//
//  Created by Adahus on 21/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

/// A "Heap" of elements in priority order and is fast.
/// Great explanation (and where the source came from) at:
/// https://www.raywenderlich.com/586-swift-algorithm-club-heap-and-priority-queue-data-structure

struct Heap<Element> {
  var elements : [Element]
  let priorityFunction : (Element, Element) -> Bool

  /// Initialiser
  init(elements: [Element] = [], priorityFunction: @escaping (Element, Element) -> Bool) {
    self.elements = elements
    self.priorityFunction = priorityFunction
    buildHeap()
  }

  mutating func buildHeap() {
    for index in (0 ..< count / 2).reversed() {
      siftDown(elementAtIndex: index)
    }
  }
  
  /// Priority queue functions
  var isEmpty : Bool { elements.isEmpty }
  var count   : Int  { elements.count   }

  func peek() -> Element? { elements.first }
  
  mutating func enqueue(_ element: Element) {
    elements.append(element)
    siftUp(elementAtIndex: count - 1)
  }
  
  mutating func siftUp(elementAtIndex index: Int) {
    let parent = parentIndex(of: index)
    guard !isRoot(index), isHigherPriority(at: index, than: parent) else { return }
    elements.swapAt(index, parent)
    siftUp(elementAtIndex: parent)
  }

  mutating func dequeue() -> Element? {
    guard !isEmpty else { return nil }
    elements.swapAt(0, count - 1)
    let element = elements.removeLast()
    if !isEmpty { siftDown(elementAtIndex: 0) }
    return element
  }
  
  mutating func siftDown(elementAtIndex index: Int) {
    let childIndex = highestPriorityIndex(for: index)
    if index == childIndex { return }
    elements.swapAt(index, childIndex)
    siftDown(elementAtIndex: childIndex)
  }
  
  /// Helper functions
  func isRoot(_ index: Int)          -> Bool { (index == 0) }
  func leftChildIndex(of index: Int)  -> Int { (2 * index) + 1 }
  func rightChildIndex(of index: Int) -> Int { (2 * index) + 2 }
  func parentIndex(of index: Int)     -> Int { (index - 1) / 2 }
  
  func isHigherPriority(at firstIndex: Int, than secondIndex: Int) -> Bool {
    priorityFunction(elements[firstIndex], elements[secondIndex])
  }

  func highestPriorityIndex(of parentIndex: Int, and childIndex: Int) -> Int {
    guard childIndex < count && isHigherPriority(at: childIndex, than: parentIndex)
      else { return parentIndex }
    return childIndex
  }
    
  func highestPriorityIndex(for parent: Int) -> Int {
    highestPriorityIndex(of: highestPriorityIndex(of: parent, and: leftChildIndex(of: parent)), and: rightChildIndex(of: parent))
  }

}

