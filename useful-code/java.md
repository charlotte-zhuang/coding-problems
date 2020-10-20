# Java

These are blocks of code that can be useful for doing coding problems. They might be used as-is, or altered to suite a specific problem.

Future me here: I had no idea that my notes were basically a shitty site-map of GeeksforGeeks xd. But I compiled and formatted everything already, and I feel like there’s _some_ value added by curating this list and making the code more suitable for competitive programming. So here it is.

## Contents

- [Java](#java)
  - [Contents](#contents)
  - [Fast I/O](#fast-io)
    - [Fast Writing](#fast-writing)
    - [Fast Reading](#fast-reading)
  - [Factoring](#factoring)
    - [Greatest Common Divisor](#greatest-common-divisor)
    - [Prime Factorization](#prime-factorization)
    - [Check if a number is prime](#check-if-a-number-is-prime)
  - [Sorting](#sorting)
    - [Merge Sort](#merge-sort)
  - [Disjoint Sets Data Structure](#disjoint-sets-data-structure)
  - [Trie Data Structure](#trie-data-structure)

## Fast I/O

### Fast Writing

```java
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
// Writing
bw.write("output string");
bw.newLine();
// Print
bw.flush();
```

### Fast Reading

I don’t remember where I got this from, but it’s similar to [Rishabh Mahrsee’s code](https://www.geeksforgeeks.org/fast-io-in-java-in-competitive-programming/)

```java
static class Reader
{
    static BufferedInputStream bi BufferedInputStream bi = new BufferedInputStream(System.in);

    // scans for the next int
    // ignores signs immediately after a digit
    // returns 0 at the end of the file
    static int scanInt()
    {
        try
        {
            int input = bi.read();
            int output = 0;
            int sign = 1;

            // keep reading until a number or sign is reached
            while (!((input >= '0' && input <= '9') || input == '-' || input == -1))
                input = bi.read();
            if (input == -1) // EOF
                return 0;

            // read the number
            if (input == '-')
            {
                sign = -1;
                input = bi.read();
            }
            while (input >= '0' && input <= '9')
            {
                output *= 10;
                output += input - '0';
                input = bi.read();
            }
            return output * sign;
        } catch (IOException e)
        {
            return 0;
        }
    }
}
```

[back to top](#java)

## Factoring

### Greatest Common Divisor

[Program to find GCD or HCF of two numbers - GeeksforGeeks](https://www.geeksforgeeks.org/c-program-find-gcd-hcf-two-numbers/)

### Prime Factorization

Returns a two-dimensional array with the number’s prime factors and their powers in increasing order. Unused part of the array is left as zeros.  
`[[factor, power], [factor, power], ..]`  
The size of the array is log_e(n) + 1 out of convenience. For large numbers, a dynamic array will perform much better.  
[source](https://www.geeksforgeeks.org/print-all-prime-factors-of-a-given-number/)

```java
static int[][] primeFactors(int num)
{
    if (num <= 1)
    {
        return new int[][]{{num, 1}};
    }

    int[][] factors = new int[(int) Math.log(num) + 1][2];
    int index = 0;

    // Add the number of 2s that divide num
    if (num % 2 == 0)
    {
        int power = 0;
        while (num % 2 == 0)
        {
            power++;
            num /= 2;
        }
        factors[index][0] = 2;
        factors[index][1] = power;
        index++;
    }
    // num must be odd
    for (int pf = 3; pf <= Math.sqrt(num); pf += 2)
    {
        // while pf divides num, increment power and divide num
        if (num % pf == 0)
        {
            int power = 0;
            while (num % pf == 0)
            {
                power++;
                num /= pf;
            }
            factors[index][0] = pf;
            factors[index][1] = power;
            index++;
        }
    }
    // if num is a prime number greater than 2
    if (num > 2)
    {
        factors[index][0] = num;
        factors[index][1] = 1;
    }

    return factors;
}
```

### Check if a number is prime

[Prime Numbers - GeeksforGeeks](https://www.geeksforgeeks.org/prime-numbers/)

[back to top](#java)

## Sorting

Using `Arrays.sort(arr)` is a very good comparison-based sort, but sometimes you need to do it yourself. Also, linear-time sorts.

### Merge Sort

Based off of code written by Rajat Mishra.  
[source](https://www.geeksforgeeks.org/merge-sort/)

```java
static class MergeSort
{
    static int[] tempArr;  // for copying integers in merge

    static void sort(int[] arr)
    {
        tempArr = new int[arr.length];
        driver(arr, 0, arr.length - 1);
    }

    // sort arr from [lIndex .. rIndex] inclusive
    static void driver(int[] arr, int lIndex, int rIndex)
    {
        if (lIndex < rIndex)
        {
            // Find the middle point
            int mIndex = (lIndex + rIndex) / 2;
            // Sort first and second halves
            driver(arr, lIndex, mIndex);
            driver(arr, mIndex + 1, rIndex);
            // Merge the sorted halves
            merge(arr, lIndex, mIndex, rIndex);
        }
    }

    // Merges the two sub-arrays of arr[].
    // First sub-array is arr[lIndex..mIndex]
    // Second sub-array is arr[mIndex+1..rIndex]
    // indices are inclusive
    static void merge(int[] arr, int lIndex, int mIndex, int rIndex)
    {
        int leftI = lIndex;
        int rightI = mIndex + 1;
        int mergeI = lIndex;

        // copy left array from arr to tempArr
        if (mIndex - lIndex >= 0)
            System.arraycopy(arr, lIndex, tempArr, lIndex, mIndex - lIndex + 1);
        // merge sub-arrays
        while (leftI <= mIndex && rightI <= rIndex)
        {
            if (tempArr[leftI] <= arr[rightI])
            {
                arr[mergeI] = tempArr[leftI];
                leftI++;
            }
            else
            {
                arr[mergeI] = arr[rightI];
                rightI++;
            }
            mergeI++;
        }
        // copy remaining elements from left array in tempArr
        if (mIndex - leftI >= 0)
            System.arraycopy(tempArr, leftI, arr, mergeI, mIndex - leftI + 1);
    }
}
```

[back to top](#java)

## Disjoint Sets Data Structure

A `DSet` represents a disjoint set.  
`DsStruct.find(DSet a)` will return the representative of `a`.  
`DsStruct.union(DSet a, DSet b)` will union the two sets (making them have the same representative).  
I made this myself, but of course there's an amazing article for everything on [GeeksforGeeks](https://www.geeksforgeeks.org/disjoint-set-data-structures/).

```java
static class DSet
    {
        DSet parent;
        int rank;

        DSet()
        {
            this.parent = this;
            this.rank = 0;
        }
    }

static class DsStruct
{
    static DSet find(DSet a)
    {
        if (a != a.parent)
            a.parent = find(a.parent);
        return a.parent;
    }

    static void union(DSet a, DSet b)
    {
        a = find(a);
        b = find(b);

        if (a != b)
        {
            if (a.rank > b.rank)
                b.parent = a;
            else
            {
                a.parent = b;
                if (a.rank == b.rank)
                    b.rank++;
            }
        }
    }
}
```

[back to top](#java)

## Trie Data Structure

[source](https://www.geeksforgeeks.org/trie-insert-and-search/)

```java
public class Trie
{
    static final int ALPHABET_SIZE = 26;
    static Node root;

    // Inserts the pattern into this Trie
    static void insert(String pattern)
    {
        Node crawl = root;

        for (int c = 0; c < pattern.length(); c++)
        {
            int child = pattern.charAt(c) - 'a';
            if (crawl.children[child] == null)
                crawl.children[child] = new Node();
            crawl = crawl.children[child];
        }
        // crawl is the last char in pattern
        crawl.isEndNode = true;
    }

    // Returns true if the pattern was found
    static boolean search(String pattern)
    {
        Node crawl = root;

        for (int c = 0; c < pattern.length(); c++)
        {
            int child = pattern.charAt(c) - 'a';
            if (crawl.children[child] == null)
                return false;
            crawl = crawl.children[child];
        }

        return (crawl != null && crawl.isEndNode);
    }

    static class Node
    {
        Node[] children;
        boolean isEndNode;

        Node()
        {
            children = new Node[ALPHABET_SIZE];
            isEndNode = false;
        }
    }
}
```

[back to top](#java)
