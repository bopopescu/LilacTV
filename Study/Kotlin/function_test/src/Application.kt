//fun foo(fooProgram: String){
//    val outFunction = "Value"
//    fun bar(barProgram: String) {
//        println(barProgram)
//        println(fooProgram)
//        println(outFunction)
//    }
//    bar(outFunction)
//}

//fun String.lastChar() = this.get(this.length - 1)

//High Order Function
//fun operation(x: Int, y: Int, op: (Int, Int) -> Int): Int {
//    println("op is executed > $op")
//    return op(x, y)
//}

//class someClass{
//    fun sum(x: Int, y: Int) = x + y
//}
//fun sum(x: Int, y: Int) = x + y


fun unaryOperation(x: Int, op: (Int) -> (Int)): Int{
    println("x is $x, op is $op")
    return op(x)
}

fun outsideFunction() {
    for(number in 1..30){
        println(number)
        unaryOperation(x = 20){
            it * number
        }
    }
}

fun main(args: Array<String>) {
//    var someString = "abcd"
//    println(someString.lastChar())

//    println(operation(1, 2, someClass()::sum))
//    println(operation(1, 2, ::sum))

//    val sum = {x: Int, y: Int -> x + y}
//    println(sum(1,2))

//    val string = "one, two, three"
//    println(string.filter { c: Char -> c in 'a'..'z' })
//    println(string.filter { it in 'a'..'z' })

    outsideFunction()
}