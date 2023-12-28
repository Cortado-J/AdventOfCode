func day23() {
  
  let code =
  """
  jio a, +19
  inc a
  tpl a
  inc a
  tpl a
  inc a
  tpl a
  tpl a
  inc a
  inc a
  tpl a
  tpl a
  inc a
  inc a
  tpl a
  inc a
  inc a
  tpl a
  jmp +23
  tpl a
  tpl a
  inc a
  inc a
  tpl a
  inc a
  inc a
  tpl a
  inc a
  tpl a
  inc a
  tpl a
  inc a
  tpl a
  inc a
  inc a
  tpl a
  inc a
  inc a
  tpl a
  tpl a
  inc a
  jio a, +8
  inc b
  jie a, +4
  tpl a
  inc a
  jmp +2
  hlf a
  jmp -7
  """
    .lines
    .map{ String($0)}
  
  print(code)
  
  func calcB(a ain: Int, b bin: Int) -> Int {
    var pointer = 0
    var a = ain
    var b = bin
    while (pointer >= 0 && pointer < code.count) {
      switch code[pointer] {
      case "inc a": a += 1;  pointer += 1
      case "tpl a": a *= 3;  pointer += 1
      case "inc b": b += 1;  pointer += 1
      case "hlf a": a = a/2; pointer += 1
        
      case "jmp +23": pointer += 23
      case "jmp +2" : pointer += 2
      case "jmp -7" : pointer -= 7
        
      case "jio a, +19": if a == 1 { pointer += 19 } else { pointer += 1 }
      case "jio a, +8" : if a == 1 { pointer += 8  } else { pointer += 1 }
        
      case "jie a, +4" : if a % 2 == 0 { pointer += 4  } else { pointer += 1 }
        
      default: fatalError("Unrecognised code!")
      }
    }
    return b
  }
  
  print("Part a: \(calcB(a: 0, b:0))")
  print("Part b: \(calcB(a: 1, b:0))")
}

