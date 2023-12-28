//
//  AOCTest.swift
//  AOCTest
//
//  Created by Adahus on 08/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

import XCTest

class AOCTest: XCTestCase {
  
//  func testDay1() {
//    let day1 = Day1()
//    XCTAssertEqual(day1.day1a(), 3464458)
//    XCTAssertEqual(day1.day1b(), 5193796)
//  }
//
//  func testDay2() {
//    let day2 = Day2()
//    XCTAssertEqual(day2.partA(), 6327510)
//    print(day2.partB(), 4112)
//  }
//
//  func testDay3() {
//    let day3 = Day3()
//    let (a,b) = day3.partAandB() // Commented because slow
//    XCTAssertEqual(a, 721)
//    XCTAssertEqual(b, 7388)
//  }
//
//  func testDay4() {
//    let day4 = Day4()
//    let (a,b) = day4.day4AandB()
//    XCTAssertEqual(a, 1790)
//    XCTAssertEqual(b, 1206)
//  }
//
//  func testDay5() {
//    let day5 = Day5()
//    XCTAssertEqual(day5.day5a(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 4601506])
//    XCTAssertEqual(day5.day5b(), [5525561])
//  }
//
//  func testDay6() {
//    let day6 = Day6()
//    let (a,b) = day6.day6AandB()
//    XCTAssertEqual(a, 271151)
//    XCTAssertEqual(b, 388)
//  }
//
//  func testDay7() {
//    let day7 = Day7()
//    XCTAssertEqual(day7.day7a(), 929800)
//    XCTAssertEqual(day7.day7b(), 15432220)
//  }
//
//  func testDay8() {
//    let day8 = Day8()
//    XCTAssertEqual(day8.parta(), 2286)
//    XCTAssertEqual(day8.partb(),
//          [
//            [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
//            [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
//            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
//            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
//            [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
//            [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0]
//    ]
//    )
//    //    [.##....##.####.#....###..]
//    //    [#..#....#....#.#....#..#.]
//    //    [#.......#...#..#....#..#.]
//    //    [#.......#..#...#....###..]
//    //    [#..#.#..#.#....#....#....]
//    //    [.##...##..####.####.#....]
//    // which is CJZLP
//  }
//
//  func testDay9() {
//    let day9 = Day9()
//    XCTAssertEqual(day9.parta(), [3380552333])
//    XCTAssertEqual(day9.partb(), [78831])
//  }
//
//  func testBearing() {
//    var a: [(Int,Int,Double)] = []
//    for x in (-4...4) {
//      for y in (-4...4) {
//        if x == -4 || x == 4 || y == -4 || y == 4 {
//          a.append((x,y,bearing(dy: y, dx: x)))
//        }
//      }
//    }
//    let b = a.sorted{
//      $0.2 < $1.2
//    }
//    b.forEach{
//      print("Bearing of (\($0.0),\($0.1)) is \($0.2)")
//    }
//  }
//
//  func testDay10() {
//    let day10 = Day10()
//    XCTAssertEqual(day10.partaandb(), [267,1309])
//  }
//
//   func testDay11() {
//     let day11 = Day11()
//     XCTAssertEqual(day11.parta(), [2252])
//     XCTAssertEqual(day11.partb(), [249])
//   }
//
//    func testDay12() {
//      let day12 = Day12()
//      XCTAssertEqual(day12.parta(), [12351])
//      XCTAssertEqual(day12.partb(), [380635029877596])
//    }
//
//  func testDay13() {
//    let day13 = Day13()
//    XCTAssertEqual(day13.parta(), [260])
//    XCTAssertEqual(day13.partb(), [12952])
//  }

//  func testDay14() {
//    let day14 = Day14()
//    XCTAssertEqual(day14.parta(), [158482])
//    XCTAssertEqual(day14.partb(), [999999])
//  }

//  func testDay15() {
//    let day15 = Day15()
//    XCTAssertEqual(day15.stats(), [236, 368])
//  }
  
  func testDay16() {
//    let day16 = Day16()
//    XCTAssertEqual(day16.parta(), [88888])
//    XCTAssertEqual(day16.partb(), [88888])
  }

    func testDay17() {
//      let day17 = Day17()
//      XCTAssertEqual(day17.parta(), [3192])
//      XCTAssertEqual(day17.partb(), [99999])
    }

  func testDay18() {
//    let day18 = Day18()
//    XCTAssertEqual(day18.parta(), [99999])
//    XCTAssertEqual(day18.partb(), [99999])
  }
  
//  func testDay19() {
//    var day19 = Day19()
//    XCTAssertEqual(day19.partA(), [99999])
//    XCTAssertEqual(day19.partB(), [99999])
//  }
  
   func testDay20() {
//     var day20 = Day20()
//     XCTAssertEqual(day20.parta(), [99999])
//     XCTAssertEqual(day20.partb(), [99999])
   }

  func testDay21() {
//    var day21 = Day21()
//    XCTAssertEqual(day21.parta(), [99999])
//    XCTAssertEqual(day21.partb(), [99999])
  }
  
  func testDay22() {
    var day22 = Day22()
    XCTAssertEqual(day22.parta(), [4684])
    day22.tests()
    XCTAssertEqual(day22.partb(), [99999])
  }

//  func testDay23() {
//    let day23 = Day23()
//    XCTAssertEqual(day23.partsAandB(), [22650,17298])
//  }

  func testDay24() {
//    let day24 = Day24()
//    XCTAssertEqual(day24.parta(), [99999])
//    XCTAssertEqual(day24.partb(), [99999])
  }

//    func testDay25() {
//      var day25 = Day25()
//      XCTAssertEqual(day25.partA(), [99999,99999])
//    }
}
