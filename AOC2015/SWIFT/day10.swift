func day10() {
  let input = "1113122113"
  func lookAndSay(_ str: String, repeat reps: Int = 1) -> String {
    var working = str
    var result = ""
    for rep in 1...reps {
      if rep > 20 { print(rep) }
      result = ""
      func get() -> Character? {
        guard let first = working.first else { return nil }
        working.removeFirst()
        return first
      }
      var last = Character(".")
      var count = 0
      func say() {
        if last != "." {
          result += String(count) + String(last)
        }
      }
      while let char = get() {
        if char != last {
          say()
          last = char
          count = 0
        }
        count += 1
      }
      say()
      working = result
    }
    return result
  }
  
  let parta = lookAndSay(input, repeat: 40)
  print(input,parta.count)
  let partb = lookAndSay(input, repeat: 50) // Slow - approx 10 minutes
  print(input,partb.count)
}
