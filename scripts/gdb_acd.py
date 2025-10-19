#!/usr/bin/env python3
"""
ACD GDB Extension - GDB commands for Autonomous Continuous Development

This extension implements the Toolchain Cognitive Standard (TCS) GDB interface
as defined in the ACD Standard Specification v1.0.

Commands:
  info ACD       - Display ACD metadata for current source location
  ACD-suggest    - Provide automated debugging suggestions based on ACD context

Reference: ACD Standard Specification v1.0, Part 2 (TCS)
"""

import gdb
import re
import os
from typing import Dict, List, Optional, Tuple


# ACD Standard Version
ACD_VERSION = "1.0.0"


# SCIS tag definitions
SCIS_TAGS = {
    "AI_PHASE", "AI_STATUS", "AI_COMPLEXITY", "AI_NOTE", "AI_DEPENDENCIES",
    "AI_COMMIT", "AI_COMMIT_HISTORY", "AI_PATTERN", "AI_STRATEGY", "AI_VERSION",
    "AI_CHANGE", "AI_TRAIN_HASH", "AI_CONTEXT", "AI_METADATA", "SOURCE_API_REF", 
    "TARGET_API_REF", "COMPILER_ERR", "RUNTIME_ERR", "FIX_REASON", "HUMAN_OVERRIDE",
    "AI_ASSIGNED_TO", "AI_TIMEOUT", "AI_MAX_RETRIES"
}


class ACDContext:
    """Represents ACD metadata context extracted from source code."""
    
    def __init__(self, file_path: str, line: int, metadata: Dict[str, str]):
        self.file_path = file_path
        self.line = line
        self.metadata = metadata
    
    def get_phase(self) -> str:
        """Get the AI_PHASE value."""
        return self.metadata.get("AI_PHASE", "UNKNOWN")
    
    def get_status(self) -> str:
        """Get the AI_STATUS value."""
        return self.metadata.get("AI_STATUS", "UNKNOWN")
    
    def get_complexity(self) -> str:
        """Get the AI_COMPLEXITY value."""
        return self.metadata.get("AI_COMPLEXITY", "UNKNOWN")
    
    def get_dependencies(self) -> List[str]:
        """Get the AI_DEPENDENCIES as a list."""
        deps = self.metadata.get("AI_DEPENDENCIES", "")
        if not deps:
            return []
        return [d.strip() for d in deps.split(',') if d.strip()]
    
    def format_status_icon(self) -> str:
        """Return an emoji/icon for the status."""
        status = self.get_status()
        icons = {
            "IMPLEMENTED": "✅",
            "PARTIAL": "🔶",
            "NOT_STARTED": "⭕",
            "FIXED": "🔧",
            "DEPRECATED": "⚠️"
        }
        return icons.get(status, "❓")
    
    def format_complexity_indicator(self) -> str:
        """Return complexity indicator."""
        complexity = self.get_complexity()
        indicators = {
            "LOW": "🟢",
            "MEDIUM": "🟡",
            "HIGH": "🟠",
            "CRITICAL": "🔴"
        }
        return indicators.get(complexity, "⚪")


