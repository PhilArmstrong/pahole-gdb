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

extern "C" {
  typedef struct {
    short a;
    char b;
    struct more_struct {
      union union_x
      {
        char c[128];
        struct s_y
        {
          char v;
          char g1_1:7;
        } y;
      } x;
      long e;
      char s1_1:1;
      char s1_2:1;
      char s2:2;
    } more;
  } testStruct;
}

using namespace std;

int main() {
  // If we don’t do something with C, the compiler won’t include it.
  vector<C> cs(5);
  for(auto c: cs) {
    cout << c.geti() << " ";
  }
  cout << endl;

  testStruct a;
  a.a = 100;
  cout << a.a << endl;
  return 0;
}
