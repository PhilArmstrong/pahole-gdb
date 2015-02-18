#include <iostream>
#include <vector>
#include <algorithm>

class C {
    int i;
    char j;
    void *l;
public:
    C()
    : i(65), j(65), l(0)
    { }
    int geti() { return i; }
    char getj() { return j; }
    void * getl() { return l; }
};

using namespace std;

int main() {
  // If we don’t do something with C, the compiler won’t include it.
  vector<C> cs(5);
  for(auto c: cs) {
    cout << c.geti() << " ";
  }
  cout << endl;
  return 0;
}
