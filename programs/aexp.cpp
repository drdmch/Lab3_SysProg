#include <iostream>
using namespace std;

// арифметичні вирази та пріоритет операцій
int main() {
    int a = 7;
    int b = 2;
    double x = 2.5;

    cout << "a + b * 3 = " << a + b * 3 << endl;
    cout << "(a + b) * 3 = " << (a + b) * 3 << endl;
    cout << "a / b = " << a / b << endl;
    cout << "a % b = " << a % b << endl;
    cout << "-a / b = " << -a / b << endl;
    cout << "x * 2 + 1 = " << x * 2 + 1 << endl;
    cout << "a > b && b > 0: " << (a > b && b > 0) << endl;
    return 0;
}
