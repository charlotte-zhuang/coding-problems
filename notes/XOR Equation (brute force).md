# XOR Equation (brute force)
[XOR Equation](https://open.kattis.com/problems/xorequation)  

## Why brute force works
Notice the 7 second CPU time limit, which is _very_ long! There are also at most 10 ‘?’ characters split among 3 numbers. We can save exponential time by only using brute force on the numbers with the fewest ‘?’ characters.
The worst-case input-size is with 3 ‘?’ characters in each input, with a runtime of 10^2n = O(2^n). We won’t even need 7 seconds!
- - - -
## Overview
1. Sort inputs by the number of ‘?’ characters
2. Make a list of all possible integers for the first two inputs
3. XOR each integer from one list to all integers in the other list
	* We can do this because XOR is its own inverse
	* x ^ y = z -> y ^ z = x
4. Count the number of pairs that match the third input
```ruby
str_nums[]	# string input
num0_perms
num1_perms
count = 0

# get permutations
Sort str_nums by '?'
num0_perms = getPerms(str_nums[0])
num1_perms = getPerms(str_nums[1])
# count the number of valid permutation pairs
for each num0 in num0_perms
	for each num1 in num1_perms
		num2 = num0 ^ num1
		if (isMatch(num2, str_nums[2])
			count += 1
return count
```
- - - -
## Finding Permutations
1. Convert the input string into an integer
2. Whenever you hit a ‘?’ character, any digit [0..9] can be a possible permutation for this number
	1. Loop through each digit
	2. Recursively find permutations as if the ‘?’ character were replaced by the digit
	3. After you do the recursion, you can return your list
3. When you reach the end of the input string, you’ve found a permutation. Add it to your list and return.
```ruby
perm_list	# list of integer permutations of str_num
str_num	# string input
dec_num	# integer permutation

for each c in str_num
	if (c != '?')	# keep filling dec_num
		dec_num = dec_num * 10 + c
	else			# branch for each digit 0..9
		dec_num *= 10
		for d in 0..9
			Recurse on next c with dec_num + d
		# recursion puts answers in perm_list for us
		return perm_list
# base case: filled in all '?' chars with a digit
perm_list.add(dec_num)
return perm_list
```
- - - -
## Checking if an integer matches the input
1. Check each digit from the integer against each character from the input
2. The ‘?’ characters from the input can match with anything
### Edge Cases
* No leading zeros
* If the number is 0, that’s not a leading zero
* The integer should have the same number of digits as the input
- - - -

## Notes
* Using arrays to store permutations is much faster than using lists
* You can use your standard library’s sorting function
Add an argument to compare using the number of ‘?’ characters
	* [Java](https://docs.oracle.com/en/java/javase/12/docs/api/java.base/java/util/Arrays.html#sort%28T%5B%5D,java.util.Comparator%29)
	`Arrays.sort(T[] a, Comparator<? super T> c)`
	* [Python](https://docs.python.org/3/howto/sorting.html#key-functions)
	`sorted(iterable,key)`
	`list.sort(key)`
	* [C++](https://devdocs.io/cpp/algorithm/sort) 
	`std::sort`
	`template< class RandomIt, class Compare >`
	`void sort( RandomIt first, RandomIt last, Compare comp )`

_by charlotte & mei_