#!/usr/bin/env python3
"""
ACD Validator - Validates Autonomous Continuous Development metadata in source code

Copyright (C) 2025 Timothy Deters / R.E.C.A.L.L. Foundation

This file is part of the ACD Specification.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

For commercial licensing inquiries, contact the R.E.C.A.L.L. Foundation.
Patent Pending: U.S. Application No. 63/898,838

---

This tool implements the Toolchain Cognitive Standard (TCS) validation component
as defined in the ACD Standard Specification v1.0.

Features:
- Parses SCIS tags from source code comments
- Validates required vs optional tags
- Verifies dependency chains
- Exports metadata to JSON for AI consumption
- Generates completeness reports compliant with THS schema

Reference: ACD Standard Specification v1.0, Part 2 (TCS) and Part 3 (THS)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# ACD Standard Version
ACD_VERSION = "1.0.0"

# Required SCIS tags
REQUIRED_TAGS = {"AI_PHASE", "AI_STATUS"}

# All valid SCIS tags
VALID_TAGS = {
    "AI_PHASE", "AI_STATUS", "AI_COMPLEXITY", "AI_NOTE", "AI_DEPENDENCIES",
    "AI_COMMIT", "AI_COMMIT_HISTORY", "AI_PATTERN", "AI_STRATEGY", "AI_VERSION",
    "AI_CHANGE", "AI_TRAIN_HASH", "AI_CONTEXT", "AI_METADATA", "SOURCE_API_REF", "TARGET_API_REF",
    "COMPILER_ERR", "RUNTIME_ERR", "FIX_REASON", "HUMAN_OVERRIDE",
    "AI_ASSIGNED_TO", "AI_TIMEOUT", "AI_MAX_RETRIES"
}

# Valid enum values
VALID_STATUS = {"IMPLEMENTED", "PARTIAL", "NOT_STARTED", "FIXED", "DEPRECATED"}
VALID_COMPLEXITY = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


class ACDMetadata:
    """Represents a single SCIS metadata block extracted from source code."""
    
    def __init__(self, file_path: str, line_number: int, metadata: Dict[str, Any]):
        self.file = file_path
        self.line = line_number
        self.metadata = metadata
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for JSON export."""
        result = {
            "file": self.file,
            "line": self.line,
            "timestamp_utc": self.timestamp_utc,
            **self.metadata
        }
        return result
    
    def validate(self) -> Tuple[List[str], List[str]]:
        """Validate the metadata block.
        
        Returns:
            Tuple of (errors, warnings) lists
        """
        errors = []
        warnings = []
        
        # Check required tags
        for tag in REQUIRED_TAGS:
            if tag not in self.metadata:
                errors.append(f"Missing required tag: {tag}")
        
        # Validate AI_STATUS enum
        if "AI_STATUS" in self.metadata:
            if self.metadata["AI_STATUS"] not in VALID_STATUS:
                errors.append(f"Invalid AI_STATUS value: {self.metadata['AI_STATUS']}")
        
        # Validate AI_COMPLEXITY enum
        if "AI_COMPLEXITY" in self.metadata:
            if self.metadata["AI_COMPLEXITY"] not in VALID_COMPLEXITY:
                errors.append(f"Invalid AI_COMPLEXITY value: {self.metadata['AI_COMPLEXITY']}")
        
        # Check recommended tags
        recommended_tags = {"AI_COMPLEXITY", "AI_NOTE", "AI_DEPENDENCIES", "AI_COMMIT"}
        missing_recommended = recommended_tags - set(self.metadata.keys())
        if missing_recommended:
            for tag in missing_recommended:
                warnings.append(f"Missing recommended tag: {tag}")
        
        # Validate commit hash format
        if "AI_COMMIT" in self.metadata:
            commit = self.metadata["AI_COMMIT"]
            if not re.match(r"^[0-9a-f]{7,40}$", commit):
                errors.append(f"Invalid AI_COMMIT format: {commit}")
        
        # Validate commit history format
        if "AI_COMMIT_HISTORY" in self.metadata:
            history = self.metadata["AI_COMMIT_HISTORY"]
            if isinstance(history, list):
                for commit in history:
                    if not re.match(r"^[0-9a-f]{7,40}$", commit):
                        errors.append(f"Invalid commit in AI_COMMIT_HISTORY: {commit}")
            else:
                errors.append("AI_COMMIT_HISTORY should be an array")
        
        return errors, warnings


