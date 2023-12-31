//
//  Day5.swift
//  AdventOfCode2021
//
//  Created by Justin Roughley on 09/12/2021.
//

func day10() {
  let inputTest =
"""
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
  
  let input =
"""
{([[[(<<[{[[[[(){}][()]][({}())]]]<{((<>[]){[]<>})({()()}(<>[]))}<{{{}()}{[]()}}>>})[<(<[[<><>][{}{
([(<(((<[({{({(){}}<{}()>)((<>{})[{}<>})}}[{[(<>())[[]]]{{[][]}(<><>)}}{<<{}()>([]())>([<>][{}])}])](<[{[
{{[[<[<(<<<{((<>[])([]<>))(<{}><()[]>)}[(((){}){<>[]})<{(){}}<<>[]>>]>{[{{<>{}}<()<>>}<<<>[]>([]<>)>][
<[{<(({([[([({{}[]}{<><>})<<[]{}>>]<<<{}{}>((){})><{{}()}<{}[]>>>)](([<([]{})<{}<>>>(<[][]>{()()})
{{<(([<[[{<{({{}<>}({}()))<[<>[]](<>[])>}><[(((){})){[()]<<>[]>}][{{<><>}(<>{})}<<()[]>({}())>]>}<[{[(()<>)
[<{{{({{[<([<{<><>}{<>{}}><<[][]>[{}<>]>]({<[]{}>[[]{}]}{([]())([][])})){<{[[][]]([]())}>([[[
{[<[<<([[<(<<<<>>({})>><({(){}}(<>{}))[{()()}(()[])]>}[<({[]})<[()[]](<>{})>>[<({}{})[()<>]><{(){}}>]]>
[(<({{<[{<(<((<><>)<[]<>>)({<><>}<<>()>)><<<()<>>[()()]>{<<>{}>[()<>]}>){{[([]{})<<><>>]([<
<<{{<{<{([{(<{<><>}>((()[])<<>{}>))({<{}>}<[[]()][<><>]>)}<{([[]()]{<>{}})}{(<<>()>{<>{}})[{<><>}{<><>}]}>]
{(<{<({{([[{<({})[()()]><[{}<>][{}[]]>}<<<[]{}>[<>()]>({{}{}}[{}[]])>]<({[[][]]({}())}[(()[]](<
<[<{[<<[(((<([()()]<()()>]([()[]][{}{}])>)[[[{<>}[<>[]]]][(<()()><<>>)<<{}{}>{<>}>]])([(<({}<>)[()()]>
(<<{{([<[<[<[{[]()}[{}<>]]<(<>[])[{}]>><[{()[]}[()[]]]<([]<>)(()())>>]{{{{()<>}{()()}}[(<><
<[([(<[[[(<[(<{}()>{()()})<<()[]>{(){}}>]><<({[]<>}<{}{}>)[{[][]}{[]{}}]>{<{()()}(()[])>{[<><>
[[([[({{{[[(<<()()>[<>[]]>)<[<<>{}>]([[]()][(){}])>]<(<{()<>}[[][]]>(([]{})[[]()]))[<({}[])
<<{[({<[[[[[{<<>()>{<>{}}}[<()()>]](<<{}<>>{{}<>]><[{}<>]<()<>>>)][((<[]{}>[[]])<{{}()}>)[((<>{}))<<<>{}>(
[[<[[<<(({{<({[]<>}([][]))>{([[]()]{{}<>}){[[]{}][()<>]}}}({{({}()}[[][]]}(((){}){<>})}(<[{}<>]{()()}>
{[{<[[(({<({[{()[]}[[][]]]}(({<><>}<{}[]>)))>}{[{(<{[]{}}{{}[]}>{<<><>>})}<{{[[][]]{<>()>}}<{
{[({<{<{[[([[<()<>}{[]<>}][<<>[]>([])]])]([({{[]()}({}())}([<>()](<><>)))])]{{<[<<[]<>>(()())>(<<>()>{<>
({([<({((<({<<()<>>[(){}]>[(<>{}){<>[]}]}){([{{}[]}])([({}()){<><>}]{[<><>]([]())))}><<[([{}[]])](
<{[{<{<<[<<<[(()<>){[][]}]([()<>]({}{}))>{(<{}{}>[<>{}])[{{}()}[(){}]]}><({<[]<>>[<>{}]}{([]<>)<[]{})})<([{}(
<[<<(({<[{{(<[[]<>]<<>()>>([{}<>]{[]()}))}{<(([]<>)<()<>>)[({}[])<[]{}>]><<<{}[]>{{}<>}>({<>[]}[(){}])>}}<(
[[[[[[(((<{<{(()())<<>{}>}>(<[<><>]({}[])})}{{<[()<>]<[]{}>>[{{}<>}[[]()]]}({<<>[]>}[<{}<>
[(({{<{[<[[(<(()())<<>()>>[<<><>><()()>])(<[{}()]><{[]()}<{}{}>>)][<[({}())<{}<>>][({}[])(()[])]>(((
(([<({{<{{[<<{[]()>(<>{})>[[{}]{{}{}}]>{<<[]{}>>[([][])[<><>]]}]<<[<<>[]>({}<>)]({<>[]}<{}{}>)>[{<{}<>>{[]()}
{(<<[{<<{({(<(<>{})(()())><(<>[]){[]<>}>){[(<>[]){[]()}]{[<>()][{}<>]]}}{([[{}()]]((<><>)))[([{}()]([]()))
[{({[[{{[<<{{[{}<>][<>]}([(){}]{<><>})}><(<[()[]][{}{}]><{[]{}}({})>)(<({}[])<()()>>{<{}{}>{[
([(({{<[<(([({{}<>}[[][]])<({}[]){{}()}>]{[[{}[]]][((){})]})<[{{{}<>}([]{})}{{[]<>}}]>)[{{<([]())({})>
<{{{<<(<{<(<{{<>()}}{({}<>)}>)>}((<{[<{}{}>([]<>)]<<[]()>[{}()]>}<{[<><>]<[]{}>}{{(){}}[[]()]}>>[({(()<>)<{}
((<[{<<{{{([[[[][]](<>[])]]{<({}[])([][])]<{{}{}}{()[]}>})}[[{<{<>[]}{<>{}}>}]]}{<[[((()<>)<()[]>){<()>({}[]
({[[{<{{<<([(<[]<>>{<>{}})<{()[]}(<>())>])<[{[<><>]({}{})}][<({}())><{()<>}(<>())>]>>>{{(([
<((<<(<(<<{{{[{}]<()<>>}{[[]<>]{<><>}}}<[[<>{}]{()()}][<()()>{[][]}]>}{[{[{}()][{}{}]}(<{}()>[{}<>])]}>>
(([<({<[[(<(<([]())({}<>)>([{}()]{<>[]}))<{{{}{}}([]{})}<({}{})<{}<>>>>>[{{<<>[]><<>{}>}({{}<>})}{({[]()}(()<
{[((<({[([(([{(){}}{{}()}][<[]()>{(){}}])[[[{}[]]{{}<>}]<{[]{}}>]){(<[<><>][[][]]>)[{{<>{}}((){})>[([]())[
[[<[<{({[({{([()<>]<()()>)}[<<[]()>>]}((({()()})(<{}>[<>()]))[(({}{}){[]}>(([][])<()()>)]))[{<[<[
[<<([((<<(([[({}{})((){})]<({}[])[{}{}]>]<{{<><>}<[]>}>)[<{{<>()}<()()>}{<<>{}>[[]()]}>[(([][])
{(<(<[[((<([{<[][]><()>}[[<>{}]]]<<((){}){[]())>[<()<>>(<>[])]>)<{<[[]][<>{}]>({<><>}[<>()])}({{{
(<{({({<[[((<<{}<>><<>()>>({{}}<<>[])))[<<{}[]><<><>>>{{[]{}}(())}])[<[([]())<<>{}>]>[[[<><
<[{[[{[({{{([<()()><<>[]>])([([]{})(<>())]{([]<>){()[]}})}<{({{}<>}{[]})([()()])}<[[[]<>><<>{}>]<[()()]<(){}
<<[<[{{({(({(<[]()>({}{}))([{}[]][[]()])}{{(()[]){<><>}}([<><>]{{}})})[{[[{}{}]({}())]{<<>{}
{{{[[[[[<(<<{(()[]){()<>}}<<(){}>(()())>>({(()[])}<<[][]>[<>()]>)>)[{[<(<>())>{<(){}>[{}{}]}]
(([<[[{(([([<<<>{}>((){})>[({}{})<()<>>]]([((){})({}())]])[[{[()()][()[]]}([[][]](<>()))][<{()<
([<{{[[{<{[({<()[]>{[]<>}}([()<>]<[]()>))]}>{[<({({}{})})>{{<[<>{}][()<>]>({[]}{[]<>})}{<[[]{}](<>())
[{<<<{{((<{<<{[]()}<<>{}>>{((){}}{()()}}>}{[((()<>){<>})]({{()()}{(){}}}(<<>()>))}><[<{<{}><(
(((<<<<{((((<{<>[]}{<>()}>)(((<>{})(<><>))))))}><<{<(<<<[]{}><[]>><{[]()}{[]())>>{{<{}<>>}{{
{{[{<(({[[[<[[(){}]]><<[{}{}]({}())>{{[][]}[()()]}>]<{<[<>{}][<>{}]>[(()[])<()[]>]}[{<{}<>>({
{[{{[<[(((([{{{}{}}}({<>{}}[[][]])]){[<([]<>)([][])><{()<>}([]())>](<({}<>)<()>>(<()[]>{{}()}))
{{[(<<[<{<{[[<<><>>[()()]]]<(([]<>))<[[]{}]<[]>>>}>}>{{[<<<[()()]({}())>{<{}()>(<>[])}>([[(){}]<{}[]>]({(
[[[<<(<[{<[[<{<>[]}{{}[]}>]{({<>{}}[<>]]<({}{})[<><>]>}]((([{}{}][{}<>]))[({<>()}(<>{}))])
{{((<<[({<<<{[(){}]({}())}([<>{}]<(){}>)>([(()<>)<{}[]>]<<[]{}><<>{}>>)>[[<{<>}((){})>[{()[]}<{}<>>]](
((<<<<(<[{((<[[]{}](<><>)>{(()<>){()[]}}))}{<({(()())[(){}]}[[[]<>]<{}<>>])<([()[]])[{{}{}}{<><>}]>]}][<[{{
[[({<{{([([<{<<>()><()()>}>((<{}<>>{<>{}})[(()<>)[{}[]]])])[{{(([]())[<><>])({<>[]}(<>{}))}[[<[]><<>[]>]({[
[[(<(<[[(<{(({<>()}(<>[])){<<>[]>{()}}){({<>()}((){}))<<{}[]>[<><>]>}}{({<<>[]>[{}<>]})[[{(
({[<({<{<(<({([]<>){{}[]}}<({}{})[{}{}]>){{([]<>){(){}}}(<[]<>>{<><>})}><[[(<>())]{([]<>)}
{{[[[<{<(<{[(({}[])({}{}))<<()<>>>][<[{}{}]{()[]}>(<[]<>>{<><>})]}<{[<<>()>]<([]())<<>()>>}>>)
(({{{<(([[<(<((){})><[[]{}][{}()]>)<{[{}{}]}<(<>[])>>>]])({{{<[<()<>>{()<>}]>([<<>{}>(()())]<<<>{}>{[]}
{{[[[[({<{[{<[()<>]<<><>>>({<>()}<<>{}>)}(({[]<>}([]))<<<><>>[[]<>]>)]<(<<()()>([]<>>>{({}{}){()()}})[[[<><
[<<{[[([(<{[{{[]()}{[][]}}{{[]()}{(){}}}]{{[{}<>]([]<>)}(<{}()><<>()>)}}<[<{{}<>}<[]<>>><[[]{}]([]{})>][{({
[[[<<(({(<<((<{}<>><(){}>)<([]<>)(()[])>)[((<>())<(){}>){{(){}}{<>[]}}]><<({(){}}{{}<>})>{[<[]{}><[]{}>](<()
({({{<[<<<[{{<{}[]>[(){}]}{(<>[]){{}}}}]{[[{[][]}{[]<>}]{(())([]{})}](<({}{})(()())><{<>()}>)}>>>]([({
<[(((<{<{[<{{{[]<>}{<><>}}{([][])[<>()]}][[[()<>]<{}[]>](({}<>)<[]()>)]>][(<{{{}[]}((){})}{{<>{}}({}()
{<{[({<<(<[<([<>]<[]()>)<({}()){()[]}>>([{()[]}[{}{}]])]>(([{[[]<>][[]<>]}[[<>()]<<>()>]>(((()[]){<>{}}){
<(({<{[(<([(<{[]{}}{[]()}>){{(<><>){[][]}}[{{}()}<[][]>]}])>(<{{{[()<>][()<>]}({{}[]}[[]{}])}}(<{{[]{}
{<[<[{{<<<([[[{}[]]{<>[]}](<<>[]>[()()])][(([]<>)]])>([[<{()}{<><>}>[(<>[])<{}()>]]]{<{<[]{}>[[]
([{[[<<<<{<[({[]{}}(<>()))[<{}<>>[[]{}]]](([{}<>]){{[]()}[<>[]]})>[{(([][])[{}[]]){(<><>)(<>[])}}(<{()<>}
<<(([<{[((<[(<(){}>[<><>])[<<>[]><()())]]{<{()[]}(()<>)>}>)[<<{<(){}><{}()>}{[{}<>]<(){}>}>><[<{<>[]}{[][
(<<[<{<(<<({<([]{}){[][]}>{<[][]>{<>{}}}}[(([]())<<><>>){<{}><<>[]>}])(<{[<>[]]}>{<[{}<>}{<>{}}><{<><>}{()[
[[[[{<[{[<(<[(()())<{}[]>][(()())<()>]><{{()()}[<>{}]}[({}()><[]<>>]>)<{{[[]<>]<[][]>}{[<><>]
{{<(({{<{(<([<[][]>(()[])])<<{<><>}<[]<>>><(<>{})>>><{[[[]{}]{<>[]}](<<>{}>(<>[]))}[[<()<>><()<>>]<{()<
<[({<[[[(<{[(<{}()><(){}>)(<[][]><<>{}>)]<<{{}[]}<{}()>>[(<>())<<><>>]>>{<[([]{})[(){}]]{[(
[{<<<({<[[[<{{<>{}}<()<>>}{[[]()][(){}]}>{(({}[])<[]{}>){<()>(()[])}}]<{<({}<>)<{}[]>>[<{}{}><<><>
{<<[(<<<(<[<<{<><>}>({<>()}(()[]))>[([<><>][[]{}])(([]<>))]]>)>[({[<([[][]]({}))<((){}){[]<>}]>[[
([<{<(<<{({<{<(){}>({}<>)}}{<[{}()][()<>]>{<[]<>>{<>[]}}}}<({[{}{}](<>[])}(<[][]>[{}<>]))<
{([<<<<{[<<[[<{}{}><[][]>]<{{}()}[()[]]>]<[(()[]){<>[]}][[[]()][()<>>]>>(<[{<>()}(<><>)]{<<>{}>{
[[([(([[[<[((<()()>)([[]{}]<[]()>))]><{{[[[]{}]([]{})][(()<>)<{}<>>]}([{()<>}]{[<>()][{}[]]})}
<<{<[<<<({{(<<[]>([])>{<{}<>><<><>>}){<<()<>><()<>>><(<>[])<{}<>>}}}{([{[]<>}{<>{}}](<()()>[{}{}]))<{<[]>
[{{(([{[<{<{{<<><>><{}[]>}}{<(<>{}){[]}>[([]{})[[]{}]]}>(({[{}]<()[]>}))}><<[{(<{}[]><[][]>)
[[[<[<[{{[<[{([]())[()[]]}{<{}<>>[()[]]}]<<{[][]}<()[]>>(<{}<>>{[]{}})>>{<<<{}()>><([]<>)[<>()]>>{{(
{{{([{({[((((([][])[[]()])[(<><>)[()[]]])[[[<>[]]{{}<>}]<[{}[]]([][])>]){[[[[][]]<()<>>](<{}<>><{}{}>
<<<[({{(<((<<{{}()]<()>>(<(){}><<>{}>)>(<{<>()}<[][]>><{<><>}{[]()}>))[(<([][])[<><>]>(<()()>{{}
<[(([[(([[({[[[]()]{()()}](<<>{}>)}){<{{<>[]}{{}{}}}{<[]()>[{}{}]}][(<()[]>[<>[]])((<>{}))]}]{[<<<<>
({{[{<[{([[({[(){}]}[{[]{}}<(){}>])<<({})[[]()]>>]<(({(){}}<[]>)<[<>{}}(<>())>)>])}<<<<[[[[]<>][{}()]]
{{{[[([<{({{{<(){}><{}()>}([()()]<<>[]>)}<<[<>()]{{}<>}><<<><>>>>})([(<(()[])({}<>)>([{}<>](<>[]))){(<<>>
<([([[<{{({{[[<>[]]({}[])]}(<({}())><[<>{}]>)}{[(<{}[]>(<>[]))([[]{}]{[]})]({([][])(<>())})}
[({({{[{<{{(([{}]){<{}[]>([][])})({[[][]]<<>[]>}[<()<>><[]>])}<<<<{}{}>{[]()}>({[][]}[()()])>({([][])[<>{}]}[
({<{(<([<[{<{<<>[]>({}{}>}([()<>]<[]<>>)>({{(){}}<<><>>}[({}{})])}]><<[(<<<>{}>([]())>)[[<[]<>>(
<[{<{<<<({[([({}<>){()()}][<()()>(<><>)]){<{()[]}<<>[]>>{{{}()}[<>[]]}}](((<[]()>{<>()})(({}<>)([]{})))({(
<<{<[[[<[<[[({()()}({}[]))[<()()>[()<>]]]]>][{[<<({}<>)[[][]]>{{{}[]}<()[]>)>]<{{[()[]][[]()]}}{<[
<{<{({({[{<{[{()<>}]<<<><>><[]<>>>}[{<[]><(){}>}<{[]{}}(()<>)>]><{<{{}()}{(){}}>{<()<>>{[]()}}}((([]<>)<<>
{(({[([(((<<([()()]<<>[]>)[<<>()>(<>{})]>[<<<><>><()>>]>[((<()()>((){})))[[<()<>><()()>)({{}[]}
<[<[<{<[{[[([[()()]<{}<>>]){[[{}[]][<>()]]{[[]{}][()<>]}}]]<[{((<>())[[][]]>}([[()<>]<[][]>])](({[
((<<[[{<({[([{<><>}[<>{}]]){(([]{}){(){}})}](<({{}()}<()<>>)({[]()}[[][]))>{{{{}()}[[][]]}<(<>{}){<>[]}>}
<{{{[([({{[(<<[]<>>[{}<>]><<[]{}>(())>)<[[<>{}]<{}<>>]<{()}<{}{}>>>]}{{[<(<>{})<[]()>><[(){}]>][{([]())}[<
[{<[<(<<{({[[<[]<>><()()>]([()()]<<>{}>)]}{(<{[]()}([]<>)><{()[]}>){<<[]()><{}<>>>({()}<<>[]>)}})}{
[{(({[{[{(<[(<[]{}>(<><>))]<[{()}({}())]>><<[({}[]){<><>}](<[][]>[()[]])>[[([][])([]<>)](([]{}])]>)}]<[<[
<({[([(<(((({(<>())<{}[]>}[(<>[]){()[]}]))){[([([]{})(<>()]]([()()][{}<>]))<<{{}}(<>[])>{{()
((({{({<{<({[(<>[]){()()}]([{}[]][{}{}])})(<<{[]{}}>{<[]<>>{()[]}}>)><{{{{{}()}}{[{}[]]<<>[]>}
(<[<<[([[{<[<({}()){()}>(<(){}><<><>>)]>{{([()[]]<<>()>)(<[]<>>)}{[{<>[]}[<>()]](<<>()><()[]
((<<({<((<(<({<><>}({}<>))({{}{}}(<>()))>((([]()){(){}})[(()())(()())]>)>){{<([{<>()}(<><>)]<{<>()
(({(<[({({([<{[]()}<<>()>>{(()<>)[[]()]}]{{[()()]((){})}{[{}<>]{(){}}}})}<<<(<()()>[{}{}])<([]{}){{}[]
{({[[{([[[<((<(){}>{{}()})[(<>{})])([[<>[]]<()[]>][(()())<[]{}>]>>]((({[{}<>]<{}{}>})({<{}[]>}{(<>
[[(({<<{[(<<(([][]){{}<>}){[{}[]]({}[])}>(({<><>})<(()<>)[<>()]})>{({[[]{}]((){})}[([]())])})(({([[][]]
<[<{[<<<{[{(<[<>[]]>{{(){}}[[]()]})}[<{[{}{}]}><(<{}()]{{}{}}){({}[])}>]]}>[({{(<({}[])({}<>)>[{{}<>}])}{
"""
  
  var counter = [0,0,0,0]
  let brackets = [")" : ("(", 3 ),
                  "]" : ("[", 57 ),
                  "}" : ("{", 1197 ),
                  ">" : ("<", 25137 )]
  
  func syntaxScore(_ text: String) -> Int {
    //print("=======")
    var stack: [Character] = []
    for character in text {
      //enum Result { case ok, incomplete, corrupted(Int) }

      //print("CURRENT:", stack.map{String($0)}.joined(), "AND THEN NEXT CHARACTER:", character)

      switch character {
      case "(", "[", "{", "<": stack.append(character)
      case ")", "]", "}", ">":
        let (expectedOpening, errorScore) = brackets[String(character)]!
        guard let last = stack.last else {
          //Incomplete!!
          print("INCOMPLETE:", stack)
          return 0
        }
        guard String(last) == expectedOpening else {
//          print(text)
//          print("STACK", stack.map{String($0)}.joined())
//          print("CHARACTER", character, "LAST", last)
//          print("Exp", expectedOpening)
//          print(text)
//          print("Expected \(expectedOpening), but found \(character) instead.")
//          print("ERR", errorScore)
          return errorScore
        }
        stack.remove(at: stack.index(before: stack.endIndex))
      default: fatalError("Unrecognised character: \(character)")
      }
    }
    if stack.count > 0 {
      let complete = ["(": 1, "[":2, "{":3, "<":4]
      print("INCOMPLETE:", stack
              .reversed()
              .reduce(0) { $0 * 5 + complete[String($1)]! }
            )
    }
    return 0
  }
  
//  print(syntaxScore("[({(<(())[]>[[{[]{<()<>>"))
//  print(syntaxScore("[({(<(())[]>[[{[]{<()<>>"))
//
  print(syntaxScore("<{([{{}}[<[[[<>{}]]]>[]]"))
  fatalError()

  let base =
  input
    .lines
    .map{ String($0).trimmingCharacters(in: .whitespaces) } // Trim whitespace
    .map{ syntaxScore($0) }
    .reduce(0, +)
    
  print("Day9")
  print(base)
//  print(parta)
  
  let partb = base
//  print(partb)
}
