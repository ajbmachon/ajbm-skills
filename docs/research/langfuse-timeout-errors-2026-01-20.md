---
topic: "Langfuse API Timeout Errors - Rate Limits and Configuration"
researched: "2026-01-20"
query: "Langfuse API timeout errors, rate limits free/hobby tier, Python SDK default timeout"
expires: "2026-02-19"
sources:
  - "https://langfuse.com/faq/all/api-limits"
  - "https://langfuse.com/faq/all/error-handling-and-timeouts"
  - "https://langfuse.com/pricing"
  - "https://github.com/langfuse/langfuse/issues/10010"
  - "https://github.com/langfuse/langfuse/issues/11028"
  - "https://github.com/orgs/langfuse/discussions/6128"
  - "https://github.com/orgs/langfuse/discussions/7532"
  - "https://github.com/langfuse/langfuse/blob/main/web/src/features/public-api/server/RateLimitService.ts"
---

# Langfuse API Timeout Errors - Rate Limits and Configuration

**TL;DR:** Hobby tier has 30 req/min for general API (NOT 20), 100 req/min for datasets, 1000 req/min for tracing. Default SDK timeout is 5 seconds for span exports (OTEL), 20 seconds for prompt fetching. Timeouts are a known issue with Langfuse Cloud, especially from Azure/higher-latency environments. Increasing `LANGFUSE_TIMEOUT` does NOT fully resolve the issue per user reports.

**Researched:** 2026-01-20 | **Expires:** 2026-02-19

## 1. Rate Limits for Hobby Tier

