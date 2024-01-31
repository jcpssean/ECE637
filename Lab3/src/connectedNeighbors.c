#include <stdlib.h>
#include <stdio.h>
#include <math.h>

struct pixel {
    int m, n; // m=row, n=col
    };

void ConnectedNeighbors(
    struct pixel s, // location of the pixel s
    double T, // threshold
    unsigned char **img,
    int width,
    int height,
    int *M, // pointer to the number of neighbors connected to s
    struct pixel c[4] // array containing the M connected neighbors to the pixel s
    ) {
        unsigned char img_s = img[s.m][s.n];

        if (s.m != 0 && fabs(img[s.m-1][s.n] - img_s) <= T) {
            c[*M].m = s.m-1;
            c[*M].n = s.n;
            (*M)++;
        }
        if (s.n != 0 && fabs(img[s.m][s.n-1] - img_s) <= T) {
            c[*M].m = s.m;
            c[*M].n = s.n-1;
            (*M)++;
        }
        if (s.m != height-1 && fabs(img[s.m+1][s.n] - img_s) <= T) {
            c[*M].m = s.m+1;
            c[*M].n = s.n;
            (*M)++;
        }
        if (s.n != width-1 && fabs(img[s.m][s.n+1] - img_s) <= T) {
            c[*M].m = s.m;
            c[*M].n = s.n+1;
            (*M)++;
        }
    }


void ConnectedSet(
    struct pixel s, // seed s
    double T, // threshold
    unsigned char **img,
    int width,
    int height,
    int ClassLabel, // integer value used to label any pixel which is connected to s
    unsigned int **seg, // If a pixel is connected to s, then assign ClassLabel to seg[i][j]
    int *NumConPixels //number of pixels which were found to be connected to s (M)
    ) {
        *NumConPixels = 0; // Initialize the count of connected pixels

        // Initialize a list B
        struct pixel *B = malloc(width * height * sizeof(struct pixel));
        int B_size = 0;

        // Add s to B
        B[B_size++] = s;

        while (B_size > 0) {
            // Remove a pixel from B
            struct pixel current = B[--B_size];

            // If the current pixel is not yet labeled
            if (seg[current.m][current.n] == 0) {
                seg[current.m][current.n] = ClassLabel; // Label the current pixel
                (*NumConPixels)++; // Increase the count of connected pixels

                // Find connected neighbors
                int M = 0;
                struct pixel c[4];
                ConnectedNeighbors(current, T, img, width, height, &M, c);

                // Add connected and unlabeled neighbors to B
                for (int i = 0; i < M; i++) {
                    if (seg[c[i].m][c[i].n] == 0) {
                        B[B_size++] = c[i];
                    }
                }
            }
        }

        free(B); // Free the dynamic array used for B
    }

