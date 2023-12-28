func day22() {
  
  enum SpellType: CaseIterable {
    case magic, drain, shield, poison, recharge
  }

  struct Spell: Hashable {
    var type: SpellType
    var mana: Int
    var instantDamage: Int = 0
    var instantHeal: Int = 0
    var effectTurns: Int = 0
  }

  struct Effect: Hashable {
    var type: SpellType
    var timer: Int
  }
  
  enum RoundResult {
    case undecided(roundSpellCost: Int)
    case playerWon(roundSpellCost: Int, spellList: [SpellType])
    case bossWon
    case notEnoughMana
    case spellEffectStillLive
  }
 
  struct Player {
    var hitpoints: Int
    var mana: Int
    var armor: Int = 0
    var effects: [Effect] = []
     
    static let spells: [SpellType: Spell] = [
      .magic    : Spell(type: .magic,    mana: 53,  instantDamage: 4),
      .drain    : Spell(type: .drain,    mana: 73,  instantDamage: 2, instantHeal: 2),
      .shield   : Spell(type: .shield,   mana: 113, effectTurns: 6),
      .poison   : Spell(type: .poison,   mana: 173, effectTurns: 6),
      .recharge : Spell(type: .recharge, mana: 229, effectTurns: 5)
    ]
    
    func hasEffect(_ type: SpellType) -> Bool {
      effects.map({$0.type}).contains(type)
    }
    
    func canCast(_ spell: Spell) -> Bool {
      !hasEffect(spell.type)
    }
    
    mutating func cast(spellType: SpellType, boss: inout Boss) -> RoundResult {
      let spell = Player.spells[spellType]!
      guard mana >= spell.mana else {
        //print("Can't cast \(spell.name) because not enough mana!")
        return .notEnoughMana
      }
      // Spend the mana!
      mana -= spell.mana
      
      // Instant damage
      let inflictedDamage = spell.instantDamage
      boss.hitpoints -= inflictedDamage
      guard boss.hitpoints > 0 else { return RoundResult.playerWon(roundSpellCost: spell.mana, spellList: []) }

      //Instant healing
      hitpoints += spell.instantHeal

      // Spell effects
//      var spellString = ""
      if spell.effectTurns > 0 {
        guard canCast(spell) else {
          //print("Can't cast \(spell.name) because it's already runnning!")
          return RoundResult.spellEffectStillLive
        }
        
        effects.append(Effect(type: spell.type, timer: spell.effectTurns))
//        spellString = " and starts effect \(spell.type) which will go on for \(spell.effectTurns) turns"
      }
      //      print("Player casts \(spell.name) which cost \(spell.mana)"
      //            + (inflictedDamage == 0 ? "" : " and inflicts \(inflictedDamage) immediate hitpoints taking boss's hitpoints to \(boss.hitpoints)")
      //            + (spell.instantHeal == 0 ? "" : " and heals \(spell.instantHeal) to brings players hitpoints back to \(hitpoints)")
      //            + spellString
      //            + "." )
      return .undecided(roundSpellCost: spell.mana)
    }
    
    mutating func timersDecrement() {
      for index in effects.indices {
        effects[index].timer -= 1
      }
      // Remove timed out effects
      effects = effects.filter{ $0.timer > 0 }
    }
    func getTimer(_ type: SpellType) -> Int {
      effects.first{ $0.type == type }?.timer ?? 0
    }
    
    mutating func turnEffects(boss: inout Boss) {
      if hasEffect(.shield) {
//        var shieldString = ""
//        if armor == 0 { shieldString = " increases armor to 7." }
//        else { shieldString = " keeps armor at 7." }
        //          print("Shield effect: (remaining \(getTimer("Shield"))) \(shieldString)")
        armor = 7
      } else {
        if armor == 7 {
          //            print("Shield ends so armor back to 0.")
        }
        armor = 0
      }
      if hasEffect(.poison) {
        boss.hitpoints -= 3
        //          print("Poison effect: (remaining \(getTimer("Poison"))) damages boss by 3 taking their hitpoints to \(boss.hitpoints).")
      }
      if hasEffect(.recharge) {
        mana += 101
        //          print("Recharge effect: (remaining \(getTimer("Recharge"))) heals player's mana by 101 taking their mana to \(mana).")
      }
      timersDecrement()
    }
  }

  struct Boss {
    var hitpoints: Int
    var damage: Int
    
    mutating func attack(player: inout Player) -> Bool {
      let inflictedDamage = max(1, damage - player.armor)
      player.hitpoints -= inflictedDamage
      //print("Boss deals \(inflictedDamage) on player whose hitpoints go down to \(player.hitpoints).")
      return player.hitpoints <= 0
    }
  }

  struct Battle {
    var player: Player
    var boss: Boss
    var spellsSoFar: [SpellType]
    var costSoFar: Int
    var hard: Bool
    var maxSpells: Int
    
    func status() {
//      print("- Player has \(player.hitpoints) hit points, \(player.armor) armor, \(player.mana) mana")
//      print("- Boss has \(boss.hitpoints) hit points")
    }
    
    // Performs a player turn followed by a boss turn
    mutating func round(spellType: SpellType) -> RoundResult {
      // Players turn
      //        print("========== Players turn =======================")
      status()
      if hard {
        player.hitpoints -= 1
        //print("Hard mode: player loses 1 hitpoint so hitpoints = \(hitpoints)")
        if player.hitpoints <= 0 { return .bossWon }
      }
      player.turnEffects(boss: &boss)

      // Check for poison finishing off the boss!
      if boss.hitpoints <= 0 {
        // A bit ambiguous whether the spell mana should be costed because the
        //   poison finishes off the boss before the spell is cast
        // As it happens, this doesn't make any difference
        
        // Alternative lines given below:
        // Don't cost the spell:
        return RoundResult.playerWon(roundSpellCost: 0, spellList: spellsSoFar)
        //Do cost the spell
        //return RoundResult.playerWon(roundSpellCost: Player.spells[spellType]!.mana, spellList: spellsSoFar + [spellType]  )
      }

      let castResult = player.cast(spellType: spellType, boss: &boss)
      switch castResult {
      case .playerWon(roundSpellCost: let roundSpellCost, spellList: _): return .playerWon(roundSpellCost: roundSpellCost, spellList: spellsSoFar + [spellType])
      case .bossWon: fatalError("Should never get a boss winning from player casting a spell!")
      case .notEnoughMana: return castResult
      case .spellEffectStillLive: return castResult
      case .undecided(roundSpellCost: let roundSpellCost):
        // Only when it's undecided do we need to give the boss a turn:
        // Boss turn
        //print("- - - - -  Boss turn:")
        status()
        player.turnEffects(boss: &boss)

        // Check for poison finishing off the boss!
        if boss.hitpoints <= 0 { return RoundResult.playerWon(roundSpellCost: roundSpellCost, spellList: spellsSoFar + [spellType] )}

        if boss.attack(player: &player) { return .bossWon }
        return .undecided(roundSpellCost: roundSpellCost)
      }
    }
    
    // Return cheapest win from this position and the list of spells cast
    func cheapestWin() -> (Int, [SpellType])? {
      // If too many spells then don't bother!!
      guard spellsSoFar.count <= maxSpells else { return nil }
//      print(spellsSoFar.map{"\($0)"} )
      var cheapest: (Int, [SpellType])? = nil
      for spellType in SpellType.allCases {
        var newBattle = self
        let nextRound = newBattle.round(spellType: spellType)
        var newCheapest: (Int, [SpellType])? = nil
        
        switch nextRound {
        case .undecided(roundSpellCost: let roundSpellCost):
          newBattle.spellsSoFar.append(spellType)
          newBattle.costSoFar += roundSpellCost
          newCheapest = newBattle.cheapestWin() // Recurse!
        case .playerWon(roundSpellCost: let roundSpellCost, spellList: _):
          newBattle.spellsSoFar.append(spellType)
          newBattle.costSoFar += roundSpellCost
          newCheapest = (newBattle.costSoFar, newBattle.spellsSoFar)
        case .bossWon: continue
        case .notEnoughMana:  continue
        case .spellEffectStillLive:  continue
        }
        
        guard let newCheap = newCheapest else {
          // No cheapest win from the new position
          continue
        }
        // We've cast a spell and have a cheapest value of that battle
        if cheapest == nil {
          cheapest = newCheap
        } else {
          if newCheap.0 < cheapest!.0 {
            cheapest = newCheap
          }
        }
      }
      return cheapest
    }
  }

  let battleA = Battle(
    player: Player(hitpoints: 50, mana: 500),
    boss: Boss(hitpoints: 51, damage: 9),
    spellsSoFar: [],
    costSoFar: 0,
    hard: false,
    maxSpells: 9
  )
  var battleB = battleA
  battleB.hard = true

  let parta = battleA.cheapestWin()!
  print("Part a: \(parta.0), \(parta.1.map{"\($0)"})")
  
  let partb = battleB.cheapestWin()!
  print("Part b: \(partb.0), \(partb.1.map{"\($0)"})")
  
}


  

                                          
                                       
