# Nexora Security Architecture

## Purpose

V0.7 establishes the security and secrets foundation for Nexora.

Security is treated as a cross-cutting concern across workflows, nodes, runtime execution, plugins, adapters, APIs, and deployment.

## Security Principles

Nexora follows these principles:

1. Default deny
2. Least privilege
3. Explicit permissions
4. Secret references instead of embedded secrets
5. No secrets in logs
6. Provider-independent security interfaces
7. Isolation between execution contexts
8. Security validation before execution

## Secrets

Secrets are represented by references.

Example:

```text
stripe.production