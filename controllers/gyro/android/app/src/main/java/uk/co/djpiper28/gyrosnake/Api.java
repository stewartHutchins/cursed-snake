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
    private int ipExt;

    public Api(Context context) {
        this.context = context;
        this.ipExt = 255;

        this.getIpAddress(); // This is to sanity check
    }

    protected String getIpAddress() {
        WifiManager wifiManager = (WifiManager) this.context.getSystemService(WIFI_SERVICE);
        String ipAddress = Formatter.formatIpAddress(wifiManager.getConnectionInfo().getIpAddress());
        Log.d(TAG, "getIpAddress: " + ipAddress);

        return ipAddress;
    }

    public String ipToBroadcast(String ipAddr) {
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

        strb.append(String.valueOf(this.ipExt));
        return strb.toString();
    }

    public void sendCommand(MovementTypes movement) throws IOException {
        final String ipAddress = ipToBroadcast(this.getIpAddress());
        Connection conn = Jsoup.connect("http://" + ipAddress + ":" + PORT);
        conn.requestBody(movement.getMovementStr());
        conn.post();
    }

    public void setIpExt(int ipExt) {
        this.ipExt = ipExt;
    }
}