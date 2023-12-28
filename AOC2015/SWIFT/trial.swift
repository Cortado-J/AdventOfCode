import Parsing

func trial() {
  let inputold = #"""
    {
      "hello": true,
      "goodbye": 42.42,
      "whatever": null,
      "xs": [1, "hello", null, false],
      "ys": {
        "0": 2,
        "1": "goodbye"
      }
    }
    """#
  let input =
  """
  [{"a":{"e":{"e":161,"a":"blue","d":{"e":-14,"a":"red"}}}}]
  """
  var jsonOutput: JSON!
  jsonOutput = json.parse(input)
  print(jsonOutput)
}
