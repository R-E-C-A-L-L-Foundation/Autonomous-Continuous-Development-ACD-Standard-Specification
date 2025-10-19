/**
 * ACD Specification - Example: Using ai_metadata.h Header
 * 
 * Copyright (C) 2025 Timothy Deters / R.E.C.A.L.L. Foundation
 * 
 * This file is part of the ACD Specification.
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 * 
 * For commercial licensing inquiries, contact the R.E.C.A.L.L. Foundation.
 * Patent Pending: U.S. Application No. 63/898,838
 * 
 * ---
 * 
 * This example demonstrates the ACD metadata format in C/C++ source code.
 * The ai_metadata.h header provides reference constants and optionally
 * a runtime API for working with ACD metadata.
 * 
 * Reference: ACD Standard Specification v1.0, Part 1 (SCIS)
 */

#include "../src/ai_metadata.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Generic API type definitions
typedef int api_error_t;
typedef void* api_stream_t;

// Error codes
#define API_SUCCESS 0
#define API_ERROR_INVALID_VALUE -1
#define API_ERROR_MEMORY_ALLOCATION -2
#define API_ERROR_NOT_IMPLEMENTED -3


/* Example 1: Simple device query function */
/*
 * AI_PHASE: DEVICE_QUERY
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: LOW
 * AI_NOTE: Queries the number of available devices
 * AI_DEPENDENCIES: INIT_HOOKS
 */
int getDeviceCount(int* count) {
    if (count == NULL) {
        return API_ERROR_INVALID_VALUE;
    }
    
    // Mock implementation - in real code, this would query the backend
    *count = 1;
    return API_SUCCESS;
}


/* Example 2: Device properties query */
/*
 * AI_PHASE: DEVICE_QUERY
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: MEDIUM
 * AI_NOTE: Retrieves device properties with backend translation
 * AI_DEPENDENCIES: INIT_HOOKS, ERROR_HANDLING
 * SOURCE_API_REF: getDeviceProperties(int device) - generic_api.h
 * TARGET_API_REF: backendGetDeviceProperties(int device) - backend_api.h
 */
int getDeviceProperties(int device) {
    if (device < 0) {
        return API_ERROR_INVALID_VALUE;
    }
    
    // Mock implementation
    printf("Device %d properties queried\n", device);
    return API_SUCCESS;
}


/* Example 3: Complex kernel launch */
/*
 * AI_PHASE: KERNEL_DISPATCH
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: HIGH
 * AI_NOTE: Launches kernel with dynamic shared memory and grid configuration
 * AI_DEPENDENCIES: STREAM_TRANSLATION, MEMORY_TRANSLATION, DEVICE_QUERY
 * AI_COMMIT: f9a8b7c
 * AI_COMMIT_HISTORY: d6e5f4c, a3b2c1d
 * AI_PATTERN: KERNEL_LAUNCH_V1
 * AI_STRATEGY: Direct translation with parameter validation and error handling
 * SOURCE_API_REF: launchKernel(func, grid, block, args, sharedMem, stream) - generic_api.h
 * TARGET_API_REF: backendLaunchKernel(func, grid, block, args, sharedMem, stream) - backend_api.h
 */
int launchKernel(void* func, int gridX, int gridY, int gridZ,
                 int blockX, int blockY, int blockZ,
                 void** args, size_t sharedMem, api_stream_t stream) {
    if (func == NULL) {
        return API_ERROR_INVALID_VALUE;
    }
    
    if (gridX <= 0 || gridY <= 0 || gridZ <= 0 ||
        blockX <= 0 || blockY <= 0 || blockZ <= 0) {
        return API_ERROR_INVALID_VALUE;
    }
    
    // Mock implementation
    printf("Kernel launched: grid(%d,%d,%d) block(%d,%d,%d) sharedMem=%zu\n",
           gridX, gridY, gridZ, blockX, blockY, blockZ, sharedMem);
    return API_SUCCESS;
}


