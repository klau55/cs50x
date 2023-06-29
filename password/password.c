// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    bool checkupper, checklower, checknumber, checkspecial = false;

    for (int i = 0; i < strlen(password); i++)
    {
        if (isupper(password[i]))
        {
            checkupper = true;
        }

        if (islower(password[i]))
        {
            checklower = true;
        }

        if (isdigit(password[i]))
        {
            checknumber = true;
        }

        if (!isalnum(password[i]))
        {
            checkspecial = true;
        }
    }
    if (checkupper &&  checklower && checknumber && checkspecial == true)
    {
        return true;
    }

    else
    {
        return false;
    }
}
