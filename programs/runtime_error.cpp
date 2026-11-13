#include <iostream>
using namespace std;

int divide(int a, int b) {
    return a / b;
}

int main() {
    cout << divide(10, 2) << endl;
    cout << divide(1, 0) << endl;
    return 0;
}
