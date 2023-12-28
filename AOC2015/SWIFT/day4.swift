import Foundation
import CryptoKit

func day4() {
  let input = "yzbqklnj"
  var needPartA = true
  var n = 0
  while true {
    n += 1
    //    if n % 100000 == 0 { print(n) }
    let code = input + String(n)
    let md5 = code.MD5
    if needPartA {
      if md5.prefix(5) == "00000" {
        print("part a: \(n)  [code=\(code) gives MD5=\(md5)]")
        needPartA = false
      }
    }
    if md5.prefix(6) == "000000" {
      print("part b: \(n)  [code=\(code) gives MD5=\(md5)]")
      break
    }
  }
}