class ACDMetadataExtractor:
    """Extracts ACD metadata from source files."""
    
    @staticmethod
    def extract_metadata_at_line(file_path: str, target_line: int) -> Optional[ACDContext]:
        """
        Extract ACD metadata for the code at or near the target line.
        
        Searches backwards from target_line to find the nearest SCIS comment block.
        
        Args:
            file_path: Path to the source file
            target_line: Line number to search from
            
        Returns:
            ACDContext if metadata found, None otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except (IOError, FileNotFoundError):
            return None
        
        if target_line > len(lines) or target_line < 1:
            return None
        
        # Search backwards from target_line for ACD metadata
        # Look up to 50 lines back
        search_start = max(0, target_line - 50)
        
        for i in range(target_line - 1, search_start - 1, -1):
            line = lines[i]
            
            # Check if this line contains AI_PHASE (start of metadata block)
            if re.search(r'AI_PHASE\s*:', line, re.IGNORECASE):
                # Found potential metadata block, extract it
                metadata = ACDMetadataExtractor._extract_metadata_block(lines, i)
                if metadata:
                    return ACDContext(file_path, i + 1, metadata)
        
        return None
    
    @staticmethod
    def _extract_metadata_block(lines: List[str], start_idx: int) -> Optional[Dict[str, str]]:
        """
        Extract all SCIS tags from a comment block starting at start_idx.
        
        Args:
            lines: List of file lines
            start_idx: Index to start extraction
            
        Returns:
            Dictionary of tag: value pairs, or None if no valid metadata
        """
        metadata = {}
        
        # Search backwards to find comment block start
        block_start = start_idx
        while block_start > 0:
            line = lines[block_start - 1]
            if '/*' in line or (block_start == start_idx):
                break
            if any(re.search(rf'{tag}\s*:', line, re.IGNORECASE) for tag in SCIS_TAGS):
                block_start -= 1
            else:
                break
        
        # Search forward to extract all tags
        i = block_start
        while i < len(lines):
            line = lines[i]
            
            # Check for comment block end
            if '*/' in line and i > start_idx:
                break
            
            # Extract SCIS tags
            for tag in SCIS_TAGS:
                pattern = rf'\*?\s*{re.escape(tag)}\s*:\s*(.+?)(?:\s*\*/)?\s*$'
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    # Remove trailing */ if present
                    value = re.sub(r'\s*\*/$', '', value)
                    metadata[tag] = value
            
            i += 1
        
        return metadata if metadata else None


class InfoACDCommand(gdb.Command):
    """
    Display ACD metadata for the current source location.
    
    Usage: info ACD
    
    Shows SCIS metadata tags including phase, status, complexity, dependencies,
    and other context information for the current execution point.
    """
    
    def __init__(self):
        super(InfoACDCommand, self).__init__("info ACD", gdb.COMMAND_STATUS)
    
    def invoke(self, arg, from_tty):
        """Execute the info ACD command."""
        # Get current frame
        try:
            frame = gdb.selected_frame()
        except gdb.error:
            print("No frame selected. Run the program first.")
            return
        
        # Get source location
        sal = frame.find_sal()
        if not sal or not sal.symtab:
            print("No source information available for current location.")
            return
        
        file_path = sal.symtab.fullname()
        line = sal.line
        
        print(f"Current Location: {file_path}:{line}\n")
        
        # Extract ACD metadata
        context = ACDMetadataExtractor.extract_metadata_at_line(file_path, line)
        
        if not context:
            print("No ACD metadata found near current location.")
            print("\nTip: ACD metadata should be in comments above the function.")
            return
        
        # Display metadata
        print("ACD Context:")
        print("-" * 70)
        
        # Display main tags
        if "AI_PHASE" in context.metadata:
            print(f"  Phase: {context.metadata['AI_PHASE']}")
        
        if "AI_STATUS" in context.metadata:
            icon = context.format_status_icon()
            print(f"  Status: {icon} {context.metadata['AI_STATUS']}")
        
        if "AI_COMPLEXITY" in context.metadata:
            indicator = context.format_complexity_indicator()
            print(f"  Complexity: {indicator} {context.metadata['AI_COMPLEXITY']}")
        
        if "AI_NOTE" in context.metadata:
            print(f"  Note: {context.metadata['AI_NOTE']}")
        
        if "AI_DEPENDENCIES" in context.metadata:
            print(f"  Dependencies: {context.metadata['AI_DEPENDENCIES']}")
        
        if "AI_COMMIT" in context.metadata:
            print(f"  Commit: {context.metadata['AI_COMMIT']}")
        
        if "AI_COMMIT_HISTORY" in context.metadata:
            print(f"  Commit History: {context.metadata['AI_COMMIT_HISTORY']}")
        
        # Display API references
        if "SOURCE_API_REF" in context.metadata:
            print(f"  Source API Ref: {context.metadata['SOURCE_API_REF']}")
        
        if "TARGET_API_REF" in context.metadata:
            print(f"  Target API Ref: {context.metadata['TARGET_API_REF']}")
        
        # Display pattern and strategy
        if "AI_PATTERN" in context.metadata:
            print(f"  Pattern: {context.metadata['AI_PATTERN']}")
        
        if "AI_STRATEGY" in context.metadata:
            print(f"  Strategy: {context.metadata['AI_STRATEGY']}")
        
        # Display error context
        if "COMPILER_ERR" in context.metadata:
            print(f"  Compiler Error: {context.metadata['COMPILER_ERR']}")
        
        if "RUNTIME_ERR" in context.metadata:
            print(f"  Runtime Error: {context.metadata['RUNTIME_ERR']}")
        
        if "FIX_REASON" in context.metadata:
            print(f"  Fix Reason: {context.metadata['FIX_REASON']}")
        
        print("")


class ACDSuggestCommand(gdb.Command):
    """
    Provide automated debugging suggestions based on ACD context.
    
    Usage: ACD-suggest
    
    Analyzes the current ACD metadata and provides context-aware debugging
    recommendations based on status, complexity, and phase information.
    """
    
    def __init__(self):
        super(ACDSuggestCommand, self).__init__("ACD-suggest", gdb.COMMAND_STATUS)
    
    def invoke(self, arg, from_tty):
        """Execute the ACD-suggest command."""
        # Get current frame
        try:
            frame = gdb.selected_frame()
        except gdb.error:
            print("No frame selected. Run the program first.")
            return
        
        # Get source location
        sal = frame.find_sal()
        if not sal or not sal.symtab:
            print("No source information available for current location.")
            return
        
        file_path = sal.symtab.fullname()
        line = sal.line
        
        # Extract ACD metadata
        context = ACDMetadataExtractor.extract_metadata_at_line(file_path, line)
        
        if not context:
            print("No ACD metadata found near current location.")
            print("\nGeneral debugging suggestions:")
            print("  1. Use 'backtrace' to see the call stack")
            print("  2. Use 'info locals' to examine local variables")
            print("  3. Use 'print <var>' to inspect specific variables")
            return
        
        print("Debugging Suggestions:")
        print("=" * 70)
        
        suggestions = []
        
        # Suggestions based on status
        status = context.get_status()
        if status == "PARTIAL":
            suggestions.append("⚠️  Code is PARTIAL - failures may be expected due to incomplete implementation")
        elif status == "NOT_STARTED":
            suggestions.append("⚠️  Code is NOT_STARTED - this is a stub or placeholder")
        elif status == "DEPRECATED":
            suggestions.append("⚠️  Code is DEPRECATED - consider using newer implementation")
        elif status == "FIXED":
            suggestions.append("✅ Code was recently FIXED - check recent changes if regression occurred")
        
        # Suggestions based on complexity
        complexity = context.get_complexity()
        if complexity == "CRITICAL":
            suggestions.append("🔴 CRITICAL complexity - carefully inspect memory safety, synchronization, and state management")
        elif complexity == "HIGH":
            suggestions.append("🟠 HIGH complexity - verify all code paths and error handling")
        elif complexity == "MEDIUM":
            suggestions.append("🟡 MEDIUM complexity - check state management and dependencies")
        
        # Suggestions based on phase
        phase = context.get_phase()
        phase_lower = phase.lower()
        if "memory" in phase_lower:
            suggestions.append("💾 Memory-related code - check for null pointers, buffer overflows, and use-after-free")
        elif "kernel" in phase_lower:
            suggestions.append("🚀 Kernel-related code - verify launch parameters and shared memory usage")
        elif "stream" in phase_lower:
            suggestions.append("🌊 Stream-related code - check for synchronization and ordering issues")
        elif "device" in phase_lower:
            suggestions.append("🖥️  Device-related code - verify device initialization and availability")
        
        # Suggestions based on dependencies
        dependencies = context.get_dependencies()
        if dependencies:
            deps_str = ", ".join(dependencies)
            suggestions.append(f"🔗 Verify dependencies are working: {deps_str}")
        
        # API reference suggestions
        if "SOURCE_API_REF" in context.metadata:
            suggestions.append(f"📖 Source API reference: {context.metadata['SOURCE_API_REF']}")
        
        if "TARGET_API_REF" in context.metadata:
            suggestions.append(f"📖 Target API reference: {context.metadata['TARGET_API_REF']}")
        
        # Error context suggestions
        if "COMPILER_ERR" in context.metadata:
            suggestions.append(f"⚠️  Previous compiler error: {context.metadata['COMPILER_ERR']}")
        
        if "RUNTIME_ERR" in context.metadata:
            suggestions.append(f"⚠️  Previous runtime error: {context.metadata['RUNTIME_ERR']}")
        
        if "FIX_REASON" in context.metadata:
            suggestions.append(f"💡 Previous fix reason: {context.metadata['FIX_REASON']}")
        
        # Commit history suggestion
        if "AI_COMMIT" in context.metadata:
            commit = context.metadata['AI_COMMIT']
            suggestions.append(f"📝 Check commit {commit} for implementation context")
            
            if "AI_COMMIT_HISTORY" in context.metadata:
                suggestions.append(f"📜 Review commit history to understand evolution: {context.metadata['AI_COMMIT_HISTORY']}")
        
        # Print suggestions
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        
        if not suggestions:
            print("No specific suggestions based on current ACD context.")
        
        print("\nTip: Use 'info ACD' for full context")
        print("")


# Register commands when loaded in GDB
try:
    InfoACDCommand()
    ACDSuggestCommand()
    print(f"ACD GDB Extension v{ACD_VERSION} loaded successfully.")
    print("Available commands:")
    print("  info ACD       - Display ACD metadata for current location")
    print("  ACD-suggest    - Get automated debugging suggestions")
except Exception as e:
    print(f"Error loading ACD GDB Extension: {e}")
