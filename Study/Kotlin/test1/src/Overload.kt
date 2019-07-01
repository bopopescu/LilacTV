fun main() {
    val m1 = Score(100,200)
    var m2 = Score(100,200)
    println(m1 + m2)
    println(m1 * m2)
    println(m1 == m2)
    println(m1 === m2)
    println(m1.equals(m2))
}
data class Score (val a: Int, val b: Int){
    operator fun plus(other: Score): Score {
        return Score(a + other.a, b + other.b)
    }
}
operator fun Score.times(other: Score): Score {
    return Score(a * other.a, b * other.b)
}