float pow(float base, int exponent)
{
  float res = 1;
  for(int i = 0; i<exponent; i++)
    res*=base;
  return res;
}
int factorial(int x)
{
  int res = 1;
  for(int i = 1; i<=x; i++)
    res*=i;
  return res;
}

float sine(float x)
{
  float res = 0;
  for(int i = 0; i<50; i++)
  {
    res += pow(-1,i)*pow(x,2*i+1)/factorial(2*i+1);
  }
  return res;
}

float main()
{
  float pi = 3.1415926535;
  return sine(pi/3);
}
