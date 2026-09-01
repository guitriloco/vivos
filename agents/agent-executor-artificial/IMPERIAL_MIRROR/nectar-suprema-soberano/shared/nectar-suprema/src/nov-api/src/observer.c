#include <stdio.h>
#include "soup_log.h"

void nov_observe_soup(const SoupEntry *entry) {
    printf("[NOV OBSERVER] Received telemetry for: %s (Rating: %u)\n", entry->name, entry->rating);
    if (entry->rating < 3) {
        printf("[NOV OBSERVER] WARNING: Low rating detected! Potential anomaly.\n");
    }
}

int main() {
    printf("Nov Observer active.\n");
    // This is just a demonstration of the logic
    return 0;
}
