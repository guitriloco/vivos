#include "soup_log.h"
#include <stdio.h>

static SoupObserver global_observer = NULL;

void set_soup_observer(SoupObserver observer) {
    global_observer = observer;
}

void print_soup_entry(const SoupEntry *entry) {
    if (global_observer) {
        global_observer(entry);
    }
    printf("[%u] %s\n", entry->id, entry->name);
    printf("    Rating: %u/5\n", entry->rating);
    printf("    Date:   %s\n", entry->date);
    printf("    Notes:  %s\n", entry->notes);
    printf("---------------------------\n");
}
