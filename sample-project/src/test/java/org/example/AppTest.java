package org.example;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class AppTest {

    @Test
    public void testAdd() {
        App app = new App();
        assertEquals(5, app.add(2, 3));
        assertEquals(0, app.add(-2, 2));
        assertEquals(7, app.add(0, 7));
    }

    @Test
    public void testMultiply() {
        App app = new App();
        assertEquals(6, app.multiply(2, 3));
        assertEquals(0, app.multiply(0, 5));
    }
}
