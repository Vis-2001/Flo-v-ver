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
  int ret = test();
  printf("3)Function returns - %d\n", ret);
  //Function returns - 1
  return ret;
}
