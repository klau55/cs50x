#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string text);

int main(int argc, string argv[])
{
if (argc != 2 || !only_digits(argv[1]))
{
    printf ("shit found\n");
    return 1;
}
return 0;
}
bool only_digits(string text)
{
    for (int i = 0; i < strlen(text); i++)
    {
        if (!isdigit(text[i]))
        {
            printf ("same shit\n");
            return false;
        }
    }

}