# Radix Sort

Compared the performance of radix sort using different radixes and bitwise vs division implementations. Testing was completed in Java 15.

## <!-- omit in toc -->Contents

- [The code](#the-code)
  - [Radix Sort Code](#radix-sort-code)
  - [Test Routine Code](#test-routine-code)
- [Procedure Comparison](#procedure-comparison)
  - [Procedure Results](#procedure-results)
  - [Procedure Conclusion](#procedure-conclusion)
- [Data Size Comparison](#data-size-comparison)
  - [Data Size Results](#data-size-results)
  - [Data Size Conclusion](#data-size-conclusion)
- [Data Range Comparison](#data-range-comparison)
  - [Data Range Results](#data-range-results)
  - [Data Range Conclusion](#data-range-conclusion)
- [Quicksort Comparison](#quicksort-comparison)
- [Conclusion](#conclusion)
  - [Caveats](#caveats)

## The code

All code can be found in the [source code folder](./source-code/radix-sort/).

### Radix Sort Code

Radix sort was implement using counting sort. Input was restricted to non-negative numbers only for simplicity. The different procedure implementations tested were:

1. Arbitrary radix, using division and modulo to calculate the counted digit.
2. Powers of 2 as radix, using bitwise operations to calculate the counted digit.

### Test Routine Code

Run-times were calculated as the average over 100 tests. Each test case times the run-time of sorting the test data. The elements in the test data were generated pseudo-randomly for each test case. The size and range of the test data and the radix for the sorting procedure were specified.

## Procedure Comparison

To ensure that there was no bias in testing based off of the order each procedure was called and that the test routine was reliable, the test routine was repeated 10 times. The first 5 routines had the bitwise procedure go first, and the last 5 routines had the division procedure go first. For all routines, the procedure order alternated between tests.

> tests: 100  
> data range: 2^24  
> data size: 10^7  
> radix: 256  

The radix was chosen arbitrarily as a reasonable size to use for the data. The data range is the limit that the division procedure can handle using the chosen radix without overflowing a 32-bit integer. The data size was chosen so as to not overflow Java's heap.

### Procedure Results

Times are in microseconds

#### Bitwise Procedure First

| Procedure | 1       | 2       | 3       | 4       | 5       |
| --------- | ------- | ------- | ------- | ------- | ------- |
| Division  | 327,833 | 328,990 | 326,578 | 328,966 | 331,122 |
| Bitwise   | 105,453 | 105,316 | 104,839 | 105,010 | 106,179 |

Confidence

| Procedure | Mean Run-time | Standard Deviation | 95% Confidence |
| --------- | ------------- | ------------------ | -------------- |
| Division  | 328,698       | 1,502              | ± 1,316        |
| Bitwise   | 105,359       | 464                | ± 406          |

---

#### Division Procedure First

| Procedure | 1       | 2       | 3       | 4       | 5       |
| --------- | ------- | ------- | ------- | ------- | ------- |
| Division  | 338,932 | 331,049 | 332,297 | 330,400 | 328,892 |
| Bitwise   | 108,616 | 105,344 | 105,956 | 105,855 | 104,904 |

Confidence

| Procedure | Mean Run-time | Standard Deviation | 95% Confidence |
| --------- | ------------- | ------------------ | -------------- |
| Division  | 332,314       | 3,486              | ± 3,056        |
| Bitwise   | 106,135       | 1,297              | ± 1,137        |

---

#### Discrepancy between bitwise first and division first routines

| Procedure | Mean Discrepancy | Standard Deviation | 95% Confidence |
| --------- | ---------------- | ------------------ | -------------- |
| Division  | 4,508            | 3,621              | ± 3,174        |
| Bitwise   | 1,286            | 1,032              | ± 905          |

### Procedure Conclusion

The test routine has a trivial margin of error compared to the run-times between the procedures.

The the bitwise procedure is roughly x3 faster than the division procedure for the chosen parameters. This is consistent with the expected equivalent asymptotic run-time of the procedures.

## Data Size Comparison

Based off of the previous tests, it was assumed that the testing order and data would not significantly affect results for large data sizes; however, results on small data sizes may be less accurate.

The bitwise procedure was used for all tests.

Parameters were tested in order of increasing radix, then increasing data size.

> tests: 100  
> data range: 2^16  
> data size: 2^12..2^24  
> radix: 2^1..2^16

The data range is the limit that a radix of 2^16 behaves like plain counting sort. A radix of 2^8 will perform 2 cycles of counting sort, a radix of 2^4 performs 4 cycles, a radix of 2^2 performs 8 cycles, and a radix of 2^1 performs 16 cycles.

### Data Size Results

Times are in microseconds

| Radix \ Size | 2^12 | 2^16  | 2^20   | 2^24    |
| ----------- | ---- | ----- | ------ | ------- |
| 2^1         | 399  | 3,364 | 61,217 | 952,782 |
| 2^2         | 243  | 1,551 | 29,087 | 459,121 |
| 2^3         | 264  | 1,746 | 22,505 | 345,384 |
| 2^4         | 236  | 1,457 | 15,892 | 228,912 |
| 2^6         | 176  | 877   | 11,770 | 179,280 |
| 2^8         | 158  | 648   | 7,708  | 118,338 |
| 2^12        | 187  | 680   | 8,749  | 167,248 |
| 2^16        | 332  | 670   | 8,660  | 174,007 |

---

Times as a percentage of radix 2^8's run-time

| Radix \ Size | 2^12 | 2^16 | 2^20 | 2^24 |
| ----------- | ---- | ---- | ---- | ---- |
| 2^1         | 253% | 519% | 794% | 805% |
| 2^2         | 154% | 239% | 377% | 388% |
| 2^3         | 167% | 269% | 292% | 292% |
| 2^4         | 149% | 225% | 206% | 193% |
| 2^6         | 111% | 135% | 153% | 151% |
| 2^8         | 100% | 100% | 100% | 100% |
| 2^12        | 118% | 105% | 114% | 141% |
| 2^16        | 210% | 103% | 112% | 147% |

### Data Size Conclusion

Anecdotally, the linear run-time can be observed from the data; as data size increases by a factor of 16, run-time roughly increases by the same factor. A radix of 2^8 performed the best for all data sizes with this range; however, radixes of 2^6, 2^12, and 2^16 were all close.

Surprisingly, the time-savings from increasing to a radix that reduces the number of cycles of counting sort does not appear to be very different than the time-savings from increasing to a radix that has the same number of cycles.

User [templatetypedef](https://stackoverflow.com/a/25675583) suggested that a radix of 2^16 may suffer from exceeding the size of cache, degrading performance. Except on small data sizes, the performance of 2^16 is nearly optimal. I have no idea how caching works in Java, and this number may depend on the client system.

## Data Range Comparison

Based off of the previous tests, it was assumed that the testing order and data would not significantly affect results for large data sizes.

The bitwise procedure was used for all tests.

Parameters were tested in order of increasing radix, then increasing data range.

> tests: 100  
> data range: 2^12..2^24  
> data size: 2^20  
> radix: 2^1..2^16

The data size was chosen arbitrarily to be small enough to compute quickly.

### Data Range Results

Times are in microseconds

| Radix \ Range | 2^12   | 2^16   | 2^20   | 2^24   |
| ------------ | ------ | ------ | ------ | ------ |
| 2^1          | 44,798 | 61,695 | 76,114 | 91,668 |
| 2^2          | 22,219 | 29,510 | 36,310 | 42,929 |
| 2^3          | 15,052 | 23,834 | 26,151 | 29,998 |
| 2^4          | 12,243 | 14,536 | 19,904 | 21,425 |
| 2^6          | 9,003  | 11,555 | 15,633 | 14,373 |
| 2^8          | 8,018  | 7,696  | 11,629 | 11,325 |
| 2^12         | 7,416  | 8,526  | 8,569  | 10,265 |
| 2^16         | 7,074  | 8,624  | 12,120 | 12,620 |

---

Times as a percentage of radix 2^8's run-time

| Radix \ Range | 2^12 | 2^16 | 2^20 | 2^24 |
| ------------ | ---- | ---- | ---- | ---- |
| 2^1          | 559% | 802% | 655% | 809% |
| 2^2          | 277% | 383% | 312% | 379% |
| 2^3          | 188% | 310% | 225% | 265% |
| 2^4          | 153% | 189% | 171% | 189% |
| 2^6          | 112% | 150% | 134% | 127% |
| 2^8          | 100% | 100% | 100% | 100% |
| 2^12         | 92%  | 111% | 74%  | 91%  |
| 2^16         | 88%  | 112% | 103% | 111% |

### Data Range Conclusion

No single radix performed better than the others for all data ranges. Radixes of 2^8, 2^12, and 2^16 all performed well. Run-times increased slightly as data ranges increased.

Interestingly, the number of cycles that counting sort is performed doesn't seem to have a noticeable impact on performance. For example, a radix of 8 performs nearly the same as a radix of 12 on a data range of 2^24, despite radix 8 using 3 cycles of counting sort and radix 12 using only 2 cycles.

## Quicksort Comparison

This section will quickly compare both the division and bitwise radix sort procedures to Quicksort.

> tests: 100  
> data range: 2^24  
> data size: 2^12..2^20

Quicksort: Java 15 Standard Library Quicksort  
Division _x_: Division radix sort with radix _x_  
Bitwise _x_: Bitwise radix sort with radix _x_

Times are in microseconds

| Procedure \ Size | 2^12 | 2^16  | 2^20   |
| ---------------- | ---- | ----- | ------ |
| Quicksort        | 381  | 5,260 | 66,833 |
| Division 10      | 518  | 5,862 | 92,082 |
| Division 256     | 268  | 2,351 | 34,815 |
| Division 10,000  | 426  | 1,676 | 24,318 |
| Bitwise 2        | 399  | 3,364 | 61,217 |
| Bitwise 256      | 158  | 648   | 7,708  |

Times as a percentage of Quicksort's run-time

| Procedure \ Size | 2^12 | 2^16 | 2^20 |
| ---------------- | ---- | ---- | ---- |
| Quicksort        | 100% | 100% | 100% |
| Division 10      | 136% | 111% | 138% |
| Division 256     | 70%  | 45%  | 52%  |
| Division 10,000  | 119% | 32%  | 36%  |
| Bitwise 2        | 105% | 64%  | 92%  |
| Bitwise 256      | 41%  | 12%  | 12%  |

## Conclusion

Quicksort is very fast. Choosing the right base for radix sort is very important, or else real-world performance can degrade to that of a comparison-based sort. Bitwise operations are significantly faster than division and modulo operations when used repeatedly in radix sort.

As a rule of thumb, bitwise radix sort using a radix of 2^8 appears to be very fast. When using division radix sort, choose a larger radix to reduce the number of cycles and avoid costly division operations.

### Caveats

Since data was generated randomly for each test case, the sorted data is not uniform, which makes comparison less accurate (except in the procedure comparison). Further analysis of performance on data that is not random and in other languages, systems, and compilers should be done. This article is also lacking in statistical analysis.
