#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "timer.h"
#include "files.h"
#include <cuda_runtime.h>

#define SOFTENING 1e-9f

/*
 * Each body contains x, y, and z coordinate positions,
 * as well as velocities in the x, y, and z directions.
 */

typedef struct { float x, y, z, vx, vy, vz; } Body;

/*
 * CUDA kernel to calculate the gravitational impact of all bodies in the system
 * on all others.
 */

__global__ void bodyForceKernel(Body *p, float dt, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        float Fx = 0.0f; float Fy = 0.0f; float Fz = 0.0f;
        float xi = p[i].x, yi = p[i].y, zi = p[i].z;

        for (int j = 0; j < n; j++) {
            float dx = p[j].x - xi;
            float dy = p[j].y - yi;
            float dz = p[j].z - zi;
            float distSqr = dx*dx + dy*dy + dz*dz + SOFTENING;
            float invDist = rsqrtf(distSqr);
            float invDist3 = invDist * invDist * invDist;

            Fx += dx * invDist3; Fy += dy * invDist3; Fz += dz * invDist3;
        }

        p[i].vx += dt*Fx; p[i].vy += dt*Fy; p[i].vz += dt*Fz;
    }
}

/*
 * CUDA kernel to integrate positions
 */

__global__ void integratePositionKernel(Body *p, float dt, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        p[i].x += p[i].vx*dt;
        p[i].y += p[i].vy*dt;
        p[i].z += p[i].vz*dt;
    }
}

int main(const int argc, const char** argv) {

    // The assessment will test against both 2<11 and 2<15.
    // Feel free to pass the command line argument 15 when you generate ./nbody report files
    int nBodies = 2<<11;
    if (argc > 1) nBodies = 2<<atoi(argv[1]);

    // The assessment will pass hidden initialized values to check for correctness.
    // You should not make changes to these files, or else the assessment will not work.
    const char * initialized_values;
    const char * solution_values;

    if (nBodies == 2<<11) {
        initialized_values = "09-nbody/files/initialized_4096";
        solution_values = "09-nbody/files/solution_4096";
    } else { // nBodies == 2<<15
        initialized_values = "09-nbody/files/initialized_65536";
        solution_values = "09-nbody/files/solution_65536";
    }

    if (argc > 2) initialized_values = argv[2];
    if (argc > 3) solution_values = argv[3];

    const float dt = 0.01f; // Time step
    const int nIters = 10;  // Simulation iterations

    int bytes = nBodies * sizeof(Body);
    float *buf;

    buf = (float *)malloc(bytes);

    Body *p = (Body*)buf;

    read_values_from_file(initialized_values, buf, bytes);

    // Allocate device memory
    Body *d_p;
    cudaMalloc((void**)&d_p, bytes);
    cudaMemcpy(d_p, p, bytes, cudaMemcpyHostToDevice);

    double totalTime = 0.0;

    // Define block size and grid size
    int blockSize = 256;
    int gridSize = (nBodies + blockSize - 1) / blockSize;

    for (int iter = 0; iter < nIters; iter++) {
        StartTimer();

        // Launch bodyForce kernel
        bodyForceKernel<<<gridSize, blockSize>>>(d_p, dt, nBodies);

        // Launch integratePosition kernel
        integratePositionKernel<<<gridSize, blockSize>>>(d_p, dt, nBodies);

        cudaDeviceSynchronize(); // Ensure kernels complete before timing

        const double tElapsed = GetTimer() / 1000.0;
        totalTime += tElapsed;
    }

    // Copy results back to host
    cudaMemcpy(p, d_p, bytes, cudaMemcpyDeviceToHost);

    double avgTime = totalTime / (double)(nIters);
    float billionsOfOpsPerSecond = 1e-9 * nBodies * nBodies / avgTime;
    write_values_to_file(solution_values, buf, bytes);

    printf("%0.3f Billion Interactions / second\n", billionsOfOpsPerSecond);

    // Free device memory
    cudaFree(d_p);
    free(buf);

    return 0;
}