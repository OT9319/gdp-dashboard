#!/usr/bin/env python3
"""
AEGIS - Security Scanner for Secrets Detection
===============================================

This script scans the repository for potential secrets, API keys,
passwords and other sensitive information.

Usage:
    python scripts/security/scan-secrets.py [--path PATH] [--output FORMAT]
"""

import os
import re
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Common patterns for secrets detection
SECRET_PATTERNS = {
    'api_key': [
        r'(?i)api[_-]?key[_-]?[:=]\s*[\'"]?([a-zA-Z0-9_-]{20,})[\'"]?',
        r'(?i)apikey[_-]?[:=]\s*[\'"]?([a-zA-Z0-9_-]{20,})[\'"]?',
    ],
    'aws_key': [
        r'AKIA[0-9A-Z]{16}',
        r'(?i)aws[_-]?access[_-]?key[_-]?id[_-]?[:=]\s*[\'"]?([A-Z0-9]{20})[\'"]?',
    ],
    'aws_secret': [
        r'(?i)aws[_-]?secret[_-]?access[_-]?key[_-]?[:=]\s*[\'"]?([a-zA-Z0-9/+=]{40})[\'"]?',
    ],
    'github_token': [
        r'ghp_[a-zA-Z0-9]{36}',
        r'gho_[a-zA-Z0-9]{36}',
        r'ghu_[a-zA-Z0-9]{36}',
    ],
    'password': [
        r'(?i)password[_-]?[:=]\s*[\'"]?([^\'"\s]{8,})[\'"]?',
        r'(?i)passwd[_-]?[:=]\s*[\'"]?([^\'"\s]{8,})[\'"]?',
    ],
    'database_url': [
        r'(?i)database[_-]?url[_-]?[:=]\s*[\'"]?((?:mysql|postgresql|mongodb)://[^\s\'",)]+)[\'"]?',
    ],
    'private_key': [
        r'-----BEGIN PRIVATE KEY-----',
        r'-----BEGIN RSA PRIVATE KEY-----',
        r'-----BEGIN OPENSSH PRIVATE KEY-----',
    ],
    'generic_secret': [
        r'(?i)secret[_-]?[:=]\s*[\'"]?([a-zA-Z0-9_-]{16,})[\'"]?',
        r'(?i)token[_-]?[:=]\s*[\'"]?([a-zA-Z0-9_-]{16,})[\'"]?',
    ]
}

# File extensions to scan
SCANNABLE_EXTENSIONS = {'.py', '.js', '.ts', '.json', '.yml', '.yaml', '.env', '.sh', '.md', '.txt'}

# Directories to ignore
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build'}


class SecretScanner:
    """Scanner for detecting potential secrets in code."""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.findings: List[Dict] = []
    
    def scan_file(self, file_path: Path) -> List[Dict]:
        """Scan a single file for secrets."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            findings = []
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for secret_type, patterns in SECRET_PATTERNS.items():
                    for pattern in patterns:
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            # Skip obvious false positives
                            if self._is_false_positive(line, match.group()):
                                continue
                                
                            findings.append({
                                'file': str(file_path.relative_to(self.root_path)),
                                'line': line_num,
                                'type': secret_type,
                                'match': match.group(),
                                'context': line.strip(),
                                'severity': self._get_severity(secret_type)
                            })
            
            return findings
            
        except Exception as e:
            print(f"Error scanning {file_path}: {e}", file=sys.stderr)
            return []
    
    def _is_false_positive(self, line: str, match: str) -> bool:
        """Check if a match is likely a false positive."""
        line_lower = line.lower()
        
        # Skip regex patterns in code (common in security scanners)
        if any(marker in line for marker in ["r'", 'r"', 're.', 'regex', 'pattern']):
            return True
        
        # Skip comments and documentation
        if any(marker in line_lower for marker in ['#', '//', '/*', '"""', "'''"]):
            if any(keyword in line_lower for keyword in ['example', 'sample', 'placeholder', 'xxx']):
                return True
        
        # Skip obvious placeholders
        if any(placeholder in match.lower() for placeholder in [
            'your_api_key', 'your-api-key', 'api_key_here', 'placeholder',
            'example', 'sample', 'test', 'fake', 'dummy', 'xxx'
        ]):
            return True
        
        # Skip patterns in security-related files themselves
        if 'security' in str(line_lower) and any(marker in line for marker in ['SECRET_PATTERNS', 'patterns']):
            return True
        
        return False
    
    def _get_severity(self, secret_type: str) -> str:
        """Get severity level for secret type."""
        high_severity = {'aws_key', 'aws_secret', 'github_token', 'private_key'}
        medium_severity = {'api_key', 'database_url'}
        
        if secret_type in high_severity:
            return 'HIGH'
        elif secret_type in medium_severity:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def scan_directory(self, directory: Path) -> None:
        """Recursively scan directory for secrets."""
        for item in directory.iterdir():
            if item.is_dir() and item.name not in IGNORE_DIRS:
                self.scan_directory(item)
            elif item.is_file() and item.suffix in SCANNABLE_EXTENSIONS:
                findings = self.scan_file(item)
                self.findings.extend(findings)
    
    def scan(self) -> List[Dict]:
        """Scan the repository for secrets."""
        self.findings = []
        self.scan_directory(self.root_path)
        return self.findings
    
    def generate_report(self, format_type: str = 'text') -> str:
        """Generate a report of findings."""
        if not self.findings:
            return "✅ No potential secrets detected."
        
        if format_type == 'json':
            return json.dumps(self.findings, indent=2)
        
        # Text format
        report = []
        report.append("🛡️  AEGIS - Security Scan Results")
        report.append("=" * 40)
        report.append(f"Found {len(self.findings)} potential security issues:\n")
        
        # Group by severity
        by_severity = {}
        for finding in self.findings:
            severity = finding['severity']
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(finding)
        
        for severity in ['HIGH', 'MEDIUM', 'LOW']:
            if severity not in by_severity:
                continue
                
            report.append(f"📍 {severity} SEVERITY ({len(by_severity[severity])} issues)")
            report.append("-" * 30)
            
            for finding in by_severity[severity]:
                report.append(f"  File: {finding['file']}:{finding['line']}")
                report.append(f"  Type: {finding['type']}")
                report.append(f"  Context: {finding['context'][:100]}...")
                report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 20)
        report.append("• Use environment variables for sensitive data")
        report.append("• Store secrets in secure vaults (GitHub Secrets, AWS Secrets Manager)")
        report.append("• Add sensitive files to .gitignore")
        report.append("• Use .env files with proper .gitignore patterns")
        
        return "\n".join(report)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Scan repository for potential secrets')
    parser.add_argument('--path', default='.', help='Path to scan (default: current directory)')
    parser.add_argument('--output', choices=['text', 'json'], default='text', 
                       help='Output format (default: text)')
    parser.add_argument('--fail-on-found', action='store_true',
                       help='Exit with code 1 if secrets are found')
    
    args = parser.parse_args()
    
    root_path = Path(args.path).resolve()
    if not root_path.exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    scanner = SecretScanner(root_path)
    findings = scanner.scan()
    
    report = scanner.generate_report(args.output)
    print(report)
    
    if args.fail_on_found and findings:
        sys.exit(1)


if __name__ == '__main__':
    main()