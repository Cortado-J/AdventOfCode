import Parsing

enum JSON: Equatable {
  indirect case array([JSON])
  case boolean(Bool)
  case null
  case number(Double)
  indirect case object([String: JSON])
  case string(String)
}

var json: AnyParser<Substring.UTF8View, JSON> {
  Skip(Whitespace())
    .take(
      object
        .orElse(array)
        .orElse(string)
        .orElse(number)
        .orElse(boolean)
        .orElse(null)
    )
    .skip(Whitespace())
    .eraseToAnyParser()
}

// MARK: Object
let object = "{".utf8
  .take(
    Many(
      Skip(Whitespace())
        .take(stringLiteral)
        .skip(Whitespace())
        .skip(":".utf8)
        .take(Lazy { json }),
      into: [:],
      separator: ",".utf8.skip(Whitespace())
    ) { object, pair in
      let (name, value) = pair
      object[name] = value
    }
  )
  .skip("}".utf8)
  .map(JSON.object)

// MARK: Array
let array = "[".utf8
  .take(
    Many(
      Lazy { json },
      separator: ",".utf8
    )
  )
  .skip("]".utf8)
  .map(JSON.array)

// MARK: String
let unicode = Prefix(4) {
  (.init(ascii: "0") ... .init(ascii: "9")).contains($0)
  || (.init(ascii: "A") ... .init(ascii: "F")).contains($0)
  || (.init(ascii: "a") ... .init(ascii: "f")).contains($0)
}
  .compactMap {
    UInt32(Substring($0), radix: 16)
      .flatMap(UnicodeScalar.init)
      .map(Character.init)
  }

let escape = "\\".utf8
  .take(
    "\"".utf8.map { "\"" }
      .orElse("\\".utf8.map { "\\" })
      .orElse("/".utf8.map { "/" })
      .orElse("b".utf8.map { "\u{8}" })
      .orElse("f".utf8.map { "\u{c}" })
      .orElse("n".utf8.map { "\n" })
      .orElse("r".utf8.map { "\r" })
      .orElse("t".utf8.map { "\t" })
      .orElse(unicode)
  )

let literal = Prefix(1...) {
  $0 != .init(ascii: "\"") && $0 != .init(ascii: "\\")
}
  .map { String(Substring($0)) }

enum StringFragment {
  case escape(Character)
  case literal(String)
}

let fragment = literal.map(StringFragment.literal)
  .orElse(escape.map(StringFragment.escape))

let stringLiteral = "\"".utf8
  .take(
    Many(fragment, into: "") {
      switch $1 {
      case let .escape(character):
        $0.append(character)
      case let .literal(string):
        $0.append(contentsOf: string)
      }
    }
  )
  .skip("\"".utf8)

let string =
stringLiteral
  .map(JSON.string)

// MARK: Number
let number = Double.parser(of: Substring.UTF8View.self)
  .map(JSON.number)

// MARK: Boolean
let boolean = Bool.parser(of: Substring.UTF8View.self)
  .map(JSON.boolean)

// MARK: Null
let null = "null".utf8
  .map { JSON.null }
