#include "soup_log.h"
#include <stdio.h>

void print_soup_entry(const SoupEntry *entry) {
    printf("[%u] %s\n", entry->id, entry->name);
    printf("    Rating: %u/5\n", entry->rating);
    printf("    Date:   %s\n", entry->date);
    printf("    Notes:  %s\n", entry->notes);
    printf("---------------------------\n");
}
