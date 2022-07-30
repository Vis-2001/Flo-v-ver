#include<stdio.h>
float test()
{
  float a = 0;
  for(int i = 0; i<50;i++)
  {
    a+=0.1;
  }
  if(a == 5)
    return 1;
  else
    return 0;

}

float main()
{

  for(double d = 0; d != 0.3; d += 0.1)
    printf("1)Value of variable d = %lf\n", d);
    /*1)Value of variable d = 0.0
      1)Value of variable d = 0.1
      1)Value of variable d = 0.2
    */

  double d = 0;
  while(d!=0.8)
  {
    printf("2)Value of variable d = %lf\n", d);
    d += 0.1;
  }
  /*2)Value of variable d = 0.0
    2)Value of variable d = 0.1
    2)Value of variable d = 0.2
    ..
    ..
    2)Value of variable d = 0.7
  */

  int ret = test();
  printf("3)Function returns - %d\n", ret);
  //Funcruon returns - 1
  return ret;
}
