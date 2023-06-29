// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 46;
int counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hashnumber = hash(word);
    node *cursor = table[hashnumber];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    return sizeof(word);

    // TODO: Improve this hash function
    //return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO

    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("dictionary loading error\n");
        return false;
    }
    char word[LENGTH + 1];
    while ((fscanf(file, "%s", word)) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);
        int hashnumber = hash(word);

      //  if (table[hashnumber] == NULL)
      //  {
      //      n->next = NULL;
      //  }
     //   else
      //  {
        n->next = table[hashnumber];
     //   }
        table[hashnumber] = n;
        counter++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    for (int i = 0; i < N; i++)
    {

    node *cursor = table[i];
    node *tmp = table[i];

    while (cursor != NULL)
    {
    cursor = cursor->next;
    free (tmp);
    tmp = cursor;
    }
    }

    return true;
}
