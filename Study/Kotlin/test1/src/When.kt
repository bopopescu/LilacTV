fun main() {
    whenUsage(2, 50, "서울시")
}

fun whenUsage(inputType: Int, score: Int, city: String) {
    when (inputType) {
        1 -> println("Type-1")
        2,3 -> println("Type-2,3")
        else -> {
            println("Undefined")
        }
    }

    when (inputType) {
        checkInputType(inputType) -> {
            println("Type is OK.")
        }
        else -> {
            print("Type is not OK.")
        }
    }

    val start = 0
    val end = 100
    when (score) {
        in start..(end/4) -> println("우수함")
        50 -> println("평균임")
        in start..end -> println("범위안에 있음")
        else -> println("범위를 벗어남")
    }

    val isSeoul = when (city) {
        is String -> city.startsWith("서울")
        else -> false
    }
    println(isSeoul)

    when {
        city.length == 0 -> println("도시명을 입력하세요")
        city.substring(0,2).equals("서울") -> println("서울이군요")
        else -> println(city)
    }
}

fun checkInputType(inputType: Int): Int{
    if (inputType >= 1 && inputType < 3) {
        return inputType
    }
    return -1
}