//
//  Vertex.swift
//  AdventOfCode2019
//
//  Created by Adahus on 20/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

public struct Vertex<T: Hashable>: Hashable {
  var data: T
}

extension Vertex: CustomStringConvertible {
  public var description: String {
    return "\(data)"
  }
}

public enum EdgeType {
  case directed, undirected
}

public struct Edge<T: Hashable>: Hashable {
  public var source: Vertex<T>
  public var destination: Vertex<T>
  public let weight: Double?
}

enum Visit<Element: Hashable> {
  case source
  case edge(Edge<Element>)
}
