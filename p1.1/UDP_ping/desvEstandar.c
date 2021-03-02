#include <math.h>

long double desvEstandar(long double datos[], long double media, int cantidad)
{
  long double resultado = 0, var = 0;
  for(int y = 0; y < cantidad; y++)
    var += pow((datos[y] - media) ,2);
  var = var/cantidad;
  resultado = sqrt(var);
  return resultado;
}