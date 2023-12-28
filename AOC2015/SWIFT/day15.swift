import Foundation

func day15() {
  struct Recipe {
    var name: String
    var capacity: Int
    var durability: Int
    var flavor: Int
    var texture: Int
    var calories: Int
    var quantity: Int = 0
  }
  
  var recipes =
  [
    Recipe(name: "Sprinkles", capacity: 2, durability: 0, flavor: -2, texture: 0, calories: 3),
    Recipe(name: "Butterscotch", capacity: 0, durability: 5, flavor: -3, texture: 0, calories: 3),
    Recipe(name: "Chocolate", capacity: 0, durability: 0, flavor: 5, texture: -1, calories: 8),
    Recipe(name: "Candy", capacity: 0, durability: -1, flavor: 0, texture: 5, calories: 8)
  ]
  print(recipes)
  
  func property(keypath: WritableKeyPath<Recipe, Int>) -> Int {
    max(0,recipes
          .map { recipe in recipe[keyPath: keypath] * recipe.quantity}
          .reduce(0, +))
  }

  var maxScore = 0
  var max100Score = 0
  for q0 in 0...100 {
    recipes[0].quantity = q0
    for q1 in 0...100-q0 {
      recipes[1].quantity = q1
      for q2 in 0...100-q0-q1 {
        recipes[2].quantity = q2
        let q3 = 100-q0-q1-q2
        recipes[3].quantity = q3

        let score = [\Recipe.capacity, \Recipe.durability, \Recipe.flavor ,\Recipe.texture]
          .map{ property(keypath: $0) }
          .reduce(1, *)
        if score > maxScore {
          maxScore = score
          print(q0,q1,q2,q3)
        }
        let calories = property(keypath: \Recipe.calories)
        if score > max100Score && calories == 500 {
          max100Score = score
        }
      }
    }
  }
  print("Part a: \(maxScore)")
  print("Part b: \(max100Score)")
}

  
