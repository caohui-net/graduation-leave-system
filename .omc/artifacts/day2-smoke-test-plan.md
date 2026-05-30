# Day 2 Smoke Test Plan

**Created:** 2026-05-30 15:49
**Phase:** 6 - Smoke Tests
**Purpose:** End-to-end verification of security fixes

## Test Scenarios

### 1. Duplicate Submission Prevention
**Setup:** Reset database, seed data
**Steps:**
1. Student 2020001 submits first application
2. Student 2020001 attempts second submission
**Expected:** First succeeds (201), second fails (409)

### 2. Cross-Counselor Permission Check
**Setup:** Use existing T001/T002 chain data
**Steps:**
1. T002 attempts to approve T001's application
**Expected:** Fails with 403

### 3. Duplicate Approval Prevention
**Setup:** Counselor approves application
**Steps:**
1. T001 approves application (creates dean approval)
2. T001 attempts to approve again
**Expected:** First succeeds (200), second fails (409)

### 4. Status/Step Validation
**Setup:** Application in PENDING_COUNSELOR state
**Steps:**
1. Attempt dean approval on counselor-stage application
**Expected:** Fails with 409 (status/step mismatch)

## Evidence Collection

For each test:
- HTTP status code
- Response body
- Database state (Application.status, Approval.decision)
- Error messages

## Success Criteria

All 4 scenarios produce expected results with correct status codes and error messages.
