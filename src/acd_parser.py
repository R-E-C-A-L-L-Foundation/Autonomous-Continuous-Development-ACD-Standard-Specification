#!/usr/bin/env python3
"""
ACD Parser - Extract and process ACD metadata from source code

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

This tool implements parsing utilities for the Source Code Intelligence Standard (SCIS)
as defined in the ACD Standard Specification v1.0.

Features:
- Parse SCIS metadata from C/C++ source files
- Export metadata in various formats (JSON, CSV, Markdown)
- Generate dependency graphs
- Create trace artifacts
- Integration with other ACD tools

Reference: ACD Standard Specification v1.0, Part 1 (SCIS) and Part 2 (TCS)
"""

import argparse
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from collections import defaultdict

# Import the validator for reuse
try:
    from validate_acd import ACDMetadata, ACDValidator, VALID_TAGS as SCIS_TAGS, ACD_VERSION
except ImportError:
    # Try to import from the same directory as this script
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    try:
        from validate_acd import ACDMetadata, ACDValidator, VALID_TAGS as SCIS_TAGS, ACD_VERSION
    except ImportError:
        print("Error: validate_acd.py not found. Make sure it's in the same directory.")
        sys.exit(1)


class ACDParser:
    """Advanced parser for ACD metadata with additional utilities."""
    
    def __init__(self, validator: ACDValidator):
        self.validator = validator
        self.metadata_by_phase: Dict[str, List[ACDMetadata]] = defaultdict(list)
        self.metadata_by_file: Dict[str, List[ACDMetadata]] = defaultdict(list)
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)
    
    def parse_and_organize(self):
        """Parse metadata and organize by phase and file."""
        for metadata_block in self.validator.acd_metadata:
            phase = metadata_block.metadata.get("AI_PHASE", "UNKNOWN")
            self.metadata_by_phase[phase].append(metadata_block)
            self.metadata_by_file[metadata_block.file].append(metadata_block)
            
            # Build dependency graph
            dependencies = metadata_block.metadata.get("AI_DEPENDENCIES", "")
            if dependencies:
                if isinstance(dependencies, list):
                    deps = dependencies
                else:
                    deps = [d.strip() for d in dependencies.split(',') if d.strip()]
                self.dependency_graph[phase].extend(deps)
    
    def export_csv(self, output_file: Path):
        """Export metadata to CSV format."""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            header = ["File", "Line", "Phase", "Status", "Complexity", "Note", 
                     "Dependencies", "Commit", "Source_API", "Target_API"]
            writer.writerow(header)
            
            # Write data
            for metadata_block in self.validator.acd_metadata:
                row = [
                    metadata_block.file,
                    metadata_block.line,
                    metadata_block.metadata.get("AI_PHASE", ""),
                    metadata_block.metadata.get("AI_STATUS", ""),
                    metadata_block.metadata.get("AI_COMPLEXITY", ""),
                    metadata_block.metadata.get("AI_NOTE", ""),
                    metadata_block.metadata.get("AI_DEPENDENCIES", ""),
                    metadata_block.metadata.get("AI_COMMIT", ""),
                    metadata_block.metadata.get("SOURCE_API_REF", ""),
                    metadata_block.metadata.get("TARGET_API_REF", "")
                ]
                writer.writerow(row)
        
        print(f"Exported CSV to: {output_file}")
    
    def export_markdown(self, output_file: Path):
        """Export metadata to Markdown format."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# ACD Metadata Report\n\n")
            f.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
            
            # Summary statistics
            f.write("## Summary\n\n")
            f.write(f"- Total files processed: {self.validator.files_processed}\n")
            f.write(f"- Files with ACD metadata: {len(self.metadata_by_file)}\n")
            f.write(f"- Total metadata blocks: {len(self.validator.acd_metadata)}\n")
            f.write(f"- Unique phases: {len(self.metadata_by_phase)}\n\n")
            
            # Phase distribution
            f.write("## Phase Distribution\n\n")
            for phase in sorted(self.metadata_by_phase.keys()):
                count = len(self.metadata_by_phase[phase])
                f.write(f"### {phase} ({count} blocks)\n\n")
                
                for metadata_block in self.metadata_by_phase[phase]:
                    status = metadata_block.metadata.get("AI_STATUS", "UNKNOWN")
                    complexity = metadata_block.metadata.get("AI_COMPLEXITY", "")
                    note = metadata_block.metadata.get("AI_NOTE", "")
                    
                    f.write(f"- **{Path(metadata_block.file).name}:{metadata_block.line}**\n")
                    f.write(f"  - Status: {status}\n")
                    if complexity:
                        f.write(f"  - Complexity: {complexity}\n")
                    if note:
                        f.write(f"  - Note: {note}\n")
                    f.write("\n")
            
            # Dependency graph
            if self.dependency_graph:
                f.write("## Dependency Graph\n\n")
                for phase, dependencies in sorted(self.dependency_graph.items()):
                    unique_deps = sorted(set(dependencies))
                    if unique_deps:
                        f.write(f"- **{phase}** depends on: {', '.join(unique_deps)}\n")
                f.write("\n")
            
            # Files
            f.write("## Files\n\n")
            for file_path in sorted(self.metadata_by_file.keys()):
                blocks = self.metadata_by_file[file_path]
                f.write(f"### {file_path}\n\n")
                f.write(f"{len(blocks)} metadata block(s)\n\n")
        
        print(f"Exported Markdown to: {output_file}")
    
    def export_dependency_dot(self, output_file: Path):
        """Export dependency graph in DOT format (for Graphviz)."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("digraph ACD_Dependencies {\n")
            f.write("  rankdir=LR;\n")
            f.write("  node [shape=box];\n\n")
            
            # Get all phases
            all_phases = set(self.metadata_by_phase.keys())
            for deps in self.dependency_graph.values():
                all_phases.update(deps)
            
            # Define nodes with status coloring
            for phase in sorted(all_phases):
                if phase in self.metadata_by_phase:
                    blocks = self.metadata_by_phase[phase]
                    # Determine predominant status
                    statuses = [b.metadata.get("AI_STATUS", "") for b in blocks]
                    status_counts = {}
                    for status in statuses:
                        status_counts[status] = status_counts.get(status, 0) + 1
                    predominant_status = max(status_counts.items(), key=lambda x: x[1])[0] if status_counts else "UNKNOWN"
                    
                    # Color based on status
                    color_map = {
                        "IMPLEMENTED": "green",
                        "PARTIAL": "yellow",
                        "NOT_STARTED": "lightgray",
                        "FIXED": "lightgreen",
                        "DEPRECATED": "orange"
                    }
                    color = color_map.get(predominant_status, "white")
                    f.write(f'  "{phase}" [style=filled, fillcolor={color}];\n')
                else:
                    # Dependency referenced but not defined
                    f.write(f'  "{phase}" [style=dashed];\n')
            
            f.write("\n")
            
            # Define edges
            for phase, dependencies in sorted(self.dependency_graph.items()):
                unique_deps = set(dependencies)
                for dep in sorted(unique_deps):
                    f.write(f'  "{phase}" -> "{dep}";\n')
            
            f.write("}\n")
        
        print(f"Exported DOT graph to: {output_file}")
        print(f"Generate image with: dot -Tpng {output_file} -o {output_file.with_suffix('.png')}")
    
    def generate_trace_artifact(self, output_file: Path, 
                                error_info: Optional[Dict[str, Any]] = None):
        """
        Generate an ACD trace artifact for debugging.
        
        Args:
            output_file: Path to save the trace artifact
            error_info: Optional error information to include
        """
        trace = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": f"parse_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "event_type": "validation_error" if error_info else "validation_success",
            "acd_metadata_summary": {
                "total_blocks": len(self.validator.acd_metadata),
                "files_processed": self.validator.files_processed,
                "phases": list(self.metadata_by_phase.keys()),
                "phase_counts": {phase: len(blocks) for phase, blocks in self.metadata_by_phase.items()}
            }
        }
        
        if error_info:
            trace["error_info"] = error_info
        
        # Include sample metadata blocks
        trace["sample_metadata"] = []
        for phase, blocks in list(self.metadata_by_phase.items())[:5]:
            if blocks:
                trace["sample_metadata"].append(blocks[0].to_dict())
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(trace, f, indent=2)
        
        print(f"Generated trace artifact: {output_file}")
    
    def find_missing_dependencies(self) -> Dict[str, List[str]]:
        """
        Find dependencies that are referenced but not implemented.
        
        Returns:
            Dictionary mapping phases to their missing dependencies
        """
        implemented_phases = set(self.metadata_by_phase.keys())
        missing = {}
        
        for phase, dependencies in self.dependency_graph.items():
            missing_deps = [dep for dep in dependencies if dep not in implemented_phases]
            if missing_deps:
                missing[phase] = sorted(set(missing_deps))
        
        return missing
    
    def analyze_implementation_status(self) -> Dict[str, Any]:
        """
        Analyze the implementation status across all phases.
        
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            "by_status": defaultdict(int),
            "by_complexity": defaultdict(int),
            "high_risk_incomplete": [],
            "critical_implemented": [],
            "deprecated_phases": []
        }
        
        for metadata_block in self.validator.acd_metadata:
            status = metadata_block.metadata.get("AI_STATUS", "UNKNOWN")
            complexity = metadata_block.metadata.get("AI_COMPLEXITY", "UNKNOWN")
            phase = metadata_block.metadata.get("AI_PHASE", "UNKNOWN")
            
            analysis["by_status"][status] += 1
            analysis["by_complexity"][complexity] += 1
            
            # Flag high-risk incomplete implementations
            if complexity in ["HIGH", "CRITICAL"] and status in ["PARTIAL", "NOT_STARTED"]:
                analysis["high_risk_incomplete"].append({
                    "phase": phase,
                    "file": metadata_block.file,
                    "line": metadata_block.line,
                    "status": status,
                    "complexity": complexity
                })
            
            # Track critical implemented phases
            if complexity == "CRITICAL" and status == "IMPLEMENTED":
                analysis["critical_implemented"].append(phase)
            
            # Track deprecated phases
            if status == "DEPRECATED":
                analysis["deprecated_phases"].append(phase)
        
        return dict(analysis)


def main():
    """Main entry point for ACD parser."""
    parser = argparse.ArgumentParser(
        description="ACD Parser - Extract and process ACD metadata from source code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse and export to JSON
  python3 acd_parser.py /path/to/source --json output.json

  # Parse and export to CSV
  python3 acd_parser.py /path/to/source --csv output.csv

  # Parse and export to Markdown
  python3 acd_parser.py /path/to/source --markdown report.md

  # Generate dependency graph
  python3 acd_parser.py /path/to/source --dot dependencies.dot

  # Generate trace artifact
  python3 acd_parser.py /path/to/source --trace trace.json

  # Analyze implementation status
  python3 acd_parser.py /path/to/source --analyze
        """
    )
    
    parser.add_argument(
        'path',
        type=str,
        help='Path to source file or directory to parse'
    )
    
    parser.add_argument(
        '--json',
        type=str,
        metavar='FILE',
        help='Export metadata to JSON file'
    )
    
    parser.add_argument(
        '--csv',
        type=str,
        metavar='FILE',
        help='Export metadata to CSV file'
    )
    
    parser.add_argument(
        '--markdown',
        type=str,
        metavar='FILE',
        help='Export metadata to Markdown file'
    )
    
    parser.add_argument(
        '--dot',
        type=str,
        metavar='FILE',
        help='Export dependency graph to DOT file'
    )
    
    parser.add_argument(
        '--trace',
        type=str,
        metavar='FILE',
        help='Generate ACD trace artifact'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze implementation status and print report'
    )
    
    parser.add_argument(
        '--repository',
        type=str,
        metavar='REPO',
        help='Repository identifier for cross-repo traceability'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = ACDValidator(verbose=args.verbose)
    print(f"[ACD Parser v{ACD_VERSION}] Starting metadata extraction")
    
    # Process path
    path = Path(args.path).resolve()
    
    if not path.exists():
        print(f"Error: Path does not exist: {path}")
        return 1
    
    if path.is_file():
        validator.process_file(path)
    elif path.is_dir():
        validator.process_directory(path)
    else:
        print(f"Error: Invalid path type: {path}")
        return 1
    
    # Create parser
    acd_parser = ACDParser(validator)
    acd_parser.parse_and_organize()
    
    print(f"Extracted {len(validator.acd_metadata)} metadata blocks from {validator.files_processed} files")
    print(f"Found {len(acd_parser.metadata_by_phase)} unique phases")
    
    # Export to requested formats
    if args.json:
        report = validator.generate_report(repository=args.repository)
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"Exported JSON to: {args.json}")
    
    if args.csv:
        acd_parser.export_csv(Path(args.csv))
    
    if args.markdown:
        acd_parser.export_markdown(Path(args.markdown))
    
    if args.dot:
        acd_parser.export_dependency_dot(Path(args.dot))
    
    if args.trace:
        acd_parser.generate_trace_artifact(Path(args.trace))
    
    if args.analyze:
        print("\n" + "=" * 70)
        print("Implementation Status Analysis")
        print("=" * 70)
        
        analysis = acd_parser.analyze_implementation_status()
        
        print("\nStatus Distribution:")
        for status, count in sorted(analysis["by_status"].items()):
            print(f"  {status}: {count}")
        
        print("\nComplexity Distribution:")
        for complexity, count in sorted(analysis["by_complexity"].items()):
            print(f"  {complexity}: {count}")
        
        if analysis["high_risk_incomplete"]:
            print("\n⚠️  High-Risk Incomplete Implementations:")
            for item in analysis["high_risk_incomplete"]:
                print(f"  - {item['phase']} ({item['file']}:{item['line']}) - {item['status']}, {item['complexity']}")
        
        if analysis["critical_implemented"]:
            print("\n✅ Critical Implemented Phases:")
            for phase in set(analysis["critical_implemented"]):
                print(f"  - {phase}")
        
        if analysis["deprecated_phases"]:
            print("\n⚠️  Deprecated Phases:")
            for phase in set(analysis["deprecated_phases"]):
                print(f"  - {phase}")
        
        # Check for missing dependencies
        missing_deps = acd_parser.find_missing_dependencies()
        if missing_deps:
            print("\n⚠️  Missing Dependencies:")
            for phase, deps in sorted(missing_deps.items()):
                print(f"  - {phase} requires: {', '.join(deps)}")
        
        print("=" * 70)
    
    # Print summary if no specific export requested
    if not any([args.json, args.csv, args.markdown, args.dot, args.trace, args.analyze]):
        validator.print_summary()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
