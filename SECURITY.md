# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Agent Souls, please report it responsibly.

**Email:** sezersivri@gmail.com

**Subject line:** `[SECURITY] Agent Souls: <brief description>`

### What to include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

### Response timeline

- **Acknowledgment:** within 48 hours
- **Initial assessment:** within 7 days
- **Fix or mitigation:** as soon as practical, depending on severity

### Scope

This project is a Markdown-based file system with Python utility scripts. Security concerns most likely involve:

- Accidental exposure of secrets (API keys, tokens) in agent memory files
- Script injection through malformed Markdown content
- Path traversal in utility scripts

### Responsible Disclosure

Please do **not** open a public GitHub issue for security vulnerabilities. Use the email above so we can assess and fix the issue before public disclosure.

We will credit reporters in the fix commit unless they prefer to remain anonymous.
