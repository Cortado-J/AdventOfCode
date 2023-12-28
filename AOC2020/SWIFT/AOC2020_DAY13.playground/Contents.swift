//let numbers = [2,3,5,7]
//let positions = [0,1,2,3]

//let numbers = [2,3,5]
//let positions = [0,1,2]

//let numbers = [2,3,5]
//let positions = [0,2,1]

//let numbers = [13, 17, 19, 23, 29, 37, 41, 523, 787]

//let numbers   = [ 7, 13, 59, 31, 19]
//let positions = [ 0,  1,  4,  6,  7]

let numbers   = [17, 41, 523, 13, 19, 23, 787, 37, 29]
let positions = [0, 7, 17, 35, 36, 40, 48, 54, 77]

var factors = numbers.map{ _ in 0 }

var t: Int { numbers[0] * factors[0] }
extension Array where Element == Int {
  func productOfPrefix(upToIndex: Int) -> Int { //Doesn;t include the index
    prefix(upTo: upToIndex).reduce(1) { $0*$1 }
  }
}

for stage in 1..<numbers.count {
  while (t + positions[stage]) % numbers[stage] != 0 {
    for i in 0..<stage {
      factors[i] += numbers.productOfPrefix(upToIndex: stage) / numbers[i]
    }
  }
  factors[stage] = (t + positions[stage]) / numbers[stage]
  print(factors)
}

print("======================")
print(factors)
print(zip(numbers,factors).map{ $0.0 * $0.1 })
print("======================")
print("Answer to part b is \(numbers[0]*factors[0])")
