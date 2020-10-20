# Spiderman’s Workout

Dynamic Programming  
[The Problem](https://open.kattis.com/problems/spiderman)

<!-- omit in toc -->
## Contents

- [Overview](#overview)
- [Building the array](#building-the-array)
- [Constructing the optimal path](#constructing-the-optimal-path)

## Overview

We’ll use a 2D array to store the minimum building heights for each climb at all possible heights.

- Rows represent how many climbs Spiderman has done so far
- Columns represent how high Spiderman is after finishing the climb
  Below are blocks of pseudo-code preceded by their explanations. The explanations are using the input `20 20 20 20`, which means 4 climbs each with a distance of 20.

```ruby
max_sum = 1000  # from problem
num_climb
climb_arr[]     # climb distances (starting index 1)

min_heights[num_climb + 1][max_sum + 1]
# row = climb index we are up to
# col = height
# min_heights[row][col] = minimum height to get to that climb at that height
```

---

## Building the array

1. **Spiderman starts at (0,0) = 0**  
   After doing no climbing, Spiderman ends at height 0 and the maximum building height (MBH) to get there was 0. ez workout
2. **(1,20) = 20**  
   After climbing from (0,0), Spiderman has to go up to height 20 since he can’t go below ground. The MBH is his current height.
3. **(2, 0) = 20 & (2,40) = 40**  
   After climbing from (1,20), Spiderman can either go down or up. If he goes down, he will end up at height 20 - 20 = 0, but the MBH is still 20. If he goes up, he will end up at height 20 + 20 = 40, and the MBH becomes his current height.
4. **(3, 20) = 20 & (3,20) = 40 & (3,60) = 60**  
   This is where the dynamic programming kicks in. If Spiderman came from (2,0), he can climb up to (3,20) with the same MBH of 20. If he came from (2,40) he can still climb down to (3,20), but his MBH of 40 carries over from before. So we’ll discard the greater MBH and save (3,20) = 20.
   From (2,40), Spiderman can also climb up to (3,60) with an MBH of 60. This might lead to the optimal path later on (but not in this example).
5. **(4,0) = 20 & (4,40) = 40 & (4,40) = 60 & (4,80) = 80**  
   The two options from row 3 are (3,20) = 20 and (3,60) = 60. From either height, Spiderman can climb up or down, leading to once again two ways to get to (4,40). We’ll save (4,0) = 20, (4,40) = 40, and (4,80) = 80 into our array.

```ruby
# find min_heights
Fill min_heights with max_sum   # max_sum means unreachable
min_heights[0][0] = 0           # start on the ground

for row in 1..num_climb
    for col in 0..max_sum
        from_row = row - 1
        # try climbing down
        from_col = col + climb_arr[col]
        down_height = min_heights[from_row][from_col]
        # try climbing up (may increase height)
        from_col = col + climb_arr[col]
        up_height = max(min_heights[from_row][from_col], col)
        # keep minimum height
        min_heights[row][col] = min(down_height, up_height)
```

---

## Constructing the optimal path

1. **Start from the end: (4,0)**  
   Spiderman has to end on the ground after the last climb, which is (4,0). If this value couldn’t be reached after constructing the array, then there’s no valid workout.
2. **From (4,0) go back to (3,20)**  
   Since climb 4 is at height 0, we must have climbed down from a height of 20 to get here.
3. **From (3,20) go back to (2,0) or (2,40)**  
   We could have climbed up from (2,0) or down from (2,40), so we’ll take the one with the lower MBH, which is (2,0) = 20.
4. **From (2,0) go back to (1,20)**  
   We had to have climbed down from row 1 to reach (2,0).
5. **From (1,20) go back to (0,0)**  
   We could have climbed up from (0,0) or down from (0,40) to reach (1,20). Since (1,20) was never reached in our array, the only option is (0,0), which is our start.
6. **Reverse the sequence to make it front-to-back**

```ruby
if min_heights[num_climb][0] == max_sum
    return "IMPOSSIBLE"     # didn't reached the ground
else
    seq         # climb sequence
    col = 0     # start on the ground
    for row in num_climb..1
        from_row = row - 1
        down_col = col + climb_arr[row]
        up_col = col - climb_arr[row]
        down_height = climb_arr[from_row][down_col]
        up_height = climb_arr[from_row][up_col]
        # add the better path to seq and update col
        if down_height < up_height
            seq.add('D')
            col = down_col
        else
            seq.add('U')
            col = up_col
    return seq.reverse()
```

_special thanks to kadin_  
[back to top](#spidermans-workout)
