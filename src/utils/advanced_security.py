#Denvil 🧑‍💻👻


import os
import subprocess
import logging
from typing import Dict

def advanced_security_scan(repo_path: str = '.', fix: bool = False) -> Dict[str, any]:
    """Performs advanced security scan on the repo and optionally auto-fixes issues."""
    results = {'vulnerabilities': [], 'secrets': [], 'fixes_applied': []}
    logger = logging.getLogger(__name__)
    
    # Step 1: Dependency Vulnerability Scan (using Safety)
    try:
        output = subprocess.check_output(['safety', 'check', '-r', 'requirements.txt'], cwd=repo_path)
        if b'vulnerabilities found' in output:
            results['vulnerabilities'] = output.decode().splitlines()
            if fix:
                subprocess.run(['pip', 'install', '--upgrade', *results['vulnerabilities'][:5]])  # Auto-upgrade top 5
                results['fixes_applied'].append('Upgraded vulnerable dependencies')
    except Exception as e:
        logger.error(f"Dependency scan failed: {e}")
    
    # Step 2: Code Security Scan (using Bandit)
    try:
        output = subprocess.check_output(['bandit', '-r', 'src/'], cwd=repo_path)
        issues = [line for line in output.decode().splitlines() if 'HIGH' in line or 'MEDIUM' in line]
        results['vulnerabilities'].extend(issues)
    except Exception as e:
        logger.error(f"Code scan failed: {e}")
    
    # Step 3: Secret Scanning (customized for AI API keys)
    secret_patterns = ['API_KEY', 'TOKEN', 'SECRET', 'OPENAI', 'ANTHROPIC', 'GOOGLE_API', 'TELEGRAM_BOT_TOKEN']
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py') or file.endswith('.env'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        if pattern in content and 'os.getenv' not in content:  # Check if hardcoded
                            results['secrets'].append(f"Potential secret in {file}")
                            if fix:
                                # Mask or move to .env
                                with open(file, 'w') as fw:
                                    fw.write(content.replace(pattern, f"os.getenv('{pattern}')"))
                                results['fixes_applied'].append(f"Masked secret in {file}")
    
    # Step 4: Auto-Fix Permissions (ensure .env and logs are ignored)
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if not os.path.exists(gitignore_path) or '.env' not in open(gitignore_path).read():
        with open(gitignore_path, 'a') as f:
            f.write('\n.env\nlogs/\n__pycache__/\n')
        results['fixes_applied'].append('Updated .gitignore for security')
    
    logger.info("Security scan complete.")
    return results

# Usage Example (integrate into main.py or run manually)
if __name__ == "__main__":
    scan_results = advanced_security_scan(fix=True)
    print(scan_results)
