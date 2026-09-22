# Secrets Management

Nexora uses secret references instead of embedding secret values into workflows, nodes, configuration, or source code.

## Example

A workflow may contain:

```text
secret: stripe.production