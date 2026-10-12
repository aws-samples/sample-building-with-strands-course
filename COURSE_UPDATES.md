# Course updates

Reviewed October 12, 2026. The recorded lessons explain the concepts; use the current
samples and readings for runnable code. The website marks material differences with
red **Changed since recording** notices. GitHub renders the corresponding warnings
with its native alert styling.

## Tested package baseline

- Python 3.12.13 for local validation; sample syntax remains compatible with Python 3.10+.
- `strands-agents==1.59.0`, including the `web-fetch` extra for web examples.
- `strands-agents-evals==1.5.0` for lesson 13.
- `bedrock-agentcore==1.24.1` for runtime imports and local entrypoint checks.
- AgentCore CLI `@aws/agentcore@0.31.1` for local scaffold/configuration checks.
- Optional reading example: `strands-dynamodb-storage==0.1.2` imports and constructor checked.

Install the normal course baseline with `pip install -r requirements.txt`.
For the offline regression suite, install `requirements-dev.txt`, then run
`python -m pytest tests -q` from the repository root. Provider-specific extras,
credentials, local model downloads, and cloud resources are separate prerequisites.

## Lesson audit

| Lesson | Findings and updates | Verification |
| --- | --- | --- |
| 1. Agent loop | Keep the vended tools migration. Add the missing `web-fetch` installation instructions and use the explicit decorated-tool import. | Imports and agent/tool construction checked. |
| 2. Providers | Preserve the direct provider constructors and walkthrough. Match the Ollama pull command to the model used in the example and update documentation links. | Provider imports and constructor signatures checked. |
| 3. MCP | Preserve the original callable transports in the sample files, URL shorthand in the reading, and each example's original endpoint. Update documentation links only. | Both forms checked against the SDK. Live listing and reads worked on both endpoints; the broader AWS MCP endpoint returned 401 during cleanup. |
| 4. Streaming | Keep the custom calculator that replaced `strands_tools.calculator`; retain the supported callback and async stream APIs. | Imports and agent/FastAPI construction checked. |
| 5. Hooks | The approval flow and reading excerpt remain unchanged. | The SDK loop test covers two deletion requests, one approved and one denied, using temporary files. |
| 6. Plugins and skills | `AgentSkills` and `GoalLoop` remain supported. Replace empty tool bodies in the reading with the actual sample tools; make the interactive demo import-safe. | Imports, skill registration, and GoalLoop API checked. |
| 7. Steering | The steering handler and reading examples remain unchanged. | Original example completes the scripted SDK tool-loop test. This test does not establish every steering decision or prove a deprecation. |
| 8. Context | Keep `context_manager="auto"`, `"agentic"`, and the currently exported experimental custom-strategy namespace. Correct truncation semantics and remove an unsourced workload-wide benchmark claim. | Preset tools, custom strategies, constructor signatures, and imports checked against the release. |
| 9. Persistence | Say explicitly that the video's FileSessionManager and S3SessionManager examples remain valid. Present snapshot sessions and memory stores as green optional-addition callouts with documentation links. Put the original File and S3 walkthroughs before the optional snapshot section. Keep the walkthrough code. | Callout wording checked against current session and memory documentation. Existing local snapshot tests cover single-agent and Graph/Swarm persistence; memory stores are documentation guidance, not a new hosted integration test. |
| 10. Agents as tools | Composition APIs and default context-reset semantics remain supported. Add the web-fetch extra prerequisite and migration notice. | Agent-as-tool construction, signatures, and imports checked. |
| 11. Graphs | GraphBuilder API remains supported. Add web fetching to the manual research workflow, add its dependency prerequisite, and clarify supported node types and cyclic graphs. | Graph construction and local snapshot-backed execution checked with a scripted model. |
| 12. Swarms | Swarm APIs and limits remain supported. Make mock tools importable and complete the reading's imports. Clarify that the SDK has default limits. | Swarm construction and local snapshot-backed execution checked. |
| 13. Evals | Keep the evaluation code corrections without change-since-recording callouts. Use one `EvaluationReport`; initialize custom evaluators and return `list[EvaluationOutput]`. Create fresh plugins per case, use local lesson files, fix the missing-ID expected trajectory and nonexistent laptop case. Supply course-local chaos and red-team examples with fresh agents. | Deterministic evaluator runs through the real Experiment API; factory isolation regression; imports, signatures, and example configuration checked. Hosted judges/simulators/attacks not run. |
| 14. Deployment | The existing AgentCore and Lambda deployment options remain. Bind the runtime cache to one actor/session pair and serialize requests; reject a different pair. Create fresh Lambda agents/plugins per request. Handle direct and CLI-wrapped prompts. Copy course files into the CLI scaffold before deployment; correct dependency floors and DynamoDB guidance. | Local runtime factory checks, two HTTP requests through the Lambda FastAPI app, and actual CLI scaffold plus memory configuration. No AWS deployment. |

## Scope of verification

The recorded walkthrough remains the starting point. Notices distinguish changes
in the demonstrated APIs from optional additions. Small code corrections are
included in the current examples without implying that the lesson's approach
has changed. Snapshot sessions and memory stores are optional additions; the
FileSessionManager and S3SessionManager examples remain valid.

The review compares the current lesson pages and course code with released packages,
current SDK source, and the earlier course source at `6383ef6` (July 8, 2026), before
the September migration. It is not a frame-by-frame review of the recordings. Notices
about older imports and context management use that source history and the lesson's
existing explicit description of what the video demonstrates.

The offline tests use a scripted model to exercise the real SDK loop without invoking
hosted models. Passing those tests verifies the code paths described above. It does
not establish model quality, account/region-specific model access, production IAM,
S3/DynamoDB/AgentCore Memory operation, a complete local pricing-server setup, or
successful hosted deployments. Those require the learner's configured environment.

The installed AgentCore package currently emits deprecation warnings for its own
experimental Bidi/hooks imports. The course uses its supported session-manager API;
those internal warnings need an upstream package update.

## Review sources

- [Python SDK source](https://github.com/strands-agents/harness-sdk/tree/bf9f11a6f7f256d7886f6e4990631c030568e248/strands-py/src/strands)
- [Published Python SDK](https://pypi.org/project/strands-agents/1.59.0/)
- [Published Evals SDK](https://pypi.org/project/strands-agents-evals/1.5.0/)
- [Published AgentCore SDK](https://pypi.org/project/bedrock-agentcore/1.24.1/)
- [Course before this update](https://github.com/aws-samples/sample-building-with-strands-course/tree/d60ebf41baae4bc2f3329d7e625e153dbe1d61a2)
- [Earlier course source](https://github.com/aws-samples/sample-building-with-strands-course/tree/6383ef6)
- [Current course reading](https://strandsagents.com/docs/learning/how-agents-really-work/)
