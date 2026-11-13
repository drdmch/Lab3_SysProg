#include <iostream>
using namespace std;

// сума чисел, факторіал і парні-непарні
int factorial(int n) {
    int res = 1;
    while (n > 1) {
        res = res * n;
        n--;
    }
    return res;
}

int main() {
    int sum = 0;
    for (int i = 1; i <= 10; i++)
        sum = sum + i;
    cout << "sum(1..10) = " << sum << endl;
    cout << "5! = " << factorial(5) << endl;

    int k = 0;
    while (k < 5) {
        if (k % 2 == 0)
            cout << k << " - парне" << endl;
        else
            cout << k << " - непарне" << endl;
        k++;
    }
    return 0;
}
