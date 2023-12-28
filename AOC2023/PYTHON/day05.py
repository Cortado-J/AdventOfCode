import sys
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
sections = text.split('\n\n')
def intify(ls):
    return [int(item.strip()) for item in ls if item != '']

#  Part A
seeds = intify(sections[0].split(":")[1].strip().split(" "))
sections = sections[1:]
maps = [[intify(line.split(" ")) for line in section.split('\n')[1:]] for section in sections]

lowest_location = sys.maxsize
for seed in seeds:
    print("seed=",seed)
    working = seed
    for map in maps:
        print("  map is:", map)
        mapped = working # in case no mapping found
        for map_range in map:
            if working in range(map_range[1], map_range[1] + map_range[2]):
                mapped = working - map_range[1] + map_range[0]
                print("    ", working, "mapped to", mapped)
        working = mapped
        print("       ->",working)
    lowest_location = min(lowest_location, working)

print(lowest_location)

#  Part B
seed_ranges_prep = [seeds[i:i + 2] for i in range(0, len(seeds), 2)]
seed_ranges = [[sr[0], sr[0]+sr[1]] for sr in seed_ranges_prep]
# print(seeds)
# print(seed_ranges)
lowest_location_b = sys.maxsize

def combine(wrange, mrange): # working range and map range
    # Returns (overlap, nonoverlap) where:
    #  overlap    is an array of sections of the wrange which        overlap with mrange and can have 0, 1 element
    #  nonoverlap is an array of sections of the wrange which do not overlap with mrange and can have 0, 1 or 2 elements
    wrsta = wrange[0]
    wrend = wrange[1]
    
    mrsta = mrange[1]
    mrend = mrange[1]+mrange[2]

    mroffset = mrange[0]-mrange[1]

    if wrsta >= mrend or wrend <= mrsta:
        # print("          no overlap")        
        # print("          We need to include the whole range with no movement:", [wrsta, wrend])
        overlap = []
        nonoverlap = [[wrsta, wrend]]
    else:
        # Overlap so:
        nonoverlap = []
        if mrsta > wrsta:
            # We need to include the first part of the working_range as a posible destination:
            # print("          We need to include the first part of the working_range as a posible destination:",[wrsta, mrsta])
            nonoverlap.append([wrsta, mrsta])
            # gather.append([wrsta, min(mrsta,wrend)])
            # print("          gather now...", gather)
        if mrend < wrend:
            # We need to include the last part of the working_range as a posible destination:
            # print("          We need to include the last part of the working_range as a posible destination:", [mrend, wrend])
            nonoverlap.append([mrend, wrend])
            # gather.append([max(mrend, wrsta), wrend])
            # print("          gather now...", gather)
        # In any case any overlap needs mapping by mroffset:
        # print("          Overlap needs mapping:", [max(wrsta, mrsta)+mroffset, min(wrend, mrend)+mroffset])
        overlap = [[max(wrsta, mrsta)+mroffset, min(wrend, mrend)+mroffset]]
        # print("          gather now...", gather)
    # print("          overlap = ", overlap, "nonoverlap = ", nonoverlap)
    return (overlap, nonoverlap)

to_ranges = seed_ranges
for map in maps:
    # print("= = = = = = = = = = = = = = = = = = = = = =")
    # print("    map is:", map)
    from_ranges = to_ranges
    to_ranges = []
    for map_range in map:
        # print("      map_range is:", map_range)
        nonoverlaps = []
        for from_range in from_ranges:
            (overlap, nonoverlap) = combine(from_range, map_range)
            to_ranges = to_ranges + overlap # Add any mapped bits to the list of destinations
            nonoverlaps = nonoverlaps + nonoverlap # And gather any remaining that didn't overlap
        # So now the nonoverlaps become the from_ramges for the next map_range:
        from_ranges = nonoverlaps
    # And now all mappings have been done which means any from_ranges left at this point
    #   have been untouched by any of the maps so they drop through
    #   and so are added to the to_ranges:
    to_ranges = to_ranges + from_ranges

#  The lowest location is the lowest start of all the to_ranges
lowest_location_b = min([pair[0] for pair in to_ranges])
print(lowest_location_b)
