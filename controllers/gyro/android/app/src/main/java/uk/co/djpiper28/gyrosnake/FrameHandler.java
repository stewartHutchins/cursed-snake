package uk.co.djpiper28.gyrosnake;

import java.io.IOException;
import java.util.LinkedList;
import java.util.Queue;

public class FrameHandler implements Runnable {
    private final static int MAX_FRAMES = 20;
    private Api api;
    private Queue<InputFrame> frameQueue;

    public FrameHandler(Api api) {
        this.api = api;
        this.frameQueue = new LinkedList<>();
        new Thread(this, "Frame Transmission Thread").start();
    }

    public void transmitFrame(InputFrame frame) {
        this.addFrame(frame);
    }

    private synchronized void addFrame(InputFrame frame) {
        this.frameQueue.add(frame);
        while (this.frameQueue.size() > MAX_FRAMES) {
            try {
                this.frameQueue.remove();
            } catch(Exception nothingQueueInQueueProbably) {
                nothingQueueInQueueProbably.printStackTrace();
            }
        }
    }

    private synchronized InputFrame getFrame() {
        try {
            return this.frameQueue.remove();
        } catch(Exception nothingQueueInQueueProbably) {
            //nothingQueueInQueueProbably.printStackTrace();
        }

        return null;
    }

    @Override
    public void run() {
        while (true) {
            InputFrame frame = this.getFrame();
            if (frame == null) {
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            } else {
                try {
                    frame.transmitFrame(this.api);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

}
