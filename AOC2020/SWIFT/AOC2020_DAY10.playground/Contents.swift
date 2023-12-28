var input = """
104
83
142
123
87
48
102
159
122
69
127
151
147
64
152
90
117
132
63
109
27
47
7
52
59
11
161
12
148
155
129
10
135
17
153
96
3
93
82
55
34
65
89
126
19
72
20
38
103
146
14
105
53
77
120
39
46
24
139
95
140
33
21
84
56
1
32
31
28
4
73
128
49
18
62
81
66
121
54
160
158
138
94
43
2
114
111
110
78
13
99
108
141
40
25
154
26
35
88
76
145
"""

//input =
//"""
//16
//10
//15
//5
//1
//11
//7
//19
//6
//12
//4
//"""
//
//input =
//"""
//28
//33
//18
//42
//31
//14
//46
//20
//48
//47
//24
//23
//49
//45
//19
//38
//39
//11
//1
//32
//25
//35
//8
//17
//7
//9
//4
//2
//34
//10
//3
//"""

let lines = input.split(omittingEmptySubsequences: false) { $0 == "\n" || $0 == "\r\n" }.map(String.init)
let adapters = lines.map{ Int($0)! }
let socket = 0
let device = adapters.max()!+3
let all = adapters + [socket, device]
let allSorted = all.sorted()
func diffCount(diff: Int) -> Int {
  var count = 0
  for index in 0..<allSorted.count-1 {
    if allSorted[index+1]-allSorted[index] == diff {
      count += 1
    }
  }
  return count
}
print(diffCount(diff: 1) * diffCount(diff: 3))
print(allSorted)

var waysDone: [Int] = allSorted.map{_ in -1}

//Assume using is increasing
func ways(from: Int) -> Int {
  let done = waysDone[from]
  if done != -1 { return done }

  let a = allSorted
  let remaining = a.count - from - 1
  var count = 0
  if remaining == 0 {
    count = 1
  } else {
    let current = a[from]
    if remaining >= 1 && a[from+1]-current <= 3 { count += ways(from: from+1) }
    if remaining >= 2 && a[from+2]-current <= 3 { count += ways(from: from+2) }
    if remaining >= 3 && a[from+3]-current <= 3 { count += ways(from: from+3) }
  }
  waysDone[from] = count
  return count
}

print(ways(from: 0))
