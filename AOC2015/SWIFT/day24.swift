func day24() {
  let input: Set<Int> = [1, 3, 5, 11, 13, 17, 19, 23, 29, 31, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
  let total = input.reduce(0, +)

  let third = total/3
  let parta = input
    .combinations(choose: 6) //Find choose by trial and error - we want smallest possible
    .filter{ $0.reduce(0,+) == third }
    .map{ $0.reduce(1,*) }
    .sorted{ $1 > $0}
    .first!
  print("Part a: \(parta)")

  let quarter = total/4
  let partb = input
    .combinations(choose: 5) //Find choose by trial and error - we want smallest possible
    .filter{ $0.reduce(0,+) == quarter }
    .map{ ($0, $0.reduce(1,*) ) }
    .sorted{ $1.1 > $0.1}
    .first!
    .1
  print("Part b: \(partb)")

}
