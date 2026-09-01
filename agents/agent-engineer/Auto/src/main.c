#include "soup_log.h"
#include "storage.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void print_usage(const char *prog_name) {
    printf("Usage: %s <command> [args]\n", prog_name);
    printf("Commands:\n");
    printf("  add <name> <rating> <notes>  Add a new soup tasting entry\n");
    printf("  list                         List all soup tasting entries\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    Storage storage;
    if (storage_open(&storage, "data/soups.dat") != 0) {
        fprintf(stderr, "Error: Could not open storage file.\n");
        return 1;
    }

    if (strcmp(argv[1], "add") == 0) {
        if (argc < 5) {
            printf("Usage: %s add <name> <rating> <notes>\n", argv[0]);
            storage_close(&storage);
            return 1;
        }

        SoupEntry entry;
        memset(&entry, 0, sizeof(SoupEntry));
        
        strncpy(entry.name, argv[2], MAX_NAME_LEN - 1);
        entry.rating = (uint8_t)atoi(argv[3]);
        strncpy(entry.notes, argv[4], MAX_NOTES_LEN - 1);

        time_t t = time(NULL);
        struct tm tm = *localtime(&t);
        snprintf(entry.date, sizeof(entry.date), "%04d-%02d-%02d", 
                 tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday);

        if (storage_add_entry(&storage, &entry) == 0) {
            printf("Entry added successfully.\n");
        } else {
            fprintf(stderr, "Error adding entry.\n");
        }
    } else if (strcmp(argv[1], "list") == 0) {
        int count = storage_list_entries(&storage);
        if (count < 0) {
            fprintf(stderr, "Error listing entries.\n");
        } else if (count == 0) {
            printf("No entries found.\n");
        }
    } else {
        print_usage(argv[0]);
    }

    storage_close(&storage);
    return 0;
}
