# Increasing Subsequence

Dynamic Programming  
[The Problem](https://open.kattis.com/problems/increasingsubsequence)

## <!-- omit in toc -->Contents

- [The Approach](#the-approach)
- [Creating the Sequence](#creating-the-sequence)
- [The Lexicographical Requirement](#the-lexicographical-requirement)
- [Pseudocode](#pseudocode)

## The Approach

Notice the problem constraints are n ≤ 200, which means up to around an O(n^3) solution will pass. We'll target O(n^2) by solving the problem in linear time for each index.

For an index i, we want to know how many increasing subsequences there are from index i to n-1 starting from index i. The naive solution would be to consider each index j in `[i+1, n-1]` as the next element in the sequence, then consider each index k in `[j+1, n-1]`, and so on.

Notice that part of the longest subsequence from j to n-1 might be the same sequence as the one from k to n-1. Consider the example below.

array = `[0, 4, 2, 6]`  
longest sequence starting from index 0 = `[0, 2, 6]`  
longest sequence starting from index 2 = `[2, 6]`  

This should be a big hint to use dynamic programming. We can avoid doing repeated work by memoizing our results as we compute them.

Let `dp[i] = length of the longest increasing subsequence starting from index i`

Then, to find `dp[i]` we just have to find the index j in `[i+1, n-1]` where `dp[j]` is maximized. We also only consider indexes where `arr[i] < arr[j]` since the sequence must be increasing.

Effectively, we are building out suffixes of sequences that we can use from earlier indexes. Because `dp[i]` depends on indexes in `[i+1, n-1]`, we need to calculate the values of `dp` from back to front.

Lastly, since we can start the sequence from any index, the answer is the maximum value in the completed `dp` array.

[back to top](#increasing-subsequence)

## Creating the Sequence

The question also asks us to return the actual sequence of numbers, not just the length. The easiest way is to maintain a successor array where `successor[i] = next index in the sequence`.

We start off with `successor[i] = i` for all i in `[0, n-1]` since no element has a successor until we create a sequence longer than 1 using our dynamic programming approach. It's more convenient in the code to think of `successor[i] = i` as "no successor" than something like `successor[i] = -1`, but either can work.

Whenever we update `dp[i]`, also update `successor[i]` with whatever index j we found produced the longest increasing subsequence.

[back to top](#increasing-subsequence)

## The Lexicographical Requirement

Annoyingly, we have to return the lexicographically first sequence if there is a tie in length. To find that sequence, break ties between two equal length options by choosing the smaller element from the array.

If we had two equally long sequence suffixes to choose from in our DP step, we should choose the one that starts with the smaller number. The beginning of the subsequence will be the same no matter what suffix we choose, so we always break ties after whatever index we are currently calculating. For example:

array = `[0, 4, 2, 6]`, we are considering index 0  
`dp[1] = 2`, which represents the sequence `[4, 6]`  
`dp[2] = 2`, which represents the sequence `[2, 6]`  
Choose `dp[2]` since `[0, 2, 6]` comes before `[0, 4, 6]`

Notice, it doesn't matter what comes before index 0 when making this decision.

[back to top](#increasing-subsequence)

## Pseudocode

```ruby
arr[0..n-1] = input
dp[0..n-1] = 1  # start with length 1 sequences
successor[0..n-1] = [0..n-1]  # each index is its own successor

for i in n-1..0
  # calculating dp[i], the longest subsequence starting from index i
  for j in i+1..n-1
    is_increasing = arr[i] < arr[j]
    is_longer = dp[j] + 1 > dp[i]
    is_lexicographically_first = dp[j] + 1 == dp[i] and arr[j] < arr[successor[i]]

    if is_increasing and (is_longer or is_lexicographically_first)
      # use the sequence start from index j as the suffix to index i
      dp[i] = dp[j] + 1
      successor[i] = j

# find the start of the best sequence
best = 0
for i in 1..n-1
  is_longer = dp[i] > best
  is_lexicographically_first = dp[i] == best and arr[i] < arr[best]
  if is_longer or is_lexicographically_first
    best = i

# reconstruct the sequence
sequence = [best]
while successor[best] != best
  best = successor[best]
  sequence.push(best)

return sequence
```

[back to top](#increasing-subsequence)
