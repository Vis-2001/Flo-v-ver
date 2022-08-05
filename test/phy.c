
float doppler(float vel, float freq)
{
  float c = 346.13;
  float resfreq = (c*freq)/(c+vel);
  return resfreq;
}


float main()
{
  return doppler(9.8, 100);
}
