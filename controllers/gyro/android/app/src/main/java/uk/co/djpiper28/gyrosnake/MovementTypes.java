package uk.co.djpiper28.gyrosnake;

public enum MovementTypes {
    X_PLUS("x+"),
    X_MINUS("x-"),
    Y_PLUS("y+"),
    Y_MINUS("y-");

    private final String movementStr;

    private MovementTypes(String str) {
        this.movementStr = str;
    }

    public String getMovementStr() {
        return this.movementStr;
    }
}
