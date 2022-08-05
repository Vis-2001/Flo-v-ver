float pow(float base, int exponent)
{
  float res = 1;
  for(int i = 0; i<exponent; i++)
    res*=base;
  return res;
}
float inverse()
{
  float a[3][3];
float inv[3][3];
float determinant=0;
for(int i=0;i<3;i++)
    for(int j=0;j<3;j++)
         a[i][j]=pow(i+j,5);
for(int i=0;i<3;i++)
    determinant = determinant + (a[0][i]*(a[1][(i+1)%3]*a[2][(i+2)%3] - a[1][(i+2)%3]*a[2][(i+1)%3]));
 for(int i=0;i<3;i++)
    for(int j=0;j<3;j++)
         inv[j][i]=((a[(i+1)%3][(j+1)%3] * a[(i+2)%3][(j+2)%3]) - (a[(i+1)%3][(j+2)%3]*a[(i+2)%3][(j+1)%3]))/ determinant;
 float cal=0;
 for(int i=0;i<3;i++)
 {
  cal+=inv[i][i];
 }
 return cal;
}
