func day9() {
  let input =
"""
Tristram to AlphaCentauri = 34
Tristram to Snowdin = 100
Tristram to Tambi = 63
Tristram to Faerun = 108
Tristram to Norrath = 111
Tristram to Straylight = 89
Tristram to Arbre = 132
AlphaCentauri to Snowdin = 4
AlphaCentauri to Tambi = 79
AlphaCentauri to Faerun = 44
AlphaCentauri to Norrath = 147
AlphaCentauri to Straylight = 133
AlphaCentauri to Arbre = 74
Snowdin to Tambi = 105
Snowdin to Faerun = 95
Snowdin to Norrath = 48
Snowdin to Straylight = 88
Snowdin to Arbre = 7
Tambi to Faerun = 68
Tambi to Norrath = 134
Tambi to Straylight = 107
Tambi to Arbre = 40
Faerun to Norrath = 11
Faerun to Straylight = 66
Faerun to Arbre = 144
Norrath to Straylight = 115
Norrath to Arbre = 135
Straylight to Arbre = 127
"""
    .lines
    .map{
      $0.split(separator: " ")
    }
    .map{
      ( $0[0], $0[2], Int($0[4])! )
    }
  
  var dict: [String:Int] = [:]
  for line in input {
    dict[line.0+">"+line.1] = line.2
    dict[line.1+">"+line.0] = line.2
  }
  print(dict)

//  let distances =
//  Set(input.map{$0.0} + input.map{$0.1}) // Gather towns
//    .permutations() // Different orders
//    .map{
//      zip($0, $0.dropFirst()) // Pair town with next town
//        .map{ $0.0 + ">" + $0.1 } // Construct journey description
//        .map{ dict[$0]! } // Lookup distance
//        .reduce(0, +) // Calculate whole journey
//    }
//    .sorted() // Get shortest first
//  print("Part a: \(distances.first!)")
//  print("Part b: \(distances.last!)")
}
