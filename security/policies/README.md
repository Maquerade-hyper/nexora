# Security Policies

Nexora follows a default-deny security model.

## Core Rules

- Secrets must not be stored directly in workflows.
- Secrets must not be committed to Git.
- Secrets must not appear in logs.
- Secret references must be used instead of secret values.
- Permissions must be explicit.
- Unknown permissions are denied by default.
- Security-sensitive operations must be validated before execution.

## Default Deny

Nexora should deny an operation unless the required permission has been explicitly granted.

## Secret Handling

A workflow should reference:

`stripe.production`

rather than containing:

`sk_live_...`

The actual secret is resolved only when required by the runtime.