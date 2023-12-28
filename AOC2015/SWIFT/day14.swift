import Darwin
func day14() {
  let input =
"""
Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.
Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.
Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.
Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.
Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.
Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.
Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.
Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds.
"""
  .lines
  .map{ $0.split(separator: " ") }

  struct Reindeer {
    var name: String
    var speed: Int
    var duration: Int
    var rest: Int

    var position: Int
    var score: Int
  }
 
  var reindeers = input.map {
    Reindeer(name: String($0[0]),
             speed: Int($0[3])!,
             duration: Int($0[6])!,
             rest: Int($0[13])!,
             position: 0,
             score: 0
    )
  }
  
  print(reindeers)
  let duration: Int = 2503

  var maxDistance = Int.min
  var winningReindeer = ""
  for reindeer in reindeers {
    let cycleTime = reindeer.duration + reindeer.rest
    let distanceInCycle = reindeer.speed * reindeer.duration
    let cycles = duration / cycleTime
    let cyclesDistance = cycles * distanceInCycle
    let remainingTime = duration - cycles * cycleTime
    let extraTravelTime = min(remainingTime, reindeer.duration)
    let extraDistance = extraTravelTime * reindeer.speed
    let totalDistance = cyclesDistance + extraDistance
    if totalDistance > maxDistance {
      maxDistance = totalDistance
      winningReindeer = reindeer.name
    }
  }
  print("Part a: \(winningReindeer) travelled \(maxDistance)")
  
  for second in 1...duration {
    for (index, reindeer) in reindeers.enumerated() {
      let cycleTime = reindeer.duration + reindeer.rest
      let timeThroughCycle = second % cycleTime
      if timeThroughCycle > 0 && timeThroughCycle <= reindeer.duration {
        reindeers[index].position += reindeer.speed
      }
    }
    let winningPosition = reindeers
      .map{ $0.position }
      .sorted(by: >)
      .first
    for (index, reindeer) in reindeers.enumerated() {
      if reindeer.position == winningPosition {
        reindeers[index].score += 1
      }
    }
  }
  let winningScore = reindeers
    .map{ $0.score }
    .sorted(by: >)
    .first!
  print("Part b: Winning score = \(winningScore)")
}

