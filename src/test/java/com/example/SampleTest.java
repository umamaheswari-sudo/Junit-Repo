package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SampleTest {

    @Test void test1() { assertEquals(5, 2 + 3); }
    @Test void test2() { assertEquals(2, 5 - 3); }
    @Test void test3() { assertEquals(6, 2 * 3); }
    @Test void test4() { assertEquals(2, 6 / 3); }
    @Test void test5() { assertEquals("hello", "he" + "llo"); }
    @Test void test6() { assertTrue(10 > 5); }
    @Test void test7() { assertFalse(5 > 10); }
    @Test void test8() { assertNull(null); }

    // ❌ Failing
    @Test void test9() { assertEquals(10, 5 + 3); }

    // ❌ Failing
    @Test void test10() { assertTrue(false); }
}
