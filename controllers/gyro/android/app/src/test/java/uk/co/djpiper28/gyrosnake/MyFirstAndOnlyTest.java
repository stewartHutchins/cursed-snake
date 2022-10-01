package uk.co.djpiper28.gyrosnake;

import org.junit.Test;

import static org.junit.Assert.*;
import static uk.co.djpiper28.gyrosnake.Api.ipToBroadcast;

public class MyFirstAndOnlyTest {

    @Test public void testIpToBroadcast() {
        assertEquals("192.168.3.255", ipToBroadcast("192.168.3.7"));
    }

}