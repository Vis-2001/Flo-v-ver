
void testfn(int, int);

int inint = 2;
int gint = 4*inint;

inline int test(unsigned static int arg, register float test)
{
  printf("h");
  {
    int d = 2;
    d = 2;
    d++;
  }
  int c = 2*arg++;
  d++;
}

void print()
{
  printf("Test %d %d", 5, 7*76);
}

int main()
{
  int var = 3;
  printf("Hello World");
  test(3,5.68);
  print();
}
