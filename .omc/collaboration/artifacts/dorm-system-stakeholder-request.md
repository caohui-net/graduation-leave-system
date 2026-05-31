# Dorm System Integration - Stakeholder Request

**Date:** 2026-05-31  
**Purpose:** Request information and access for dormitory management system integration  
**Priority:** High (blocks production readiness)

---

## Background

We are developing a graduation leave application system that requires integration with the dormitory management system to verify student checkout status before final approval.

**Current status:** Using mock provider that returns simulated checkout data. Need real integration for production deployment.

---

## Required Information

### 1. System Owner and Contact

**Questions:**
- Who owns/maintains the dormitory management system?
- Contact person for integration requests (name, email, phone)?
- Department responsible for system access and permissions?

---

### 2. Integration Method

**Options we can support:**
- **REST API:** Preferred method if available
- **SOAP API:** Can integrate if REST not available
- **Database read access:** Direct query if API not available
- **File export:** CSV/Excel periodic exports as fallback
- **Manual process:** Last resort if no system integration possible

**Questions:**
- What integration methods does your system support?
- Is there existing API documentation?
- What authentication method is required (API key, OAuth, database credentials)?

---

### 3. Data Requirements

**Minimum required fields:**
- Student ID (学号) - to match our student records
- Checkout status - completed/pending/not_started
- Checkout date - when checkout was completed (if applicable)
- Blocking reason - why checkout is pending (if applicable)

**Optional helpful fields:**
- Dorm building and room number
- Checkout operator (who processed the checkout)
- Checkout notes or comments

**Questions:**
- What fields are available in your system?
- What are the exact field names and data types?
- Are there additional fields that might be useful?

---

### 4. Access and Credentials

**Requirements:**
- API endpoint URL or database connection string
- Authentication credentials (API key, username/password, etc.)
- Network access information (VPN required? IP whitelist?)
- Test/sandbox environment for development and testing

**Questions:**
- How do we obtain access credentials?
- Is there a test environment we can use?
- What are the network access requirements?
- Are there rate limits or usage quotas?

---

### 5. Test Data

**Requirements:**
- Sample student IDs with known checkout statuses
- Examples of each status (completed, pending, not_started)
- Examples of blocking reasons (if applicable)
- Edge cases for testing (invalid student ID, system errors, etc.)

**Questions:**
- Can you provide test student IDs with known statuses?
- What are the possible checkout statuses in your system?
- What are common blocking reasons?

---

### 6. Technical Specifications

**Questions:**
- System availability and uptime (24/7 or business hours only)?
- Expected response time for queries?
- Data freshness (real-time or periodic updates)?
- Error handling and retry recommendations?
- Monitoring and alerting capabilities?

---

## Our Integration Approach

**Current implementation:**
- Mock provider interface: `DormCheckoutProvider.check_status(student_id) -> DormCheckoutResult`
- Returns: status (completed/pending/not_started/unknown), blocking_reason, checkout_date
- Error handling: graceful degradation if provider unavailable

**Production requirements:**
- Real provider adapter implementing same interface
- Caching layer to reduce load on your system
- Retry logic for transient failures
- Monitoring and alerting for integration health
- Fallback to manual verification if system unavailable

---

## Timeline

**Development phase:** Currently in Week 4 of 10-week development cycle  
**Production target:** Week 10 (approximately 6 weeks from now)  
**Integration deadline:** Week 7-8 (need access and testing by then)

**Immediate needs:**
- Contact information and initial discussion (this week)
- API documentation or database schema (Week 5)
- Test credentials and sandbox access (Week 6)
- Production credentials (Week 8)

---

## Next Steps

**Please provide:**
1. Contact information for system owner/integration lead
2. Any existing documentation (API docs, database schema, user guides)
3. Preferred integration method
4. Timeline for providing access and credentials

**We will:**
1. Review documentation and assess integration approach
2. Develop adapter implementation
3. Test in sandbox/test environment
4. Coordinate production deployment

---

## Contact Information

**Project team:**
- Project lead: [To be filled]
- Technical lead: [To be filled]
- Email: [To be filled]
- Phone: [To be filled]

---

**Status:** Ready to send to dormitory system stakeholders  
**Action:** Fill in contact information and send to appropriate department