Rate limits are applied **per-organization**, not per-project [[source](https://langfuse.com/faq/all/api-limits)].

| Resource | Hobby Tier Limit | Notes |
|----------|-----------------|-------|
| **Tracing** (`/ingestion`, `/otel`) | 1,000 req/min | Batched endpoints used by SDKs [[source](https://langfuse.com/faq/all/api-limits)] |
| **Legacy Tracing** | 100 req/min | Legacy ingestion endpoints [[source](https://langfuse.com/faq/all/api-limits)] |
| **General API** | 30 req/min | All other API calls [[source](https://langfuse.com/faq/all/api-limits)] |
| **Datasets API** | 100 req/min | Dataset operations [[source](https://langfuse.com/faq/all/api-limits)] |
| **Metrics API** | 100 req/day | Analytics data fetching [[source](https://langfuse.com/faq/all/api-limits)] |
| **Trace Deletion** | 50 req/day | DELETE operations [[source](https://langfuse.com/faq/all/api-limits)] |
| **Prompts GET** | No limit | Fetching prompts is unlimited [[source](https://langfuse.com/faq/all/api-limits)] |

**Rate limit response:**
- HTTP status code: 429
- Response includes `Retry-After` header with seconds to wait [[source](https://langfuse.com/faq/all/api-limits)]

### Hobby Tier Additional Constraints

| Constraint | Limit |
|------------|-------|
| Included usage | 50k units [[source](https://langfuse.com/pricing)] |
| Access to historical data | 30 days [[source](https://langfuse.com/pricing)] |
| Users | 2 [[source](https://langfuse.com/pricing)] |
| Payload size | 5MB per request, 5MB per response [[source](https://langfuse.com/faq/all/api-limits)] |

## 2. Default Timeouts in Python SDK

**There are multiple timeout values depending on the operation:**

| Operation | Default Timeout | Configuration |
|-----------|-----------------|---------------|
| **Span export (OTEL)** | 5 seconds | `LANGFUSE_TIMEOUT` env var [[source](https://github.com/langfuse/langfuse/issues/10010)] |
| **Prompt fetching** | 20 seconds | `fetch_timeout_seconds` parameter [[source](https://langfuse.com/faq/all/error-handling-and-timeouts)] |
| **Prompt retries** | 2 retries | `max_retries` parameter [[source](https://langfuse.com/faq/all/error-handling-and-timeouts)] |

### Configuration Examples

**Prompt fetching (per-call):**
```python
# Python SDK
prompt = langfuse.get_prompt("movie-critic", max_retries=3)
prompt = langfuse.get_prompt("movie-critic", fetch_timeout_seconds=30)
```
[[source](https://langfuse.com/faq/all/error-handling-and-timeouts)]

**Global timeout (environment variable):**
```bash
export LANGFUSE_TIMEOUT=10  # seconds
```
[[source](https://github.com/langfuse/langfuse/issues/10010)]

**OpenTelemetry exporter timeouts:**
```bash
export OTEL_EXPORTER_OTLP_TIMEOUT=30000  # milliseconds
export OTEL_EXPORTER_OTLP_TRACES_TIMEOUT=30000  # milliseconds
```
[[source](https://github.com/langfuse/langfuse/issues/10010)]

**Reduce batch size:**
```bash
export LANGFUSE_FLUSH_AT=64  # default is higher
```
[[source](https://github.com/langfuse/langfuse/issues/10010)]

## 3. Known Timeout Issues

### Issue: Intermittent ReadTimeoutError with Langfuse Cloud

**Status:** Open issue, actively being investigated [[source](https://github.com/langfuse/langfuse/issues/10010)]

**Symptoms:**
- `TimeoutError: The read operation timed out`
- `urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='cloud.langfuse.com', port=443): Read timed out`
- Errors occur intermittently, not consistently
- Timeouts persist even after increasing `LANGFUSE_TIMEOUT` to 60 seconds [[source](https://github.com/langfuse/langfuse/issues/10010)]

**User Report (Azure App Service, Hobby Plan, EU region):**
> "In the last six hours I see 12 traces on Langfuse and 6 of these errors in my Azure App Service logs."
> "I also increased LANGFUSE_TIMEOUT to 60. There may have been a slight reduction in errors, but I did not test scientifically and the error rate remains high." [[source](https://github.com/langfuse/langfuse/issues/10010)]

**Important Finding:** Timeout errors do NOT always mean data loss. Traces may still be recorded if retries succeed [[source](https://github.com/langfuse/langfuse/issues/10010)].

### Issue: December 2025 Cloud Incident

On December 10, 2025, there was a documented incident with ReadTimeout errors on Langfuse Cloud. The team added monitoring and adjusted alerting [[source](https://github.com/langfuse/langfuse/issues/11028)].

### Issue: Rate Limiting Behavior Changes

A user on Hobby plan reported sudden 429 rate limit errors in March 2025 that were working previously. Langfuse team engaged privately to investigate [[source](https://github.com/orgs/langfuse/discussions/6128)].

## 4. Mitigation Strategies

Based on official documentation and GitHub issues:

| Strategy | Environment Variable | Notes |
|----------|---------------------|-------|
| Increase timeout | `LANGFUSE_TIMEOUT=10` | May not fully resolve [[source](https://github.com/langfuse/langfuse/issues/10010)] |
| Reduce batch size | `LANGFUSE_FLUSH_AT=64` | Reduces payload per request [[source](https://github.com/langfuse/langfuse/issues/10010)] |
| Enable debug logging | `LANGFUSE_DEBUG=True` | Get more diagnostic info [[source](https://github.com/langfuse/langfuse/issues/10010)] |
| OTEL timeouts | `OTEL_EXPORTER_OTLP_TIMEOUT=30000` | For OpenTelemetry exporter [[source](https://github.com/langfuse/langfuse/issues/10010)] |

**Code-level mitigation for prompts:**
```python
prompt = langfuse.get_prompt(
    "my-prompt",
    max_retries=5,
    fetch_timeout_seconds=30
)
```
[[source](https://langfuse.com/faq/all/error-handling-and-timeouts)]

## 5. What Causes Timeout Errors

Based on GitHub issues and documentation:

1. **Network latency** - Higher latency environments (Azure App Service, cloud functions) are more susceptible [[source](https://github.com/langfuse/langfuse/issues/10010)]

2. **Default 5-second timeout too short** - The SDK's default timeout can be insufficient for higher-latency connections [[source](https://github.com/langfuse/langfuse/issues/10010)]

3. **Large batch sizes** - Large payloads can take longer to transmit and process [[source](https://github.com/langfuse/langfuse/issues/10010)]

4. **Langfuse Cloud backend issues** - There have been documented incidents affecting cloud performance [[source](https://github.com/langfuse/langfuse/issues/11028)]

5. **NOT the Hobby plan specifically** - The user in issue #10010 is on Hobby plan, but Langfuse team has not confirmed the plan as the cause [[source](https://github.com/langfuse/langfuse/issues/10010)]

## 6. Unresolved Questions

From the GitHub issues, these remain unclear:

- Why timeouts persist even with 60-second timeout configured [[source](https://github.com/langfuse/langfuse/issues/10010)]
- Whether EU region (cloud.langfuse.com) has different performance than US region (us.cloud.langfuse.com)
- Whether Hobby tier experiences more timeouts than paid tiers (no documentation confirms this)

## Quick Reference

| Question | Answer | Source |
|----------|--------|--------|
| Hobby general API limit? | 30 req/min | [[source](https://langfuse.com/faq/all/api-limits)] |
| Hobby tracing limit? | 1000 req/min | [[source](https://langfuse.com/faq/all/api-limits)] |
| Default span export timeout? | 5 seconds | [[source](https://github.com/langfuse/langfuse/issues/10010)] |
| Default prompt fetch timeout? | 20 seconds | [[source](https://langfuse.com/faq/all/error-handling-and-timeouts)] |
| How to increase timeout? | `LANGFUSE_TIMEOUT` env var | [[source](https://github.com/langfuse/langfuse/issues/10010)] |
| Does timeout = data loss? | Not necessarily | [[source](https://github.com/langfuse/langfuse/issues/10010)] |

## Sources

- [Langfuse API Limits Documentation](https://langfuse.com/faq/all/api-limits)
- [Error Handling and Timeouts FAQ](https://langfuse.com/faq/all/error-handling-and-timeouts)
- [Langfuse Pricing Page](https://langfuse.com/pricing)
- [GitHub Issue #10010: TimeoutError on Azure App Service](https://github.com/langfuse/langfuse/issues/10010)
- [GitHub Issue #11028: ReadTimeout errors for cloud.langfuse.com](https://github.com/langfuse/langfuse/issues/11028)
- [GitHub Discussion #6128: Sudden Rate Limit Issues on Hobby Plan](https://github.com/orgs/langfuse/discussions/6128)
- [GitHub Discussion #7532: Create Prompt Times Out](https://github.com/orgs/langfuse/discussions/7532)
- [RateLimitService.ts source code](https://github.com/langfuse/langfuse/blob/main/web/src/features/public-api/server/RateLimitService.ts)
