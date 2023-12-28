func day17() {
  let input = [50, 44, 11, 49, 42, 46, 18, 32, 26, 40, 21, 7, 18, 43, 10, 47, 36, 24, 22, 40]
  var gather: [[Int]] = []
  
  func ways(volume: Int, sizes: [Int], soFar: [Int] = []) -> Int {
    if volume == 0 {
      gather.append(soFar)
      return 1
    }
    if sizes.count == 1 {
      if volume == sizes[0] {
        gather.append(soFar + [volume])
        return 1
      }
      return 0
    }

    let dropped = Array(sizes.dropFirst())
    return ways(volume: volume, sizes: dropped, soFar: soFar) +
    ( volume < sizes[0]
      ? 0
      : ways(volume: volume-sizes[0], sizes: dropped, soFar: soFar + [sizes[0]])
    )
  }
  let _ = ways(volume: 150, sizes: input)
  print("Part a: \(gather.count)")
  let containers = gather.map{ $0.count }
  let partb = containers.filter{ $0 == containers.reduce(Int.max, min) }.count
  print("Part b: \(partb)")
}

