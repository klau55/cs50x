#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{


    typedef uint8_t BYTE;
    int BLOCK_SIZE = 512;
    int count = 0;
    BYTE buffer[BLOCK_SIZE];
    FILE *img = NULL;
    char *filename = malloc(8);

    if (argc != 2 || argv[1] == NULL)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *raw_file = fopen(argv[1], "r");

    // найди тут проблему с рид
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)
                // ili kaunt = 0?
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "w");
            count++;
        }
        if (img != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, img);
        }

    }
    fclose(raw_file);
    if (img != NULL)
    {
        fclose(img);
        free(filename);
        return 0;
    }
}