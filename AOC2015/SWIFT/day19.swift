import Parsing

func day19() {
  let mappingInputTest =
"""
e => H
e => O
H => HO
H => OH
O => HH
"""
  let mappingInput =
"""
Al => ThF
Al => ThRnFAr
B => BCa
B => TiB
B => TiRnFAr
Ca => CaCa
Ca => PB
Ca => PRnFAr
Ca => SiRnFYFAr
Ca => SiRnMgAr
Ca => SiTh
F => CaF
F => PMg
F => SiAl
H => CRnAlAr
H => CRnFYFYFAr
H => CRnFYMgAr
H => CRnMgYFAr
H => HCa
H => NRnFYFAr
H => NRnMgAr
H => NTh
H => OB
H => ORnFAr
Mg => BF
Mg => TiMg
N => CRnFAr
N => HSi
O => CRnFYFAr
O => CRnMgAr
O => HP
O => NRnFAr
O => OTi
P => CaP
P => PTi
P => SiRnFAr
Si => CaSi
Th => ThCa
Ti => BP
Ti => TiTi
e => HF
e => NAl
e => OMg
"""
  
  struct Mapping {
    var from: String
    var to: String
  }
  
  // Sample to parse: "cats: 2"
  let mapParser = Prefix { $0 != " " }
    .skip(" => ")
    .take( Prefix { $0 != "\n" })
    .map{ Mapping(from: String($0.0), to: String($0.1) ) }
  let mapsParser = Many(mapParser, separator: "\n")
  
  let mapping = mapsParser.parse(mappingInput)!
  
  var mappingCompact: [String:[String]] = [:]
  for mapp in mapping {
    mappingCompact[mapp.from] = (mappingCompact[mapp.from] ?? []) + [mapp.to]
  }
  print(mapping)
  print(mappingCompact)
  
  let inputTest = "HOHOHO"

  let input = String(
"""
CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl
"""
  )
  
  var outputs: Set<String> = []
  for mapp in mapping {
    let searchingFor = String(mapp.from)
    let replaceWith  = String(mapp.to)
    let foundRanges = input.ranges(of: searchingFor)
    for foundRange in foundRanges {
      let withReplacement = input.replacingCharacters(in: foundRange, with: replaceWith)
      //print("withReplacement='\(withReplacement)'")
      outputs.insert(withReplacement)
    }
  }
  print("Part a: \(outputs.count)")
  
  // For Part B work in reverse!
  // Minimum steps to revrse back to e:
  func back(_ str: String) -> Set<String> {
    var result: Set<String> = []
    for mapp in mapping {
      let searchingFor = String(mapp.to)
      let replaceWith  = String(mapp.from)
      let foundRanges = str.ranges(of: searchingFor)
      for foundRange in foundRanges {
        //print("REPLACING \(searchingFor) WITH \(replaceWith)")
        let withReplacement = str.replacingCharacters(in: foundRange, with: replaceWith)
        //print("[\(withReplacement.count)] withReplacement='\(withReplacement)'")
        result.insert(withReplacement)
      }
    }
    return result
  }
  
  func back(_ strs: Set<String>) -> Set<String> {
    var result: Set<String> = []
    for str in strs {
      result.formUnion(back(str))
    }
    return result
  }

//  var working: Set<String> = [input]
//  print(working)
//  var step = 0
//  while !working.contains("e") {
//    working = back(working)
//    step += 1
//    let shortest = Array(working).sorted{$0.count < $1.count}.prefix(10)
//    print(step, shortest[0].count, shortest)
//  }
  
  // Analysis of what leads to what gives a simple formula:
  print("Part b: ",
        input.filter{ $0.isUppercase }.count // All elements start with a capital letter!
        - input.filter{ $0 == "n" }.count // All n are part of Rn
        - input.filter{ $0 == "r" }.count // All r are part of Ar
        - input.filter{ $0 == "Y" }.count * 2
        - 1
  )
}
