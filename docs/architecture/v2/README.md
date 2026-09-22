# Nexora V2 — Workflow Execution Engine

V2 transforms Nexora from a workflow-definition system into a workflow-execution system.

## Execution Pipeline

Workflow
→ Validation
→ Execution Planning
→ Dependency Resolution
→ Execution Engine
→ Executor Registry
→ Node Executor
→ Execution Context
→ Node Result
→ Run Lifecycle
→ Execution Events

## V2 capabilities

- Workflow execution
- Node executor abstraction
- Executor registry
- Sequential execution
- Execution context
- Node output propagation
- Dependency-aware execution
- Failure handling
- Executor exception handling
- Workflow cancellation
- Execution lifecycle tracking
- Execution event system
- Event sinks
- End-to-end execution integration

## Execution boundaries

The execution engine does not implement individual backend capabilities.

It delegates node behavior to NodeExecutor implementations.

Future executors may include:

- HTTP
- Database
- Authentication
- Storage
- Queue
- Payment
- Email
- Custom code
- Language-specific runtimes

## Event architecture

The engine emits immutable execution events through an ExecutionEventSink.

The sink abstraction allows future integrations such as:

- Studio live updates
- persistent execution history
- logging
- WebSocket streaming
- message queues
- monitoring systems

## V2 limitations

V2 intentionally does not provide:

- distributed workers
- persistent execution queue
- retry policies
- production API
- BIR
- language adapters
- real database nodes
- payment nodes
- Studio UI
- deployment orchestration

These belong to later versions.

## Design principle

The execution engine is infrastructure.

Individual node capabilities are extensions.

This separation allows Nexora to evolve from local synchronous execution toward larger runtime architectures without replacing the workflow model.