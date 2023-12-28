func day21() {
  struct Item: Hashable {
    var category: String
    var name: String
    var cost: Int
    var damage: Int
    var armor: Int
  }
  
  let items = [
    Item(category: "Weapon", name: "Dagger", cost:8, damage: 4, armor: 0),
    Item(category: "Weapon", name: "Shortsword", cost:10, damage: 5, armor: 0),
    Item(category: "Weapon", name: "Warhammer", cost:25, damage: 6, armor: 0),
    Item(category: "Weapon", name: "Longsword", cost:40, damage: 7, armor: 0),
    Item(category: "Weapon", name: "Greataxe", cost:74, damage: 8, armor: 0),
    
    
    Item(category: "Armor", name: "Leather", cost:13, damage: 0, armor: 1),
    Item(category: "Armor", name: "Chainmail", cost:31, damage: 0, armor: 2),
    Item(category: "Armor", name: "Splintmail", cost:53, damage: 0, armor: 3),
    Item(category: "Armor", name: "Bandedmail", cost:75, damage: 0, armor: 4),
    Item(category: "Armor", name: "Platemail", cost:102, damage: 0, armor: 5),
    
    
    Item(category: "Ring", name: "Damage +1", cost:25, damage: 1, armor: 0),
    Item(category: "Ring", name: "Damage +2", cost:50, damage: 2, armor: 0),
    Item(category: "Ring", name: "Damage +3", cost:100, damage: 3, armor: 0),
    Item(category: "Ring", name: "Defense +1", cost:20, damage: 0, armor: 1),
    Item(category: "Ring", name: "Defense +2", cost:40, damage: 0, armor: 2),
    Item(category: "Ring", name: "Defense +3", cost:80, damage: 0, armor: 3),
    
    
    ]
  
  func itemList(ofCategory: String) -> [Item] {
    items.filter{ $0.category == ofCategory }
  }

  print(items)

  class Character {
    var name: String
    var hitpoints: Int
    var items: [Item]
    
    var damage: Int { items.map{$0.damage}.reduce(0,+) }
    var armor: Int { items.map{$0.armor}.reduce(0,+) }
    
    init(name: String, hitpoints: Int, items: [Item]) {
      self.name = name
      self.hitpoints = hitpoints
      self.items = items
    }

    func attacked(by attacker: Character) {
      let inflictedDamage = max(1, attacker.damage - armor)
      hitpoints -= inflictedDamage
      //print("\(attacker.name) deals \(inflictedDamage) on \(name) whose hitpoints go down to \(hitpoints).")
    }
    
    // return true if you win and false if enemy wins
    func battle(opponent: Character) -> Bool {
      while true {
        opponent.attacked(by: self)
        if opponent.hitpoints <= 0 { return true }
        attacked(by: opponent)
        if hitpoints <= 0 { return false }
      }
    }
  }

  //  // Test:
  //  let testplayer = Character(
  //    name: "Player",
  //    hitpoints: 8,
  //    items: [Item(category: "Test", name: "Test", cost: 0, damage: 5, armor: 5)]
  //  )
  //  let testboss = Character(
  //    name: "Boss",
  //    hitpoints: 12,
  //    items: [Item(category: "Boss", name: "Boss", cost: 0, damage: 7, armor: 2)]
  //  )
  //  let result = testplayer.battle(opponent: testboss)
  //  print(result)

  // 1 weapon
  let weaponLists =
  Array(itemList(ofCategory: "Weapon").combinations(choose: 1))
  
  // 0-1 armor
  let armorLists =
  Array(itemList(ofCategory: "Armor").combinations(choose: 0)) +
  Array(itemList(ofCategory: "Armor").combinations(choose: 1))
  
  // 0-2 rings
  let ringLists =
  Array(itemList(ofCategory: "Ring").combinations(choose: 0)) +
  Array(itemList(ofCategory: "Ring").combinations(choose: 1)) +
  Array(itemList(ofCategory: "Ring").combinations(choose: 2))

  //print(weaponLists.count, armorLists.count, ringLists.count)
  
  var minimumCost = Int.max
  for weaponList in weaponLists {
    for armorList in armorLists {
      for ringList in ringLists {
        let equipmentList = weaponList + armorList + ringList
        let equipmentCost = equipmentList.map{ $0.cost }.reduce(0, +)
        if equipmentCost < minimumCost { // Don;t bother to do the battle if th cos is more!
          let boss = Character(
            name: "Boss",
            hitpoints: 104,
            items: [Item(category: "Boss", name: "Boss", cost: 0, damage: 8, armor: 1)]
          )
          let player = Character(
            name: "Player",
            hitpoints: 100,
            items: equipmentList
          )
          if player.battle(opponent: boss) {
            minimumCost = equipmentCost
            print("Cheapest winning equipment so far costs \(equipmentCost) and is: \(equipmentList.map{ $0.name}.joined(separator: ", ")).")
          }
        }
      }
    }
  }
  print("Part a: \(minimumCost)")

  var maximumCost = Int.min
  for weaponList in weaponLists {
    for armorList in armorLists {
      for ringList in ringLists {
        let equipmentList = weaponList + armorList + ringList
        let equipmentCost = equipmentList.map{ $0.cost }.reduce(0, +)
        if equipmentCost > maximumCost { // Don;t bother to do the battle if th cos is more!
          let boss = Character(
            name: "Boss",
            hitpoints: 104,
            items: [Item(category: "Boss", name: "Boss", cost: 0, damage: 8, armor: 1)]
          )
          let player = Character(
            name: "Player",
            hitpoints: 100,
            items: equipmentList
          )
          if !player.battle(opponent: boss) {
            maximumCost = equipmentCost
            print("Most expensive losing equipment so far costs \(equipmentCost) and is: \(equipmentList.map{ $0.name}.joined(separator: ", ")).")
          }
        }
      }
    }
  }
  print("Part b: \(maximumCost)")
}
