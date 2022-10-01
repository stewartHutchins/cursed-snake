package uk.co.djpiper28.gyrosnake.vectmaths;

public class VectorMaths {
    private VectorMaths() {

    }

    public static float getXAngle(float[] vect) {
        // ( a · b ) / |a| |b| = cos ð
        // arccos ((a · b) / |a| |b|) = ð
        // a = [ x, y , z ]
        // b = [ 1, 0, 0 ]

        float aDotB = vect[1];
        float modAModB = abs(vect);

        return (float) (Math.acos(aDotB/modAModB) - Math.PI / 2);
    }

    public static float getYAngle(float []vect) {
        // ( a · b ) / |a| |b| = cos ð
        // arccos ((a · b) / |a| |b|) = ð
        // a = [ x, y , z]
        // b = [ 0, 1, 0]

        float aDotB = vect[0];
        float modAModB = abs(vect);

        return (float) (Math.acos(aDotB/modAModB) - Math.PI / 2);
    }

    public static float abs(float []vect) {
        float ret = 0;
        for (float v : vect) {
            ret += v * v;
        }

        return (float) Math.sqrt(ret);
    }
}
