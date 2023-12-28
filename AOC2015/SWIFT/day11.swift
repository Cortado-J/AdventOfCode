func day11() {
  let input = "hxbxwxba"
  
  func increment(_ password: [Character]) -> [Character] {
    var index = password.count
    var result = password
    while index >= 0 {
      index -= 1
      if result[index] == "z" {
        result[index] = "a"
      } else {
        result[index] = result[index].nextUnicode()
        return result
      }
    }
    fatalError("Can't increment any more!!")
  }

  func isValid(_ password: [Character]) -> Bool {
    //Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    let test1 = zip(zip(password, password.dropFirst()), password.dropFirst().dropFirst())
      .map{ $0.0.1 == $0.0.0.nextUnicode() && $0.1 == $0.0.1.nextUnicode() ? 1 : 0}
    guard test1.reduce(0, +) > 0 else {
      //print("\(password.reduce(""){$0 + [$1]}) failed test 1 (No increasing straight of at least 3 letters)")
      return false
    }

    //Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
    guard password.filter({ "iol".contains($0) }).count == 0 else {
      //print("\(password.reduce(""){$0 + [$1]}) failed test 2 (Contans one of i o l)")
      return false
    }

    // Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
    let test3 = zip(password, password.dropFirst())
      .filter{ $0.0 == $0.1 }
      .map{ $0.0 }
    guard Set(test3).count > 1 else {
      //print("\(password.reduce(""){$0 + [$1]}) failed test 3 (Didn't find 2 different non-overlapping pairs)")
      return false
    }

    return true
  }

  func nextvalid(_ password: String) -> String {
    var working = password.map{$0}
    repeat {
      working = increment(working)
      //    print(working.reduce(""){$0 + [$1]})
    } while !isValid(working)
    return working.reduce(""){$0 + [$1]}
  }
  
  let passworda = nextvalid(input)
  print("Part a: \(passworda)")
  let passwordb = nextvalid(passworda)
  print("Part b: \(passwordb)")

  
}

