#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size

    int start;

do
{
    start = get_int ("Start population: ");
     if (start < 9)
        {
            printf ("*ERROR* Start size should be more than 9. Try again \n");
        }
}
while (start < 9);


    // TODO: Prompt for end size

    int end;
do
{
    end = get_int ("End population: ");
    if (end < start)
        {
            printf ("*ERROR* End size can't be lower than start size. Try again \n");
        }
}
while (start > end);

    // TODO: Calculate number of years until we reach threshold

    int years = 0;
    while (start < end)
    {
        start = start + (start/3) - (start/4);
    years++;
    }

    // TODO: Print number of years

    printf("Years: %d\n", years);
}
