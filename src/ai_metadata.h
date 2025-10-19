/**
 * @file ai_metadata.h
 * @brief ACD (Autonomous Continuous Development) Metadata Header
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
 * This header provides C/C++ macros and utilities for embedding ACD metadata
 * in source code according to the Source Code Intelligence Standard (SCIS).
 * 
 * Reference: ACD Standard Specification v1.0, Part 1 (SCIS)
 * Version: 1.0.0
 * 
 * Usage:
 *   Include this header in your source files to use ACD metadata macros.
 *   Metadata is embedded as structured comments that can be parsed by
 *   ACD-compliant tools (validators, GDB extensions, etc.).
 * 
 * Example:
 *   ACD_METADATA_BEGIN()
 *   ACD_PHASE("MEMORY_TRANSLATION")
 *   ACD_STATUS("IMPLEMENTED")
 *   ACD_COMPLEXITY("MEDIUM")
 *   ACD_NOTE("Implements unified memory allocation")
 *   ACD_DEPENDENCIES("INIT_HOOKS, ERROR_HANDLING")
 *   ACD_METADATA_END()
 *   void* allocateMemory(size_t size) {
 *       // Implementation
 *   }
 */

#ifndef ACD_AI_METADATA_H
#define ACD_AI_METADATA_H

/**
 * ACD Standard Version
 */
#define ACD_VERSION "1.0.0"

/**
 * Note: These macros are provided as documentation and reference.
 * 
 * Due to C preprocessor limitations, macro-based metadata embedding
 * doesn't work well in practice. Instead, write metadata directly as
 * structured comments above your functions.
 * 
 * The macros below serve as a reference guide for the SCIS tag format
 * that should be used in comments.
 */

/* Recommended metadata format (write directly in comments): */
/*
 * AI_PHASE: <phase_name>
 * AI_STATUS: <status_value>
 * AI_COMPLEXITY: <complexity_value>
 * AI_NOTE: <description>
 * AI_DEPENDENCIES: <comma_separated_dependencies>
 * AI_COMMIT: <git_commit_hash>
 * AI_COMMIT_HISTORY: <comma_separated_previous_commits>
 * SOURCE_API_REF: <source_api_reference>
 * TARGET_API_REF: <target_api_reference>
 */


/* Status and Complexity Constants */

/* AI_STATUS values */
#define ACD_STATUS_IMPLEMENTED   "IMPLEMENTED"
#define ACD_STATUS_PARTIAL       "PARTIAL"
#define ACD_STATUS_NOT_STARTED   "NOT_STARTED"
#define ACD_STATUS_FIXED         "FIXED"
#define ACD_STATUS_DEPRECATED    "DEPRECATED"

/* AI_COMPLEXITY values */
#define ACD_COMPLEXITY_LOW       "LOW"
#define ACD_COMPLEXITY_MEDIUM    "MEDIUM"
#define ACD_COMPLEXITY_HIGH      "HIGH"
#define ACD_COMPLEXITY_CRITICAL  "CRITICAL"


/* Runtime API (optional) */

#ifdef ACD_ENABLE_RUNTIME_API

#include <stdbool.h>

/**
 * Structure representing parsed ACD metadata
 */
typedef struct {
    const char* phase;
    const char* status;
    const char* complexity;
    const char* note;
    const char* dependencies;
    const char* commit;
    const char* commit_history;
    const char* source_api_ref;
    const char* target_api_ref;
} acd_metadata_t;

/**
 * Check if a status indicates the code is production-ready
 * @param status AI_STATUS value
 * @return true if status is IMPLEMENTED or FIXED
 */
static inline bool acd_is_production_ready(const char* status) {
    if (!status) return false;
    return (strcmp(status, ACD_STATUS_IMPLEMENTED) == 0) ||
           (strcmp(status, ACD_STATUS_FIXED) == 0);
}

/**
 * Check if a complexity level is high risk
 * @param complexity AI_COMPLEXITY value
 * @return true if complexity is HIGH or CRITICAL
 */
static inline bool acd_is_high_risk(const char* complexity) {
    if (!complexity) return false;
    return (strcmp(complexity, ACD_COMPLEXITY_HIGH) == 0) ||
           (strcmp(complexity, ACD_COMPLEXITY_CRITICAL) == 0);
}

#endif /* ACD_ENABLE_RUNTIME_API */


#endif /* ACD_AI_METADATA_H */
