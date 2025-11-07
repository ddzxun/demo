package main

import "fmt"

func A() {
	defer fmt.Println("defer in A")
	fmt.Println("A start")
	B1()
	fmt.Println("A end") // 不会执行
}

func B() {
	defer fmt.Println("defer in B")
	fmt.Println("B start")
	C()
	fmt.Println("B end") // 不会执行
}

func B1() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("Recovered in B:", r)
		}
	}()
	defer fmt.Println("defer in B")
	fmt.Println("B start")
	C()
	fmt.Println("B end") // 不执行
}

func C() {
	defer fmt.Println("defer in C")
	fmt.Println("C start")
	panic("panic in C")
	fmt.Println("C end") // 不会执行
}

func main() {
	defer fmt.Println("defer in main")
	fmt.Println("main start")
	A()
	fmt.Println("main end") // 不会执行
}
