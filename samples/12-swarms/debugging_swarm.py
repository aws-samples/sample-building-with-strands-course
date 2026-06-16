from strands import Agent, tool
from strands.multiagent import Swarm


# =============================================================================
# Mock tools that simulate production debugging capabilities
# =============================================================================
@tool
def check_application_logs(service_name: str, time_range: str = "last_hour") -> str:
    """Search application logs for errors and anomalies.

    Args:
        service_name: Name of the service to check logs for
        time_range: Time range to search (e.g., "last_hour", "last_24h")
    """
    return f"""[Log Analysis for {service_name} - {time_range}]
- 14:32:01 ERROR PaymentService: Connection timeout to database (5 occurrences)
- 14:32:15 ERROR PaymentService: Failed to process transaction tx-8891 - DBConnectionError
- 14:33:02 WARN PaymentService: Retry attempt 3/3 failed for db connection pool
- 14:33:45 ERROR PaymentService: Circuit breaker OPEN for database connections
- 14:34:00 INFO PaymentService: Fallback response returned for 12 requests"""


@tool
def check_metrics_dashboard(service_name: str, metric_type: str = "all") -> str:
    """Pull metrics from the monitoring dashboard.

    Args:
        service_name: Name of the service to check metrics for
        metric_type: Type of metrics - "latency", "errors", "throughput", or "all"
    """
    return f"""[Metrics Dashboard for {service_name}]
- Error rate: 23% (baseline: 0.1%) — spike started at 14:31 UTC
- P99 latency: 12,400ms (baseline: 180ms)
- Database connection pool: 0 available / 50 max (exhausted)
- CPU: 34% (normal)
- Memory: 61% (normal)
- Active DB connections: 50/50 (saturated since 14:31)"""


@tool
def check_recent_deployments(time_range: str = "last_24h") -> str:
    """Check recent deployments and infrastructure changes.

    Args:
        time_range: Time range to search for deployments
    """
    return f"""[Recent Deployments - {time_range}]
- 14:28 UTC: payment-service v2.4.1 deployed (changed: connection pool config)
  Commit: "Reduce max idle connections from 20 to 5 for cost optimization"
  Author: dev-team-3
- 12:00 UTC: monitoring-agent v1.2.0 deployed (no service impact)
- Yesterday 09:00 UTC: auth-service v3.1.0 deployed (unrelated)"""


@tool
def check_infrastructure_status(component: str = "all") -> str:
    """Check infrastructure health for databases, networks, and compute.

    Args:
        component: Specific component to check - "database", "network", "compute", or "all"
    """
    return f"""[Infrastructure Status - {component}]
- RDS Primary (payment-db): Status AVAILABLE, connections 50/50 (MAX)
- RDS Read Replica: Status AVAILABLE, connections 12/50
- Network: No packet loss, latency normal
- Load Balancer: Healthy, no 5xx from LB itself
- Note: Connection limit on payment-db was not changed. Pool exhaustion is client-side."""


# =============================================================================
# Debugging Swarm Agents
# =============================================================================

triage = Agent(
    name="triage",
    system_prompt="""You are the incident triage agent. When a production issue is reported,
    do an initial assessment and hand off to the most relevant specialist.
    If it sounds like an application error, hand off to log_analyst.
    If it sounds like a performance or capacity issue, hand off to metrics_analyst.
    If it sounds like a deployment or infrastructure issue, hand off to deployment_reviewer.""",
)

log_analyst = Agent(
    name="log_analyst",
    system_prompt="""You analyze application logs to identify root causes.
    Use the check_application_logs tool to investigate.
    If you find evidence pointing to infrastructure or deployment issues, hand off to the relevant specialist.
    If you find the root cause, provide a clear summary and resolution recommendation.""",
    tools=[check_application_logs],
)

metrics_analyst = Agent(
    name="metrics_analyst",
    system_prompt="""You analyze system metrics and dashboards to identify performance issues.
    Use the check_metrics_dashboard tool to investigate.
    If metrics point to a recent change causing the issue, hand off to deployment_reviewer.
    If metrics point to application-level errors, hand off to log_analyst.
    If you identify the root cause, provide a clear summary.""",
    tools=[check_metrics_dashboard],
)

deployment_reviewer = Agent(
    name="deployment_reviewer",
    system_prompt="""You review recent deployments and infrastructure changes to find what caused an incident.
    Use check_recent_deployments and check_infrastructure_status to investigate.
    If you find the problematic change, provide the root cause, the specific deployment, and a rollback recommendation.
    If the issue isn't deployment-related, hand off to the appropriate specialist.""",
    tools=[check_recent_deployments, check_infrastructure_status],
)

# =============================================================================
# Create and run the swarm
# =============================================================================

debugging_swarm = Swarm(
    [triage, log_analyst, metrics_analyst, deployment_reviewer],
    entry_point=triage,
    max_handoffs=10,
    max_iterations=10,
    execution_timeout=300.0,
    node_timeout=120.0,
    repetitive_handoff_detection_window=6,
    repetitive_handoff_min_unique_agents=2,
)

result = debugging_swarm(
    "The payment service is returning 500 errors for about 25% of requests. Started around 30 minutes ago."
)

print(f"\nStatus: {result.status}")
print(f"Path: {' → '.join(n.node_id for n in result.node_history)}")
