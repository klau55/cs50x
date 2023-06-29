#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

char rotate(char p, int k);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int i = 0; i < strlen(argv[1]); i++)
    {

        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int k = atoi(argv[1]);
    string plaintext = get_string("plaintext: ");
    int textlength = strlen(plaintext);
    char ciphertext[textlength + 1];

    for (int j = 0; j < textlength; j++)
    {
        ciphertext[j] = rotate(plaintext[j], k);
    }

    ciphertext[textlength] = '\0';
    printf("ciphertext: %s\n", ciphertext);
}

char rotate(char p, int k)
{
    char ci, c;
    if (isupper(p))
    {
        ci = ((p - 65) + k) % 26;
        c = ci + 65;
    }
    else if (islower(p))
    {
        ci = ((p - 97) + k) % 26;
        c = ci + 97;
    }
    else
    {
        return p;
    }
    return c;
}