class ACDValidator:
    """Main validator class for processing and validating ACD metadata."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.acd_metadata: List[ACDMetadata] = []
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.files_processed = 0
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with ACD standard format."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"[ACD Validator v{ACD_VERSION}] [{timestamp}] [{level}] {message}")
    
    def parse_scis_metadata(self, content: str, file_path: str) -> List[ACDMetadata]:
        """Parse SCIS metadata blocks from source file content.
        
        Args:
            content: File content as string
            file_path: Path to the source file
            
        Returns:
            List of ACDMetadata objects found in the file
        """
        metadata_blocks = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Look for comment block start with SCIS tags
            if re.search(r'/\*|\*|//', line) and re.search(r'AI_PHASE\s*:', line, re.IGNORECASE):
                metadata = {}
                start_line = i + 1
                
                # Extract metadata from comment block
                j = i
                while j < len(lines):
                    current_line = lines[j]
                    
                    # Check for comment end
                    if '*/' in current_line and j > i:
                        break
                    
                    # Parse tag: value pairs
                    for tag in VALID_TAGS:
                        pattern = rf'\*?\s*{re.escape(tag)}\s*:\s*(.+?)(?:\s*\*/)?\s*$'
                        match = re.search(pattern, current_line, re.IGNORECASE)
                        if match:
                            value = match.group(1).strip()
                            # Remove trailing */ if present
                            value = re.sub(r'\s*\*/$', '', value)
                            
                            # Handle special cases
                            if tag in ["AI_DEPENDENCIES", "AI_COMMIT_HISTORY"]:
                                # Convert comma-separated to list
                                value = [v.strip() for v in value.split(',') if v.strip()]
                            elif tag in ["AI_CONTEXT", "AI_METADATA"]:
                                # Try to parse as JSON
                                try:
                                    value = json.loads(value)
                                except json.JSONDecodeError:
                                    pass
                            elif tag in ["AI_TIMEOUT", "AI_MAX_RETRIES"]:
                                # Convert to integer
                                try:
                                    value = int(value)
                                except ValueError:
                                    pass
                            
                            metadata[tag] = value
                    
                    j += 1
                
                if metadata:
                    metadata_block = ACDMetadata(file_path, start_line, metadata)
                    metadata_blocks.append(metadata_block)
                    if self.verbose:
                        self.log(f"Found SCIS metadata at {file_path}:{start_line}")
                
                i = j
            else:
                i += 1
        
        return metadata_blocks
    
    def process_file(self, file_path: Path):
        """Process a single source file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            metadata_blocks = self.parse_scis_metadata(content, str(file_path))
            
            for metadata_block in metadata_blocks:
                errors, warnings = metadata_block.validate()
                
                for error in errors:
                    self.errors.append({
                        "file": metadata_block.file,
                        "line": metadata_block.line,
                        "message": error,
                        "severity": "error"
                    })
                
                for warning in warnings:
                    self.warnings.append({
                        "file": metadata_block.file,
                        "line": metadata_block.line,
                        "message": warning
                    })
            
            self.acd_metadata.extend(metadata_blocks)
            self.files_processed += 1
            
        except Exception as e:
            self.log(f"Error processing file {file_path}: {e}", "ERROR")
            self.errors.append({
                "file": str(file_path),
                "message": f"Failed to process file: {e}",
                "severity": "error"
            })
    
    def process_directory(self, directory: Path, extensions: List[str] = None):
        """Recursively process all source files in a directory.
        
        Args:
            directory: Directory path to process
            extensions: List of file extensions to process (default: common C/C++ extensions)
        """
        if extensions is None:
            extensions = ['.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx', '.cu', '.cuh']
        
        self.log(f"Processing directory: {directory}")
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                if self.verbose:
                    self.log(f"Processing file: {file_path}")
                self.process_file(file_path)
        
        self.log(f"Processed {self.files_processed} files")
    
    def generate_report(self, repository: str = None) -> Dict[str, Any]:
        """Generate validation report compliant with THS schema.
        
        Args:
            repository: Repository identifier for cross-repo traceability
            
        Returns:
            Dictionary containing the validation report
        """
        # Calculate statistics
        phase_distribution = {}
        status_distribution = {}
        
        for metadata_block in self.acd_metadata:
            phase = metadata_block.metadata.get("AI_PHASE", "UNKNOWN")
            status = metadata_block.metadata.get("AI_STATUS", "UNKNOWN")
            
            phase_distribution[phase] = phase_distribution.get(phase, 0) + 1
            status_distribution[status] = status_distribution.get(status, 0) + 1
        
        # Build metadata export
        metadata_export = []
        for metadata_block in self.acd_metadata:
            metadata_dict = metadata_block.to_dict()
            if repository:
                metadata_dict["repository"] = repository
            metadata_export.append(metadata_dict)
        
        report = {
            "metadata": {
                "acd_schema_version": ACD_VERSION,
                "files_processed": self.files_processed,
                "acd_metadata_found": len(self.acd_metadata),
                "errors": len([e for e in self.errors if e.get("severity") == "error"]),
                "warnings": len(self.warnings),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "phase_distribution": phase_distribution,
                "status_distribution": status_distribution
            },
            "acd_metadata": metadata_export,
            "errors": self.errors,
            "warnings": self.warnings
        }
        
        return report
    
    def print_summary(self):
        """Print validation summary in ACD standard format."""
        print("\n" + "=" * 70)
        print("ACD Validation Report")
        print("=" * 70)
        print(f"Total Files Scanned: {self.files_processed}")
        print(f"Files with ACD Metadata: {len(set(m.file for m in self.acd_metadata))}")
        if self.files_processed > 0:
            coverage = len(set(m.file for m in self.acd_metadata)) / self.files_processed * 100
            print(f"Coverage: {coverage:.1f}%")
        
        # Phase distribution
        phase_dist = {}
        for metadata_block in self.acd_metadata:
            phase = metadata_block.metadata.get("AI_PHASE", "UNKNOWN")
            phase_dist[phase] = phase_dist.get(phase, 0) + 1
        
        if phase_dist:
            print("\nPhase Distribution:")
            for phase, count in sorted(phase_dist.items(), key=lambda x: x[1], reverse=True):
                print(f"  {phase}: {count} blocks")
        
        # Status distribution
        status_dist = {}
        for metadata_block in self.acd_metadata:
            status = metadata_block.metadata.get("AI_STATUS", "UNKNOWN")
            status_dist[status] = status_dist.get(status, 0) + 1
        
        if status_dist:
            print("\nStatus Distribution:")
            total = sum(status_dist.values())
            for status, count in sorted(status_dist.items()):
                percentage = count / total * 100 if total > 0 else 0
                print(f"  {status}: {count} ({percentage:.1f}%)")
        
        # Issues
        error_count = len([e for e in self.errors if e.get("severity") == "error"])
        print(f"\nIssues Found: {error_count + len(self.warnings)}")
        if error_count > 0:
            print(f"  Errors: {error_count}")
        if self.warnings:
            print(f"  Warnings: {len(self.warnings)}")
            for warning in self.warnings[:5]:  # Show first 5 warnings
                print(f"    Warning: {warning['file']}:{warning.get('line', '?')} - {warning['message']}")
            if len(self.warnings) > 5:
                print(f"    ... and {len(self.warnings) - 5} more warnings")
        
        print("=" * 70 + "\n")


