import Foundation

func day25() {
  
  // Return index followed by result
  func result(row: Int, col: Int) -> (Int, Int) {
    
    let indexStart = row + col - 1 // Row on which the diagonal (which contains the item) starts (1 based)
    let indexHead = indexStart * (indexStart - 1) / 2 + 1 // Index of that start (1 based)
    let index = indexHead + col - 1 // Index of the row, col position (1 based)

    let power = index - 1 // 17868281

    let start = 20151125
    let factor = 252533
    let modulus = 33554393
    
    // We need to know (start * factor ^ power) % modulus
    
    // Because modulus is prime and greater than the power (so does not divide factor)
    // Fermat's little theorem tells us that:
    // factor ^ (modulus-1) % modulus = 1
    // which means we can reduce power by modulus-1 multiple times without affecting the result
    // i.e. we can just calculate:
    // (start * factor ^ (power % (modulus-1) ) ) % modulus
    
    let reducedPower = power % (modulus-1)
  
    var working = start
    if reducedPower > 0 {
      for _ in 1...reducedPower {
        working = (working * factor) % modulus
      }
    }
    let result = working

    //    let multiplier = factor ^^ reducedPower
    //    let result = (start * multiplier ) % modulus
    return (index, result)
  }
  
  for row in 1...6 {
    for col in 1...6 {
      let test = result(row: row, col: col)
      print("row:\(row) col:\(col) index:\(test.0) result:\(test.1)")
    }
  }

  let parta = result(row: 2947, col: 3029)
  print(parta.1)
  
}
