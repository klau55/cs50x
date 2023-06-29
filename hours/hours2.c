#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

float calc_hours (int hours[], int weeks, char totalavg);
int main (void)
{
    int weeks = get_int("Specify amount of weeks: ");
    int hours[weeks];
    for (int i = 0; i < weeks; i++)
    {
        hours[i] = get_int("Specify amount of hours on week %i: ", i);
    }

    printf ("%i hours[1] %i weeks\n", hours[2], weeks);



}