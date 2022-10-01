package uk.co.djpiper28.gyrosnake;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

public class MainActivity extends AppCompatActivity {
    private FrameHandler frameHandler;
    private Api api;

    public MainActivity() {
        this.api = new Api(this.getApplicationContext());
        this.frameHandler = new FrameHandler(this.api);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}