# Narrow Art Gallery

Dynamic Programming  
[The Problem](https://open.kattis.com/problems/narrowartgallery)

## <!-- omit in toc -->Contents

- [Spotting a DP problem in the wild](#spotting-a-dp-problem-in-the-wild)
- [How many rooms should we close?](#how-many-rooms-should-we-close)
- [Choosing the room to close](#choosing-the-room-to-close)
- [Defining the relationship between rows](#defining-the-relationship-between-rows)
- [Pseudocode](#pseudocode)
- [Improvements](#improvements)

## Spotting a DP problem in the wild

There are a few tell-tale clues that hint at a DP solution in this problem.

1. Limits are pretty small (_N, k_ ≤ 200)
2. Few possible states

By few possible states, I mean that if we want to solve the problem for row _n + 1_, assuming we know the solution for row _n_, there are only a few parameters we care about. To find the maximum value of all the rooms in the museum up to row _n + 1_ after closing some of them, we need:

1. Maximum value of the rooms up to row _n_
2. Whether a room on row _n_ is closed
3. The number of closed rooms up to row _n_

## How many rooms should we close?

Suppose we want to find the maximum value up to row 2. The first question you might have is, how many rooms should we close? We really want the maximum value up to row _N_ (the entire museum) after closing _k_ rooms, so who knows how many rooms we should close before row 2 and how many we should close afterwards.

We need to find the answer to all possibilities, i.e. the maximum value up to row 2 after closing 0 rooms, 1 room, … , _k_ rooms. To accomplish this, we'll need to store our state in an array _A_ of length _k + 1_ where `A[c]` is the maximum value up to the row we're on, after closing _c_ rooms.

## Choosing the room to close

How does the state of row 1 determine the state of row 2? Let's come up with the options we can take.

1. Keep both rooms on row 2 open.
2. Close the left room, if right room on row 1 is open
3. Close the right room, if left room on row 1 is open

Notice that we have another parameter to add to our state: which side of a row is closed. Once again, we can't tell whether closing the left or right room is better so we can keep track of both. Let's duplicate our state array into _L_ and _R_ for left and right.

`L[c]` is the same as `A[c]`, except with the left room on our current row open. `R[c]` is the opposite of `L[c]` Note that `L[c]` and `R[c]` might be the same if the best strategy is to leave both rooms on our row open (or there's a coincidence).

## Defining the relationship between rows

Given the state of row _i_, how do we calculate the state of row _i + 1_? Let's focus on just the _L_ array for now. Let's also define `L[i][c]` as the state `L[c]` on row _i_, _a_ as the value of the left room on row _i + 1_, and _b_ as the value of the right room on row _i + 1_.

**Keep both rooms open:** `L[i+1][c] = max(L[i][c], R[i][c]) + a + b`

Since there's no risk of blocking the museum, we are free to consider row _i_ with either of the left or right room open and pick the best option. We add the value of both rooms on row _i + 1_,

**Close the right room:** `L[i+1][c+1] = L[i][c] + a`

We can only close the right room on row _i + 1_ if the left room on row _i_ was open. This increments the number of rooms we've closed to _c + 1_ and we only add the value of the left room on row _i + 1_.

We can simply reverse left and right to get the state of _R_ due to symmetry.

## Pseudocode

To reduce repeating code, let's write a function to compute the next state of either _L_ or _R_. There are many ways to do this, eg. create another array to contain both with `A[0] = L` and `A[1] = R`. If you're on one side, XOR against 1 to flip to the other side (`A[0^1] = A[1]` and `A[1^1] = A[0]`).

For clarity, I'm not going to do that. Below, `A = L` and `B = R`, or the other way around. Since some states of _A, B_ are inaccessible (we can't close 10 rooms on row 1), negative infinity will indicate no value (negative infinity plus anything is still negative infinity).

```coffee
# A[i][c] = maximum value up to row i after closing c rooms
# i       = we're solving for row i+1
# a, b    = room values in row i+1 on side A and B
function solve_next_row(A, B, i, a, b)
    # solve for all c
    for c = 1 upto A[i].length
        open_both_from_A  = A[i][c] + a + b
        open_both_from_B  = B[i][c] + a + b
        open_one          = A[i][c-1] + a

        A[i+1] = max(open_both_from_A, open_both_from_B, open_one)

    # A[i][0] = sum of all rooms up to row i
    A[i+1][0] = A[i][0] + a + b
```

We just need to solve for row _1_ up to row _N_, then our answer will be stored in the state array.

```coffee
# N       = number of rows
# k       = rooms to close

# L[i][c] = maximum value of rooms up to row i after closing c rooms
#           (left room open)
# R[i][c] = maximum value of rooms up to row i after closing c rooms
#           (right room open)

# row 0 with no rooms closed = value of 0
L[0][0] = 0
R[0][0] = 0

# solve for rows 1 to N
for i = 0 upto N - 1
    # left_val, right_val = value of rooms on row i + 1
    solve_next_row(L, R, i, left_val, right_val)
    solve_next_row(R, L, i, right_val, left_val)

# maximum value up to row N after closing k rooms
# with either the left or right room open
return max(L[N][k], R[N][k])
```

## Improvements

1. The space-complexity of the above solution is Θ(_Nk_). Try an implementation that uses Θ(_k_) space (notice we only care about the last row we touched)
2. There are an awful lot of variables floating around. We can use a single 3D array or two 2D arrays, and a double for loop to solve the problem (see how XOR can help above)
