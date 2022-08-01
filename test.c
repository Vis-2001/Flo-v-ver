#include<stdio.h>
#define MAX_VAL 10
void testfn(int, int);

float intint = 2.6;
float global_int = 2.65;

int global_arr[] = {1,2,3,4,5,6};

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
  int arrmultidim[10][10];
  for(int i = 0; i<10;i++)
  for(int j = 0; j<10;j++)
    arrmultidim[i][j]=i+j;
  int var = 3.6;
  printf("Hello World");
  float a = test(var,8.687);
  int i = 9-arr[7];
  for(int j = 0; j<i; j++)
    a+=0.1;
  print();
  printf("%f\n", a);
  return a;
}
