# Nexora V1 Architecture

V1 establishes the foundational workflow model for Nexora.

## Pipeline

NodeDefinition
→ NodeRegistry
→ NodeFactory
→ NodeInstance
→ WorkflowGraph
→ Workflow
→ WorkflowValidator
→ WorkflowPlanner
→ ExecutionPlan
→ WorkflowRun
→ NodeRun

## V1 capabilities

- Workflow graph representation
- Node definitions
- Node registry
- Node instances
- Node factory
- Graph validation
- Node configuration validation
- Workflow validation
- Workflow JSON serialization
- Workflow JSON deserialization
- Execution planning
- Dependency ordering
- Cycle detection
- Workflow run lifecycle
- Node run lifecycle

## V1 intentionally does not contain

- Actual node execution
- Worker infrastructure
- Distributed execution
- Queue processing
- Runtime scheduling
- Database persistence
- Production API
- Studio UI
- Language compilation
- BIR
- Marketplace
- Deployment automation

These capabilities belong to later versions.

## Design principle

Generic backend functionality will eventually be represented as reusable nodes.

Unique business logic remains expressible through code.

V1 establishes the model required for that system.