package uk.co.djpiper28.gyrosnake;

import static android.content.Context.WIFI_SERVICE;

import android.content.Context;
import android.net.wifi.WifiManager;
import android.text.format.Formatter;
import android.util.Log;

import org.jsoup.Connection;
import org.jsoup.Jsoup;

import java.io.IOException;

public class Api {
    private static final int PORT = 6969;
    private final static String TAG = "DEBUG";
    private Context context;

    public Api(Context context) {
        this.context = context;

        this.getIpAddress(); // This is to sanity check
    }

    protected String getIpAddress() {
        WifiManager wifiManager = (WifiManager) this.context.getSystemService(WIFI_SERVICE);
        String ipAddress = Formatter.formatIpAddress(wifiManager.getConnectionInfo().getIpAddress());
        Log.d(TAG, "getIpAddress: " + ipAddress);

        return ipAddress;
    }

    public static String ipToBroadcast(String ipAddr) {
        StringBuilder strb = new StringBuilder();

        int dots = 0;
        for (char c : ipAddr.toCharArray()) {
            strb.append(c);
            if (c == '.') {
                dots++;
            }

            if (dots == 3) {
                break;
            }
        }

        strb.append("255");
        return strb.toString();
    }

    public void sendCommand(MovementTypes movement) throws IOException {
        final String ipAddress = ipToBroadcast(this.getIpAddress());
        Connection conn = Jsoup.connect(ipAddress + ":" + PORT);
        conn.data(movement.getMovementStr());
        conn.post();
    }

}