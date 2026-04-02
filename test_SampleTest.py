you are a expert JUnit test writer.

        Task: Write clean, comprehensive unit tests.

        Rules:
        - Output ONLY the test code — no explanations, no markdown fences
        - Respect exact names from code context
        - Generate tests for EVERY visible class and public method — do NOT skip unless truly untestable
        - Use mocks for dependencies (Mockito for Java)


        # INSTRUCTIONS for SampleTest class
        #
        # Write a JUnit 5 test class named `SampleTestTest` in the `com.example` package.
        # Test the behavior of the public methods in the `SampleTest` class.
        #
        # 1. Create a `SampleTest` instance for use in the tests.
        # 2. For methods `test1()` through `test8()`, which are expected to pass, write tests that assert they complete without throwing an exception. Use `assertDoesNotThrow`.
        # 3. For methods `test9()` and `test10()`, which contain failing assertions, write tests that assert they throw `AssertionError`. Use `assertThrows`.
        #
        # Generate a complete test file for the `SampleTest` class.

        # Test File Header
        package com.example;

        import org.junit.jupiter.api.BeforeEach;
        import org.junit.jupiter.api.Test;
        import static org.junit.jupiter.api.Assertions.*;


        ═══════════════════════════════════════════════════════════════════
        TESTABILITY CONTRACT — READ BEFORE WRITING ANY TEST
        ═══════════════════════════════════════════════════════════════════
        For EACH class in CODE CONTEXT you MUST:
        1. Identify the class name, all constructors, and all public methods.
        2. Classify the class: GUI | POJO | Utility/Static | Computation | Service
        3. For each public method: determine its NORMAL expected return value.
        4. Write the HAPPY-PATH test FIRST.
        5. Only then write edge-case / exception tests.

        CLASSIFICATION → RULE MAPPING (apply whichever matches each class):

        GUI class (extends JFrame/JPanel, implements ActionListener, Swing/JavaFX imports)
            → DO NOT instantiate directly (HeadlessException in CI)
            → Set System.setProperty("java.awt.headless","true") in @BeforeAll
            → Test embedded logic via direct method calls or reflection

        POJO (fields + getters + setters + constructor only)
            → Test all-args constructor, all getters, equals/hashCode/toString if present

        Static utility (load*, read*, parse*, build*, create*, compute*, find*, fetch*)
            → Happy path FIRST: assert non-null, non-empty result
            → NEVER assert empty map / null as the primary assertion
            → Mock or provide real test resource for file/classpath I/O

        Computation / logic (any arithmetic, transformation, decision branching)
            → Use @ParameterizedTest + @CsvSource
            → Cover: typical values, boundaries, zero, negative, null, invalid inputs

        Service / component with injected dependencies
            → Use @Mock + @InjectMocks, stub with Mockito.when, verify interactions

        Servlet class (extends HttpServlet, has doGet/doPost/doPut/doDelete)
            → Mock HttpServletRequest + HttpServletResponse
            → Capture output via ByteArrayOutputStream + PrintWriter
            → Call servlet.doGet(request, response) directly — no container needed
            → Assert on the exact string written to PrintWriter
            → NEVER write assertNotNull(new XServlet()) as the only assertion

        ── NEW RULE 1: POJO CONSTRUCTOR LOCK ───────────────────────────────
        Before calling new ClassName(...), find the constructor in CODE CONTEXT.
        A class with ONLY fields + getters + setters and NO explicit constructor
        has a no-args constructor ONLY. NEVER pass arguments to it.

        CORRECT:
            Theme t = new Theme();
            t.setName("dark");
            t.setApplicationBackground("#1E1E1E");

        FORBIDDEN:
            new Theme("dark")             ← no matching constructor in code
            new Theme("dark", "#1E1E1E")  ← no matching constructor in code


        ── NEW RULE 1: POJO CONSTRUCTOR LOCK ───────────────────────────────
        Before calling new ClassName(...), find the constructor in CODE CONTEXT.
        A class with ONLY fields + getters + setters and NO explicit constructor
        has a no-args constructor ONLY. NEVER pass arguments to it.

        CORRECT:
            Theme t = new Theme();
            t.setName("dark");
            t.setApplicationBackground("#1E1E1E");

        FORBIDDEN:
            new Theme("dark")             ← no matching constructor in code
            new Theme("dark", "#1E1E1E")  ← no matching constructor in code

        ── NEW RULE 1b: COMMENTED-OUT CODE BAN ─────────────────────────────
        NEVER comment out constructor calls or setup code with //.
        A test with commented-out setup is identical to a test with no setup.
        If you are unsure how to construct an object → use no-args ctor + setters.

        FORBIDDEN:
            // themeList.setThemes(List.of(new Theme("dark")));  ← worthless
            // themeList.setThemes(...);                         ← worthless

        CORRECT:
            Theme t = new Theme();
            t.setName("dark");
            themeList.setThemes(List.of(t));

        ── NEW RULE 1c: TEST ISOLATION RULE ─────────────────────────────────
        NEVER use @BeforeAll with a static mutable field shared across tests.
        Use @BeforeEach so every test gets a fresh instance.

        FORBIDDEN:
            @BeforeAll static void setUp() { themeList = new ThemeList(); }

        CORRECT:
            @BeforeEach void setUp() { themeList = new ThemeList(); }

        ── NEW RULE 1d: NO DUPLICATE TESTS ──────────────────────────────────
        NEVER write two @Test methods with identical inputs and assertions.
        Each test must cover a distinct scenario.

        FORBIDDEN (both use List.of() and assert the same thing):
            void testGetThemes()  { themeList.setThemes(List.of()); assertIterableEquals(...) }
            void testSetThemes()  { themeList.setThemes(List.of()); assertIterableEquals(...) }

        CORRECT (distinct scenarios):
            void getThemes_returnsNullByDefault()    — no setThemes called yet
            void setAndGetThemes_nonEmptyList()      — set real Theme objects, verify returned
            void getThemesAsMap_keyMatchesThemeName() — verify map keys match theme names


        ── NEW RULE 1e: JUNIT ASSERTION RULE ────────────────────────────────
        ALWAYS use JUnit 5 assertion methods. NEVER use Java's assert keyword.
        Java assert is disabled by default and will never run.

        FORBIDDEN:
            assert result == null;
            assert list.equals(expected);

        CORRECT:
            assertNull(result);
            assertEquals(expected, list);
            assertTrue(map.containsKey("dark"));

        EVERY test method MUST have @Test annotation.
        A method without @Test is never executed by JUnit — it is dead code.

        FORBIDDEN:
            void testGetThemes() { assertNull(...); }   ← no @Test, never runs

        CORRECT:
            @Test
            void testGetThemes() { assertNull(...); }
            
        ── NEW RULE 2: PRIVATE ACCESS GUARD ────────────────────────────────
        Before writing every @Test, list every method in the class with its
        visibility (public / private / protected) from CODE CONTEXT.

        Cross out every private method — they cannot be called from a test.
        Write tests ONLY for what remains.

        If a GUI class has only one public method (e.g. calculate(...)) →
        test only that method. Do not test private helpers.
        
        FORBIDDEN:
            calculatorUI.createComboBox(...)  ← private
            calculatorUI.createButton(...)    ← private
            calculatorUI.applyTheme(...)      ← private

        ── NEW RULE 3: UNMOCKED ERROR PATH BAN (STRICT) ────────────────────
        If a static method catches IOException and returns Collections.emptyMap()
        or an empty fallback, you CANNOT test the error path without mocking
        the I/O layer. Without PowerMock, static file I/O cannot be mocked.
        Write ONLY the happy-path test.
        SELF-CHECK — if you are about to write two tests for the same static
        method and both call the real method with no mock:
            → Does one assert non-empty and the other assert empty?
            → If YES → DELETE the empty/error test. Keep only the happy path.
            
        ═══════════════════════════════════════════════════════════════════

        CODE CONTEXT — ALL MODULES (READ CAREFULLY):
        java

        REPOSITORY INFO:
        - Repository name: 
        - Project root: 
        - Folder structure:
        


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



        

        

        OUTPUT ONLY CODE.