/* Example 4: Partial implementation */
/*
 * AI_PHASE: GRAPH_TRANSLATION
 * AI_STATUS: PARTIAL
 * AI_COMPLEXITY: CRITICAL
 * AI_NOTE: Graph capture implementation in progress - basic structure only, missing node optimization
 */
int captureGraphBegin(void** graph, api_stream_t stream) {
    if (graph == NULL) {
        return API_ERROR_INVALID_VALUE;
    }
    
    // TODO: Implement full graph capture logic
    printf("Graph capture begin (PARTIAL IMPLEMENTATION)\n");
    return API_ERROR_NOT_IMPLEMENTED;
}


/* Example 5: Not started implementation */
/*
 * AI_PHASE: GRAPH_TRANSLATION
 * AI_STATUS: NOT_STARTED
 * AI_COMPLEXITY: HIGH
 * AI_NOTE: Placeholder for graph instantiation - requires graph capture to be completed first
 */
int instantiateGraph(void* graph) {
    if (graph == NULL) {
        return API_ERROR_INVALID_VALUE;
    }
    
    printf("Graph instantiation not implemented yet\n");
    return API_ERROR_NOT_IMPLEMENTED;
}


/* Example 6: Recently fixed with error context */
/*
 * AI_PHASE: STREAM_TRANSLATION
 * AI_STATUS: FIXED
 * AI_COMPLEXITY: MEDIUM
 * AI_NOTE: Stream synchronization with proper error handling
 * AI_DEPENDENCIES: INIT_HOOKS, ERROR_HANDLING
 * AI_COMMIT: c9d8e7f
 * AI_COMMIT_HISTORY: b8c7d6e, a7b6c5d
 * AI_PATTERN: STREAM_SYNC_V2
 * AI_CHANGE: Fixed race condition in stream synchronization
 * RUNTIME_ERR: Segmentation fault on NULL stream handle
 * FIX_REASON: Added NULL check before dereferencing stream handle
 * HUMAN_OVERRIDE: Reviewed by T. Deters on 2025-10-19
 * SOURCE_API_REF: synchronizeStream(stream) - generic_api.h
 * TARGET_API_REF: backendStreamSynchronize(stream) - backend_api.h
 */
int synchronizeStream(api_stream_t stream) {
    // Fixed: Added NULL check
    if (stream == NULL) {
        return API_ERROR_INVALID_VALUE;
    }
    
    // Mock implementation
    printf("Stream synchronized\n");
    return API_SUCCESS;
}


/* Example 7: Async memory operation */
/*
 * AI_PHASE: MEMORY_TRANSLATION
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: HIGH
 * AI_NOTE: Asynchronous memory copy with stream management and error handling
 * AI_DEPENDENCIES: INIT_HOOKS, ERROR_HANDLING, STREAM_TRANSLATION, DEVICE_QUERY
 * AI_COMMIT: e8f7a6b
 * AI_COMMIT_HISTORY: d7e6f5a, c6d5e4f
 * AI_PATTERN: ASYNC_MEMCPY_V1
 * AI_STRATEGY: Convert API stream to backend stream, validate parameters, perform async copy
 * SOURCE_API_REF: copyMemoryAsync(dst, src, size, kind, stream) - generic_api.h
 * TARGET_API_REF: backendMemcpyAsync(dst, src, size, kind, stream) - backend_api.h
 */
int copyMemoryAsync(void* dst, const void* src, size_t size,
                    int kind, api_stream_t stream) {
    if (dst == NULL || src == NULL || size == 0) {
        return API_ERROR_INVALID_VALUE;
    }
    
    if (stream == NULL) {
        return API_ERROR_INVALID_VALUE;
    }
    
    // Mock implementation
    printf("Async memory copy: %zu bytes (kind=%d)\n", size, kind);
    return API_SUCCESS;
}


