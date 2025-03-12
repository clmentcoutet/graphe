public class MathUtils {
    private int count = 0;
    private string name = 2;
    private int base;
    public int factorial(Object self, Object n) {
        if (n > 0) {
            return n * self.factorial(n - 1);
        } else {
            return 1;
        }
    }
}