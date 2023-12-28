func day20() {
  let input = 29000000

  let max = 1000000 // Guess - if no answer then increase this
  var houses = Array(repeating: 1, count: max)
  for elf in 2...max {
    for house in stride(from: elf-1, to: max, by: elf) {
      houses[house] += elf
    }
    if houses[elf-1] * 10 >= input {
      print("Part a: \(elf)")
      break
    }
  }
  
  let maxb = max // Might need to be different from max
  var points = Array(repeating: 1, count: maxb)
  for elf in 2...maxb {
    var i = 0
    for house in stride(from: elf-1, to: maxb, by: elf) {
      points[house] += elf
      i += 1
      if i >= 50 { break }
    }
    if points[elf-1] * 11 >= input {
      print("Part b: \(elf)")
      break
    }
  }
  
}
