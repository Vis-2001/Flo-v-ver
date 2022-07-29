#define MAX_VAL 10
void testfn(int, int);

float inint = 2.6;
float gint = 2.65;

int garr[] = {1,2,3,4,5,6};

float test(float arg, float test)
{
  printf("h");
  {
    int d = 2;
    d++;
  }
  float c = arg+++test;
  return c;
}

void print()
{
  printf("Test %d %d", 5, 7*76);
}

float main()
{
  int arr[MAX_VAL] = {1,2,3,4};
  for(int j = 0; j<10;j++)
    arr[j]=j;
  int var = 3.6;
  printf("Hello World");
  float a = test(var,8.68);
  int i = 9-arr[7];
  switch(i)
  {
    case 0:
          break;
    case 1:
          a++;
          break;
    case 2:
          a+=2;
    case 3:
          a+=3;
          break;
    default:
          a+=4;
  }
  print();
  return a;
}