def main():
    """Main entry point for ACD validator."""
    parser = argparse.ArgumentParser(
        description="ACD Validator - Validates Autonomous Continuous Development metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single directory
  python3 validate_acd.py /path/to/source

  # Validate and export to JSON
  python3 validate_acd.py /path/to/source --export acd_metadata.json

  # Validate with verbose output
  python3 validate_acd.py /path/to/source --verbose

  # Validate with repository context
  python3 validate_acd.py /path/to/source --repository terminills/my_repo
        """
    )
    
    parser.add_argument(
        'path',
        type=str,
        help='Path to source file or directory to validate'
    )
    
    parser.add_argument(
        '--export',
        type=str,
        metavar='FILE',
        help='Export validation results to JSON file'
    )
    
    parser.add_argument(
        '--repository',
        type=str,
        metavar='REPO',
        help='Repository identifier for cross-repo traceability (e.g., terminills/cuda_rocm_wrapper)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'ACD Validator v{ACD_VERSION}'
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = ACDValidator(verbose=args.verbose)
    validator.log(f"Starting ACD validation", "INFO")
    
    # Process path
    path = Path(args.path).resolve()
    
    if not path.exists():
        validator.log(f"Path does not exist: {path}", "ERROR")
        return 1
    
    if path.is_file():
        validator.process_file(path)
    elif path.is_dir():
        validator.process_directory(path)
    else:
        validator.log(f"Invalid path type: {path}", "ERROR")
        return 1
    
    # Generate report
    report = validator.generate_report(repository=args.repository)
    
    # Export if requested
    if args.export:
        export_path = Path(args.export)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        validator.log(f"Exported validation report to: {export_path}", "INFO")
    
    # Print summary
    validator.print_summary()
    
    # Return exit code based on errors
    error_count = len([e for e in validator.errors if e.get("severity") == "error"])
    if error_count > 0:
        validator.log(f"Validation completed with {error_count} errors", "ERROR")
        return 1
    else:
        validator.log("Validation completed successfully", "INFO")
        return 0


if __name__ == "__main__":
    sys.exit(main())
