//
//  Graphable.swift
//  AdventOfCode2019
//
//  Created by Adahus on 21/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

public protocol Graphable {
  associatedtype Element: Hashable
  var description: CustomStringConvertible { get }
  
  func createVertex(data: Element) -> Vertex<Element>
  func add(_ type: EdgeType, from source: Vertex<Element>, to destination: Vertex<Element>, weight: Double?)
  func weight(from source: Vertex<Element>, to destination: Vertex<Element>) -> Double?
  func edges(from source: Vertex<Element>) -> [Edge<Element>]?
}

extension Graphable {
  func route(to destination: Vertex<Element>, in tree: [Vertex<Element> : Visit<Element>]) -> [Edge<Element>] {
    
    var vertex = destination
    var path : [Edge<Element>] = []
    
    while let visit = tree[vertex],
      case .edge(let edge) = visit {
        
        path = [edge] + path
        vertex = edge.source
    }
    return path
  }
  
  func distance(to destination: Vertex<Element>, in tree: [Vertex<Element> : Visit<Element>]) -> Double {
    let path = route(to: destination, in: tree)
    let distances = path.compactMap{ $0.weight }
    return distances.reduce(0.0, { $0 + $1 })
  }
  
  public func dijkstra(from source: Vertex<Element>, to destination: Vertex<Element>) -> [Edge<Element>]? {
    var visits : [Vertex<Element> : Visit<Element>] = [source: .source]
    var priorityQueue = Heap<Vertex<Element>>(priorityFunction: { self.distance(to: $0, in: visits) < self.distance(to: $1, in: visits) })
    priorityQueue.enqueue(source)
    
    while let visitedVertex = priorityQueue.dequeue() {
      if visitedVertex == destination {
        return route(to: destination, in: visits)
      }
      let neighbourEdges = edges(from: visitedVertex) ?? []
      for edge in neighbourEdges {
        if let weight = edge.weight {
          if visits[edge.destination] != nil {
            if distance(to: visitedVertex, in: visits) + weight < distance(to: edge.destination, in: visits)
            {
              visits[edge.destination] = .edge(edge)
              priorityQueue.enqueue(edge.destination)
            }
          }
          else {
            visits[edge.destination] = .edge(edge)
            priorityQueue.enqueue(edge.destination)
          }
        }
      }
    }
    return nil
  }
}

extension Graphable {
  public func breadthFirstSearch(from source: Vertex<Element>, to destination: Vertex<Element>) -> [Edge<Element>]? {
    var queue = Queue<Vertex<Element>>()
    queue.enqueue(source)
    var visits : [Vertex<Element> : Visit<Element>] = [source: .source]

    while let visitedVertex = queue.dequeue() {
      if visitedVertex == destination {
        var vertex = destination
        var route: [Edge<Element>] = []

        while let visit = visits[vertex],
          case .edge(let edge) = visit {

          route = [edge] + route
          vertex = edge.source
        }
        return route
      }
      let neighbourEdges = edges(from: visitedVertex) ?? []
      for edge in neighbourEdges {
        if visits[edge.destination] == nil {
          queue.enqueue(edge.destination)
          visits[edge.destination] = .edge(edge)
        }
      }
    }
    return nil
  }
}
