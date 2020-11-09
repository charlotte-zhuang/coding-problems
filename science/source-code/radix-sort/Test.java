import java.util.Arrays;

public class Test {
  static final int NUM_TESTS = 100;

  public static void main(String[] args) throws Exception {
    // run tests one at a time
  }

  /**
   * Compare the run-times of division and bitwise radix sort.
   * 
   * @param bitwiseFirst 1 if bitwise procedure goes first, otherwise 0.
   */
  static void procedureComparison(int bitwiseFirst) {
    // parameters
    final int TEST_SIZE = 10000000;
    final int RANGE = 1 << 24;
    final int DEGREE = 8;
    final int RADIX = 1 << DEGREE;
    // results
    long divTime = 0;
    long bitTime = 0;
    // test loop
    for (int t = 0; t < NUM_TESTS; t++) {
      // generate test data
      int[] arr = new int[TEST_SIZE];
      int[] arr2;
      for (int i = 0; i < arr.length; i++) {
        arr[i] = (int) (Math.random() * RANGE);
      }
      arr2 = arr.clone();
      // time sorting
      if (t % 2 == bitwiseFirst) {
        long start1 = System.nanoTime();
        RadixSort.sortDivision(arr, RADIX);
        long stop1 = System.nanoTime();
        long start2 = System.nanoTime();
        RadixSort.sortBitwise(arr2, DEGREE);
        long stop2 = System.nanoTime();
        divTime += stop1 - start1;
        bitTime += stop2 - start2;
      } else {
        long start1 = System.nanoTime();
        RadixSort.sortBitwise(arr, DEGREE);
        long stop1 = System.nanoTime();
        long start2 = System.nanoTime();
        RadixSort.sortDivision(arr2, RADIX);
        long stop2 = System.nanoTime();
        bitTime += stop1 - start1;
        divTime += stop2 - start2;
      }
    }
    // output
    System.out.printf("Division: average %,d%n", divTime / (NUM_TESTS * 1000));
    System.out.printf("Bitwise: average %,d%n", bitTime / (NUM_TESTS * 1000));
  }

  /**
   * Test the average run-time of bitwise radix sort.
   * 
   * @param testSize The size of the test data.
   * @param range    The range of the test data.
   * @param degree   The degree of 2 used as a base.
   */
  static void parameterComparison(int testSize, int range, int degree) {
    long time = 0;
    // test loop
    for (int t = 0; t < NUM_TESTS; t++) {
      // generate test data
      int[] arr = new int[testSize];
      for (int i = 0; i < arr.length; i++) {
        arr[i] = (int) (Math.random() * range);
      }
      // time sorting
      long start = System.nanoTime();
      RadixSort.sortBitwise(arr, degree);
      long stop = System.nanoTime();
      time += stop - start;
    }
    // output
    System.out.printf("Size %,d Range %,d Degree %d: average %,d%n", testSize, range, degree,
        time / (NUM_TESTS * 1000));
  }

  /**
   * Test the average run-time of Quicksort.
   * 
   * @param testSize The size of the test data.
   * @param degree   The degree of 2 used as a base.
   */
  static void quicksortComparison(int testSize) {
    // parameters
    final int RANGE = 1 << 24;
    // results
    long time = 0;
    // test loop
    for (int t = 0; t < NUM_TESTS; t++) {
      // generate test data
      int[] arr = new int[testSize];
      for (int i = 0; i < arr.length; i++) {
        arr[i] = (int) (Math.random() * RANGE);
      }
      // time sorting
      long start1 = System.nanoTime();
      Arrays.sort(arr);
      long stop1 = System.nanoTime();
      time += stop1 - start1;
    }
    // output
    System.out.printf("Standard Quicksort on %,d elements: average %,d%n", testSize, time / (NUM_TESTS * 1000));
  }

}
