#ifndef SOUP_LOG_H
#define SOUP_LOG_H

#include <stdio.h>

#define MAX_NAME_LEN 256
#define MAX_NOTES_LEN 512

typedef struct {
    int id;
    char name[MAX_NAME_LEN];
    unsigned int rating;
    char date[16];
    char notes[MAX_NOTES_LEN];
} SoupEntry;

static inline void print_soup_entry(const SoupEntry *entry) {
    printf("[SOUP] ID: %d, Name: %s, Rating: %u, Date: %s, Notes: %s\n",
           entry->id, entry->name, entry->rating, entry->date, entry->notes);
}

#endif // SOUP_LOG_H
