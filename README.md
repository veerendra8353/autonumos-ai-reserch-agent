# Autonomous AI Research Agent

This project is an autonomous multi-agent research system that
plans, searches, validates, self-corrects, and synthesizes information
using external tools.

## Architecture
![Architecture](docs/architecture.png)

## Agents
- Director: Breaks query into sub-questions
- Researcher: Searches external sources
- Validator: Scores credibility
- Devil’s Advocate: Finds contradictions
- Synthesizer: Produces final answer with confidence

## Prompt Library
See `/prompts` folder for all agent instructions.

## Logs
Agent reasoning and tool usage is stored in:
`/logs/agent_trace.json`

## Stress Testing
Failure modes and mitigations are documented in:
`docs/stress-test.md`