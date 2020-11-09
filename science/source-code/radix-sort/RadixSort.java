public class RadixSort {

  /**
   * Sorts an array using radix sort with bitwise operations.
   *
   * @param arr The array to be sorted.
   * @param deg The degree of 2 used as the base for counting sort.
   */
  static void radixSortBitwise(int[] arr, int deg) {
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
    // copy the final array from arr to temp if the reference of arr and temp were
    // swapped
    if ((maxShift / deg & 1) == 0) {
      System.arraycopy(arr, 0, temp, 0, arr.length);
    }
  }

  /**
   * Sorts an array using radix sort with division.
   *
   * @param arr   The array to be sorted.
   * @param radix The base for counting sort.
   */
  static void radixSortDivision(int[] arr, int radix) {
    int[] temp = new int[arr.length];
    int maxDeg = 0;
    // find maxDeg
    for (int elem : arr) {
      maxDeg = Math.max(maxDeg, elem);
    }
    // loop from least to most significant digit
    for (int deg = 1; deg <= maxDeg; deg *= radix) {
      int[] count = new int[radix];
      // find count of each digit
      for (int elem : arr) {
        int digit = (elem / deg) % radix;
        count[digit]++;
      }
      // rebase count
      for (int j = 1; j < count.length; j++) {
        count[j] += count[j - 1];
      }
      // insert elements to temp in reverse order
      for (int j = arr.length - 1; j >= 0; j--) {
        int digit = (arr[j] / deg) % radix;
        count[digit]--;
        temp[count[digit]] = arr[j];
      }
      // swap arr and temp
      int[] swap = arr;
      arr = temp;
      temp = swap;
    }
    // copy the final array from arr to temp if the reference of arr and temp were
    // swapped
    if ((int) (Math.log(maxDeg) / Math.log(radix)) % 2 == 0) {
      System.arraycopy(arr, 0, temp, 0, arr.length);
    }
  }

}
