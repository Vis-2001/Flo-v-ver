#define DIM 3

float doppler(float vel, float freq)
{
  float c = 346.13;
  float resfreq = (c*freq)/(c+vel);
  return resfreq;
}

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

float determinant()
{
  float det = 0;
  float arr1[DIM][DIM];
  for(int i = 0; i<DIM; i++)
    for(int j = 0; j<DIM; j++)
      arr1[i][j] = pow(j,i);

  for(int i=0;i<3;i++)
       det = det + (arr1[0][i]*(arr1[1][(i+1)%3]*arr1[2][(i+2)%3] - arr1[1][(i+2)%3]*arr1[2][(i+1)%3]));
  return det;
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
  //return doppler(9.8, 100);
  //return determinant();
  return sine(pi/3);
}
