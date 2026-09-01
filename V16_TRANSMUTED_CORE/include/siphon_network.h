#ifndef SIPHON_NETWORK_H
#define SIPHON_NETWORK_H

#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <fcntl.h>
#include <cstring>
#include <iostream>

// Simulation of a high-speed network capture interface
class HighPerformanceSocket {
public:
    HighPerformanceSocket(int port) : port(port) {
        sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        if (sockfd < 0) {
            perror("socket");
        }

        // Set non-blocking
        int flags = fcntl(sockfd, F_GETFL, 0);
        fcntl(sockfd, F_SETFL, flags | O_NONBLOCK);

        struct sockaddr_in servaddr;
        memset(&servaddr, 0, sizeof(servaddr));
        servaddr.sin_family = AF_INET;
        servaddr.sin_addr.s_addr = INADDR_ANY;
        servaddr.sin_port = htons(port);

        if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
            perror("bind");
        }
    }

    ~HighPerformanceSocket() {
        if (sockfd >= 0) close(sockfd);
    }

    // Capture the next price update from the wire
    bool poll_price(double& price) {
        char buffer[1024];
        ssize_t n = recv(sockfd, buffer, sizeof(buffer), 0);
        if (n > 0) {
            // In a real eBPF/Bare-metal scenario, we'd parse the raw packet header here
            // For this transmuted core, we'll assume a simple binary float for speed
            if (n >= sizeof(double)) {
                memcpy(&price, buffer, sizeof(double));
                return true;
            }
        }
        return false;
    }

private:
    int sockfd;
    int port;
};

#endif // SIPHON_NETWORK_H
