lat = 30.0
lon = -75.0

endLAT = 35.0
endLON = -90.0

diffLAT = endLAT - lat
diffLON = endLON - lon

slope = diffLAT / diffLON

if slope > 1:
    slopeLON = 1
    slopeLAT = 1 / slope

else:
    slopeLAT = 1
    slopeLON = 1 / slope

perp_slope_left = (slopeLON, -slopeLON)
perp_slope_right = (-slopeLON, slopeLAT)

corridor_lat = get_pathagory_for_corridor_to_the_left(?, ?)  # a2 + b2 / c2?
corridor_lon = get_pathagory_for_corridor_to_the_right(?, ?)  # a2 + b2 / c2?

step_lat = lat  # begininng
step_lon = lon
print(step_lat, step_lon)  # print
for each in range(1, 10):
    step_lat += slopeLAT    # add the slope
    step_lon += slopeLON    # add the slope
    print(step_lat, step_lon)


# div_diff_lat = diffLAT / 10
# div_diff_lon = diffLON / 10
