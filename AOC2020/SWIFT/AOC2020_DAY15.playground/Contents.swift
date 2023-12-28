var numbers = [0,3,6]
numbers = [0,1,4,13,15,12,16]

var turns: [Int] = []
var latest: [Int:(Int,Int?)] = [:] // Looks up number and provides: when spken last AND when spoken before that

func record(turn: Int, number: Int) {
  turns.append(number)
  print(turn, number)
}

for turn in 1...30000000 {
  if turn <= numbers.count {
    record(turn: turn, number: numbers[turn-1])
  } else {
    let consider = turns[turn-2]
    let findIn = turns.dropLast()
    //print("consider=\(consider)  findIn=\(findIn)")
    if let last = turns
      .dropLast()
      .lastIndex(of: turns[turn-2]) {
      // There was a previous telling of that number:
      //print("record(turn: turn, number: (turn-1) - last): turn=\(turn), last=\(last))")
      record(turn: turn, number: turn-2 - last)
    } else {
      // No previous telling of that number:
      record(turn: turn, number: 0)
    }
  }
}
