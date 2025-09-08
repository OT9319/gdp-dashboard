#!/usr/bin/env python3
"""
AEGIS - Dependency Security Checker
===================================

This script checks the security of project dependencies using
known vulnerability databases and best practices.

Usage:
    python scripts/security/check-dependencies.py [--requirements PATH]
"""

import argparse
import json
import sys
import subprocess
import pkg_resources
from pathlib import Path
from typing import List, Dict, Optional
import urllib.request
import urllib.error


class DependencyChecker:
    """Checker for dependency security issues."""
    
    def __init__(self, requirements_file: Optional[Path] = None):
        self.requirements_file = requirements_file
        self.findings: List[Dict] = []
    
    def get_installed_packages(self) -> Dict[str, str]:
        """Get list of installed packages and their versions."""
        packages = {}
        for dist in pkg_resources.working_set:
            packages[dist.project_name.lower()] = dist.version
        return packages
    
    def parse_requirements(self) -> Dict[str, str]:
        """Parse requirements.txt file."""
        if not self.requirements_file or not self.requirements_file.exists():
            return {}
        
        packages = {}
        try:
            with open(self.requirements_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Simple parsing - handle package==version
                        if '==' in line:
                            name, version = line.split('==', 1)
                            packages[name.strip().lower()] = version.strip()
                        else:
                            # Package without version specified
                            packages[line.lower()] = 'unknown'
        except Exception as e:
            print(f"Error reading requirements file: {e}", file=sys.stderr)
        
        return packages
    
    def check_package_age(self, package_name: str, version: str) -> Dict:
        """Check if package version is outdated (simplified check)."""
        # This is a simplified check - in practice, you'd use PyPI API
        # For now, we'll check for some common patterns that suggest old versions
        
        outdated_indicators = {
            'streamlit': ['1.0', '1.1', '1.2'],  # Versions older than current
            'pandas': ['1.0', '1.1', '1.2'],
            'numpy': ['1.19', '1.20'],
        }
        
        if package_name.lower() in outdated_indicators:
            old_versions = outdated_indicators[package_name.lower()]
            for old_version in old_versions:
                if version.startswith(old_version):
                    return {
                        'type': 'outdated_version',
                        'package': package_name,
                        'current_version': version,
                        'severity': 'MEDIUM',
                        'message': f'Package {package_name} version {version} may be outdated',
                        'recommendation': f'Consider updating {package_name} to the latest version'
                    }
        
        return {}
    
    def check_known_vulnerabilities(self, packages: Dict[str, str]) -> List[Dict]:
        """Check packages against known vulnerabilities (simplified)."""
        # This is a simplified check - in production, you'd use safety, 
        # snyk, or similar tools with real vulnerability databases
        
        known_vulnerable = {
            # Example entries - these would come from real vulnerability databases
            'requests': {
                'versions': ['2.25.0', '2.25.1'],
                'cve': 'Example-CVE-2021-1234',
                'description': 'Example vulnerability in requests'
            }
        }
        
        findings = []
        for package, version in packages.items():
            if package in known_vulnerable:
                vuln_info = known_vulnerable[package]
                if version in vuln_info['versions']:
                    findings.append({
                        'type': 'known_vulnerability',
                        'package': package,
                        'version': version,
                        'cve': vuln_info['cve'],
                        'description': vuln_info['description'],
                        'severity': 'HIGH',
                        'recommendation': f'Update {package} to a patched version'
                    })
        
        return findings
    
    def check_license_compatibility(self, packages: Dict[str, str]) -> List[Dict]:
        """Check for potentially problematic licenses."""
        # List of licenses that might require attention
        problematic_licenses = [
            'GPL-3.0', 'AGPL-3.0', 'SSPL-1.0'  # Copyleft licenses
        ]
        
        # This would normally query package metadata for license info
        # For now, return empty as this requires more complex implementation
        return []
    
    def check_maintenance_status(self, packages: Dict[str, str]) -> List[Dict]:
        """Check if packages are actively maintained."""
        # List of packages known to be unmaintained or deprecated
        unmaintained = {
            'python2': 'Python 2 is no longer supported',
            'six': 'Consider migrating away from six if using Python 3 only'
        }
        
        findings = []
        for package in packages:
            if package in unmaintained:
                findings.append({
                    'type': 'maintenance_concern',
                    'package': package,
                    'severity': 'MEDIUM',
                    'message': unmaintained[package],
                    'recommendation': f'Consider alternatives to {package}'
                })
        
        return findings
    
    def run_safety_check(self) -> List[Dict]:
        """Run safety check if available."""
        try:
            # Try to run safety if installed
            result = subprocess.run(['safety', 'check', '--json'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and result.stdout:
                safety_data = json.loads(result.stdout)
                return [{
                    'type': 'safety_vulnerability',
                    'package': item.get('package', 'unknown'),
                    'version': item.get('installed_version', 'unknown'),
                    'cve': item.get('advisory', 'unknown'),
                    'description': item.get('advisory', 'Safety vulnerability detected'),
                    'severity': 'HIGH',
                    'recommendation': 'Update to a secure version'
                } for item in safety_data]
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
            # Safety not available or failed
            pass
        
        return []
    
    def check_dependencies(self) -> List[Dict]:
        """Perform comprehensive dependency check."""
        findings = []
        
        # Get packages from requirements.txt if available, otherwise installed packages
        if self.requirements_file and self.requirements_file.exists():
            packages = self.parse_requirements()
            print(f"📦 Checking {len(packages)} packages from requirements.txt")
        else:
            packages = self.get_installed_packages()
            print(f"📦 Checking {len(packages)} installed packages")
        
        # Run various checks
        findings.extend(self.check_known_vulnerabilities(packages))
        findings.extend(self.check_maintenance_status(packages))
        findings.extend(self.run_safety_check())
        
        # Check for outdated versions
        for package, version in packages.items():
            age_check = self.check_package_age(package, version)
            if age_check:
                findings.append(age_check)
        
        return findings
    
    def generate_report(self, findings: List[Dict], format_type: str = 'text') -> str:
        """Generate a report of dependency findings."""
        if not findings:
            return "✅ No dependency security issues detected."
        
        if format_type == 'json':
            return json.dumps(findings, indent=2)
        
        # Text format
        report = []
        report.append("🛡️  AEGIS - Dependency Security Report")
        report.append("=" * 45)
        report.append(f"Found {len(findings)} potential dependency issues:\n")
        
        # Group by severity
        by_severity = {}
        for finding in findings:
            severity = finding.get('severity', 'UNKNOWN')
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(finding)
        
        for severity in ['HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']:
            if severity not in by_severity:
                continue
                
            report.append(f"📍 {severity} SEVERITY ({len(by_severity[severity])} issues)")
            report.append("-" * 35)
            
            for finding in by_severity[severity]:
                report.append(f"  Package: {finding.get('package', 'unknown')}")
                if 'version' in finding:
                    report.append(f"  Version: {finding['version']}")
                report.append(f"  Issue: {finding.get('type', 'unknown')}")
                if 'cve' in finding:
                    report.append(f"  CVE: {finding['cve']}")
                report.append(f"  Description: {finding.get('description', finding.get('message', 'No description'))}")
                if 'recommendation' in finding:
                    report.append(f"  Recommendation: {finding['recommendation']}")
                report.append("")
        
        # General recommendations
        report.append("💡 GENERAL RECOMMENDATIONS")
        report.append("-" * 28)
        report.append("• Keep dependencies up to date")
        report.append("• Use tools like safety or snyk for regular security scans")
        report.append("• Pin versions in requirements.txt for reproducible builds")
        report.append("• Regularly review and audit dependencies")
        report.append("• Consider using virtual environments")
        
        return "\n".join(report)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Check dependencies for security issues')
    parser.add_argument('--requirements', help='Path to requirements.txt file')
    parser.add_argument('--output', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--fail-on-found', action='store_true',
                       help='Exit with code 1 if issues are found')
    
    args = parser.parse_args()
    
    requirements_file = None
    if args.requirements:
        requirements_file = Path(args.requirements)
        if not requirements_file.exists():
            print(f"Error: Requirements file '{args.requirements}' not found", file=sys.stderr)
            sys.exit(1)
    
    checker = DependencyChecker(requirements_file)
    findings = checker.check_dependencies()
    
    report = checker.generate_report(findings, args.output)
    print(report)
    
    if args.fail_on_found and findings:
        sys.exit(1)


if __name__ == '__main__':
    main()