/* Example 8: Distributed agent coordination */
/*
 * AI_PHASE: PEER_MEMORY_ACCESS
 * AI_STATUS: PARTIAL
 * AI_COMPLEXITY: CRITICAL
 * AI_NOTE: Peer-to-peer memory access implementation in progress by distributed agent
 * AI_DEPENDENCIES: DEVICE_QUERY, MEMORY_TRANSLATION
 * AI_ASSIGNED_TO: agent_memory_specialist_01
 * AI_TIMEOUT: 300
 * AI_MAX_RETRIES: 3
 * AI_CONTEXT: { "agent_session": "session_456", "retry_count": 0 }
 * SOURCE_API_REF: enablePeerAccess(peerDevice) - generic_api.h
 * TARGET_API_REF: backendEnablePeerAccess(peerDevice) - backend_api.h
 */
int enablePeerAccess(int peerDevice) {
    if (peerDevice < 0) {
        return API_ERROR_INVALID_VALUE;
    }
    
    // Implementation being completed by assigned agent
    printf("Peer access enable (IN PROGRESS)\n");
    return API_ERROR_NOT_IMPLEMENTED;
}


/* Example demonstrating the runtime API (requires ACD_ENABLE_RUNTIME_API) */
#ifdef ACD_ENABLE_RUNTIME_API

void demonstrate_runtime_api() {
    printf("\nACD Runtime API Demonstration:\n");
    printf("==============================\n");
    
    // Check if status values are production ready
    printf("IMPLEMENTED is production ready: %s\n", 
           acd_is_production_ready(ACD_STATUS_IMPLEMENTED) ? "yes" : "no");
    printf("PARTIAL is production ready: %s\n",
           acd_is_production_ready(ACD_STATUS_PARTIAL) ? "yes" : "no");
    
    // Check if complexity levels are high risk
    printf("CRITICAL is high risk: %s\n",
           acd_is_high_risk(ACD_COMPLEXITY_CRITICAL) ? "yes" : "no");
    printf("LOW is high risk: %s\n",
           acd_is_high_risk(ACD_COMPLEXITY_LOW) ? "yes" : "no");
}

#endif


/* Main function demonstrating usage */
int main() {
    printf("ACD Metadata Header Example\n");
    printf("===========================\n\n");
    
    int device_count = 0;
    int result;
    
    // Test device query functions
    result = getDeviceCount(&device_count);
    printf("Device count: %d (result: %d)\n", device_count, result);
    
    result = getDeviceProperties(0);
    printf("Get device properties result: %d\n", result);
    
    // Test kernel launch
    void* mock_func = (void*)0x1000;
    result = launchKernel(mock_func, 1, 1, 1, 256, 1, 1, NULL, 0, NULL);
    printf("Launch kernel result: %d\n", result);
    
    // Test stream synchronization
    api_stream_t mock_stream = (api_stream_t)0x2000;
    result = synchronizeStream(mock_stream);
    printf("Synchronize stream result: %d\n", result);
    
    // Test memory operations
    char src[100], dst[100];
    result = copyMemoryAsync(dst, src, 100, 1, mock_stream);
    printf("Async memory copy result: %d\n", result);
    
    // Test partial implementations
    printf("\nTesting partial/not-started implementations:\n");
    void* graph = NULL;
    result = captureGraphBegin(&graph, mock_stream);
    printf("Capture graph result: %d\n", result);
    
    result = instantiateGraph(graph);
    printf("Instantiate graph result: %d\n", result);
    
    result = enablePeerAccess(1);
    printf("Enable peer access result: %d\n", result);
    
#ifdef ACD_ENABLE_RUNTIME_API
    demonstrate_runtime_api();
#endif
    
    printf("\nAll functions executed. Check ACD metadata with:\n");
    printf("  python3 ../src/validate_acd.py .\n");
    printf("  python3 ../src/acd_parser.py . --analyze\n");
    
    return 0;
}
