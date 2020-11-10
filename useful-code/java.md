# Java

These are blocks of code that can be useful for doing coding problems. They might be used as-is, or altered to suite a specific problem.

## <!-- omit in toc -->Contents

- [Fast I/O](#fast-io)
  - [Fast Writing](#fast-writing)
  - [Fast Reading](#fast-reading)
- [Factoring](#factoring)
  - [Greatest Common Divisor](#greatest-common-divisor)
  - [Prime Factorization](#prime-factorization)
  - [Check if a number is prime](#check-if-a-number-is-prime)
- [Sorting](#sorting)
  - [Merge Sort](#merge-sort)
  - [Quicksort (Lomuto Partition)](#quicksort-lomuto-partition)
  - [Quicksort (Hoare's Partition)](#quicksort-hoares-partition)
  - [Counting Sort](#counting-sort)
  - [Radix Sort (with Division)](#radix-sort-with-division)
  - [Radix Sort (with Bitwise Operations)](#radix-sort-with-bitwise-operations)
- [Selection](#selection)
  - [Quickselect (Lomuto Partition)](#quickselect-lomuto-partition)
  - [Quickselect (Hoare's Partition)](#quickselect-hoares-partition)
  - [Boyer-Moore Majority Vote](#boyer-moore-majority-vote)
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

Watch out for overflow on the scan double method.

```java
static class Reader {
  BufferedInputStream bi;

  Reader() {
    bi = new BufferedInputStream(System.in);
  }

  /**
   * Scans for an integer. Skips the character immediately after the number.
   *
   * @return The number.
   * @return 0 at end-of-file
   */
  int scanInt() {
    try {
      int input = bi.read();
      int output = 0;
      int sign = 1;
      // keep reading until a number or sign is reached
      while (!((input >= '0' && input <= '9') || input == '-' || input == -1)) {
        input = bi.read();
      }
      // EOF
      if (input == -1) {
        return 0;
      }
      // read the number
      if (input == '-') {
        sign = -1;
        input = bi.read();
      }
      while (input >= '0' && input <= '9') {
        output *= 10;
        output += input - '0';
        input = bi.read();
      }
      return output * sign;
    } catch (IOException ignored) {
      return 0;
    }
  }

  /**
   * Scans for a decimal number. Skips the character immediately after the number.
   *
   * @return The number.
   * @return 0 at end-of-file
   */
  double scanDouble() {
    try {
      int input = bi.read();
      int sign = 1;
      long output = 0;
      long decimal = 1;
      boolean foundDecimal = false;
      // keep reading until a number, sign, or decimal is reached
      while (!((input >= '0' && input <= '9') || input == '-' || input == '.' || input == -1)) {
        input = bi.read();
      }
      // EOF
      if (input == -1) {
        return 0;
      }
      // read the number
      if (input == '-') {
        sign = -1;
        input = bi.read();
      }
      while (input >= '0' && input <= '9' || input == '.') {
        if (input == '.') {
          foundDecimal = true;
        } else {
          if (foundDecimal) {
            decimal *= 10;
          }
          output *= 10;
          output += input - '0';
        }
        input = bi.read();
      }
      return (double) sign * output / decimal;
    } catch (IOException ignored) {
      return 0;
    }
  }

  /**
   * Scans for an unsigned binary number. Skips the character immediately after
   * the number.
   *
   * @return The number.
   * @return 0 at end-of-file.
   */
  int scanBinaryUnsigned() {
    try {
      int input = bi.read();
      int output = 0;
      // keep reading until a number is reached
      while (!(input == '0' || input == '1' || input == -1)) {
        input = bi.read();
      }
      // EOF
      if (input == -1) {
        return 0;
      }
      // read the number
      while (input == '0' || input == '1') {
        output <<= 1;
        output |= input - '0';
        input = bi.read();
      }
      return output;
    } catch (IOException ignored) {
      return 0;
    }
  }

  /**
   * Scans for a binary number in two's complement form. Skips the character
   * immediately after the number.
   *
   * @return The number.
   * @return 0 at end-of-file.
   */
  int scanBinarySigned() {
    try {
      int input = bi.read();
      int output = 0;
      // keep reading until a number is reached
      while (!(input == '0' || input == '1' || input == -1)) {
        input = bi.read();
      }
      // EOF
      if (input == -1) {
        return 0;
      }
      // sign extension
      if (input == '1') {
        output = ~output;
      }
      input = bi.read();
      // read the number
      while (input == '0' || input == '1') {
        output <<= 1;
        output |= input - '0';
        input = bi.read();
      }
      return output;
    } catch (IOException ignored) {
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

This method has a runtime of O(n^0.5), where n is the size of the factored number.  
It can greatly benefit from a fast prime check, to see if a number has any factors (see below).

```java
/**
 * Finds all prime factors of a number.
 *
 * @param num The number to prime factorize.
 * @return A list of factor, power pairs sorted by factor. {[factor, power],
 *         [factor, power], [factor, power],…}.
 */
static List<int[]> primeFactors(int num) {
  List<int[]> factors = new LinkedList<>();
  // Return numbers that are too small
  if (num <= 1) {
    factors.add(new int[] { num, 1 });
    return factors;
  }
  // Add the number of twos that divide num
  if ((num & 1) == 0) {
    int power = 0;
    do {
      power++;
      num >>>= 1;
    } while ((num & 1) == 0);
    factors.add(new int[] { 2, power });
  }
  // num must be odd
  for (int pf = 3; pf <= Math.sqrt(num); pf += 2) {
    // while pf divides num, increment power and divide num
    if (num % pf == 0) {
      int power = 0;
      do {
        power++;
        num /= pf;
      } while (num % pf == 0);
      factors.add(new int[] { pf, power });
    }
  }
  // if num is a prime number greater than 2
  if (num > 2) {
    factors.add(new int[] { num, 1 });
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

This code uses a top-down merge sort with a temporary array for copying elements and a check if elements are already sorted before merging.  
Performance can be improved by reusing the temporary array and by using insertion sort on small arrays, but the improvement is small.

```java
static class MergeSort {

  /**
   * Sorts an entire array using merge sort.
   *
   * @param arr The array to be sorted.
   */
  static void sort(int[] arr) {
    sort(arr, new int[arr.length], 0, arr.length);
  }

  /**
   * Sorts an array in a specific range using merge sort.
   *
   * @param arr        The array to be sorted.
   * @param temp       An array for copying elements.
   * @param leftBound  The lower bound.
   * @param rightBound The upper bound (not inclusive).
   */
  static void sort(int[] arr, int[] temp, int leftBound, int rightBound) {
    if (leftBound + 1 < rightBound) {
      int midIndex = (leftBound + rightBound) / 2;
      sort(arr, temp, leftBound, midIndex);
      sort(arr, temp, midIndex, rightBound);
      merge(arr, temp, leftBound, midIndex, rightBound);
    }
  }

  /**
   * Merges two adjacent sorted sub-arrays.
   *
   * @param arr        The array containing the sub-arrays
   * @param temp       An array for copying elements.
   * @param leftBound  The lower bound of the left-hand sub-array
   * @param midIndex   The mid point between the sub-arrays (part of the
   *                   right-hand sub-array)
   * @param rightBound The upper bound of the right-hand sub-array (not inclusive)
   */
  static void merge(int[] arr, int[] temp, int leftBound, int midIndex, int rightBound) {
    int lp = leftBound;
    int rp = midIndex;
    int mp = leftBound;
    // check if sub-arrays are already sorted
    if (arr[midIndex - 1] <= arr[midIndex]) {
      return;
    }
    // copy the left sub-array from arr to tempArr
    if (midIndex - leftBound > 0) {
      System.arraycopy(arr, leftBound, temp, leftBound, midIndex - leftBound);
    }
    // merge the sub-arrays
    while (lp < midIndex && rp < rightBound) {
      if (temp[lp] <= arr[rp]) {
        arr[mp] = temp[lp];
        lp++;
      } else {
        arr[mp] = arr[rp];
        rp++;
      }
      mp++;
    }
    // copy remaining elements from left array in tempArr
    if (midIndex - lp > 0) {
      System.arraycopy(temp, lp, arr, mp, midIndex - lp);
    }
  }
}
```

[back to top](#java)

### Quicksort (Lomuto Partition)

This code uses a single-pivot randomized Quicksort with three partitions done in a Lomuto scheme. The third partition contains elements equal to the pivot and grows from the right-hand side of the array.  
Performance can be improved by using insertion sort on small arrays, but the improvement is small. If implementing tail-call optimization, recurse on the smaller partition first.

```java
static class Quicksort {
  /**
   * Sorts an entire array using Quicksort.
   *
   * @param arr The array to be sorted.
   */
  static void sort(int[] arr) {
    sort(arr, 0, arr.length);
  }

  /**
   * Sorts an array in a specific range using Quicksort.
   *
   * @param arr        The array to be sorted.
   * @param leftBound  The lower bound.
   * @param rightBound The upper bound (not inclusive).
   */
  static void sort(int[] arr, int leftBound, int rightBound) {
    if (leftBound + 1 < rightBound) {
      int[] pivots = partition(arr, leftBound, rightBound);
      sort(arr, leftBound, pivots[0]);
      sort(arr, pivots[1], rightBound);
    }
  }

  /**
   * Partitions an array around a random pivot into 3 partitions.
   *
   * @param arr        The array to be sorted.
   * @param leftBound  The lower bound.
   * @param rightBound The upper bound (not inclusive).
   * @return The range of the pivot elements: [start, end] (not including end)
   */
  static int[] partition(int[] arr, int leftBound, int rightBound) {
    int range = rightBound - leftBound;
    int rand = leftBound + (int) (Math.random() * range);
    int pivot = arr[rand];
    int pp = rightBound - 1;
    int lp = leftBound;
    int rp = leftBound;
    // move the pivot to the end of the array
    swap(arr, rand, pp);
    // swap elements that are less than the pivot from the right partition to the
    // left partition
    // swap elements that are equal to the pivot to the end of the array
    for (; rp < pp; rp++) {
      if (arr[rp] < pivot) {
        swap(arr, lp, rp);
        lp++;
      } else if (arr[rp] == pivot) {
        pp--;
        swap(arr, rp, pp);
        rp--;
      }
    }
    // move the elements that are equal to the pivot to the middle of the array
    int pivotCount = rightBound - pp;
    int midSize = Math.min(pivotCount, pp - lp);
    System.arraycopy(arr, lp, arr, rightBound - midSize, midSize);
    Arrays.fill(arr, lp, lp + midSize, pivot);
    return new int[] { lp, lp + pivotCount };
  }

  /**
  * Swaps a pair of elements in an array.
  *
  * @param arr The array.
  * @param a   The index of the first element.
  * @param b   The index of the second element.
  */
  static void swap(int[] arr, int a, int b) {
    int temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;
  }
}
```

[back to top](#java)

### Quicksort (Hoare's Partition)

This code uses a single-pivot randomized Quicksort with Hoare's partition.  
Performance can be improved by using insertion sort on small arrays, but the improvement is small. If implementing tail-call optimization, recurse on the smaller partition first.

```java
static class Quicksort {
  /**
   * Sorts an entire array using Quicksort.
   *
   * @param arr The array to be sorted.
   */
  static void sort(int[] arr) {
    sort(arr, 0, arr.length);
  }

  /**
   * Sorts an array in a specific range using Quicksort.
   *
   * @param arr        The array to be sorted.
   * @param leftBound  The lower bound.
   * @param rightBound The upper bound (not inclusive).
   */
  static void sort(int[] arr, int leftBound, int rightBound) {
    if (leftBound + 1 < rightBound) {
      int midPoint = partition(arr, leftBound, rightBound);
      sort(arr, leftBound, midPoint);
      sort(arr, midPoint, rightBound);
    }
  }

  /**
   * Partitions an array around a random pivot.
   *
   * @param arr        The array to be sorted.
   * @param leftBound  The lower bound.
   * @param rightBound The upper bound (not inclusive).
   * @return The mid-point, which is contained in the right partition.
   */
  static int partition(int[] arr, int leftBound, int rightBound) {
    int range = rightBound - leftBound;
    int rand = leftBound + (int) (Math.random() * range);
    int pivot = arr[rand];
    int pp = (rightBound + leftBound) / 2;
    int lp = leftBound;
    int rp = rightBound;
    // move the pivot to the middle of the array
    swap(arr, rand, pp);
    // loop through the low partition until an element greater than or equal to the
    // pivot is found
    for (; lp < rp; lp++) {
      if (arr[lp] >= pivot) {
        // loop through the high partition until an element less than or equal to the
        // pivot is found
        for (rp--; rp > lp; rp--) {
          if (arr[rp] <= pivot) {
            swap(arr, lp, rp);
            break;
          }
        }
      }
    }
    // note: lp may have crossed-over into the right partition
    return rp;
  }

  /**
  * Swaps a pair of elements in an array.
  *
  * @param arr The array.
  * @param a   The index of the first element.
  * @param b   The index of the second element.
  */
  static void swap(int[] arr, int a, int b) {
    int temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;
  }
}
```

[back to top](#java)

### Counting Sort

This code will find the range of values in an array to count the number of each element offset by the minimum value. It performs well on data with a range up to about 2^12.

Performance can be improved by parameterizing the range or by using a guaranteed range that is close to the actual range, but the improvement is small.

```java
/**
 * Sorts an array using counting sort.
 *
 * @param arr The array to be sorted.
 * @return The sorted array.
 */
static int[] countingSort(int[] arr) {
  int[] sorted = new int[arr.length];
  int upperBound = Integer.MIN_VALUE;
  int lowerBound = Integer.MAX_VALUE;
  // find the range of elements
  for (int elem : arr) {
    upperBound = Math.max(upperBound, elem);
    lowerBound = Math.min(lowerBound, elem);
  }
  int[] count = new int[upperBound - lowerBound + 1];
  // find count of each element
  for (int elem : arr) {
    int index = elem - lowerBound;
    count[index]++;
  }
  // rebase count
  for (int j = 1; j < count.length; j++) {
    count[j] += count[j - 1];
  }
  // insert elements into sorted array in reverse order
  for (int j = arr.length - 1; j >= 0; j--) {
    int index = arr[j] - lowerBound;
    count[index]--;
    sorted[count[index]] = arr[j];
  }
  return sorted;
}
```

[back to top](#java)

### Radix Sort (with Division)

This code uses counting sort as a subroutine for radix sort, with a temporary array that alternates with the given array for copying elements.  
Performance greatly depends on the radix chosen and the magnitudes of the elements. The loop to find the maximum degree can be parameterized to avoid repeating work, but the improvement in performance is small.  
Watch out for overflow when using large a radix.

[Radix Sort Performance](../science/radix-sort.md)

```java
/**
 * Sorts an array using radix sort.
 *
 * @param arr   The array to be sorted.
 * @param radix The base for counting sort.
 * @return The sorted array.
 */
static int[] radixSort(int[] arr, int radix) {
  int[] temp = new int[arr.length];
  int maxDeg = 0;
  // find maxDeg
  for (int elem : arr) {
    maxDeg = Math.max(maxDeg, Math.abs(elem));
  }
  // loop from least to most significant digit
  for (int deg = 1; deg <= maxDeg; deg *= radix) {
    int[] count = new int[radix * 2 - 1];
    // find count of each digit
    for (int elem : arr) {
      int digit = (elem / deg) % radix + radix - 1;
      count[digit]++;
    }
    // rebase count
    for (int j = 1; j < count.length; j++) {
      count[j] += count[j - 1];
    }
    // insert elements to temp in reverse order
    for (int j = arr.length - 1; j >= 0; j--) {
      int digit = (arr[j] / deg) % radix + radix - 1;
      count[digit]--;
      temp[count[digit]] = arr[j];
    }
    // swap arr and temp
    int[] swap = arr;
    arr = temp;
    temp = swap;
  }
  // The reference of arr and temp may have swapped.
  return arr;
}
```

[back to top](#java)

### Radix Sort (with Bitwise Operations)

This code uses counting sort as a subroutine for radix sort, with a temporary array that alternates with the given array for copying elements. It is written to only handle non-negative integers.  
Performance greatly depends on the radix chosen and the magnitudes of the elements. The loop to find the maximum shift can be parameterized to avoid repeating work, but the improvement in performance is small.

[Radix Sort Performance](../science/radix-sort.md)

```java
/**
 * Sorts an array of non-negative integers using radix sort.
 *
 * @param arr The array to be sorted.
 * @param deg The degree of 2 used as the base for counting sort.
 * @return The sorted array.
 */
static int[] radixSort(int[] arr, int deg) {
  int[] temp = new int[arr.length];
  int radix = 1 << deg;
  int mod = radix - 1;
  int maxShift = 0;
  // find maxShift
  for (int elem : arr) {
    maxShift = Math.max(maxShift, elem);
  }
  maxShift = (int) (Math.log(maxShift) / Math.log(radix)) * deg;
  // loop from least to most significant digit
  for (int shift = 0; shift <= maxShift; shift += deg) {
    int[] count = new int[radix];
    // find count of each digit
    for (int elem : arr) {
      int digit = elem >>> shift & mod;
      count[digit]++;
    }
    // rebase count
    for (int j = 1; j < count.length; j++) {
      count[j] += count[j - 1];
    }
    // insert elements to temp in reverse order
    for (int j = arr.length - 1; j >= 0; j--) {
      int digit = arr[j] >>> shift & mod;
      count[digit]--;
      temp[count[digit]] = arr[j];
    }
    // swap arr and temp
    int[] swap = arr;
    arr = temp;
    temp = swap;
  }
  // the reference of arr and temp may have swapped.
  return arr;
}
```

[back to top](#java)

## Selection

[Counting sort](#counting-sort) seems to have great performance on data with a range up to about 2^12.

### Quickselect (Lomuto Partition)

This code uses a single-pivot randomized Quickselect with a Lomuto partition.  
Performance can be greatly improved by using counting sort instead of a selection algorithm on arrays with a limited range of values.

```java
/**
 * Selects the kth smallest element in an unsorted array.
 *
 * @param arr        The array of elements
 * @param leftBound  The lower bound
 * @param rightBound The upper bound (not inclusive)
 * @param target     The kth element to select (from index 0)
 * @return The kth smallest element (from index 0)
 */
static int quickselect(int[] arr, int leftBound, int rightBound, int target) {
  int range = rightBound - leftBound;
  if (range == 1) {
    return arr[leftBound];
  }
  int rand = leftBound + (int) (Math.random() * range);
  int pivot = arr[rand];
  int pp = rightBound - 1;
  int lp = leftBound;
  int rp = leftBound;
  int pivotCount = 1;
  // move the pivot to the end of the array
  swap(arr, rand, pp);
  // swap elements that are less than the pivot from the right partition to the
  // left partition
  for (; rp < pp; rp++) {
    if (arr[rp] < pivot) {
      swap(arr, lp, rp);
      lp++;
    } else if (arr[rp] == pivot) {
      pivotCount++;
    }
    // elements equal to the pivot stay in the right partition
  }
  // return the partition that contains the target
  int leftSize = lp - leftBound;
  if (leftSize > target) {
    return quickselect(arr, leftBound, lp, target);
  }
  if (leftSize + pivotCount > target) {
    return pivot;
  }
  return quickselect(arr, lp, rp, target - leftSize - 1);
}

/**
 * Swaps a pair of elements in an array.
 *
 * @param arr The array.
 * @param a   The index of the first element.
 * @param b   The index of the second element.
 */
static void swap(int[] arr, int a, int b) {
  int temp = arr[a];
  arr[a] = arr[b];
  arr[b] = temp;
}
```

[back to top](#java)

### Quickselect (Hoare's Partition)

This code uses a single-pivot randomized Quickselect with Hoare's partition.  
Performance can be greatly improved by using counting sort instead of a selection algorithm on arrays with a limited range of values.

```java
/**
 * Selects the kth smallest element in an unsorted array.
 *
 * @param arr        The array of elements
 * @param leftBound  The lower bound
 * @param rightBound The upper bound (not inclusive)
 * @param target     The kth element to select (from 0)
 * @return The kth smallest element (from 0)
 */
static int quickselect(int[] arr, int leftBound, int rightBound, int target) {
  int range = rightBound - leftBound;
  if (range == 1) {
    return arr[leftBound];
  }
  int rand = leftBound + (int) (Math.random() * range);
  int pivot = arr[rand];
  int pp = (rightBound + leftBound) / 2;
  int lp = leftBound;
  int rp = rightBound;
  int leftCount = 0;
  int rightCount = 0;
  // move the pivot to the middle of the array
  swap(arr, rand, pp);
  // loop through the low partition until an element greater than or equal to the
  // pivot is found
  for (; lp < rp; lp++) {
    if (arr[lp] >= pivot) {
      if (arr[lp] == pivot) {
        rightCount++;
      }
      // loop through the high partition until an element less than or equal to the
      // pivot is found
      for (rp--; rp > lp; rp--) {
        if (arr[rp] <= pivot) {
          if (arr[rp] == pivot) {
            leftCount++;
          }
          swap(arr, lp, rp);
          break;
        }
      }
    }
  }
  // note: lp may have crossed-over into the right partition
  int leftSize = rp - leftBound;
  // return the partition that contains the target
  if (leftSize - leftCount > target) {
    return quickselect(arr, leftBound, rp, target);
  }
  if (leftSize + rightCount > target) {
    return pivot;
  }
  return quickselect(arr, rp, rightBound, target - leftSize);
}

/**
 * Swaps a pair of elements in an array.
 *
 * @param arr The array.
 * @param a   The index of the first element.
 * @param b   The index of the second element.
 */
static void swap(int[] arr, int a, int b) {
  int temp = arr[a];
  arr[a] = arr[b];
  arr[b] = temp;
}
```

[back to top](#java)

### Boyer-Moore Majority Vote

```java
/**
 * Finds an index of the element in an array that has a strict majority.
 *
 * @param arr The array of elements.
 * @return An index of the majority element.
 * @return -1 if there is no majority.
 */
static int findMajority(int[] arr) {
  int majority = -1;
  int count = 0;
  // find the majority element
  for (int i = 0; i < arr.length; i++) {
    if (count == 0) {
      count++;
      majority = i;
    } else if (arr[majority] == arr[i]) {
      count++;
    } else {
      count--;
    }
  }
  // count occurrences of majority
  count = 0;
  for (int elem : arr) {
    if (elem == arr[majority]) {
      count++;
    }
  }
  return count > arr.length / 2 ? majority : -1;
}
```

[back to top](#java)

## Disjoint Sets Data Structure

This code uses path-compression and union by rank.

```java
/**
 * A disjoint set.
 */
static class DSet {
  DSet parent;
  int rank;

  DSet() {
    this.parent = this;
    this.rank = 0;
  }
}

/**
 * A disjoint sets data-structure.
 */
static class DsStruct {
  /**
   * Finds a set's representative.
   *
   * @param x The disjoint set that we're searching for.
   * @return The representative of the disjoint set.
   */
  static DSet find(DSet x) {
    if (x != x.parent) {
      x.parent = find(x.parent);
    }
    return x.parent;
  }

  /**
   * Unions two sets.
   *
   * @param a The first set to union.
   * @param b The second set to union.
   */
  static void union(DSet a, DSet b) {
    a = find(a);
    b = find(b);
    if (a != b) {
      if (a.rank > b.rank) {
        b.parent = a;
      } else {
        a.parent = b;
        if (a.rank == b.rank) {
          b.rank++;
        }
      }
    }
  }
}
```

[back to top](#java)

## Trie Data Structure

[source](https://www.geeksforgeeks.org/trie-insert-and-search/)

```java
/**
 * A trie data structure.
 */
static class Trie {
  static final int ALPHABET_SIZE = 26;
  Node root;

  /**
   * Constructs a trie with an empty root.
   */
  Trie() {
    root = new Node();
  }

  /**
   * Inserts a pattern into this trie.
   *
   * @param pattern The pattern to be inserted.
   */
  void insert(String pattern) {
    Node crawl = root;
    // crawl down the trie, creating new nodes as needed
    for (int c = 0; c < pattern.length(); c++) {
      int child = index(pattern.charAt(c));
      if (crawl.children[child] == null) {
        crawl.children[child] = new Node();
      }
      crawl = crawl.children[child];
    }
    // crawl is the last char in pattern
    crawl.isEndNode = true;
  }

  /**
   * Finds a pattern in this trie.
   *
   * @param pattern The pattern to search for.
   * @return True if the pattern is in this trie.
   */
  boolean search(String pattern) {
    Node crawl = root;
    // crawl down the trie
    for (int c = 0; c < pattern.length(); c++) {
      int child = index(pattern.charAt(c));
      // check if the char exists
      if (crawl.children[child] == null) {
        return false;
      }
      crawl = crawl.children[child];
    }
    // check if the last char is in the pattern and is an end node
    return (crawl != null && crawl.isEndNode);
  }

  /**
   * Determines the index of a char in a children array.
   *
   * @param c The char to index.
   * @return The index of c in a children array.
   */
  int index(char c) {
    return c - 'a';
  }

  /**
   * A trie node.
   */
  class Node {
    Node[] children;
    boolean isEndNode;

    /**
     * Constructs an empty node.
     */
    Node() {
      children = new Node[ALPHABET_SIZE];
      isEndNode = false;
    }
  }
}
```

[back to top](#java)
