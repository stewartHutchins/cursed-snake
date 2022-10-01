package uk.co.djpiper28.gyrosnake;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

public class InputFrame {
    private boolean xPlus;
    private boolean xMinus;
    private boolean yPlus;
    private boolean yMinus;

    public InputFrame() {
        this.xPlus = false;
        this.xMinus = false;
        this.yPlus = false;
        this.yMinus = false;
    }

    public void addInput(MovementTypes type) {
        switch(type) {
            case X_PLUS:
                this.xPlus = true;
                break;
            case X_MINUS:
                this.xMinus = true;
                break;
            case Y_PLUS:
                this.yPlus = true;
                break;
            case Y_MINUS:
                this.yMinus = true;
                break;
        }
    }

    public void transmitFrame(Api api) throws IOException {
        List<MovementTypes> things = new LinkedList<>();
        if (this.xPlus) things.add(MovementTypes.X_PLUS);
        if (this.xMinus) things.add(MovementTypes.X_MINUS);
        if (this.yPlus) things.add(MovementTypes.Y_PLUS);
        if (this.yMinus) things.add(MovementTypes.Y_MINUS);

        for (MovementTypes thing : things) {
            api.sendCommand(thing);
        }
    }

    public boolean isxPlus() {
        return xPlus;
    }

    public boolean isxMinus() {
        return xMinus;
    }

    public boolean isyPlus() {
        return yPlus;
    }

    public boolean isyMinus() {
        return yMinus;
    }
}
