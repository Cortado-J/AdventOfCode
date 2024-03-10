#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
rows = text.splitlines()
# print(rows)
P = []
smallest = 1000000000 * 1000000000 * 1000000000
resulta = None
for index, row in enumerate(rows):
    pva = row.split(" ")
    p=pva[0][3:-2].split(",")
    v=pva[1][3:-2].split(",")
    a=pva[2][3:-1].split(",")

    p=(int(p[0]),int(p[1]),int(p[2]))
    v=(int(v[0]),int(v[1]),int(v[2]))
    a=(int(a[0]),int(a[1]),int(a[2]))
    # print(p,v,a)
    P.append((p,v,a))
    long = abs(p[0])+abs(p[1])+abs(p[2]) + (abs(v[0])+abs(v[1])+abs(v[2])) * 1000000000 + (abs(a[0])+abs(a[1])+abs(a[2])) * 1000000000 * 1000000000
    if long < smallest:
        smallest = long
        resulta = index

print(f"Result A = {resulta}")

import math
collisions = [] # Array of (time, P1, P2)
# for x in P:
#     print(x)
# print("===========")
for index1 in range(len(P)):
    P1 = P[index1]
    (p1,v1,a1) = P1
    for index2 in range(index1+1, len(P)):
        P2 = P[index2]
        (p2,v2,a2) = P2
        # print(f"{index1}, ({p1[0]}, {v1[0]}, {a1[0]})     {index2}, ({p2[0]}, {v2[0]}, {a2[0]})")
        # Calculate x deltas
        pd = p1[0]-p2[0]; vd = v1[0]-v2[0]; ad = a1[0]-a2[0]
        T1 = None
        T2 = None
        if ad == 0: # No acceleration so we can just look at velocity and position:
            if vd == 0: # No velocity either so a fixed position
                if pd == 0: # Same two points (probably won;t happen but included for completness!)
                    T1 = 0
                    T2 = None
                else:
                    # No acceleration or velocity and positions are different
                    continue
            else:
                # No acceleration but some velocity so it's just a linear equation:
                T1 = -pd/vd # Just one solution
                T2 = None
        else:
            # Some acceleration so it's a quadratic
            # Tempting to thing the coefficients are: ad, vd, pd
            # But the discrete method of updating velocity and then distance (rather than something continuous)
            # means that instead teh coefficients are:
            A = ad/2
            B = vd + (ad/2)
            C = pd
            # Calculate "B squared minus 4 A C":
            under_root = B * B - 4 * A * C
            if under_root < 0:
                #  No solutions
                continue
            root = math.sqrt(under_root)
            T1 = (-B + root)/(2 * A)
            T2 = (-B - root)/(2 * A)
        KeepT1 = T1
        KeepT2 = T2
        if KeepT2 == -21.2:
            k = 4
        if not T1.is_integer() or T1 < 0:
            #  We're not interested in non-integer or negative solutions
            T1 = None
        if T2 != None:
            if not T2.is_integer() or T2 < 0:
                #  We're not interested in non-integer or negative solutions
                T2 = None
        if T1 == None and T2 == None:
            continue
        if T1 == T2:
            # If solutions are the same treat as one:
            T2 = None
        #  At least one of T1 and T2 is a possibility:
        if T1 == None:
            # Swap
            T1, T2  = T2, T1
        if T1 != None and T2 != None:
            # Both are possibilities
            if T2 < T1:
                # Swap
                T1, T2  = T2, T1
        # So we have:
        # EITHER: T1 = Only solution   , T2 = None
        # OR:     T1 = Earlier solution, T2 = Later

        # We've found one or two times when the two particles meet in x dimension so need to test y and z
        # Check for y and z colliding
        if p1[1] + (v1[1]+(a1[1]/2))*T1 + (a1[1]/2)*T1*T1 ==\
           p2[1] + (v2[1]+(a2[1]/2))*T1 + (a2[1]/2)*T1*T1\
            and\
           p1[2] + (v1[2]+(a1[2]/2))*T1 + (a1[2]/2)*T1*T1 ==\
           p2[2] + (v2[2]+(a2[2]/2))*T1 + (a2[2]/2)*T1*T1:
            # They meet in y and z dimension too:
            collision = (T1, P1, P2)
            # print(collision)
            collisions.append(collision)
        if T2 != None:
            # There's a second time when they meet in the x dimension:
            if p1[1] + (v1[1]+(a1[1]/2))*T2 + (a1[1]/2)*T2*T2 ==\
               p2[1] + (v2[1]+(a2[1]/2))*T2 + (a2[1]/2)*T2*T2\
               and\
               p1[2] + (v1[2]+(a1[2]/2))*T2 + (a1[2]/2)*T2*T2 ==\
               p2[2] + (v2[2]+(a2[2]/2))*T2 + (a2[2]/2)*T2*T2:
                # They meet in y and z dimension too:
                collision = (T2, P1, P2)
                # print(collision)
                collisions.append(collision)
# We have a list of collisions!
# But we need to handle them in time order, removing any collisions and particles as we go.
# So start by sorting:
collisions = sorted(collisions, key=lambda x: x[0])
number_of_collisions = len(collisions)
print(number_of_collisions)

# Make working be a set with all the points:
working = set()
for p in P:
    working.add(p)

# Now work through the collisions in order:
index = 0
while index < len(P):
    time_of_collision = collisions[index][0]
    # We need to remove all collisions at that time:
    eliminate = set()
    while index < len(P) and collisions[index][0] == time_of_collision:        
        P1 = collisions[index][1]
        P2 = collisions[index][2]
        # Check the two points have not been eliminated previously
        if P1 in working and P2 in working:
            # Both points present so we can eliminate them both:
            eliminate.add(P1)
            eliminate.add(P2)
        index += 1
    # Now we've processed all at that time so we can eliminate:
    working -= eliminate
    # And then loop to get the next collision time...

resultb = len(working)
print(f"Result B = {resultb}")
