//
//  IntCode.swift
//  AdventOfCode2019
//
//  Created by Adahus on 02/12/2019.
//  Copyright © 2019 Adahus. All rights reserved.
//

var showIntcode = false

enum ParameterMode: Int {
  case position  = 0
  case immediate = 1
  case relative  = 2
}

enum ParameterType {
  case read
  case write
  case input
  case output
}

struct Signature {
  var parameters: [ParameterType]
}

enum Function {
  case binary( (Int, Int) -> Int )
  case input
  case output
  case jump( (Int) -> Bool )
  case base
  case stop
  
  /// Describes the signature of the parameters used for this function
  var signature: Signature {
    switch self {
    case .binary: return Signature(parameters: [.read, .read, .write])
    case .input:  return Signature(parameters: [.write              ])
    case .output: return Signature(parameters: [.read               ])
    case .jump:   return Signature(parameters: [.read, .read        ])
    case .base:   return Signature(parameters: [.read               ])
    case .stop:   return Signature(parameters: [                    ])
    }
  }
  
  var length: Int { signature.parameters.count }
  
}

struct OpDef {
  var desc: String /// Description of the opcdoe
  var function: Function  /// Function to be used by the opcode
  var parameterCount: Int { function.length }
  var length: Int { 1 + parameterCount } /// One for the opcode and one each parameter
}

enum OpCode: Int {
  case add          = 1
  case multiply     = 2
  case input        = 3
  case output       = 4
  case jumpIfTrue   = 5
  case jumpIfFalse  = 6
  case lessThan     = 7
  case equals       = 8
  case relativeBase = 9
  case stop         = 99
  
  var lookup: OpDef {
    switch self {
    case .add:          return OpDef(desc: "ADD"      , function: .binary(+)                    )
    case .multiply:     return OpDef(desc: "MULTIPLY" , function: .binary(*)                    )
    case .input:        return OpDef(desc: "INPUT"    , function: .input                        )
    case .output:       return OpDef(desc: "OUTPUT"   , function: .output                       )
    case .jumpIfTrue:   return OpDef(desc: "JUMP NZ"  , function: .jump({ $0 != 0})             )
    case .jumpIfFalse:  return OpDef(desc: "JUMP Z"   , function: .jump({ $0 == 0})             )
    case .lessThan:     return OpDef(desc: "LESSTHAN" , function: .binary({ $0 <  $1 ? 1 : 0 }) )
    case .equals:       return OpDef(desc: "EQUALS"   , function: .binary({ $0 == $1 ? 1 : 0 }) )
    case .relativeBase: return OpDef(desc: "REBASE"   , function: .base                         )
    case .stop:         return OpDef(desc: "STOP"     , function: .stop                         )
    }
    
  }
  
  var parameterCount: Int { lookup.parameterCount }
  var function: Function  { lookup.function }
  var length:   Int       { lookup.length }
  var description: String { lookup.desc }
}

struct Operation {
  var memory: Memory  /// memory is a class so this is just a reference to the memory
  var address: Int
  
  init(memory: Memory, address: Int) {
    self.memory = memory
    memory.checkInRange(address)
    self.address = address
  }

  var value: Int { memory.read(address) }

  var opCode: OpCode {
    guard let opCode = OpCode(rawValue: value % 100)  else { fatalError("Invalid opcode: \(value)") }
    return opCode
  }
  
  /// Note that parameter is 1 based so parameter: 1 is the first parameter
  func getModeOf(parameter: Int) -> ParameterMode {
    let parameterModeValue = value.digit(parameter + 1) // Which makes 100s digit be parametermode of 1st parameter
    guard let parameterMode = ParameterMode(rawValue: parameterModeValue) else {
      fatalError("Invalid parameter mode: \(parameterModeValue)")
    }
    return parameterMode
  }

  var description: String {
    String("[\(String(format: "%04d", address))] \(String((opCode.description) + "            "))"
      .prefix(18))
  }

}

enum ExecResult {
  case next  /// When an instruction has been executed and there's more available
  case waitingForInput /// Input instruction found but no input available
  case outputAvailable /// When at least one output is available
  case stop  /// When a stop has been found
}

class IntCode {
  var name: String
  var memory: Memory
  var execPointer: Int
  var inputStream: Fifo<Int>
  var outputStream: Fifo<Int>
  
