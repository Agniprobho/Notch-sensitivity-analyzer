#include "notch.hh"
#include <cmath>

double alpha(double Su)
{
	double a=0.001*pow((300/Su),1.8);
	return a;
}

double nsp(double a, double r, int n)	//Peterson notch sensitivity: we are using for steel and steel alloys
{
	if (n==0)
		a*=25.4;
	double q=r/(r+a);
	return q;
}

double nsn(double rho, double r, int n)	//Neuber notch sensitivity: we are using for aluminium alloys
{
	if (n==0)
		rho*=25.4;
	double q=1/(1+pow((rho/r),0.5));
	return q;
}

double su_s(double alpha)
{
	double Su=300/pow((alpha/0.001),(1/1.8));
	return Su;
}

double su_a(double alpha)
{
	double Su;
	if (alpha==0.08)	//Aluminium Alloy 356.0 as cast
		Su=22;
	else if (alpha==0.025)	//Aluminium Alloy 6061
		Su=43;
	else if (alpha==0.015)	//Aluminium Alloy 7075
		Su=87;
	return Su;
}
