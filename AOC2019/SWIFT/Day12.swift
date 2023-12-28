//
//  Day12.swift
//  AdventOfCode2019
//
//  Created by Adahus on 12/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

struct SpaceLocation {
  var x: Int
  var y: Int
  var z: Int
}

struct Velocity {
  var x: Int
  var y: Int
  var z: Int
}

class Moon {
  var id: Int
  var location: SpaceLocation
  var velocity: Velocity
  
  init(id: Int, location: SpaceLocation) {
    self.id = id
    self.location = location
    velocity = Velocity(x: 0, y: 0, z: 0)
  }
  
  func vel(for other: Moon) {
    if location.x > other.location.x { velocity.x -= 1; other.velocity.x += 1 }
    if location.x < other.location.x { velocity.x += 1; other.velocity.x -= 1 }
    if location.y > other.location.y { velocity.y -= 1; other.velocity.y += 1 }
    if location.y < other.location.y { velocity.y += 1; other.velocity.y -= 1 }
    if location.z > other.location.z { velocity.z -= 1; other.velocity.z += 1 }
    if location.z < other.location.z { velocity.z += 1; other.velocity.z -= 1 }
  }
  
  func loc() {
    location.x += velocity.x
    location.y += velocity.y
    location.z += velocity.z
  }
  
  var pot: Int { abs(location.x) + abs(location.y) + abs(location.z) }
  var kin: Int  { abs(velocity.x) + abs(velocity.y) + abs(velocity.z) }
  var tot: Int  { pot * kin }
  
  var desc: String { "L: \(location.x),\(location.y),\(location.z)  V: \(velocity.x),\(velocity.y),\(velocity.z)"}
}

struct Galaxy {
  var moons: [Moon]
  
  func stepIt() {
    for a in (0..<moons.count) {
      for b in (a+1..<moons.count) {
        moons[a].vel(for: moons[b])
      }
    }
    for a in (0..<moons.count) {
      moons[a].loc()
    }
  }
  
  func show() {
    for a in (0..<moons.count) {
      print(moons[a].desc)
    }
  }
  
  var energy: Int { moons.reduce(0) { $0 + $1.tot } }
  
  var posx : [Int] { moons.map { $0.location.x } + moons.map { $0.velocity.x } }
  var posy : [Int] { moons.map { $0.location.y } + moons.map { $0.velocity.y } }
  var posz : [Int] { moons.map { $0.location.z } + moons.map { $0.velocity.z } }
}

struct Day12 {
  var galaxy = Galaxy(moons: [
    Moon(id: 1, location: SpaceLocation(x:3, y:3, z:0)),
    Moon(id: 2, location: SpaceLocation(x:4, y:-16, z:2)),
    Moon(id: 3, location: SpaceLocation(x:-10, y:-6, z:5)),
    Moon(id: 4, location: SpaceLocation(x:-3, y:0, z:-13))
    ]
  )

  func parta() -> [Int] {
    galaxy.show()
    for _ in (1...1000) {
      galaxy.stepIt()
      galaxy.show()
    }
    
    return [galaxy.energy]
  }
  
  func partb() -> [Int] {
//    return [286332*13*883*115807]
    galaxy.show()
    let posx = galaxy.posx
    let posy = galaxy.posy
    let posz = galaxy.posz

    var todox = true
    var todoy = true
    var todoz = true

    var count = 1
    var countx: Int!
    var county: Int!
    var countz: Int!
    while todox || todoy || todoz {
      galaxy.stepIt()
      if todox && posx == galaxy.posx { print("x: \(count)"); countx = count; todox = false}
      if todoy && posy == galaxy.posy { print("y: \(count)"); county = count; todoy = false }
      if todoz && posz == galaxy.posz { print("z: \(count)"); countz = count; todoz = false }
      //      galaxy.show()
      count += 1
    }

    return [ lcm([countx,county,countz]) ]
  }
}
