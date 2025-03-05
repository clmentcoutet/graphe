class MathUtils {
    let count : Number = 0
    let name : string = 2
    let base : Number

    function factorial(self, n) : Number {
        if (n > 0) {
            return n * self.factorial(n - 1)
        }
        else {
            return 1
        }
    }