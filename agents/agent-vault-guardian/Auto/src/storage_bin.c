#include "storage.h"
#include <stdlib.h>
#include <string.h>

int storage_open(Storage *storage, const char *filename) {
    storage->filename = strdup(filename);
    storage->file = fopen(filename, "ab+");
    if (!storage->file) {
        return -1;
    }
    return 0;
}

int storage_add_entry(Storage *storage, const SoupEntry *entry) {
    if (!storage->file) return -1;
    
    // Auto-increment ID based on file size
    fseek(storage->file, 0, SEEK_END);
    long size = ftell(storage->file);
    SoupEntry entry_to_write = *entry;
    entry_to_write.id = (uint32_t)(size / sizeof(SoupEntry)) + 1;

    if (fwrite(&entry_to_write, sizeof(SoupEntry), 1, storage->file) != 1) {
        return -1;
    }
    fflush(storage->file);
    return 0;
}

int storage_list_entries(Storage *storage) {
    if (!storage->file) return -1;

    rewind(storage->file);
    SoupEntry entry;
    int count = 0;
    while (fread(&entry, sizeof(SoupEntry), 1, storage->file) == 1) {
        print_soup_entry(&entry);
        count++;
    }
    return count;
}

void storage_close(Storage *storage) {
    if (storage->file) {
        fclose(storage->file);
        storage->file = NULL;
    }
    if (storage->filename) {
        free(storage->filename);
        storage->filename = NULL;
    }
}
