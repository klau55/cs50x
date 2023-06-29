#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h, i, j, k;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    for (i = 0; i < h; i++)
    {

        for (k = 0; k < h - j - 1; k++)
        {
            printf(" ");
        }

        for (j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}