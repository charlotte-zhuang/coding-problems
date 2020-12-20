# Spiderman’s Workout

Dynamic Programming  
[The Problem](https://open.kattis.com/problems/spiderman)

## <!-- omit in toc -->Contents

- [Overview](#overview)
- [Building the array](#building-the-array)
  - [Sample Input](#sample-input)
  - [Min-Heights Array](#min-heights-array)
  - [Steps to build the array](#steps-to-build-the-array)
  - [Min-Heights Array Pseudocode](#min-heights-array-pseudocode)
- [Constructing the optimal path](#constructing-the-optimal-path)
  - [Steps to find the path](#steps-to-find-the-path)
  - [Find Path Pseudocode](#find-path-pseudocode)

## Overview

We’ll use a 2D array to store the minimum building heights for each climb at all possible heights.

- Rows represent how many climbs Spiderman has done so far
- Columns represent how high Spiderman is after finishing the climb

```ruby
max_sum = 1000  # from problem
num_climb
climb_arr[]     # climb distances in the range [1..num_climb]

min_heights[][]
# row = climb index we are up to in the range [0..num_climb + 1]
# col = height in the range [0..max_sum + 1]
# min_heights[row][col] = minimum height to get to that climb at that height
```

---

## Building the array

### Sample Input

```ruby
4
20 20 20 20
```

> 4 climbs; all height 20

### Min-Heights Array

| height: | 0   | …   | 20  | …   | 40  | …   | 60  | …   | 80  | …   |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| climb 0 | 0   | --  | --  | --  | --  | --  | --  | --  | --  | --  |
| climb 1 | --  | --  | 20  | --  | --  | --  | --  | --  | --  | --  |
| climb 2 | 20  | --  | --  | --  | 40  | --  | --  | --  | --  | --  |
| climb 3 | --  | --  | 20  | --  | --  | --  | 60  | --  | --  | --  |
| climb 4 | 20  | --  | --  | --  | 40  | --  | --  | --  | 80  | --  |

### Steps to build the array

0. **Spiderman starts at (0,0) = 0**
   - _(0,0)_  
     After doing no climbing, Spiderman ends at height 0 and the maximum building height (MBH) to get there was 0. ez workout
1. **(1,20) = 20**
   - _(1,20)_  
     After climbing from (0,0), Spiderman has to go up to height 20 since he can’t go below ground. The MBH is his current height.
2. **(2, 0) = 20 & (2,40) = 40**  
   After climbing from (1,20), Spiderman can either go down or up.
   - _(2,0)_  
     If he goes down, he will end up at height 20 - 20 = 0, but the MBH is still 20.
   - _(2,40)_  
     If he goes up, he will end up at height 20 + 20 = 40, and the MBH becomes his current height.
3. **(3, 20) = 20 & (3,20) = 40 & (3,60) = 60**  
   This is where the dynamic programming kicks in.
   - _(3,20)_
     1. Climb up from (2,0), keeping an MBH of 20.
     2. Climb down from (2,40), keeping an MBH of 40.
     3. Keep the lower MBH of 20.
   - _(3,60)_
     - Climb up from (2,40), increasing MBH to 60.
     - This might lead to the optimal path later on (but not in this example).
4. **(4,0) = 20 & (4,40) = 40 & (4,40) = 60 & (4,80) = 80**  
   From row 3, Spiderman can climb up or down from both heights.
   - _(4,0)_  
     Climb down from (3,20), keeping an MBH of 20
   - _(4,40)_
     1. Climb up from (3,20), increasing MBH to 40.
     2. Climb down from (3,60), with the same MBH of 60.
     3. Keep the lower MBH of 40.
   - _(4,80)_  
     Climb up from (3,60), increasing MBH to 80.

### Min-Heights Array Pseudocode

```ruby
# find min_heights
Fill min_heights with max_sum   # max_sum means unreachable
min_heights[0][0] = 0           # start on the ground

for row in 1..num_climb
    for col in 0..max_sum
        from_row = row - 1
        # try climbing down
        from_col = col + climb_arr[row]
        down_height = min_heights[from_row][from_col]
        # try climbing up (may increase height)
        from_col = col - climb_arr[row]
        up_height = max(min_heights[from_row][from_col], col)
        # keep minimum height
        min_heights[row][col] = min(down_height, up_height)
```

---

## Constructing the optimal path

### <!-- omit in toc -->Min-Heights Array (copied from before)

| height: | 0   | …   | 20  | …   | 40  | …   | 60  | …   | 80  | …   |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| climb 0 | 0   | --  | --  | --  | --  | --  | --  | --  | --  | --  |
| climb 1 | --  | --  | 20  | --  | --  | --  | --  | --  | --  | --  |
| climb 2 | 20  | --  | --  | --  | 40  | --  | --  | --  | --  | --  |
| climb 3 | --  | --  | 20  | --  | --  | --  | 60  | --  | --  | --  |
| climb 4 | 20  | --  | --  | --  | 40  | --  | --  | --  | 80  | --  |

### Steps to find the path

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

### Find Path Pseudocode

```ruby
if min_heights[num_climb][0] == max_sum
    return "IMPOSSIBLE"     # didn't reached the ground
seq         # climb sequence (a deque or dynamic string would work)
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
