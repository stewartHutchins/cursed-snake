package uk.co.djpiper28.gyrosnake;

import static android.Manifest.permission.HIGH_SAMPLING_RATE_SENSORS;
import static android.Manifest.permission.INTERNET;

import androidx.appcompat.app.AppCompatActivity;

import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import uk.co.djpiper28.gyrosnake.vectmaths.VectorMaths;

public class MainActivity extends AppCompatActivity implements Runnable {
    private static final String TAG = "DEBUG";
    private static final long POLL_TIME = 1000 / 60;
    private static final double TRIGGER_ANGLE_X = 20d;
    private static final double TRIGGER_ANGLE_Y = TRIGGER_ANGLE_X;
    private static final int PERMISSION_REQUEST_CODE = 180;
    private static final int DEFAULT_IP_EXT = 7;
    private FrameHandler frameHandler;
    private Api api;
    private SensorManager sensorManager;
    private Sensor sensor;
    private long lastTransmission;
    private InputFrame currentFrame;
    private SensorEventListener sensorEventListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        this.api = new Api(this.getApplicationContext());
        this.frameHandler = new FrameHandler(this.api);
        this.lastTransmission = 0;

        EditText edit = this.findViewById(R.id.ipEdit);
        edit.setText(String.valueOf(DEFAULT_IP_EXT));
        this.api.setIpExt(DEFAULT_IP_EXT);

        edit.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                api.setIpExt(Integer.valueOf(edit.getText().toString()));
                return true;
            }
        });

        this.requestPermissions(new String[] { HIGH_SAMPLING_RATE_SENSORS }, PERMISSION_REQUEST_CODE);
        this.requestPermissions(new String[] { WIFI_AWARE_SERVICE }, PERMISSION_REQUEST_CODE + 1);
        this.requestPermissions(new String[] { INTERNET }, PERMISSION_REQUEST_CODE + 2);

        new Thread(this, "Sensor Transmission Invocation Daemon").start();
    }

    @Override
    public void run() {
        while (true) {
            long t = System.currentTimeMillis();
            if (t - this.lastTransmission >= POLL_TIME) {
                this.lastTransmission = t;
                InputFrame buffer = this.currentFrame;
                this.currentFrame = new InputFrame();
                this.frameHandler.transmitFrame(buffer);
            } else {
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        switch (requestCode) {
            case PERMISSION_REQUEST_CODE:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    this.sensorManager = (SensorManager) this.getSystemService(this.getApplicationContext().SENSOR_SERVICE);
                    if (this.sensorManager == null) {
                        Log.e(TAG, "onCreate: Cannot get sensor manager");
                        Toast.makeText(this.getApplicationContext(), "Cannot get sensor manager", Toast.LENGTH_LONG).show();
                        break;
                    }

                    this.sensor = sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION);
                    if (this.sensor == null) {
                        Log.e(TAG, "onCreate: Cannot get sensor");
                        Toast.makeText(this.getApplicationContext(), "Cannot get sensor", Toast.LENGTH_LONG).show();
                        break;
                    }

                    this.sensorEventListener = new SensorEventListener() {
                        @Override
                        public void onAccuracyChanged(Sensor sensor, int accuracy) {
                            // don't care about this one
                        }

                        @Override
                        public void onSensorChanged(SensorEvent event) {
                            float[] values = event.values;
                            float xAngle = values[2];
                            float yAngle = -values[1];

                            if (Math.abs(xAngle) >= TRIGGER_ANGLE_X) {
                                if (xAngle < 0) currentFrame.addInput(MovementTypes.X_PLUS);
                                else currentFrame.addInput(MovementTypes.X_MINUS);
                            }

                            if (Math.abs(yAngle) >= TRIGGER_ANGLE_Y) {
                                if (yAngle < 0) currentFrame.addInput(MovementTypes.Y_PLUS);
                                else currentFrame.addInput(MovementTypes.Y_MINUS);
                            }

                            findViewById(R.id.left).setVisibility(currentFrame.isxMinus() ? View.VISIBLE : View.INVISIBLE);
                            findViewById(R.id.right).setVisibility(currentFrame.isxPlus() ? View.VISIBLE : View.INVISIBLE);
                            findViewById(R.id.up).setVisibility(currentFrame.isyPlus() ? View.VISIBLE : View.INVISIBLE);
                            findViewById(R.id.down).setVisibility(currentFrame.isyMinus() ? View.VISIBLE : View.INVISIBLE);
                        }
                    };

                    if (!this.sensorManager.registerListener(this.sensorEventListener, this.sensor, SensorManager.SENSOR_DELAY_GAME)) {
                        Log.e(TAG, "onCreate: Cannot request listener");
                        Toast.makeText(this.getApplicationContext(), "Cannot request listener", Toast.LENGTH_LONG).show();
                        break;
                    }
                } else {
                    Log.e(TAG, "onCreate: No permissions");
                    Toast.makeText(this.getApplicationContext(), "No permissions", Toast.LENGTH_LONG).show();
                    break;
                }
                break;
            default:
                break;
        }

        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

}
