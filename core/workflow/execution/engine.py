from core.nodes.instances.model import NodeInstance
from core.workflow.execution.context import ExecutionContext
from core.workflow.execution.control import ExecutionController
from core.workflow.execution.dependencies import DependencyResolver
from core.workflow.execution.events import (
    ExecutionEvent,
    ExecutionEventSink,
    ExecutionEventType,
)
from core.workflow.execution.registry import NodeExecutorRegistry
from core.workflow.models import Workflow
from core.workflow.planning import WorkflowPlanner
from core.workflow.runs import WorkflowRun, WorkflowRunLifecycle


class WorkflowExecutionEngine:
    """Executes a planned workflow using registered node executors."""

    def __init__(
        self,
        executor_registry: NodeExecutorRegistry,
        event_sink: ExecutionEventSink | None = None,
    ) -> None:
        self.executor_registry = executor_registry
        self.event_sink = event_sink

    def _find_node(
        self,
        workflow: Workflow,
        node_id: str,
    ) -> NodeInstance:
        for node in workflow.graph.nodes:
            if node.id == node_id:
                return node

        raise KeyError(f"Node not found: {node_id}")

    def _emit(self, event: ExecutionEvent) -> None:
        if self.event_sink is not None:
            self.event_sink.emit(event)

    def execute(
        self,
        workflow: Workflow,
        run: WorkflowRun,
        controller: ExecutionController | None = None,
    ) -> WorkflowRun:
        """Execute a workflow from planning through completion."""

        planner = WorkflowPlanner()
        plan = planner.create_plan(workflow)

        lifecycle = WorkflowRunLifecycle()

        for step in plan.steps:
            lifecycle.add_node(run, step.node_id)

        lifecycle.mark_ready(run)
        lifecycle.mark_running(run)

        self._emit(
            ExecutionEvent(
                event_type=ExecutionEventType.WORKFLOW_STARTED,
                workflow_id=workflow.id,
                run_id=run.id,
            )
        )

        context = ExecutionContext(
            workflow_id=workflow.id,
            run_id=run.id,
        )

        resolver = DependencyResolver(plan)

        execution_controller = (
            controller
            if controller is not None
            else ExecutionController()
        )

        completed_nodes: set[str] = set()
        running_nodes: set[str] = set()

        while len(completed_nodes) < len(plan.steps):
            if execution_controller.cancellation_requested:
                lifecycle.mark_cancelled(run)
                execution_controller.mark_cancelled()

                self._emit(
                    ExecutionEvent(
                        event_type=ExecutionEventType.WORKFLOW_CANCELLED,
                        workflow_id=workflow.id,
                        run_id=run.id,
                    )
                )

                return run

            ready_nodes = resolver.ready_nodes(
                completed_nodes,
                running_nodes,
            )

            if not ready_nodes:
                error = "Workflow execution cannot make progress"

                lifecycle.mark_failed(
                    run,
                    error,
                )

                self._emit(
                    ExecutionEvent(
                        event_type=ExecutionEventType.WORKFLOW_FAILED,
                        workflow_id=workflow.id,
                        run_id=run.id,
                        message=error,
                    )
                )

                return run

            for node_id in ready_nodes:
                if execution_controller.cancellation_requested:
                    lifecycle.mark_cancelled(run)
                    execution_controller.mark_cancelled()

                    self._emit(
                        ExecutionEvent(
                            event_type=ExecutionEventType.WORKFLOW_CANCELLED,
                            workflow_id=workflow.id,
                            run_id=run.id,
                        )
                    )

                    return run

                node = self._find_node(
                    workflow,
                    node_id,
                )

                node_run = run.nodes[node_id]

                node_run.mark_ready()

                self._emit(
                    ExecutionEvent(
                        event_type=ExecutionEventType.NODE_READY,
                        workflow_id=workflow.id,
                        run_id=run.id,
                        node_id=node_id,
                    )
                )

                node_run.mark_running()
                running_nodes.add(node_id)

                self._emit(
                    ExecutionEvent(
                        event_type=ExecutionEventType.NODE_STARTED,
                        workflow_id=workflow.id,
                        run_id=run.id,
                        node_id=node_id,
                    )
                )

                executor = self.executor_registry.get(node)

                try:
                    result = executor.execute(
                        node,
                        context,
                    )
                except Exception as exc:
                    error = str(exc) or "Node execution failed"

                    node_run.mark_failed(error)

                    running_nodes.remove(node_id)

                    self._emit(
                        ExecutionEvent(
                            event_type=ExecutionEventType.NODE_FAILED,
                            workflow_id=workflow.id,
                            run_id=run.id,
                            node_id=node_id,
                            message=error,
                        )
                    )

                    lifecycle.mark_failed(
                        run,
                        error,
                    )

                    self._emit(
                        ExecutionEvent(
                            event_type=ExecutionEventType.WORKFLOW_FAILED,
                            workflow_id=workflow.id,
                            run_id=run.id,
                            message=error,
                        )
                    )

                    return run

                if not result.success:
                    error = (
                        result.error
                        or "Node execution failed"
                    )

                    node_run.mark_failed(error)

                    running_nodes.remove(node_id)

                    self._emit(
                        ExecutionEvent(
                            event_type=ExecutionEventType.NODE_FAILED,
                            workflow_id=workflow.id,
                            run_id=run.id,
                            node_id=node_id,
                            message=error,
                        )
                    )

                    lifecycle.mark_failed(
                        run,
                        error,
                    )

                    self._emit(
                        ExecutionEvent(
                            event_type=ExecutionEventType.WORKFLOW_FAILED,
                            workflow_id=workflow.id,
                            run_id=run.id,
                            message=error,
                        )
                    )

                    return run

                context.set_output(
                    node_id,
                    result.output,
                )

                node_run.mark_completed()

                running_nodes.remove(node_id)
                completed_nodes.add(node_id)

                self._emit(
                    ExecutionEvent(
                        event_type=ExecutionEventType.NODE_COMPLETED,
                        workflow_id=workflow.id,
                        run_id=run.id,
                        node_id=node_id,
                    )
                )

        lifecycle.mark_completed(run)

        self._emit(
            ExecutionEvent(
                event_type=ExecutionEventType.WORKFLOW_COMPLETED,
                workflow_id=workflow.id,
                run_id=run.id,
            )
        )

        return run