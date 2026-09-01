#ifndef SOUP_LOG_H
#define SOUP_LOG_H

#include <stdint.h>

#define MAX_NAME_LEN 64
#define MAX_NOTES_LEN 256

typedef struct {
    uint32_t id;
    char name[MAX_NAME_LEN];
    uint8_t rating; // 1-5
    char date[16];  // YYYY-MM-DD
    char notes[MAX_NOTES_LEN];
} SoupEntry;

void print_soup_entry(const SoupEntry *entry);

#endif // SOUP_LOG_H
