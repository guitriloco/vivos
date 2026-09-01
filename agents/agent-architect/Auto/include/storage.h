#ifndef STORAGE_H
#define STORAGE_H

#include "soup_log.h"
#include <stdio.h>

typedef struct {
    FILE *file;
    char *filename;
} Storage;

int storage_open(Storage *storage, const char *filename);
int storage_add_entry(Storage *storage, const SoupEntry *entry);
int storage_list_entries(Storage *storage);
void storage_close(Storage *storage);

#endif // STORAGE_H