  init(program: [Int], name: String = "") {
    self.memory = Memory(initial: program)
    self.name = name
    execPointer = 0
    inputStream = Fifo()
    outputStream = Fifo()
  }
    
  func set(execPointer: Int) {
    memory.checkInRange(execPointer)
    self.execPointer = execPointer
  }
  
  // return false when stop
  func exec(yieldWhenOutputAvailable: Bool) -> ExecResult {
    let base = execPointer
    let operation = Operation(memory: memory, address: base)

    var message = "\(name)> "
    defer { debug(message, show: showIntcode) }
    
    func addToMessage(_ extra: String) { message += extra }
    
    addToMessage(operation.description)
    
    func read(parameter: Int) -> Int {
      let value = memory.readParameter(base: base, offset: parameter, mode: operation.getModeOf(parameter: parameter))
      switch operation.getModeOf(parameter: parameter) {
      case .position:
        addToMessage("[\(base+parameter)]=\(value)")
      case .immediate:
        addToMessage("#\(value)")
      case .relative:
        addToMessage("[\(memory.relativeBase)+\(base+parameter)]=\(value)")
      }
      return value
    }
    
    func write(parameter: Int, value: Int) {
      memory.writeParameter(base: base, offset: parameter, mode: operation.getModeOf(parameter: parameter), value: value)
      switch operation.getModeOf(parameter: parameter) {
      case .position:
        addToMessage("[\(base+parameter)]=\(value)")
      case .immediate:
        addToMessage("#\(value)")
      case .relative:
        addToMessage("[\(memory.relativeBase)+\(base+parameter)]=\(value)")
      }
    }
    
    /// Use the opcode to decide what to do:
    switch operation.opCode.function {
      
    /// Binary function
    case .binary(let function):
      addToMessage("(")
      let param1 = read(parameter: 1)
      addToMessage(", ")
      let param2 = read(parameter: 2)
      addToMessage(") -> ")
      let calculation = function(param1, param2)
      write(parameter: 3, value: calculation)
      set(execPointer: base + operation.opCode.length)
      
    /// Take input from input stream and store at address of parameetr 1
    case .input:
      addToMessage("INPUT -> ")
      guard let input = inputStream.get() else {
        addToMessage("WAITING")
        return .waitingForInput /// Note that execPointer is left pointing at the same instruction so that when exec is called again it will try the input again which should have been filled by run.
      }
      write(parameter: 1, value: input)
      set(execPointer: base + operation.opCode.length)
      
    /// Take value at address of parmater 1 and send to output
    case .output:
      addToMessage("(")
      let param = read(parameter: 1)
      addToMessage(") -> OUTPUT")
      outputStream.put(param)
      set(execPointer: base + operation.opCode.length)
      if yieldWhenOutputAvailable { return .outputAvailable }
      
    case .base:
      addToMessage("(")
      let param = read(parameter: 1)
      addToMessage(") -> RELATIVEBASE")
      memory.relativeBase += param
      set(execPointer: base + operation.opCode.length)
      
    /// Test parameter 1 using the test function and if true then jump to
    case .jump(let function):
      //      addToMessage(" IF (")
      if function( read(parameter: 1) ) {
        //        addToMessage(" IS ZERO/NONZERO: JUMP TO ")
        addToMessage(" TO ")
        set(execPointer: read(parameter: 2) )
      } else {
//        addToMessage(" IS ZERO/NONZERO: NO JUMP")
        addToMessage(" NO JUMP TO ")
        set(execPointer: base + operation.opCode.length)
      }
      
    case .stop:
      return .stop
    }
    return .next
  }
  
  @discardableResult
  func run(input: [Int] = [], yieldWhenOutputAvailable: Bool = false) -> [Int] {
    inputStream.put(input)
    
    ///If there's some output and we've been asked to yield when it's available then return it straight away - no need to execute any instructions
    if yieldWhenOutputAvailable {
      let output = outputStream.getAll()
      if output.count > 0 { return output }
    }
    /// Note that result of exec can be:
    /// case next  /// When an instruction has been executed
    /// case waitingForInput /// Input instruction found but no input available.
    /// case outputAvailable /// When output is available
    /// case stop  /// When a stop has been found
    while exec(yieldWhenOutputAvailable: yieldWhenOutputAvailable) == .next {
       //print("+", terminator: "")
    }
    return outputStream.getAll()
  }
  
  
  
}
