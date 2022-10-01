package uk.co.djpiper28.gyrosnake.vectmaths;

public class VectorMaths {
    private VectorMaths() {

    }

    public static float abs(float []vect) {
        float ret = 0;
        for (float v : vect) {
            ret += v * v;
        }

        return (float) Math.sqrt(ret);
    }
}
