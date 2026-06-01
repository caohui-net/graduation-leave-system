# Dorm Provider Discovery - Investigation Brief

**Date:** 2026-05-31  
**Status:** Discovery phase  
**Goal:** Remove external dependency blocker for production

---

## Objective

Identify and document requirements for integrating with real dormitory management system to replace mock provider.

---

## Discovery Tasks

### 1. Identify Owner/Contact

**Questions:**
- Who owns the dormitory management system?
- Contact person for integration requests?
- Department responsible for system access?

**Status:** 🔍 Needs investigation

### 2. Integration Method

**Options:**
- **API:** REST/SOAP endpoints
- **Database:** Direct read access
- **File Exchange:** CSV/Excel exports
- **Manual:** No system integration

**Questions:**
- What integration methods are supported?
- Is there existing API documentation?
- What authentication is required?

**Status:** 🔍 Needs investigation

### 3. Data Schema

**Required Fields:**
- Student ID (学号)
- Checkout status (completed/pending/not_started)
- Blocking reason (if pending)
- Checkout date (if completed)

**Questions:**
- What fields are available?
- What are field names/types?
- Are there additional useful fields?

**Status:** 🔍 Needs investigation

### 4. Access Credentials

**Requirements:**
- API keys or database credentials
- Network access (VPN required?)
- Sandbox/test environment

**Questions:**
- How to obtain credentials?
- Is there a test environment?
- What are network restrictions?

**Status:** 🔍 Needs investigation

### 5. Test Data

**Requirements:**
- Test student IDs with known states
- Expected checkout statuses
- Edge cases (pending with reasons)

**Questions:**
- Can we get test student IDs?
- What are expected states for testing?
- Are there edge cases to test?

**Status:** 🔍 Needs investigation

### 6. Network/Access Constraints

**Questions:**
- Is system accessible from internet?
- VPN required?
- IP whitelist needed?
- Firewall rules?

**Status:** 🔍 Needs investigation

---

## Current Mock Provider

**Location:** `backend/apps/applications/providers.py`

**Interface:**
```python
class DormCheckoutProvider:
    def check_status(self, student_id: str) -> DormCheckoutResult:
        """Check dormitory checkout status for student"""
        pass
```

**Mock Behavior:**
- Returns `completed` for most students
- Returns `pending` for student IDs ending in '999'
- Returns `not_started` for student IDs ending in '000'

---

## Integration Requirements

### Minimum Viable Integration

**Must Have:**
- Query checkout status by student ID
- Return status (completed/pending/not_started/unknown)
- Return blocking reason if pending
- Handle errors gracefully

**Nice to Have:**
- Batch query support
- Caching layer
- Retry logic
- Monitoring/logging

### Production Requirements

**Before Production:**
- Real provider integration OR
- Approved manual fallback process
- Test coverage for integration
- Error handling for provider failures
- Monitoring/alerting

---

## Next Steps

1. **User Input Required:**
   - Contact information for dorm system owner
   - Existing documentation if available
   - Known integration constraints

2. **Investigation:**
   - Review any existing documentation
   - Contact system owner
   - Request API/database access
   - Obtain test credentials

3. **Implementation:**
   - Create real provider adapter
   - Add integration tests
   - Add error handling
   - Add monitoring

---

## Blockers

**Current Blockers:**
- No contact information for dorm system owner
- No documentation available
- No access credentials

**Resolution:**
- Requires user/stakeholder input
- Cannot proceed without external information

---

**Status:** Awaiting user input on dorm system details
**Priority:** High (blocks production readiness)
**Timeline:** Discovery should complete before Phase 4C
