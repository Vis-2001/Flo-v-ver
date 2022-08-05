#define DIM 3

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
