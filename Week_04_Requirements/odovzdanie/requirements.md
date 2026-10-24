# Software Requirements Specification

*Generated on 2026-10-24 from the input corpus `corpus` by an agentic requirements-refinement network.*

## Contents

1. [Introduction](#1-introduction)
2. [Source documents](#2-source-documents)
3. [Priority scale](#3-priority-scale)
4. [Glossary](#4-glossary)
5. [Requirements overview](#5-requirements-overview)
6. [Requirements by area](#6-requirements-by-area)
7. [Blacklist](#7-blacklist)
8. [Conflict resolution log](#8-conflict-resolution-log)
9. [Quality assurance](#9-quality-assurance)
10. [Appendix: traceability matrix](#appendix-traceability-matrix)

## 1. Introduction

This document specifies **268 requirements** derived from **20 source documents** (emails, meeting minutes, interviews, a survey, an early draft specification and reference documentation). The network extracted 667 candidate requirements, merged semantic duplicates, resolved conflicts, assigned priorities and reviewed the result in a validate-review-revise loop. Every requirement has a unique ID, a short name, a one-sentence statement, a paragraph-long description, a priority from the scale in section 3 and a trace to the documents it was derived from. Items that were discarded are listed with the reason in section 7.

| Pipeline step | Kind | Model |
|---|---|---|
| Loader | deterministic | - |
| Extractor | LLM | gpt-5-mini |
| Merger (taxonomy, merge, duplicate check) | LLM + code | gpt-5.6-luna |
| Conflict checker | LLM + code | gpt-6-luna |
| Prioritiser | LLM + code | gpt-5.6-luna |
| Validator | deterministic | - |
| Reviewer | LLM + code | gpt-6-luna |
| Reviser | LLM + code | gpt-5.6-luna |
| Renderer | deterministic | - |

## 2. Source documents

| ID | Type | Date | File | Title | Requirements |
|---|---|---|---|---|---|
| D01 | email | Mon, 06 Apr 2009 08:42:11 -0500 | `conversations/conv_pines014_material_volume.eml` | Volume reporting - how do we count what we have? | 11 |
| D02 | email | Wed, 08 Apr 2009 09:30:00 -0500 | `conversations/conv_pines015_capacity_interface.eml` | Can we see all branches at once? | 11 |
| D03 | email | Mon, 13 Apr 2009 10:15:00 -0500 | `conversations/conv_pines016_shelf_space.eml` | Shelf space vs. usage - help needed | 4 |
| D04 | email | Mon, 11 May 2009 09:00:00 -0500 | `conversations/conv_pines018_item_transfer.eml` | Moving items between branches - utility needed | 16 |
| D05 | email | Thu, 16 Apr 2009 09:00:00 -0500 | `conversations/conv_pines019_020_missing_intransit.eml` | Missing and damaged items - we need a report | 5 |
| D06 | email | Tue, 21 Apr 2009 08:30:00 -0500 | `conversations/conv_pines021_item_purging.eml` | Weeding reports - item purging needs | 6 |
| D07 | email | Fri, 24 Apr 2009 10:00:00 -0500 | `conversations/conv_pines022_deletions.eml` | Tracking deletions - who deleted what? | 10 |
| D08 | email | Wed, 29 Apr 2009 09:15:00 -0500 | `conversations/conv_pines023_patron_characteristics.eml` | Patron reports by demographics - how? | 5 |
| D09 | email | Tue, 05 May 2009 08:45:00 -0500 | `conversations/conv_pines024_inactive_patrons.eml` | Inactive patrons report needed | 11 |
| D10 | specification | January 27, 2009 | `early_draft_srs_galecia.txt` | DRAFT SOFTWARE REQUIREMENTS SPECIFICATION | 167 |
| D11 | email | Mon, 13 Jul 2009 09:15:00 -0500 | `email_financial_reports.eml` | Financial reporting requirements - discussion thread | 13 |
| D12 | email | Mon, 27 Jul 2009 08:30:00 -0500 | `email_report_features.eml` | Report features and interface requirements | 16 |
| D13 | email | Thu, 09 Apr 2009 09:15:32 -0500 | `email_staff_login.eml` | Staff login difficulties - need for streamlined access | 8 |
| D14 | reference | March 15, 2009 | `evergreen_reference_2009.txt` | EVERGREEN ILS - REPORTING MODULE OVERVIEW | 60 |
| D15 | interview | May 8, 2009 | `interview_cataloging_2009-05-08.txt` | PINES REPORTS WORKING GROUP - INTERVIEW RECORD | 21 |
| D16 | interview | May 10, 2009 | `interview_sysadmin_2009-05-10.txt` | PINES REPORTS WORKING GROUP - INTERVIEW RECORD | 14 |
| D17 | meeting | March 15, 2009 | `meeting_minutes/meeting_2009-03-15_minutes.txt` | PINES REPORTS WORKING GROUP - FIRST MEETING MINUTES | 13 |
| D18 | meeting | July 20, 2009 | `meeting_minutes/meeting_2009-07-20_minutes.txt` | PINES REPORTS WORKING GROUP - SECOND MEETING MINUTES | 34 |
| D19 | meeting | June 30, 2009 | `meeting_tech_subcommittee_2009-06-30.txt` | PINES TECHNICAL SUBCOMMITTEE MEETING NOTES | 21 |
| D20 | survey | April 1 - April 20, 2009 | `survey_results_2009.txt` | PINES STAFF REPORTS SURVEY - RESULTS SUMMARY | 41 |

## 3. Priority scale

Priorities follow the MoSCoW method. The prioritiser applied exactly these definitions, using the evidence in the sources: explicit priority wording, formal decisions in meeting minutes, the number of independent sources and stakeholders, survey support, and legal, security or technical obligations.

| Priority | Meaning | Requirements |
|---|---|---|
| **Must** | Essential for the system to be acceptable. Explicitly marked as critical or mandatory, agreed as a decision by the working group, required by law, audit or policy, or a hard technical constraint. Without it the system fails its purpose. | 50 |
| **Should** | Important and expected, typically requested by several stakeholders or sources, but the system is still usable without it for a time, or a workaround exists. | 113 |
| **Could** | Desirable improvement with limited impact, typically raised by a single stakeholder or as an example; implemented if time and budget allow. | 103 |
| **Won't** | Acknowledged but explicitly deferred or of very low value for this release; recorded so it is not forgotten. | 2 |

## 4. Glossary

All requirements use the preferred terms below (consistent vocabulary).

| Term | Definition | Instead of |
|---|---|---|
| **audit log** | An append-only record of significant actions, changes, access decisions, or deletions. | audit trail, history log, activity log |
| **bibliographic record** | The descriptive catalog record representing a work or title. | bib record, bibliographic record entry, title record |
| **branch** | A physical library location represented in the system. | library, site, location when referring to a physical library branch |
| **branch location** | The branch associated with an item, transaction, patron, or report scope. | library location, site location, home library |
| **consortium** | The group of branches and organizations managed together by the system. | library system, network, enterprise when referring to the participating library group |
| **historical reporting** | Reporting against data preserved for a prior point in time or period. | snapshot reporting, ย้อนหลัง reporting, archive reporting |
| **ILS** | The integrated library system that supplies or consumes library operational data. | library platform, back-end system, core system |
| **in-transit item** | An item currently moving between branches or other destinations. | transit item, transfer item, shipping item |
| **item** | A physical or digital copy that can be circulated or managed. | copy, volume, resource when referring to a specific cataloged unit |
| **null value** | A database value that is absent or unknown, distinct from an empty string or zero. | blank, empty, missing value when referring specifically to database null |
| **output format** | The file or presentation format used to deliver report results. | export type, file type, media type |
| **patron** | A person who is eligible to use library services and has a patron record. | borrower, member, customer, user when referring to a library patron |
| **permission** | An individual authorization to perform an operation or access data. | privilege, right, access when referring to a specific authorization |
| **query** | A saved or ad hoc specification for selecting and relating data. | search, filter when referring to the complete data-selection definition |
| **report** | A generated presentation of selected, calculated, or aggregated system data. | listing, output, extract when referring to a generated report |
| **report run** | One execution of a report or report template. | job, process, instance when referring to a report execution |
| **report template** | A reusable definition of a report's fields, criteria, layout, and output behavior. | report form, canned query, report model |
| **staff role** | A named set of permissions assigned to one or more staff users. | user type, profile, group when referring to authorization capabilities |
| **staff user** | An authenticated person who operates the system on behalf of the organization. | librarian, employee, operator, administrator when referring to a general staff user |
| **transaction** | A recorded circulation, hold, payment, billing, or related business event. | activity, event, operation when referring to a business record |

## 5. Requirements overview

| ID | Name | Priority | Area | Sources |
|---|---|---|---|---|
| [REQ-001](#req-001) | Board and Executive Reports | Must | Reporting and analytics | D10, D12, D18 |
| [REQ-002](#req-002) | Canned Report Definitions | Must | Reporting and analytics | D10 |
| [REQ-003](#req-003) | Consortium Reporting Configuration | Must | Reporting and analytics | D17 |
| [REQ-004](#req-004) | Executive Reports Interface | Must | Reporting and analytics | D17, D18 |
| [REQ-005](#req-005) | Fine-Grained Reporting | Must | Reporting and analytics | D10 |
| [REQ-006](#req-006) | Management Reporting Tools | Must | Reporting and analytics | D17 |
| [REQ-007](#req-007) | Circulation Reports | Should | Reporting and analytics | D20 |
| [REQ-008](#req-008) | Configurable Report Levels | Should | Reporting and analytics | D09 |
| [REQ-009](#req-009) | Cross-Branch Comparison Reporting | Should | Reporting and analytics | D03, D18 |
| [REQ-010](#req-010) | Cross-Tabulated Transaction Reports | Should | Reporting and analytics | D10, D12 |
| [REQ-011](#req-011) | Deletion Audit Query Interface | Should | Reporting and analytics | D07 |
| [REQ-012](#req-012) | Demographic Filtering and Grouping | Should | Reporting and analytics | D08, D10 |
| [REQ-013](#req-013) | Historical Reporting | Should | Reporting and analytics | D01, D10, D14, D19, D20 |
| [REQ-014](#req-014) | Material Item Count Report | Should | Reporting and analytics | D01, D10, D15 |
| [REQ-015](#req-015) | Missing Item Reports | Should | Reporting and analytics | D10, D20 |
| [REQ-016](#req-016) | Multi-Level Data Aggregation | Should | Reporting and analytics | D02, D03 |
| [REQ-017](#req-017) | Report Queue Visibility | Should | Reporting and analytics | D10, D12, D14, D18, D20 |
| [REQ-018](#req-018) | Shelf Space Reporting and Estimation | Should | Reporting and analytics | D03, D10, D15, D18 |
| [REQ-019](#req-019) | Staff Productivity Reports | Should | Reporting and analytics | D17, D20 |
| [REQ-020](#req-020) | Transaction Activity Reports | Should | Reporting and analytics | D10, D12 |
| [REQ-021](#req-021) | Uncataloged Material Usage Reporting | Should | Reporting and analytics | D10, D15 |
| [REQ-022](#req-022) | Branch Capacity Trends | Could | Reporting and analytics | D02 |
| [REQ-023](#req-023) | Configurable Capacity Metrics | Could | Reporting and analytics | D02 |
| [REQ-024](#req-024) | Deletion Location Reports | Could | Reporting and analytics | D07 |
| [REQ-025](#req-025) | Deletion Period Reports | Could | Reporting and analytics | D07 |
| [REQ-026](#req-026) | Deletion Transaction Aggregation | Could | Reporting and analytics | D07 |
| [REQ-027](#req-027) | Deletion Type Reports | Could | Reporting and analytics | D07 |
| [REQ-028](#req-028) | Expanded Report Types | Could | Reporting and analytics | D14 |
| [REQ-029](#req-029) | Holdings Time-Series Reports | Could | Reporting and analytics | D01 |
| [REQ-030](#req-030) | Inactive Patron Branch Counts | Could | Reporting and analytics | D09 |
| [REQ-031](#req-031) | Top Deleting Users Report | Could | Reporting and analytics | D07 |
| [REQ-032](#req-032) | Expose Reporting Fields | Must | Query and data selection | D14, D20 |
| [REQ-033](#req-033) | Query Data Access Control | Must | Query and data selection | D10 |
| [REQ-034](#req-034) | Advanced Query Builder | Should | Query and data selection | D08, D10, D12, D14 |
| [REQ-035](#req-035) | Filter Branches | Should | Query and data selection | D02 |
| [REQ-036](#req-036) | Filter by Branch Location | Should | Query and data selection | D01 |
| [REQ-037](#req-037) | Flexible Reporting Periods | Should | Query and data selection | D03 |
| [REQ-038](#req-038) | Manual Selection of Transfer Items | Should | Query and data selection | D04, D10, D15, D20 |
| [REQ-039](#req-039) | Query Candidate Materials | Should | Query and data selection | D04, D20 |
| [REQ-040](#req-040) | Report Selection Criteria Disclosure | Should | Query and data selection | D10, D12, D14 |
| [REQ-041](#req-041) | Save Transfer and Other Queries | Should | Query and data selection | D04, D10, D15, D20 |
| [REQ-042](#req-042) | Sort Branch Lists | Should | Query and data selection | D02 |
| [REQ-043](#req-043) | Consolidated MARC Fields in Reports | Could | Query and data selection | D10, D20 |
| [REQ-044](#req-044) | Exclude Specified Patrons | Could | Query and data selection | D09 |
| [REQ-045](#req-045) | Filter by Survey Name | Could | Query and data selection | D10, D19 |
| [REQ-046](#req-046) | Upload Filter Lists | Could | Query and data selection | D10, D14 |
| [REQ-047](#req-047) | Consortium Template Support | Must | Report authoring and presentation | D17, D18 |
| [REQ-048](#req-048) | Report Output Formats | Must | Report authoring and presentation | D10, D14, D19, D20 |
| [REQ-049](#req-049) | Staff Report Authoring | Must | Report authoring and presentation | D10, D17, D20 |
| [REQ-050](#req-050) | Template Query Migration | Must | Report authoring and presentation | D19 |
| [REQ-051](#req-051) | Administrator Template Creation | Should | Report authoring and presentation | D10, D12, D20 |
| [REQ-052](#req-052) | Branch Capacity Overview | Should | Report authoring and presentation | D02, D10 |
| [REQ-053](#req-053) | Consolidated Report Output | Should | Report authoring and presentation | D01, D10 |
| [REQ-054](#req-054) | Customizable Report Categories | Should | Report authoring and presentation | D01 |
| [REQ-055](#req-055) | Email Report Delivery | Should | Report authoring and presentation | D10, D14, D20 |
| [REQ-056](#req-056) | Inactive Patron Fine Flags | Should | Report authoring and presentation | D09 |
| [REQ-057](#req-057) | Inactive Patron Mailing Addresses | Should | Report authoring and presentation | D09 |
| [REQ-058](#req-058) | Open Template Reporting | Should | Report authoring and presentation | D10, D14 |
| [REQ-059](#req-059) | Report Template Edit Restrictions | Should | Report authoring and presentation | D10, D12 |
| [REQ-060](#req-060) | Reporting Interface Types | Should | Report authoring and presentation | D10, D14 |
| [REQ-061](#req-061) | Separate Edit and Circulation Dates | Should | Report authoring and presentation | D14, D15 |
| [REQ-062](#req-062) | Template Management | Should | Report authoring and presentation | D14 |
| [REQ-063](#req-063) | Template Run Or Modify | Should | Report authoring and presentation | D10, D12 |
| [REQ-064](#req-064) | Canned Report Date Presets | Could | Report authoring and presentation | D10 |
| [REQ-065](#req-065) | Canned Report Display Editing | Could | Report authoring and presentation | D10, D14 |
| [REQ-066](#req-066) | Capacity Status Indicators | Could | Report authoring and presentation | D02 |
| [REQ-067](#req-067) | Clone Report Definitions | Could | Report authoring and presentation | D12 |
| [REQ-068](#req-068) | Collection Development Reports | Could | Report authoring and presentation | D20 |
| [REQ-069](#req-069) | Comparative Report Columns | Could | Report authoring and presentation | D10 |
| [REQ-070](#req-070) | Prewritten Report Templates | Could | Report authoring and presentation | D10 |
| [REQ-071](#req-071) | Program Attendance Reports | Could | Report authoring and presentation | D20 |
| [REQ-072](#req-072) | Report Delivery Address Book | Could | Report authoring and presentation | D10, D14 |
| [REQ-073](#req-073) | Selectable Report Data | Could | Report authoring and presentation | D10 |
| [REQ-074](#req-074) | Shared Report Spaces | Could | Report authoring and presentation | D14 |
| [REQ-075](#req-075) | Template Sharing Controls | Could | Report authoring and presentation | D14 |
| [REQ-076](#req-076) | Background Report Processing | Must | Report operations and delivery | D09, D14, D16, D18 |
| [REQ-077](#req-077) | Last Item Report | Must | Report operations and delivery | D06, D10, D14, D15 |
| [REQ-078](#req-078) | Cancel Report Runs | Should | Report operations and delivery | D10, D14, D19, D20 |
| [REQ-079](#req-079) | Data Quality Reports | Should | Report operations and delivery | D10, D15, D18 |
| [REQ-080](#req-080) | Prioritize Report Queue | Should | Report operations and delivery | D10, D12, D14 |
| [REQ-081](#req-081) | Recurring Report Scheduling | Should | Report operations and delivery | D09, D10, D14, D20 |
| [REQ-082](#req-082) | Bibliographic Records With Holds | Could | Report operations and delivery | D10 |
| [REQ-083](#req-083) | Bibliographic Records Without Items Report | Could | Report operations and delivery | D10, D15 |
| [REQ-084](#req-084) | Capacity Data CSV Export | Could | Report operations and delivery | D02 |
| [REQ-085](#req-085) | Edit Recurring Report Selections | Could | Report operations and delivery | D10 |
| [REQ-086](#req-086) | In-Transit Items With Holds | Could | Report operations and delivery | D10 |
| [REQ-087](#req-087) | Inactive Patrons CSV Export | Could | Report operations and delivery | D09 |
| [REQ-088](#req-088) | Invalid Patron Branch Report | Could | Report operations and delivery | D10 |
| [REQ-089](#req-089) | Item-Level Holds | Could | Report operations and delivery | D10 |
| [REQ-090](#req-090) | Items Not Recently Checked Out | Could | Report operations and delivery | D10 |
| [REQ-091](#req-091) | Overdue In-Transit Items | Could | Report operations and delivery | D10 |
| [REQ-092](#req-092) | Schedule Multiple Reports | Could | Report operations and delivery | D14 |
| [REQ-093](#req-093) | Accurate Check-In Timestamp | Must | Circulation and transaction reporting | D14, D20 |
| [REQ-094](#req-094) | Check-In Count Reporting | Must | Circulation and transaction reporting | D10, D20 |
| [REQ-095](#req-095) | Checkout and Renewal Count Reporting | Must | Circulation and transaction reporting | D10, D20 |
| [REQ-096](#req-096) | Checkout Count Report | Must | Circulation and transaction reporting | D10 |
| [REQ-097](#req-097) | Total Circulation Count Report | Must | Circulation and transaction reporting | D10 |
| [REQ-098](#req-098) | Branch Holds Count | Should | Circulation and transaction reporting | D01 |
| [REQ-099](#req-099) | Circulation By Age Demographic | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-100](#req-100) | Circulation By County | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-101](#req-101) | Circulation By Dewey | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-102](#req-102) | Circulation By MARC Fields | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-103](#req-103) | Circulation Reporting by Modifier Categories | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-104](#req-104) | Claims Returned Report | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-105](#req-105) | Hold Status Reports | Should | Circulation and transaction reporting | D01, D10, D20 |
| [REQ-106](#req-106) | Holds Purchase Alert Report | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-107](#req-107) | Items In Circulation Count | Should | Circulation and transaction reporting | D01 |
| [REQ-108](#req-108) | Items On Shelf Count | Should | Circulation and transaction reporting | D01 |
| [REQ-109](#req-109) | Patron Transaction Totals | Should | Circulation and transaction reporting | D10 |
| [REQ-110](#req-110) | Stale Holds Report | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-111](#req-111) | Transaction Grouping Dimensions | Should | Circulation and transaction reporting | D10, D20 |
| [REQ-112](#req-112) | Transactions By Reporting Scope | Should | Circulation and transaction reporting | D10, D20 |
| [REQ-113](#req-113) | Unfilled Holds Report | Should | Circulation and transaction reporting | D10, D14 |
| [REQ-114](#req-114) | Annual Holds Placed Report | Could | Circulation and transaction reporting | D10 |
| [REQ-115](#req-115) | Circulation By Home Branch | Could | Circulation and transaction reporting | D10 |
| [REQ-116](#req-116) | Circulation By Shelving Location | Could | Circulation and transaction reporting | D10 |
| [REQ-117](#req-117) | Hold Request Origin Counts | Could | Circulation and transaction reporting | D10 |
| [REQ-118](#req-118) | In-House Use Count Report | Could | Circulation and transaction reporting | D10 |
| [REQ-119](#req-119) | IntraPINES Loans Report | Could | Circulation and transaction reporting | D10 |
| [REQ-120](#req-120) | Items Received For Holds | Could | Circulation and transaction reporting | D10 |
| [REQ-121](#req-121) | Items Sent For Holds | Could | Circulation and transaction reporting | D10 |
| [REQ-122](#req-122) | Monthly Non-Cat In-House Use | Could | Circulation and transaction reporting | D10 |
| [REQ-123](#req-123) | Non-Cat Count Reports | Could | Circulation and transaction reporting | D10 |
| [REQ-124](#req-124) | Transaction Type Reporting | Could | Circulation and transaction reporting | D20 |
| [REQ-125](#req-125) | Transaction Workstation Filters | Could | Circulation and transaction reporting | D10 |
| [REQ-126](#req-126) | Branch Capacity Distribution Analysis | Must | Inventory and collection management | D17 |
| [REQ-127](#req-127) | Collection Usage Analysis | Must | Inventory and collection management | D17 |
| [REQ-128](#req-128) | Consolidated In-Transit Item Reporting | Must | Inventory and collection management | D05, D10, D15, D18 |
| [REQ-129](#req-129) | Missing and Damaged Item Reporting | Must | Inventory and collection management | D05, D10, D15, D18 |
| [REQ-130](#req-130) | Batch Item Branch-Location Changes | Should | Inventory and collection management | D04, D10, D15, D20 |
| [REQ-131](#req-131) | Batch Item Status Conversion | Should | Inventory and collection management | D06, D15 |
| [REQ-132](#req-132) | Collection Price Value Report | Should | Inventory and collection management | D10, D14 |
| [REQ-133](#req-133) | Configurable Overdue Reports | Should | Inventory and collection management | D10, D14 |
| [REQ-134](#req-134) | Configurable Purge Candidate Criteria | Should | Inventory and collection management | D06, D10, D15 |
| [REQ-135](#req-135) | Inventory Reports | Should | Inventory and collection management | D18 |
| [REQ-136](#req-136) | Item Use Count Report | Should | Inventory and collection management | D10, D14 |
| [REQ-137](#req-137) | Items Added Date Reporting | Should | Inventory and collection management | D10, D14 |
| [REQ-138](#req-138) | Low-Labor Uncataloged Material Processing | Should | Inventory and collection management | D10, D15 |
| [REQ-139](#req-139) | Missing MARC Fields Report | Should | Inventory and collection management | D10, D14 |
| [REQ-140](#req-140) | New Acquisitions Report | Should | Inventory and collection management | D01 |
| [REQ-141](#req-141) | Quick Uncataloged Distribution | Should | Inventory and collection management | D10, D15 |
| [REQ-142](#req-142) | Transfer Reversion to Original Branch | Should | Inventory and collection management | D04, D10, D15, D20 |
| [REQ-143](#req-143) | Uncataloged Inventory Tracking | Should | Inventory and collection management | D10, D15 |
| [REQ-144](#req-144) | Weeding Report | Should | Inventory and collection management | D10, D14, D18 |
| [REQ-145](#req-145) | Batch Status Conversion Report | Could | Inventory and collection management | D10 |
| [REQ-146](#req-146) | Bibliographic Records Added Report | Could | Inventory and collection management | D10, D14 |
| [REQ-147](#req-147) | Bibliographic Records Count | Could | Inventory and collection management | D10 |
| [REQ-148](#req-148) | Bibliographic Records Edited Report | Could | Inventory and collection management | D10, D14 |
| [REQ-149](#req-149) | Bibliographic Text Item Report | Could | Inventory and collection management | D10 |
| [REQ-150](#req-150) | Branch Capacity Drill-Down | Could | Inventory and collection management | D02 |
| [REQ-151](#req-151) | Branch Capacity Reports | Could | Inventory and collection management | D18 |
| [REQ-152](#req-152) | Collection Age Report | Could | Inventory and collection management | D10, D14 |
| [REQ-153](#req-153) | Currently Checked-Out Items | Could | Inventory and collection management | D10 |
| [REQ-154](#req-154) | Deleted Items Count | Could | Inventory and collection management | D10 |
| [REQ-155](#req-155) | Deleted Last Copy Report | Could | Inventory and collection management | D10 |
| [REQ-156](#req-156) | Deleted Last-Item Report | Could | Inventory and collection management | D10 |
| [REQ-157](#req-157) | Fines-Stopped Item Reporting | Could | Inventory and collection management | D10, D14 |
| [REQ-158](#req-158) | High-Use Items Report | Could | Inventory and collection management | D10 |
| [REQ-159](#req-159) | Item Circulation Date | Could | Inventory and collection management | D20 |
| [REQ-160](#req-160) | Items Count Report | Could | Inventory and collection management | D10 |
| [REQ-161](#req-161) | Items Edited Report | Could | Inventory and collection management | D10, D14 |
| [REQ-162](#req-162) | Long-Overdue Item Reporting | Could | Inventory and collection management | D10 |
| [REQ-163](#req-163) | Manual and Scheduled Purge and Cleanup | Could | Inventory and collection management | D06 |
| [REQ-164](#req-164) | Missing Damaged Title Frequencies | Could | Inventory and collection management | D05 |
| [REQ-165](#req-165) | Item Transfer Utility | Should | Transfers and transit management | D10, D15 |
| [REQ-166](#req-166) | Overdue In-Transit Detection Threshold | Should | Transfers and transit management | D05 |
| [REQ-167](#req-167) | Printable Transfer Pull Lists | Should | Transfers and transit management | D04 |
| [REQ-168](#req-168) | Query Transfer Candidates | Should | Transfers and transit management | D10, D15 |
| [REQ-169](#req-169) | Sort In-Transit by Due Date | Should | Transfers and transit management | D05 |
| [REQ-170](#req-170) | Undo Transfer Operation | Should | Transfers and transit management | D04 |
| [REQ-171](#req-171) | Printable Transit Labels | Could | Transfers and transit management | D04 |
| [REQ-172](#req-172) | Provide Demographic Analysis Reports | Must | Patron and demographic reporting | D10, D17, D18, D20 |
| [REQ-173](#req-173) | Calculate Configurable Age Brackets | Should | Patron and demographic reporting | D08 |
| [REQ-174](#req-174) | Provide Patron Count Reports | Should | Patron and demographic reporting | D10, D14 |
| [REQ-175](#req-175) | Report Patron Behavior Statistics | Should | Patron and demographic reporting | D10, D20 |
| [REQ-176](#req-176) | Report Patron Inactivity | Should | Patron and demographic reporting | D09, D10 |
| [REQ-177](#req-177) | Use Patron Table Demographics | Should | Patron and demographic reporting | D08 |
| [REQ-178](#req-178) | List Patrons by Survey Answer | Could | Patron and demographic reporting | D10 |
| [REQ-179](#req-179) | Monthly Patron Addition Reporting | Could | Patron and demographic reporting | D10 |
| [REQ-180](#req-180) | Report Barred Patrons | Could | Patron and demographic reporting | D10 |
| [REQ-181](#req-181) | Report Inactive Status Patrons | Could | Patron and demographic reporting | D10, D14 |
| [REQ-182](#req-182) | Report Patrons by Expiration | Could | Patron and demographic reporting | D10 |
| [REQ-183](#req-183) | Report Patrons by Notes | Could | Patron and demographic reporting | D10 |
| [REQ-184](#req-184) | Report Voter Survey Responses | Could | Patron and demographic reporting | D10, D14 |
| [REQ-185](#req-185) | Accounting Audit Compliance | Must | Financial reporting and accounts | D10, D11 |
| [REQ-186](#req-186) | Financial Reporting Verification | Must | Financial reporting and accounts | D17, D18, D20 |
| [REQ-187](#req-187) | Aged Debt Reporting | Should | Financial reporting and accounts | D10, D14 |
| [REQ-188](#req-188) | Balance Threshold Query | Should | Financial reporting and accounts | D10, D11 |
| [REQ-189](#req-189) | Branch Payment and Waiver Tracking | Should | Financial reporting and accounts | D10, D11 |
| [REQ-190](#req-190) | Financial Transaction Associations | Should | Financial reporting and accounts | D10, D11 |
| [REQ-191](#req-191) | Fines Charges Accrual Reports | Should | Financial reporting and accounts | D10, D11 |
| [REQ-192](#req-192) | Fines Waived Reports | Should | Financial reporting and accounts | D10, D11 |
| [REQ-193](#req-193) | Item Value Report | Should | Financial reporting and accounts | D10, D11 |
| [REQ-194](#req-194) | Patron Balance Reports | Should | Financial reporting and accounts | D10, D11 |
| [REQ-195](#req-195) | Payments Time Method Reports | Should | Financial reporting and accounts | D10, D11 |
| [REQ-196](#req-196) | Bills Owed Report | Could | Financial reporting and accounts | D10 |
| [REQ-197](#req-197) | Detailed Payment Reporting | Could | Financial reporting and accounts | D10 |
| [REQ-198](#req-198) | Detailed Voids Report | Could | Financial reporting and accounts | D10 |
| [REQ-199](#req-199) | Easy Financial Updates | Could | Financial reporting and accounts | D10 |
| [REQ-200](#req-200) | Historical Snapshot Bills | Could | Financial reporting and accounts | D14, D20 |
| [REQ-201](#req-201) | Anonymize Demographic Statistics | Must | Data governance, audit, and retention | D10, D20 |
| [REQ-202](#req-202) | Financial Retention Enforcement | Must | Data governance, audit, and retention | D11 |
| [REQ-203](#req-203) | Include Null and Blank Records | Must | Data governance, audit, and retention | D08, D10, D14, D19, D20 |
| [REQ-204](#req-204) | Payment Reconciliation Ledger | Must | Data governance, audit, and retention | D10, D11 |
| [REQ-205](#req-205) | Privacy-Protected Transaction Archive | Must | Data governance, audit, and retention | D10, D12 |
| [REQ-206](#req-206) | Deletion Audit Logging | Should | Data governance, audit, and retention | D06, D07 |
| [REQ-207](#req-207) | Deletion Compliance Reports | Should | Data governance, audit, and retention | D07 |
| [REQ-208](#req-208) | Deletion Counts Tracking | Should | Data governance, audit, and retention | D07, D10, D15, D20 |
| [REQ-209](#req-209) | Destructive Operation Safeguards | Should | Data governance, audit, and retention | D06 |
| [REQ-210](#req-210) | Transaction Retention Aggregates | Should | Data governance, audit, and retention | D10, D20 |
| [REQ-211](#req-211) | Denied Deletion Attempt Logging | Could | Data governance, audit, and retention | D07 |
| [REQ-212](#req-212) | Report Run Audit History | Could | Data governance, audit, and retention | D14 |
| [REQ-213](#req-213) | Report Template Integrity | Could | Data governance, audit, and retention | D10 |
| [REQ-214](#req-214) | Staff Login Audit Logging | Could | Data governance, audit, and retention | D13 |
| [REQ-215](#req-215) | Transfer History Display | Could | Data governance, audit, and retention | D04 |
| [REQ-216](#req-216) | Transfer Operation Audit Log | Could | Data governance, audit, and retention | D04 |
| [REQ-217](#req-217) | Unique Excel Export Rows | Could | Data governance, audit, and retention | D20 |
| [REQ-218](#req-218) | Local System Configuration | Must | Security and access control | D17 |
| [REQ-219](#req-219) | Predefined Staff Role Support | Must | Security and access control | D10, D16, D17, D19 |
| [REQ-220](#req-220) | Role and Permission Administration | Must | Security and access control | D10, D12, D13, D16, D19 |
| [REQ-221](#req-221) | Role-Based Permission Assignment | Must | Security and access control | D10, D13, D16, D18, D19 |
| [REQ-222](#req-222) | Fine-Grained Report Permissions | Should | Security and access control | D10, D12, D14, D20 |
| [REQ-223](#req-223) | Item Transfer Authorization | Should | Security and access control | D04 |
| [REQ-224](#req-224) | Session Security Controls | Should | Security and access control | D13 |
| [REQ-225](#req-225) | Shared Report Folders | Should | Security and access control | D10, D12, D20 |
| [REQ-226](#req-226) | Staff Identity Authentication | Should | Security and access control | D10, D13, D18 |
| [REQ-227](#req-227) | Username Password Fallback | Should | Security and access control | D10, D13 |
| [REQ-228](#req-228) | Staff Password Change Report | Could | Security and access control | D14 |
| [REQ-229](#req-229) | Centralized Multi-Branch Operation | Must | Integration and data architecture | D10, D18, D19 |
| [REQ-230](#req-230) | OPAC Feature Independence | Must | Integration and data architecture | D10, D18 |
| [REQ-231](#req-231) | PostgreSQL 8.3 Compatibility | Must | Integration and data architecture | D16 |
| [REQ-232](#req-232) | Read-Only ILS Integration | Must | Integration and data architecture | D10, D18, D19 |
| [REQ-233](#req-233) | Read-Only OPAC Integration | Must | Integration and data architecture | D10, D18, D19 |
| [REQ-234](#req-234) | Relational Reporting Backend | Must | Integration and data architecture | D10, D16, D18, D19 |
| [REQ-235](#req-235) | Vendor Data Interfaces | Must | Integration and data architecture | D10, D18, D19 |
| [REQ-236](#req-236) | Combined Financial Data | Should | Integration and data architecture | D11 |
| [REQ-237](#req-237) | Documented Technical Constraints | Should | Integration and data architecture | D18 |
| [REQ-238](#req-238) | Reportable Record Types | Could | Integration and data architecture | D14 |
| [REQ-239](#req-239) | Reusable Transfer Query Tool | Could | Integration and data architecture | D04 |
| [REQ-240](#req-240) | Unified Patron Activity Query | Could | Integration and data architecture | D09 |
| [REQ-241](#req-241) | Separate Reporting Database | Won't | Integration and data architecture | D14 |
| [REQ-242](#req-242) | Client Access Options | Must | Deployment and environments | D10, D18 |
| [REQ-243](#req-243) | Environment Separation and Migration | Must | Deployment and environments | D10, D14, D16, D18, D19 |
| [REQ-244](#req-244) | Supported Server Platforms | Must | Deployment and environments | D10, D16, D18 |
| [REQ-245](#req-245) | Browser Compatibility | Should | Deployment and environments | D10, D16, D18 |
| [REQ-246](#req-246) | Enterprise ILS Deployment Context | Should | Deployment and environments | D10, D18, D19 |
| [REQ-247](#req-247) | Optional Card-Reader Deployment | Could | Deployment and environments | D13 |
| [REQ-248](#req-248) | Optional Streamlined Login | Could | Deployment and environments | D13 |
| [REQ-249](#req-249) | Patron-Facing Scope Exclusion | Won't | Deployment and environments | D17 |
| [REQ-250](#req-250) | Accessibility Support | Must | Usability, accessibility, and documentation | D10, D14, D16, D18, D19 |
| [REQ-251](#req-251) | Integrated Hierarchical Help | Must | Usability, accessibility, and documentation | D10, D14, D16, D18, D19 |
| [REQ-252](#req-252) | Standards-Compliant HTML | Must | Usability, accessibility, and documentation | D10, D16, D18, D19 |
| [REQ-253](#req-253) | Detailed Error Feedback | Should | Usability, accessibility, and documentation | D10, D18, D19 |
| [REQ-254](#req-254) | Usable Reporting Interfaces | Should | Usability, accessibility, and documentation | D12, D20 |
| [REQ-255](#req-255) | Batch Transfer Preview | Could | Usability, accessibility, and documentation | D04 |
| [REQ-256](#req-256) | Branch Grouping | Could | Usability, accessibility, and documentation | D02 |
| [REQ-257](#req-257) | Quick-Access Report Guidance | Could | Usability, accessibility, and documentation | D10, D14 |
| [REQ-258](#req-258) | Consortium Capacity Support | Must | Performance, scalability, and reliability | D10, D18 |
| [REQ-259](#req-259) | Interactive Service Protection | Must | Performance, scalability, and reliability | D10, D16, D19 |
| [REQ-260](#req-260) | Immediate Financial Updates | Should | Performance, scalability, and reliability | D11 |
| [REQ-261](#req-261) | Report Performance Under Load | Should | Performance, scalability, and reliability | D10, D14, D20 |
| [REQ-262](#req-262) | Transaction-Safe Batch Updates | Should | Performance, scalability, and reliability | D04 |
| [REQ-263](#req-263) | Efficient Batch Transfers | Could | Performance, scalability, and reliability | D04 |
| [REQ-264](#req-264) | Read-Only Reporting Replicas | Could | Performance, scalability, and reliability | D16 |
| [REQ-265](#req-265) | Scalable Capacity Overview | Could | Performance, scalability, and reliability | D02 |
| [REQ-266](#req-266) | Configure Transfer Alert Recipients | Should | Notifications and workflow automation | D04 |
| [REQ-267](#req-267) | Assign Cleanup Tasks | Could | Notifications and workflow automation | D09 |
| [REQ-268](#req-268) | Run Notice Reports | Could | Notifications and workflow automation | D10 |

## 6. Requirements by area

### 6.1 Reporting and analytics

*31 requirements - Must: 6, Should: 15, Could: 10, Won't: 0*

<a id="req-001"></a>
#### REQ-001 Board and Executive Reports

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide predefined board and executive reports for staff users and external consumers, including statistics required for the Georgia Annual Report and Application for State Aid.

Staff users need standardized reports for boards, executives, and other external consumers. The predefined reports shall include basic statistics required by the Georgia Annual Report and Application for State Aid. They shall be runnable by staff users and support governance and compliance reporting.

*Priority rationale:* It is supported by 12 stakeholders and three source types, and includes statistics required for the Georgia Annual Report and Application for State Aid, indicating a policy or compliance need.

*Stakeholders:* External consumers, State reporting, directors, library boards, admins, Library boards, Library Managers, Library Administrators ...

<details><summary>Evidence</summary>

- D10: "These should include basic statistics like those required by the Georgia Annual Report and Application for State Aid."
- D12: "Pre-defined reports for library boards with basic statistics (Georgia Annual Report requirements)."
- D10: "The system should provide pre-defined reports for consumption by library boards and other external consumers."

</details>

<a id="req-002"></a>
#### REQ-002 Canned Report Definitions

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall support the canned report definitions described in Appendix A.

Staff users need the report definitions documented in the supplied report examples. The system shall support the fields, criteria, and behavior needed to implement those canned reports. Appendix A is the authoritative source for the specific definitions covered by this requirement.

*Priority rationale:* The requirement is explicitly marked “must,” which is a direct priority signal despite being documented only in the specification.

*Stakeholders:* Administrators, Staff

<details><summary>Evidence</summary>

- D10: "The system must be able to support the reporting definitions as described in the attached report examples (see Appendix A)."

</details>

<a id="req-003"></a>
#### REQ-003 Consortium Reporting Configuration

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt)

**Statement:** The system shall allow the Global System Administrator to configure the system and generate statistical reports for the consortium as a whole.

The Global System Administrator needs consortium-level control over reporting and related system configuration. The system shall support applying software changes and configurations at the consortium level. It shall also generate aggregated statistical reports for the entire consortium.

*Priority rationale:* The meeting recorded agreement that the Global System Administrator would configure the system and generate consortium-level reports, providing formal decision evidence.

*Stakeholders:* Global System Administrator, PINES Services Specialist

<details><summary>Evidence</summary>

- D17: "Global System Administrator: Manages PINES at the consortium level, implementing software changes and configurations, and generating statistical reports for PINES as a whole."

</details>

<a id="req-004"></a>
#### REQ-004 Executive Reports Interface

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide an Executive Reports Interface containing a compiled list of reports suitable for executive and board use.

Executive and board users need a focused interface for accessing high-level reports. The interface shall present a compiled list of prioritized or summary reports. It supports oversight and decision-making without requiring users to locate individual reports elsewhere.

*Priority rationale:* The Executive Reports Interface was accepted twice in meeting minutes as part of the adopted Reports Working Group mission.

*Stakeholders:* Library Directors, Library Managers, Global System Administrator, Reports Working Group, Katherine Gregory, Directors, Board members

<details><summary>Evidence</summary>

- D17: "Compile a list of reports needed for an Executive Reports Interface."
- D18: "Compile a list of reports needed for an Executive Reports Interface."

</details>

<a id="req-005"></a>
#### REQ-005 Fine-Grained Reporting

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall support the fine-grained reporting requirements described in Appendix B.

Staff users need the detailed reporting capabilities documented in the supplied specification. The system shall support the fine-grained reports and data-selection behavior described in Appendix B. Appendix B is the authoritative source for the specific requirements covered by this capability.

*Priority rationale:* The requirement is explicitly marked “must” in the specification, providing a direct mandatory priority signal.

*Stakeholders:* Administrators, Staff

<details><summary>Evidence</summary>

- D10: "The system must be able to support the fine-grained reports requirements as described in the attached specification (see Appendix B)."

</details>

<a id="req-006"></a>
#### REQ-006 Management Reporting Tools

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt)

**Statement:** The system shall provide reports and analysis tools for planning, evaluation, and oversight by managers and staff users.

The reporting and analytics area shall focus on management processes rather than patron-facing functions. Managers and staff users need tools for planning, evaluating results, and overseeing operations. The tools shall support analysis of organizational data for those purposes.

*Priority rationale:* Meeting minutes formally accepted management reporting and analysis tools as part of the system scope, with five stakeholders supporting the scope.

*Stakeholders:* Library Managers, Library Directors, Local System Administrators, Staff, Global System Administrator

<details><summary>Evidence</summary>

- D17: "Katherine explained that the group would focus on Management Processes - that is, reports and analysis tools used by library managers, administrators, and staff for planning, evaluation, and oversight purposes."

</details>

<a id="req-007"></a>
#### REQ-007 Circulation Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D20 (survey_results_2009.txt)

**Statement:** The system shall provide circulation reports including checkouts, check-ins, and renewals.

Staff users need reports focused on circulation transactions. The reports shall include checkout, check-in, and renewal metrics. These reports support routine circulation monitoring and analysis.

*Priority rationale:* The 78% survey result indicates broad stakeholder support, although it comes from only one source and has no formal decision.

*Stakeholders:* library staff

<details><summary>Evidence</summary>

- D20: "Circulation reports (checkouts, check-ins, renewals): 78%"

</details>

<a id="req-008"></a>
#### REQ-008 Configurable Report Levels

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml)

**Statement:** The system shall allow reports to be generated at configurable organizational levels such as consortium, home branch, county, and other supported groupings.

Staff users need to select the organizational scope of a report. Supported levels shall include consortium-wide, home branch, county, and additional levels as configured. The selected level shall determine the report scope.

*Priority rationale:* Multiple participants requested configurable reporting levels, and the requirement has three stakeholders plus an email agreement, making it important though not formally mandated.

*Stakeholders:* Maria Rodriguez, George Tuttle, Katherine Gregory

<details><summary>Evidence</summary>

- D09: "The list should be configurable to different levels - System, Home Library, County, etc."

</details>

<a id="req-009"></a>
#### REQ-009 Cross-Branch Comparison Reporting

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D03 (conversations/conv_pines016_shelf_space.eml), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide a comparison view and reports for comparing selected branches, including their genre and format breakdowns and other supported metrics.

Both requirements address cross-branch comparison reporting. The system shall enable comparison across multiple branches and provide a side-by-side view of selected branches' genre and format breakdowns.

*Priority rationale:* Comparison reporting is supported by four stakeholders across email and meeting sources and is expected to help identify outliers, but no formal decision makes it nonessential.

*Stakeholders:* LaToya Davidson, Directors, Branch managers, jennifer.durham@statesboro.lib.org

<details><summary>Evidence</summary>

- D18: "Need for cross-branch comparison reports"
- D03: "Also, can we include a "comparison" view that shows each library's breakdown side by side? That would make it easy to spot outliers."

</details>

<a id="req-010"></a>
#### REQ-010 Cross-Tabulated Transaction Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml)

**Statement:** The system shall allow transaction reports to be cross-tabulated by terminal, branch, consortium, hour, patron age range, patron type, and patron location.

Staff users need to analyze transaction statistics across operational and patron dimensions. Cross-tabulation shall support terminal, branch, consortium, hour, patron age range, patron type, and patron location. This allows transaction patterns to be compared across different contexts.

*Priority rationale:* The requirement is explicitly marked “should” and is supported by five stakeholders across the specification and an email.

*Stakeholders:* Staff, Library boards, directors, admins, report authors

<details><summary>Evidence</summary>

- D10: "It should be possible to cross-tabulate per terminal, per branch, per library system, per hour, per patron age range, per patron type, and per patron location."

</details>

<a id="req-011"></a>
#### REQ-011 Deletion Audit Query Interface

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall allow authorized staff users to query and view the deletion audit log, including searching by record identifier.

The deletion audit interface shall allow authorized staff users to query and view deletion records in the deletion audit log. It shall support using a record identifier as a query criterion. This capability shall enable authorized staff users to trace deleted records and investigate why a patron's record disappeared.

*Priority rationale:* Four stakeholders agreed in email that authorized staff need searchable deletion audit access, and the audit-trail use case makes this important even without a formal decision.

*Stakeholders:* Robert Chen, Katherine Gregory, Dana Peeler, George Tuttle

<details><summary>Evidence</summary>

- D07: "A report interface to query this audit table"
- D07: "If we accidentally delete something we shouldn't have, we need to be able to trace it. Also, the deletion log would help with troubleshooting. "Why did this patron's record disappear?" - check the log."

</details>

<a id="req-012"></a>
#### REQ-012 Demographic Filtering and Grouping

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D08 (conversations/conv_pines023_patron_characteristics.eml), D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall allow patron and circulation data in reports and queries to be filtered and grouped by supported patron demographic characteristics, including age range, zip code, county of residence, home branch, patron type, and preferred language, and shall provide aggregate metrics for those groupings.

Reports and queries shall support filtering patron and circulation data by age range, zip code, county of residence, home branch, patron type, and preferred language. They shall also support grouping the data by these characteristics. The system shall provide aggregate metrics based on the resulting demographic groups. This capability shall support analysis of circulation and patron counts by supported demographic characteristics.

*Priority rationale:* The requirement is described as “essential,” has seven stakeholders across two sources, and includes multiple email agreements, but lacks a meeting decision.

*Stakeholders:* Jennifer Durham, Susan Sexton-Cooley, Maria Rodriguez, Katherine Gregory, Latoya Davidson, Staff, Administrators

<details><summary>Evidence</summary>

- D08: "Can we also GROUP BY these fields? Like, show me circulation by age range, or patron count by home branch?"
- D08: "The system should allow queries and reports to be limited or grouped by various patron characteristics, including: - Age range - Zip code - County of residence - Home branch - Patron type - Preferred language"
- D08: "Both LIMIT (filter) and GROUP BY (aggregate) should be supported"

</details>

<a id="req-013"></a>
#### REQ-013 Historical Reporting

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml), D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide historical reporting for a specified past date or date range through a historical reporting warehouse or snapshot capability, while also supporting real-time reporting of current data.

Both requirements require reporting against preserved historical data for a prior point in time or period. The system shall provide a historical reporting warehouse or snapshot capability for specified past dates or date ranges and shall continue to support reporting on current data where applicable.

*Priority rationale:* Historical reporting has broad support across five source types and nine stakeholders, but its only recorded agreement is in an email rather than meeting minutes.

*Stakeholders:* library staff, Robert Chen, Katherine Gregory, Latoya Davidson, Technical Subcommittee, staff, data, PINES IT Department ...

<details><summary>Evidence</summary>

- D20: ""Historical reporting - I want to see what the data looked like on a specific date in the past, even if the shelving location has changed""
- D01: "We can also add date filters - volume at any point in time, not just current."
- D19: ""Some reports need to be real-time... Others are historical... We probably need a reporting warehouse for historical data.""

</details>

<a id="req-014"></a>
#### REQ-014 Material Item Count Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall provide a Material Item Count Report showing collection item counts and related counts for a selected branch or consortium scope and point in time.

The report shall show the total number of items in the collection and related counts for the selected branch or consortium scope at the selected point in time. It shall support breakdowns by acquisition, shelf status, circulation status, and category where applicable. Category examples include total items, holds, adult fiction, and board books. The report shall support understanding collection size based on new acquisitions, items on the shelf, and items in circulation.

*Priority rationale:* The Material Volume Report is supported by three source types, seven stakeholders, and email agreements calling it a key requirement needed for board and assessment reporting.

*Stakeholders:* Maria Rodriguez, Katherine Gregory, Pines reports working group, Susan Sexton-Cooley, Staff, Administrators, Thomas Wright

<details><summary>Evidence</summary>

- D01: "Here's what I'm hearing for the "Material Volume Report" requirement:"
- D01: "Like total items in library, number of holds, number of adult fiction, number of board books..."
- D10: "The report should allow breaking down volume in categories such as: total items in library, number of holds, number of adult fiction, number of board books, etc."

</details>

<a id="req-015"></a>
#### REQ-015 Missing Item Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide item reports identifying items whose status is Missing, including missing-item inventory reporting.

M021 broadly requires item reporting for inventory, weeding, and missing items, while M093 specifies the missing-item report by status. The merged requirement shall provide item reports that identify items with a Missing status as part of the system's inventory and item-reporting capabilities.

*Priority rationale:* The 65% survey result and specification support indicate that missing-item reports are broadly expected, although they lack a formal decision.

*Stakeholders:* library staff, Staff, staff

<details><summary>Evidence</summary>

- D20: "Item reports (inventory, weeding, missing): 65%"
- D10: "Examples of periodic reports include: - Missing items"
- D10: "List of Items with a status of Missing"

</details>

<a id="req-016"></a>
#### REQ-016 Multi-Level Data Aggregation

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml), D03 (conversations/conv_pines016_shelf_space.eml)

**Statement:** The system shall support aggregation and grouping of underlying data across required combinations of branch, consortium, genre, and format levels.

The system shall aggregate centralized data across branches to produce consortium-wide overviews. The system shall support report calculations and grouping at the branch and consortium levels. The system shall also support aggregation and grouping at the genre and format levels, including required combinations of these organizational and collection levels.

*Priority rationale:* Aggregation across branch, consortium, genre, and format is supported by two email sources and an agreement describing it as feasible and implied by system-wide reporting.

*Stakeholders:* robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "The data is centralized in our database, so we can build queries that aggregate across all branches."
- D03: "We can also add the per-library and per-system breakdown. That's just adding GROUP BY clauses to the right levels."

</details>

<a id="req-017"></a>
#### REQ-017 Report Queue Visibility

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide a report queue interface showing the position and status of each staff user's report run.

Staff users shall be able to view the position of their report runs in the queue, including how many reports are ahead of theirs. The interface shall show when each report run was submitted, its ownership, and its status. The interface shall show the estimated completion of report runs when available.

*Priority rationale:* Report queue visibility has support from five source types, 11 stakeholders, and a 68% survey result, but is explicitly marked “should” rather than mandatory.

*Stakeholders:* Staff, PINES IT Department, staff users, staff, IT/help desk, IT, library staff, admins ...

<details><summary>Evidence</summary>

- D10: "Staff should be able to see where their report is in the queue of reports waiting to run."
- D14: "The management processes reporting system needs to: 3. Add report queue visibility and status indicators"
- D12: "They need to see: How many reports are ahead of theirs"

</details>

<a id="req-018"></a>
#### REQ-018 Shelf Space Reporting and Estimation

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D03 (conversations/conv_pines016_shelf_space.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide and automate a Shelf Space Report for a selected branch or the consortium, estimating shelf space from item dimensions when available and using an item-count proxy or another supported method when dimensions are unavailable.

The requirements describe the same Shelf Space Report capability. The report shall show collection, circulation, and estimated shelf-space metrics by genre and format for a selected branch or the consortium; shelf space is not maintained as a directly tracked database value, so the system shall estimate it from item dimensions when available and otherwise use an item-count proxy or another supported estimation method. Generation shall be automated so staff users do not need to collect the data manually or build spreadsheets.

*Priority rationale:* Shelf-space reporting has four source types, ten stakeholders, and several email agreements, while its explicit “should” signal and pending estimation method make it important but not essential.

*Stakeholders:* robert.chen@gapubliclib.org, maria.rodriguez@dalton-whitman.lib.org, susansexton-cooley@saraboblib.org, katherine.gregory@gapubliclib.org, thomas.wright@augusta-reed.lib.org, Staff, Administrators, Thomas Wright ...

<details><summary>Evidence</summary>

- D03: "Count items per genre/format (this is the "percentage of collection")"
- D03: "for each genre and format of material, compare: 1. Percentage of total circulations 2. Percentage of the collection 3. Percentage of total shelf space"
- D03: "Sum checkouts per genre/format (this is the "percentage of circulations")"

</details>

<a id="req-019"></a>
#### REQ-019 Staff Productivity Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide reports and analysis tools for staff productivity and workflow, including time spent per transaction.

Managers and staff users need to analyze staff productivity, workflow, and supervision-related measures. Reports shall support productivity metrics such as time spent per transaction. The results shall help evaluate staffing and operational workflows.

*Priority rationale:* Staff productivity reporting was included in the scope accepted in meeting minutes and is also supported by a survey, but no critical or mandatory signal is present.

*Stakeholders:* Staff, Library Managers, Local System Administrators, library staff, administrators

<details><summary>Evidence</summary>

- D17: "Analyzing staff productivity and workflow"
- D20: "Staff productivity reports (time spent per transaction)"

</details>

<a id="req-020"></a>
#### REQ-020 Transaction Activity Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml)

**Statement:** The system shall provide transaction reports showing traffic and use of items, including checkouts, check-ins, holds placed, and holds filled.

Staff users need transaction reports to understand traffic and overall service usage. Reports shall present counts and trends for checkouts, check-ins, holds placed, and holds filled. These metrics support operational monitoring and analysis of service demand.

*Priority rationale:* The requirement is marked “should” and supported by five stakeholders across an email and the specification, making it important but not formally mandatory.

*Stakeholders:* directors, library boards, staff, Staff, Library boards

<details><summary>Evidence</summary>

- D12: "Activity reports showing traffic and volume of use - checkouts, check-ins, holds placed, holds filled."
- D10: "Activity reports should indicate traffic and volume of use, displaying statistics on check-outs, check-ins, holds placed, and holds filled."

</details>

<a id="req-021"></a>
#### REQ-021 Uncataloged Material Usage Reporting

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall identify usage of uncataloged material and include its transactions in circulation statistics and reports.

Both requirements cover reporting on the use of uncataloged material. The system shall identify uncataloged-material usage and include the associated transactions in circulation statistics and reports, including applicable circulation reporting outputs.

*Priority rationale:* Uncataloged-material usage reporting is supported by an interview and the specification and is needed to include those transactions in circulation statistics, though no formal decision is recorded.

*Stakeholders:* Thomas Wright, Staff, Administrators

<details><summary>Evidence</summary>

- D15: "ability to identify how the material is being used."
- D15: "We also need to count transactions and include them in circulation statistics and reports."
- D10: "Support needed for: - Ability to identify how the material is being used"

</details>

<a id="req-022"></a>
#### REQ-022 Branch Capacity Trends

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall present trend data showing whether each branch's capacity is growing or shrinking over time.

Staff users and managers need capacity trends for long-term planning. Trend information shall be available for branches in both overview and branch-detail views. The trends shall indicate whether a branch is growing or shrinking over time.

*Priority rationale:* The request has only one email source and two stakeholders, with email agreement representing stakeholder support rather than a formal decision.

*Stakeholders:* jennifer.durham@statesboro.lib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "One more thing - can the capacity interface also show trends? Like, is this branch growing or shrinking?"

</details>

<a id="req-023"></a>
#### REQ-023 Configurable Capacity Metrics

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall allow staff users with appropriate permissions to configure the metrics used to define capacity.

The meaning of capacity must be adaptable to local reporting needs. Configurable options shall include measures such as number of items versus shelf space, physical items versus a configured limit, and circulation volume versus processing capacity. The selected metrics shall determine how capacity is evaluated and reported.

*Priority rationale:* This is a single-stakeholder configuration question from one email with no confirmed decision or explicit priority signal.

*Stakeholders:* robert.chen@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "Also, what specific metrics define "capacity"? Is it: - Number of items vs. shelf space? - Number of physical items vs. a configured limit? - Circulation volume vs. processing capacity?"

</details>

<a id="req-024"></a>
#### REQ-024 Deletion Location Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall provide reports showing deletions by branch.

Staff users need to compare deletion activity among branches. Reports shall show deletion counts or results by branch. This helps identify branches with unusually high deletion activity.

*Priority rationale:* Branch-level deletion reporting has one email source and three stakeholders, with email agreement but no formal decision or stronger priority signal.

*Stakeholders:* Susan Sexton-Cooley, Maria Rodriguez, Katherine Gregory

<details><summary>Evidence</summary>

- D07: "Deletions by location"

</details>

<a id="req-025"></a>
#### REQ-025 Deletion Period Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall provide reports showing total deletions by reporting period.

Staff users need to monitor the volume of deletions over time. Reports shall show totals for periods such as month, quarter, and year. These totals support operational review and auditing.

*Priority rationale:* Period-based deletion totals were agreed by two stakeholders in email only, so they are useful but not essential for initial acceptance.

*Stakeholders:* Susan Sexton-Cooley, Katherine Gregory

<details><summary>Evidence</summary>

- D07: "From an administrative perspective, we need reports showing: - Total deletions per period (month, quarter, year)"

</details>

<a id="req-026"></a>
#### REQ-026 Deletion Transaction Aggregation

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall allow deletion reports to aggregate deletion transactions by date range, staff user, and record type.

Authorized staff users need to analyze deletion transactions for auditing and operational review. Reports shall support selectable date ranges and grouping or filtering by the staff user who performed the deletion and by record type. Record types may include items, patrons, and bibliographic records.

*Priority rationale:* Deletion aggregation has only one email source and two stakeholders, and its agreement is email-based rather than a formal meeting decision.

*Stakeholders:* Robert Chen, Katherine Gregory

<details><summary>Evidence</summary>

- D07: "We can aggregate by date range, by user, by record type."

</details>

<a id="req-027"></a>
#### REQ-027 Deletion Type Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall provide reports showing deletions broken down by record type.

Staff users need to distinguish deletions of items, patrons, bibliographic records, and other record types. Reports shall support filtering and counting by record type. This helps identify differences in deletion activity across data categories.

*Priority rationale:* Deletion breakdown by record type has limited support from two stakeholders in one email and no formal decision.

*Stakeholders:* Susan Sexton-Cooley, Katherine Gregory

<details><summary>Evidence</summary>

- D07: "From an administrative perspective, we need reports showing: - Deletions by type (item vs patron vs other)"

</details>

<a id="req-028"></a>
#### REQ-028 Expanded Report Types

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall expand the available report types to cover identified reporting gaps in Evergreen 1.4.0.4.

Staff users need reporting coverage beyond the currently available report types. The expansion shall address the identified gaps in Evergreen 1.4.0.4, including the specific report categories identified in the source material. This is a high-level coverage requirement rather than a definition of one individual report.

*Priority rationale:* Expanded report types are identified as a gap in a single reference document with no survey, interview, or meeting confirmation.

*Stakeholders:* PINES IT Department, library staff

<details><summary>Evidence</summary>

- D14: "The management processes reporting system needs to: 1. Expand the available report types to cover all identified gaps"

</details>

<a id="req-029"></a>
#### REQ-029 Holdings Time-Series Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml)

**Statement:** The system shall provide reports showing changes in a branch's holdings item count over time.

Staff users and managers need to track whether holdings are growing or declining. Reports shall present time-series data for holdings item counts in charts or tables. They shall support recent-period measures such as items added during the last 30, 60, or 90 days.

*Priority rationale:* Holdings time-series reporting has one email source and three stakeholders, with email support describing it as helpful rather than mandatory.

*Stakeholders:* Robert Chen, Latoya Davidson, Katherine Gregory

<details><summary>Evidence</summary>

- D01: "We can definitely build reports that show volume changes over time."

</details>

<a id="req-030"></a>
#### REQ-030 Inactive Patron Branch Counts

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml)

**Statement:** The system shall provide consortium-level reports of inactive patron counts by branch, with sorting or reporting to identify branches with the most inactive patrons.

Staff users need to identify branches with high numbers of inactive patrons. The system shall aggregate inactive patron counts by branch at the consortium level. Results shall support sorting or reporting so branches can be prioritized for cleanup.

*Priority rationale:* Inactive-patron branch counts are requested by only two stakeholders in one email and have no formal decision or broad corroboration.

*Stakeholders:* George Tuttle, Katherine Gregory

<details><summary>Evidence</summary>

- D09: "At the system level, I can see which branches have the most inactive patrons."

</details>

<a id="req-031"></a>
#### REQ-031 Top Deleting Users Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall provide reports identifying the staff users who delete the most records.

Authorized staff users need to identify unusually high deletion activity by individual staff users. Reports shall rank staff users by deletion count over selectable reporting periods. This supports process review and investigation of potential issues.

*Priority rationale:* The top-deleting-users report has only one email source, two stakeholders, and an email agreement, making it a useful enhancement rather than a release necessity.

*Stakeholders:* Susan Sexton-Cooley, Katherine Gregory

<details><summary>Evidence</summary>

- D07: "From an administrative perspective, we need reports showing: - Top users who delete the most records"

</details>

### 6.2 Query and data selection

*15 requirements - Must: 2, Should: 9, Could: 4, Won't: 0*

<a id="req-032"></a>
#### REQ-032 Expose Reporting Fields

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall expose relevant bibliographic record, item, patron, and other database fields for report selection, filtering, grouping, and output.

Reporting users need access to a broader selection of database fields than is currently available in the report writer. Exposed bibliographic record fields shall include examples such as identifiers, fingerprint, scan timestamp, edition, ISBN, ISSN, publisher, publication date, place of publication, and physical description. Exposed item fields shall include examples such as barcode, status, call number, purchase data, shelving location, and reserve identifier, while patron fields shall include examples such as barcode, branch association, patron group, contact details, address, birth date, and creation date. The available fields shall support filtering as well as report output and grouping.

*Priority rationale:* Broad field exposure is foundational to selecting, filtering, grouping, and reporting data, and the two-source evidence identifies limited field availability as a current system deficiency.

*Stakeholders:* PINES IT Department, cataloging staff, circulation and collection staff, cataloging and reporting staff, patron services, library staff

<details><summary>Evidence</summary>

- D14: "For bibliographic_record: - id, fingerprint, scan_timestamp, record_type, edition, language, ISBN, ISSN, UPC, EAN, publisher_name, publication_date, place_of_publication, physical_description"
- D14: "For item: - id, barcode, label, copy_number, location (copy_location), status (acq status), circ_modifier, call_number, purchase_date, purchase_price, shelving_location, age_hold_protect, reserve_id"
- D14: "Limited field selection (not all database fields are available)"

</details>

<a id="req-033"></a>
#### REQ-033 Query Data Access Control

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall allow authorized staff roles or administrators to control which tables and fields each staff user may access through the query tool.

Authorization settings shall govern staff user access to queryable tables and fields through the query tool. Authorized staff roles or administrators shall control which tables and fields each staff user may access. These settings shall limit staff users to selecting, filtering, grouping, and reporting only on permitted data.

*Priority rationale:* Controlling staff access to query tables and fields is a security and privacy control, and such access restrictions are a hard governance requirement even though the available source labels it only “should.”

*Stakeholders:* Administrators, Local System Administrators

<details><summary>Evidence</summary>

- D10: "Administrators should control staff access to tables and fields."
- D10: "Administrators should control staff access to tables and fields."

</details>

<a id="req-034"></a>
#### REQ-034 Advanced Query Builder

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D08 (conversations/conv_pines023_patron_characteristics.eml), D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a user-friendly query builder that supports selecting fields and values, Boolean logic, regular expressions, joins, and combined conditions across bibliographic, item, patron, transaction, financial, and related records.

Staff users need to design queries against all relevant record types, including bibliographic records, items, patrons, transactions, and financial data. The query builder shall support field selection, picklists, selectable regular expressions, and a full range of Boolean operators such as AND, OR, and NOT. It shall support combined demographic and activity conditions and joins across key relationships, including bibliographic record to item, item to circulation transaction, patron to circulation transaction, patron to money, and actor to circulation transaction. These capabilities are needed for cross-entity reporting and complex selection tasks.

*Priority rationale:* This is supported by four sources, 12 stakeholders, and two email agreements, but the evidence labels it “should” and does not record a formal meeting decision.

*Stakeholders:* Latoya Davidson, Susan Sexton-Cooley, Robert Chen, Staff, Administrators, PINES IT Department, technical report authors, directors ...

<details><summary>Evidence</summary>

- D08: "Can we combine demographic filters? Like "show me all Juvenile patrons in zip code 30505 who haven't checked anything out in 6 months"?"
- D08: "We can support both AND and OR logic."
- D10: "Staff should be able to: - Use a full range of Boolean operators"

</details>

<a id="req-035"></a>
#### REQ-035 Filter Branches

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall allow users to filter branches by region, branch type, current load, and system or regional group.

Staff users need to limit branch-based views to relevant subsets when many branches are present. Filtering shall support region, branch type, and current load. Users shall also be able to select or group branches by system or regional group to keep overviews manageable.

*Priority rationale:* Branch filtering is supported by three stakeholders and an email agreement, but the agreement is not recorded in meeting minutes and the requirement has only one source.

*Stakeholders:* jennifer.durham@statesboro.lib.org, robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "Maybe we should group by system/region? Or allow filtering?"

</details>

<a id="req-036"></a>
#### REQ-036 Filter by Branch Location

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml)

**Statement:** The system shall allow report queries to filter counts by branch location.

Users need to restrict report counts to a selected branch location, such as their own branch. The filter shall limit the counted items to those associated with the specified branch location. This supports branch-specific reporting and analysis.

*Priority rationale:* Filtering by branch location is a core reporting use case supported by three stakeholders and an email agreement, although no formal meeting decision is recorded.

*Stakeholders:* Robert Chen, Maria Rodriguez, Pines reports working group

<details><summary>Evidence</summary>

- D01: "Counts all items with a location = your library"

</details>

<a id="req-037"></a>
#### REQ-037 Flexible Reporting Periods

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D03 (conversations/conv_pines016_shelf_space.eml)

**Statement:** The system shall allow users to select arbitrary date ranges and predefined quarterly periods for reporting.

Users need to choose start and end dates for report data, including circulation data used in Shelf Space Report metrics. The system shall provide preset calendar-quarter options for recurring reviews while retaining arbitrary date selection for seasonal analysis and quarter-by-quarter comparisons. Directors need both predefined and custom period views for regular reporting.

*Priority rationale:* Arbitrary and quarterly periods address recurring seasonal and management-review needs, but the evidence comes from only one email and two stakeholders.

*Stakeholders:* latoya.davidson@twinlakeslib.org, jennifer.durham@statesboro.lib.org

<details><summary>Evidence</summary>

- D03: "Can we also filter by date range? Like, what was the shelf space utilization in Q1 vs. Q2? Seasons matter for our collection."
- D03: "Our directors review this data quarterly and need both views."

</details>

<a id="req-038"></a>
#### REQ-038 Manual Selection of Transfer Items

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow staff users to manually select individual records, titles, or items from query results for inclusion in a transfer batch or other subsequent action.

Both requirements cover manual selection from query results, with M189 specifying the transfer-batch use case. The merged capability shall let staff users select specific titles or items from query results and use those selections for transfer batches or other authorized follow-up actions.

*Priority rationale:* Manual selection is supported across four source types and by 39% survey support, making it important, but there is no formal decision or majority-level evidence.

*Stakeholders:* jennifer.durham@statesboro.lib.org, maria.rodriguez@dalton-whitman.lib.org, thomas.wright@augusta-reed.lib.org, administrators, Staff, Thomas Wright

<details><summary>Evidence</summary>

- D04: "I also want to be able to MANUALLY SELECT from query results. Maybe I run a query and get 100 candidate items, but I only want to move 25 of them. I should be able to check boxes and select which ones to include."
- D20: "Manually select from query results: 39%"
- D10: "The utility should include: - Ability to manually select titles from query results"

</details>

<a id="req-039"></a>
#### REQ-039 Query Candidate Materials

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml), D20 (survey_results_2009.txt)

**Statement:** The system shall provide queries that identify candidate materials for administrative actions such as weeding or transfer.

Staff users need to identify materials that may require collection-management action. The query capability shall support candidate selection for activities such as weeding and batch transfer. It may build on the general query tool while serving these administrative use cases.

*Priority rationale:* Candidate-material queries are supported by two sources and six stakeholders, with 44% survey support indicating substantial demand without establishing a mandatory decision.

*Stakeholders:* maria.rodriguez@dalton-whitman.lib.org, robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org, thomas.wright@augusta-reed.lib.org, administrators, library staff

<details><summary>Evidence</summary>

- D04: "Query builder for candidate selection - we can reuse the report query tool for this."
- D20: "Query for candidate materials: 44%"

</details>

<a id="req-040"></a>
#### REQ-040 Report Selection Criteria Disclosure

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall clearly define and display the report or query selections and criteria used to generate results within on-screen and exported report results.

These requirements all require transparency about the selections and criteria underlying report results. The system shall display the report name where applicable, the query or report parameters, and the selection criteria alongside or within on-screen and exported results, using clear definitions of the criteria applied.

*Priority rationale:* Selection-criteria disclosure is supported by three source types, eight stakeholders, and repeated evidence that criteria are currently not displayed, but no formal decision makes it mandatory.

*Stakeholders:* Staff, staff, admins, report authors, PINES IT Department, staff users, auditors, individual

<details><summary>Evidence</summary>

- D10: "The system should provide the query selections along with the results, so users can see what criteria were used to generate the report."
- D12: "System provides query selections along with results."
- D10: "Report results would include the date selection criteria at the top or bottom to quickly see date range selected along with the name of the report"

</details>

<a id="req-041"></a>
#### REQ-041 Save Transfer and Other Queries

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow staff users to save queries for repeated use, including queries used to select transfer candidates.

Staff users shall be able to save queries and reuse them for subsequent reporting activities. Saved queries shall also be reusable for selecting transfer candidates, including recurring monthly selection activities. Saved queries may be shared or published for use by other staff users where permitted.

*Priority rationale:* Saving queries has broad support across four source types, 73% and 58% survey signals, and is described as “crucial” for monthly work, but no meeting-minute decision is recorded.

*Stakeholders:* library staff, administrators, thomas.wright@augusta-reed.lib.org, maria.rodriguez@dalton-whitman.lib.org, robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org, Thomas Wright, Staff

<details><summary>Evidence</summary>

- D20: "Ability to save and reuse queries: 73%"
- D04: "The "save queries for repeated use" is crucial. We do this monthly - move all items in genre X that haven't circulated in 6 months."
- D04: "Save/share queries - similar to report templates."

</details>

<a id="req-042"></a>
#### REQ-042 Sort Branch Lists

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall allow users to sort branch capacity lists by region, branch type, and current load.

Staff users need to order branch overviews to support operational decision-making. Sorting shall include region, branch type, and current load. This capability is separate from filtering and allows users to organize the full or filtered list.

*Priority rationale:* Sorting branch lists is supported by an email agreement and recurring operational criteria, but it has only one source and an email agreement rather than a formal decision.

*Stakeholders:* jennifer.durham@statesboro.lib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "I'd want to be able to sort and filter. By region, by library type, by current load..."

</details>

<a id="req-043"></a>
#### REQ-043 Consolidated MARC Fields in Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow selected MARC fields to be presented together on a single report output row for the associated bibliographic record or item.

Staff users shall be able to select specific MARC fields for reporting. The system shall present the selected MARC field values together on a single report output row rather than across multiple rows. The row shall correspond to the relevant bibliographic record or item.

*Priority rationale:* The capability appears in only two sources, with support from three stakeholders and no agreement or stronger priority signal beyond a single survey request.

*Stakeholders:* library staff, cataloger, staff

<details><summary>Evidence</summary>

- D20: ""Need to pull specific MARC fields but they're spread across multiple rows""
- D10: "Ability to pull MARC record fields so that they appear on a single row of data"

</details>

<a id="req-044"></a>
#### REQ-044 Exclude Specified Patrons

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml)

**Statement:** The system shall allow users to exclude specified patrons from the inactive report based on patron flags or patron types.

Staff users need to omit patrons who should not appear in inactive-patron outreach or analysis. Exclusion criteria shall support do-not-disturb flags, VIP patrons, staff members, and patrons who have opted out of communications. The capability shall be available as filters or exclusion rules for the inactive report.

*Priority rationale:* This is a useful exclusion feature supported by one email and two stakeholders, with only an email-based agreement rather than a formal decision.

*Stakeholders:* Latoya Davidson, Katherine Gregory

<details><summary>Evidence</summary>

- D09: "One more thing - we should be able to EXCLUDE certain patrons from the inactive report. For example: - Patrons with "do not disturb" flags - VIP patrons - Staff members - Patrons who have opted out of communications"

</details>

<a id="req-045"></a>
#### REQ-045 Filter by Survey Name

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall allow users to select a survey by name and resolve that name to its survey identifier when executing a query.

Staff users need to filter reports using a human-readable survey name rather than entering a survey identifier. The system shall provide survey names as selectable criteria. It shall resolve the selected name to the corresponding survey identifier internally before executing the query.

*Priority rationale:* Selecting surveys by name is supported by only two stakeholders across a meeting and the draft specification, with no formal decision or broader priority evidence.

*Stakeholders:* Technical Subcommittee, staff

<details><summary>Evidence</summary>

- D19: "The ability to filter by survey name rather than survey ID requires the system to resolve names to IDs internally."
- D10: "Ability to select the survey name and not have to enter the survey id for filtering"

</details>

<a id="req-046"></a>
#### REQ-046 Upload Filter Lists

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall allow users to upload text files containing identifiers such as barcodes or TCNs for use as report filter criteria.

Staff users need to filter reports using large lists of identifiers without entering each value manually. The system shall accept uploaded text lists and use them as filter criteria or large inclusion lists. Uploaded identifiers shall be usable to limit report results to the corresponding items or patrons.

*Priority rationale:* Uploading identifier lists is supported only by the reference and draft specification and three stakeholders, with no decision or stronger priority signal.

*Stakeholders:* PINES IT Department, staff users, staff

<details><summary>Evidence</summary>

- D14: "No ability to upload text files for filtering (barcodes, TCNs)"
- D14: "No ability to upload text files for filtering (barcodes, TCNs)"
- D10: "Ability to upload a text file such as barcodes or TCN to use for filtering on a report"

</details>

### 6.3 Report authoring and presentation

*29 requirements - Must: 4, Should: 13, Could: 12, Won't: 0*

<a id="req-047"></a>
#### REQ-047 Consortium Template Support

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall support the creation, storage, distribution, migration, and use of report templates across the consortium.

Templates shall be made available to participating branches to standardize reporting outputs and formats. The capability shall support templates needed for all PINES branches and their distribution for use. Templates shall also be suitable for migration between supported environments.

*Priority rationale:* Two meeting-minute agreements accepted consortium template support as part of the adopted mission and deliverables.

*Stakeholders:* Reports Working Group, Katherine Gregory, All PINES libraries, PINES Libraries, Local System Administrators, Global System Administrator

<details><summary>Evidence</summary>

- D18: "Determine and create templates needed for all PINES libraries."
- D17: "Determine and create templates needed for all PINES libraries."

</details>

<a id="req-048"></a>
#### REQ-048 Report Output Formats

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide report output in configurable formats including CSV, HTML, Excel or pivot-capable output, and PDF.

Staff users shall be able to produce reports in configurable output formats for report delivery and analysis. The supported formats shall include CSV, HTML, Excel, pivot-capable output, and PDF. The system shall allow the selected output format to be applied when generating a report.

*Priority rationale:* Multiple output formats have support from four source types, eight stakeholders, a 61% survey result, a “required” signal, and a formal meeting agreement.

*Stakeholders:* PINES IT Department, staff users, staff, management, business analysts, library staff, individual, Robert Chen

<details><summary>Evidence</summary>

- D14: "Provide multiple output formats and scheduling options"
- D10: "Pivot table output"
- D14: "No pivot table output"

</details>

<a id="req-049"></a>
#### REQ-049 Staff Report Authoring

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D17 (meeting_minutes/meeting_2009-03-15_minutes.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow authorized staff users to create, run, author, and manage custom reports and report templates by selecting permitted data, criteria, and display options.

Both requirements specify staff creation and management of reporting content. Authorized staff users shall be able to create and author custom or on-demand reports, select permitted data and criteria, run the reports, and manage report content and associated report templates within their permissions.

*Priority rationale:* A meeting-minute agreement identifies staff as the primary report content creators, and the requirement is supported by meeting, specification, and survey evidence.

*Stakeholders:* System administrators, Staff, staff, library staff

<details><summary>Evidence</summary>

- D10: "...and/or to run ad hoc reports on specific sets of data."
- D10: "Noncanned or On Demand Reports - preset but have the ability to edit selection criteria and display options"
- D20: "Custom/on-demand reports: 29%"

</details>

<a id="req-050"></a>
#### REQ-050 Template Query Migration

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall provide export and import of report templates, permission settings, and saved queries between environments.

Staff users shall be able to migrate report definitions and related authorization settings between development, training, and production environments. The migration capability shall include report templates, permission settings, and saved queries. Exported definitions shall be importable into another supported environment.

*Priority rationale:* Export and import of templates and queries received an explicit agreement in meeting minutes, which is strong evidence of a mandatory consortium decision.

*Stakeholders:* Robert Chen

<details><summary>Evidence</summary>

- D19: ""Export/import of templates, permission settings, and saved queries.""

</details>

<a id="req-051"></a>
#### REQ-051 Administrator Template Creation

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D20 (survey_results_2009.txt)

**Statement:** The system shall allow authorized administrators to create report templates that staff users can run or modify within permitted limits.

Administrators need to create centrally managed report templates for consistent reporting. Templates shall be usable as-is and may be modified when the template permits it. Created templates shall be made available to staff users.

*Priority rationale:* Supported by 81% of the survey and seven stakeholders across three sources, making administrator-created templates important, but no formal meeting decision makes it a Must.

*Stakeholders:* administrators, library staff, System administrators, Staff, admins, directors, staff

<details><summary>Evidence</summary>

- D20: "Ability to create report templates: 81%"
- D10: "System administrators should be able to create report templates that are available to staff."
- D12: "Admins need to create report templates that are available to staff."

</details>

<a id="req-052"></a>
#### REQ-052 Branch Capacity Overview

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml), D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a high-level capacity overview for all branches, including branch capacity summaries and visual cues that allow staff users to identify available capacity at a glance.

Both requirements describe a high-level interface for reviewing capacity across branches. The merged capability shall show capacity metrics and summaries for all branches and provide visual cues that help staff users recognize available or constrained capacity quickly.

*Priority rationale:* Seven stakeholders and an email agreement support the need for an all-branch capacity overview, although the agreement is not recorded in meeting minutes.

*Stakeholders:* george.tuttle@piedmontlib.org, chris.sharp@gapubliclib.org, Administrators, Staff, maria.rodriguez@dalton-whitman.lib.org, katherine.gregory@gapubliclib.org, pines-reports-working-group@gapl.org

<details><summary>Evidence</summary>

- D02: "It would have been so much easier if I could have seen at a glance which branches had capacity."
- D10: "The system should provide an interface showing the capacity of all branches."
- D02: "As a branch manager, I need to see the capacity of all branches in our system, not just my own."

</details>

<a id="req-053"></a>
#### REQ-053 Consolidated Report Output

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml), D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a single consolidated report that combines selected counts, breakdowns, and related report results.

Staff users need one report instead of manually collecting information from multiple screens. The consolidated output shall support counts, category breakdowns, holds, and time filters where applicable. Users shall also be able to select multiple canned reports or report templates and view their results in one document.

*Priority rationale:* A group agreement in an email and a documented manual workaround across two sources support consolidation as an important usability improvement, but not a formal Must decision.

*Stakeholders:* Maria Rodriguez, Katherine Gregory, individual, staff

<details><summary>Evidence</summary>

- D01: "I'm currently pulling it manually from three different screens. :("
- D10: "Canned reports can be checked off from a list to run at the same time and will be viewed within one document."

</details>

<a id="req-054"></a>
#### REQ-054 Customizable Report Categories

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml)

**Statement:** The system shall allow authorized users to define and select categories for grouping report data.

Report results shall support category breakdowns such as fiction or non-fiction, format, age group, adult fiction, and board books. Administrators or other authorized users shall be able to add or select categories relevant to reporting needs. This allows different branches to use breakdowns appropriate to their collections.

*Priority rationale:* Customizable categories have email agreements from multiple stakeholders and support across five stakeholders, although no meeting-minute decision is recorded.

*Stakeholders:* Latoya Davidson, Katherine Gregory, Pines reports working group, Robert Chen, Susan Sexton-Cooley

<details><summary>Evidence</summary>

- D01: "Can we make the categories customizable? Different libraries might want different breakdowns."
- D01: "Groups by categories (fiction/non-fiction, format, etc.)"

</details>

<a id="req-055"></a>
#### REQ-055 Email Report Delivery

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall support delivery of generated reports by email to staff-specified recipients as attachments or links.

The system shall allow staff users to enter and select email addresses for report recipients. It shall deliver generated reports by email either as attached report files or as links to the reports. This enables staff-selected recipients to receive reports by email rather than relying solely on downloading them from the web interface.

*Priority rationale:* Email delivery is supported by three source types, five stakeholders, and a 45% survey result, making it important but not essential without a formal decision.

*Stakeholders:* PINES IT Department, staff users, library staff, individual, staff

<details><summary>Evidence</summary>

- D14: "No email delivery (reports can only be downloaded from the web interface)"
- D20: "Email delivery of reports: 45%"
- D10: "Ability to enter email addresses for report to be sent to"

</details>

<a id="req-056"></a>
#### REQ-056 Inactive Patron Fine Flags

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml)

**Statement:** The system shall identify inactive patrons with outstanding fines in report results so they can receive separate handling.

Reports shall distinguish inactive patrons who still owe fines from other inactive patrons. Staff users can use this distinction to exclude or handle these patrons differently during outreach. The capability shall identify the relevant patron records and their outstanding fines.

*Priority rationale:* The group agreed by email that inactive patrons with fines need separate handling, and three stakeholders support it, but the agreement is not a formal meeting decision.

*Stakeholders:* Dana Peeler, Susan Sexton-Cooley, Katherine Gregory

<details><summary>Evidence</summary>

- D09: "Also, should we flag patrons who are inactive but still owe fines? We should probably handle those differently."

</details>

<a id="req-057"></a>
#### REQ-057 Inactive Patron Mailing Addresses

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml)

**Statement:** The system shall include current mailing addresses for patrons in the inactive patron report.

Staff users need to use the report for postal outreach such as mailing postcards. The report shall include the complete current mailing address fields needed for that outreach. Address data shall be associated with the relevant inactive patron record.

*Priority rationale:* Mailing addresses are backed by an email agreement and an operational outreach need, making them important despite support from only two stakeholders in one source.

*Stakeholders:* Dana Peeler, Katherine Gregory

<details><summary>Evidence</summary>

- D09: "We mail postcards to inactive patrons, so the report needs to include current mailing addresses."

</details>

<a id="req-058"></a>
#### REQ-058 Open Template Reporting

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide an open-template reporting interface for creating flexible, branch-defined report templates and queries.

The interface shall expose permitted attributes associated with transactions, patrons, items, bills, and bibliographic records for selection, filtering, and display. It shall support advanced relationships, user-defined fields, and custom output formatting where available. Staff users shall be able to create flexible report definitions beyond canned templates.

*Priority rationale:* Open-template reporting is identified as a missing capability across two sources and four stakeholders, making it an important authoring function without a formal Must decision.

*Stakeholders:* staff, PINES IT Department, technical staff, cataloging staff

<details><summary>Evidence</summary>

- D10: "Open template would have all attributes associated with say circulation, patrons, items, bills, and bibs to select from for filtering and the same attributes for displaying."
- D14: "Open Template Reporting - does not exist"

</details>

<a id="req-059"></a>
#### REQ-059 Report Template Edit Restrictions

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml)

**Statement:** The system shall allow authorized administrators to restrict which report-template filters and display fields staff users may modify.

Authorized administrators shall be able to lock specified template filters and display fields. Staff users shall be able to modify only the filters and display fields permitted by those restrictions. For example, staff users may set a call number range for a weeding report or add or remove display fields from a pick list without changing whether deleted items are included. These restrictions shall help administrators certify dependable report output.

*Priority rationale:* Five stakeholders across two sources support administrator restrictions on template edits, making this important for controlled authoring even without a formal decision.

*Stakeholders:* admins, front-line staff, directors, System administrators, Local System Administrators

<details><summary>Evidence</summary>

- D12: "Admins should be able to limit which filters and display fields can be altered. Example: Front-line staff can set a call number range for a weeding report or add/remove display fields from a pick list, but can't alter the template to display deleted items."
- D10: "Administrators should be able to limit which filters and display fields can be altered, to certify a dependable output."

</details>

<a id="req-060"></a>
#### REQ-060 Reporting Interface Types

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide canned reports, on-demand reports, and open-template reporting interfaces.

Canned reports shall provide predefined recurring reports. On-demand reports shall provide preset reports with editable run parameters and display options. Open-template reporting shall provide fully flexible attribute selection and report-definition capabilities.

*Priority rationale:* The three reporting interfaces are described across two sources and four stakeholders, indicating an expected core capability although no meeting decision is recorded.

*Stakeholders:* individual, staff, PINES IT Department, King County specification

<details><summary>Evidence</summary>

- D10: "15.1 Three Interfaces Three interfaces are needed: a) Canned reports ... b) Noncanned or On Demand Reports ... c) Open Template Reporting"
- D14: "Three interfaces (canned, on-demand, open template) - only basic canned exists"

</details>

<a id="req-061"></a>
#### REQ-061 Separate Edit and Circulation Dates

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall provide separate last-edit and last-circulation dates, with the edit date excluding circulation transactions.

Report results shall distinguish the last bibliographic or item edit date from the last circulation date. Staff users need the edit date to reflect only edits to the bibliographic record or item and not circulation transactions. The system shall present the last circulation date as a separate field rather than combining it with the edit date.

*Priority rationale:* Separate bibliographic and circulation dates are supported by an interview and reference source and address a specific reporting accuracy gap, though no formal decision is recorded.

*Stakeholders:* Thomas Wright, PINES IT Department, cataloging staff

<details><summary>Evidence</summary>

- D15: "I need to be able to see the last edit date on reports, but it should be only when the item is edited and not include the last circulation. The current system combines these dates."

</details>

<a id="req-062"></a>
#### REQ-062 Template Management

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide report template management for saving, organizing, reusing, editing, sharing, versioning, and deleting report definitions subject to permissions.

Staff users need a central way to manage reusable report templates and their definitions. Management shall support organizing templates, maintaining versions, and controlling permitted sharing and editing. Authorized users shall also be able to delete templates where allowed.

*Priority rationale:* Template management addresses a stated system gap and is supported by two stakeholders in a reference source, making it important but not formally mandatory.

*Stakeholders:* PINES IT Department, staff users

<details><summary>Evidence</summary>

- D14: "No report template management system"

</details>

<a id="req-063"></a>
#### REQ-063 Template Run Or Modify

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml)

**Statement:** The system shall allow staff users to run a report template as-is or run a permitted modifiable item.

Staff users shall be able to execute a report template without changing it when the predefined report is sufficient. When permitted, they shall be able to modify an item for individual needs while preserving the original report template. The allowed modifications shall remain subject to report template restrictions and permissions.

*Priority rationale:* Running templates unchanged or with permitted modifications is supported by two sources and five stakeholders, making it an important expected behavior without a formal decision.

*Stakeholders:* staff, admins, front-line staff, System administrators, Staff

<details><summary>Evidence</summary>

- D12: "Templates should be runnable as-is or modified. Changes shouldn't compromise results."
- D10: "These templates should be runnable as-is or modifiable for individual needs."

</details>

<a id="req-064"></a>
#### REQ-064 Canned Report Date Presets

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall allow canned reports to be run using predefined date ranges.

Staff users shall be able to run canned reports for standard periods without manually entering dates. Supported examples include yesterday, last week, last month, and last year. The date preset shall determine the data period used by the report run.

*Priority rationale:* Predefined date ranges appear only in the specification with no priority signal or corroborating stakeholder support.

*Stakeholders:* individual, staff

<details><summary>Evidence</summary>

- D10: "Will have the ability for it to run by yesterday's data, last week's, last month's, or last year's."

</details>

<a id="req-065"></a>
#### REQ-065 Canned Report Display Editing

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall allow authorized users to edit the display options of canned reports.

Users with appropriate permissions shall be able to customize the fields displayed by a canned report, including adding fields such as shelving location. Display options may include field selection, field ordering, sorting, and permitted output formats. These changes shall affect presentation without requiring the underlying canned report definition to be replaced.

*Priority rationale:* Display editing is supported by only two sources and three stakeholders, with the evidence describing a gap but not establishing a formal priority.

*Stakeholders:* PINES IT Department, staff users, staff

<details><summary>Evidence</summary>

- D14: "No ability to edit canned report display options"
- D10: "Ability to edit canned report for display purposes such as adding shelving location as a display"

</details>

<a id="req-066"></a>
#### REQ-066 Capacity Status Indicators

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall provide color-coded visual indicators for branch capacity status.

The overview shall use visual status indicators to distinguish branches that are under capacity, nearing capacity, or at or over capacity. The suggested mapping is green for under capacity, yellow for getting full, and red for at or over capacity. These indicators shall highlight status in the capacity overview.

*Priority rationale:* Color coding is a desirable example raised by one stakeholder in one email and is not supported by a decision or broader evidence.

*Stakeholders:* chris.sharp@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "Maybe color-coding - green for under capacity, yellow for getting full, red for at/over capacity"

</details>

<a id="req-067"></a>
#### REQ-067 Clone Report Definitions

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D12 (email_report_features.eml)

**Statement:** The system shall allow authorized users to clone an existing report or report template into a new variant without modifying the original.

Cloning shall create a separate report or report template based on an existing definition. The original definition shall remain unchanged. The capability shall be restricted to users with the appropriate permission.

*Priority rationale:* Report cloning is requested in one email by three stakeholders but has no formal decision or independent source support.

*Stakeholders:* staff, admins, managers

<details><summary>Evidence</summary>

- D12: "We also need the ability to "clone" reports - take an existing template and create a new one based on it."

</details>

<a id="req-068"></a>
#### REQ-068 Collection Development Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D20 (survey_results_2009.txt)

**Statement:** The system shall support custom reports for collection development.

Staff users shall be able to create or run reports supporting collection development decisions. The reports shall support local analysis of collection-related data. This is a specific custom reporting use case in addition to general report authoring capabilities.

*Priority rationale:* Collection development reporting is supported only by one survey source and one stakeholder, without a stated priority signal.

*Stakeholders:* library staff

<details><summary>Evidence</summary>

- D20: "Among those who use custom reports, the most common are: Collection development reports"

</details>

<a id="req-069"></a>
#### REQ-069 Comparative Report Columns

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall produce report outputs with comparative columns and calculated percentage differences across time periods.

Reports shall support comparisons such as last month's circulation, the previous month's circulation, and the previous year's corresponding month. The output shall support percentage-difference calculations between the selected periods. Comparative values shall be presented as report columns suitable for analysis.

*Priority rationale:* Comparative columns and percentage differences appear only in the early specification and lack corroboration or priority signals.

*Stakeholders:* staff, management

<details><summary>Evidence</summary>

- D10: "Ability to determine the output results in a way such that a result could have one column for last month's circs, another for previous month's circ, a percent difference column, previous year's month column, a percent difference from last month to last year's month column"

</details>

<a id="req-070"></a>
#### REQ-070 Prewritten Report Templates

**Priority:** Could &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall be delivered with a set of pre-written canned report templates.

The product shall include a baseline set of canned report templates at delivery. These templates shall provide predefined reports for recurring reporting needs. The specific set of included templates is to be established as part of product delivery.

*Priority rationale:* Prewritten canned templates are specified only in the early specification and have one stakeholder with no supporting priority signal.

*Stakeholders:* product

<details><summary>Evidence</summary>

- D10: "There should be a certain set of templates that are pre-written and delivered with the product."

</details>

<a id="req-071"></a>
#### REQ-071 Program Attendance Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D20 (survey_results_2009.txt)

**Statement:** The system shall support custom reports for program attendance tracking.

Staff users shall be able to create or run reports that capture program attendance information. The reports shall support local reporting needs associated with programs. This is a specific custom reporting use case.

*Priority rationale:* Program attendance reports are requested only in one survey by one stakeholder and have no explicit priority signal.

*Stakeholders:* library staff

<details><summary>Evidence</summary>

- D20: "Program attendance tracking"

</details>

<a id="req-072"></a>
#### REQ-072 Report Delivery Address Book

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a reusable address book for managing destinations and recipients of report delivery.

The address book shall allow staff users to maintain regularly used email addresses and other report delivery destinations. Report authors shall be able to use the address book when configuring reusable report delivery profiles. This reuse shall support delivery of reports to commonly used recipients and destinations without requiring them to be managed separately for each profile.

*Priority rationale:* An address book is supported by two sources and four stakeholders but is described as something that would be “great to have,” indicating a desirable enhancement.

*Stakeholders:* PINES IT Department, staff users, individual, staff

<details><summary>Evidence</summary>

- D14: "No address book for report delivery"
- D14: "No address book for report delivery"
- D10: "would be great to have an address book of regularly used addresses"

</details>

<a id="req-073"></a>
#### REQ-073 Selectable Report Data

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall allow authorized users to select the data parts and fields included in a report.

Report authoring shall allow users to choose arbitrary permitted data parts for inclusion in report results. The selected data may determine which fields are displayed in the report output. Selection shall remain subject to the permissions and restrictions of the report or report template.

*Priority rationale:* Selectable report data is mentioned only in the specification with two stakeholders and no explicit priority signal.

*Stakeholders:* individual, staff

<details><summary>Evidence</summary>

- D10: "Check off any part of data you want"

</details>

<a id="req-074"></a>
#### REQ-074 Shared Report Spaces

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide shared folders or shared spaces for storing and organizing report definitions and templates for authorized groups.

Authorized groups shall be able to access shared areas containing report templates and definitions. Shared spaces shall support organization of reusable reporting assets and permissions inheritance where configured. Access shall be limited to the staff users or staff roles authorized for the shared area.

*Priority rationale:* Shared report spaces are raised in one reference source by two stakeholders as an absent concept, without broader support or a decision.

*Stakeholders:* PINES IT Department, staff users

<details><summary>Evidence</summary>

- D14: "No shared folders concept"

</details>

<a id="req-075"></a>
#### REQ-075 Template Sharing Controls

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide controls to share report templates with specified staff users, staff roles, or branches using configurable permissions.

Authorized users shall be able to share report templates at user, staff role, branch, or consortium scope as permitted. Sharing controls shall distinguish read-only use from edit rights. The controls shall also support separate authorization for creating and running reports where required.

*Priority rationale:* Sharing controls are mentioned in one reference source by two stakeholders, with no formal decision or broader corroboration, so they are a desirable enhancement.

*Stakeholders:* PINES IT Department, staff users

<details><summary>Evidence</summary>

- D14: "No shared folders concept; No fine-grained control over who can create vs. run reports"

</details>

### 6.4 Report operations and delivery

*17 requirements - Must: 2, Should: 4, Could: 11, Won't: 0*

<a id="req-076"></a>
#### REQ-076 Background Report Processing

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml), D14 (evergreen_reference_2009.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall queue and execute long-running reports and complex queries asynchronously without blocking foreground staff-user operations.

The system shall run long-running reports and complex queries in the background through asynchronous processing and queuing. This shall allow staff users to continue interactive sessions and other foreground operations while processing occurs. Background processing shall prevent report generation from slowing down the circulation client or disrupting other system functions during open hours.

*Priority rationale:* A meeting-recorded agreement, four independent sources, eight stakeholders, and signals describing the need as a major performance concern make asynchronous processing essential.

*Stakeholders:* PINES IT Department, Robert Chen, Katherine Gregory, Staff, George Tuttle, Dana Peeler, Working Group, Circulation staff

<details><summary>Evidence</summary>

- D14: "No background processing for long-running reports"
- D09: "For 3.5 million patrons, this query could be slow. We should run it as a background report and cache results."
- D16: "We need to make sure reports can be queued and processed in the background."

</details>

<a id="req-077"></a>
#### REQ-077 Last Item Report

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D06 (conversations/conv_pines021_item_purging.eml), D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall provide a report identifying items that are the only copy within a selectable branch or consortium scope.

The report shall identify items that are the last copy within the selected branch or consortium scope. It shall include items that represent the last copy in the consortium. Staff users need this report to identify last-copy items for cataloging activities, including editing WorldCat entries. The report shall support selection of either a branch or the consortium as its scope.

*Priority rationale:* The requirement has a CRITICAL signal, explicit stakeholder support across four sources and ten stakeholders, and an agreement documenting the requested scope.

*Stakeholders:* Catalogers, Staff, Maria Rodriguez, Thomas Wright, Latoya Davidson, Katherine Gregory, Robert Chen, PINES IT Department ...

<details><summary>Evidence</summary>

- D10: "Examples of periodic reports include: - Items that are the last copy in the system"
- D10: "The system should provide a last copy report that singles out a library system's last copies, to assist catalogers who need to edit WorldCat entries."
- D06: "CRITICAL: We need a "last copy report" that identifies our library system's last copies."

</details>

<a id="req-078"></a>
#### REQ-078 Cancel Report Runs

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow authorized staff users to cancel queued, scheduled, or running report runs and record the cancellation.

Authorized staff users need to stop report runs that have not started or are currently processing. The report processor shall periodically check for cancellation signals so that long-running report runs can stop, and cancellation shall update the queue and report history as appropriate. Cancellation actions shall be audited, and associated schedules or report definitions shall be updated as needed.

*Priority rationale:* The need to cancel running reports is supported by four source types and eight stakeholders, but there is no formal decision or critical signal.

*Stakeholders:* PINES IT Department, staff users, library staff, administrators, staff, individual, Technical Subcommittee, Robert Chen

<details><summary>Evidence</summary>

- D14: "No ability to cancel a running report"
- D20: ""Ability to cancel a scheduled or running report""
- D14: "No ability to cancel a running report"

</details>

<a id="req-079"></a>
#### REQ-079 Data Quality Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide data quality reports identifying issues such as invalid item types and item call numbers that exceed the acceptable length.

The data quality reporting capability shall provide specific reports for invalid item types and item call numbers that exceed the acceptable length. These reports shall identify items affected by invalid item types and excessively long call numbers. The capability shall support identification of these and other data quality issues.

*Priority rationale:* Data quality reporting is supported across an interview, meeting, and specification by six stakeholders, making it important despite the example-oriented signal.

*Stakeholders:* Jennifer Durham, Cataloging staff, System administrators, Thomas Wright, Catalogers, Staff

<details><summary>Evidence</summary>

- D18: "Data quality reports are needed"
- D15: "Data quality reports - items with long call numbers"
- D15: "Data quality reports - items with invalid item type"

</details>

<a id="req-080"></a>
#### REQ-080 Prioritize Report Queue

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall allow authorized staff users to set and modify priorities for report runs in the processing queue.

Authorized staff users need to advance important reports ahead of lower-priority or resource-consuming reports. Priorities shall apply to individual report runs and, where supported, certain types of reports. The queue processor shall use these priorities to order execution or reserve resources during peak periods.

*Priority rationale:* Queue prioritization is supported by three sources, seven stakeholders, and repeated signals that it is crucial or important, but lacks a formal meeting decision.

*Stakeholders:* PINES IT Department, operations staff, staff, administrators, admins, directors, IT

<details><summary>Evidence</summary>

- D14: "No ability to prioritize certain types of reports"
- D10: "Ability to prioritize certain types of reports so they will pop to the top of the queue over resource-consuming reports"
- D12: "Also, the ability to prioritize certain reports is crucial. A director's board report should be able to jump ahead of a staff member's ad-hoc query."

</details>

<a id="req-081"></a>
#### REQ-081 Recurring Report Scheduling

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml), D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow staff users to schedule reports to run immediately or recur hourly, daily, weekly, monthly, or yearly.

Staff users need to automate report runs at recurring frequencies and request immediate execution when needed. Scheduling options shall include Run ASAP, Hourly, Daily, Weekly, Monthly, and Yearly. The capability shall support recurring reports generally and periodic runs of the inactive patrons report, including schedules such as quarterly where applicable, and shall retain historical cached results for that report.

*Priority rationale:* Recurring scheduling is supported by four sources, eight stakeholders, and a 52% survey signal, making it important even without a formal decision.

*Stakeholders:* individual, staff, George Tuttle, Katherine Gregory, library staff, administrators, PINES IT Department, staff users

<details><summary>Evidence</summary>

- D10: "Ability to select Run ASAP, Hourly, Daily, Weekly, Monthly, Yearly"
- D09: "We run this quarterly to clean up our patron database."
- D20: "Ability to schedule recurring reports: 52%"

</details>

<a id="req-082"></a>
#### REQ-082 Bibliographic Records With Holds

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall generate a periodic report of bibliographic records with holds.

Staff users need a periodic report identifying bibliographic records that have holds. The report supports monitoring and follow-up of works or titles with outstanding holds. It shall be available as a recurring report rather than only as an ad hoc result.

*Priority rationale:* This is an example report mentioned only in the early specification, with one source and one stakeholder and no stronger priority evidence.

*Stakeholders:* Staff

<details><summary>Evidence</summary>

- D10: "Examples of periodic reports include: - Bibliographic records with holds"

</details>

<a id="req-083"></a>
#### REQ-083 Bibliographic Records Without Items Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall provide a report identifying bibliographic records that have no attached items.

The report shall identify bibliographic records without associated items. The system shall support periodic reporting of these records. The system shall also support on-demand reporting of these records.

*Priority rationale:* Although supported by an interview and the specification and five stakeholders, it is still presented only as an example with no explicit priority signal or decision.

*Stakeholders:* Catalogers, Staff, cataloger, staff, Thomas Wright

<details><summary>Evidence</summary>

- D10: "Examples of periodic reports include: - Bibliographic records with no item records"
- D10: "Bib Records with No Volumes attached"
- D15: "Data quality reports - bibliographic records with no item records."

</details>

<a id="req-084"></a>
#### REQ-084 Capacity Data CSV Export

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall provide a CSV export of the capacity overview and selected branch data.

Staff users need to provide capacity overview and selected branch data to stakeholders for analysis in spreadsheets. The system shall generate this data in CSV output format. The export is specifically intended to support directors and other stakeholders who use spreadsheets.

*Priority rationale:* CSV export has an email agreement and a practical spreadsheet use case, but support comes from only one source and two stakeholders.

*Stakeholders:* jennifer.durham@statesboro.lib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "And export to CSV for the directors who want spreadsheets."

</details>

<a id="req-085"></a>
#### REQ-085 Edit Recurring Report Selections

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall allow staff users to edit the report selections and email recipients of a recurring report schedule.

Staff users need to maintain recurring deliveries as reporting needs change. They shall be able to add or remove reports included in a recurring schedule and change its recipient email addresses. These edits shall apply to the selected recurring schedule without requiring it to be recreated.

*Priority rationale:* Editing recurring report selections is mentioned only in the specification and has limited support from two stakeholders, with no priority signal.

*Stakeholders:* individual, staff

<details><summary>Evidence</summary>

- D10: "Ability to edit recurring reports by adding or removing report selections as well as editing the email addresses"

</details>

<a id="req-086"></a>
#### REQ-086 In-Transit Items With Holds

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall generate a periodic report of in-transit items with outstanding holds.

Staff users need to identify in-transit items that also have holds placed on them. The report shall combine the item's in-transit status with its outstanding hold information. It shall be available periodically for operational follow-up.

*Priority rationale:* This periodic report is only a specification example with two stakeholders and no corroborating decision or priority signal.

*Stakeholders:* Front-line staff, Staff

<details><summary>Evidence</summary>

- D10: "Examples of periodic reports include: - In-transit items with outstanding hold"

</details>

<a id="req-087"></a>
#### REQ-087 Inactive Patrons CSV Export

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml)

**Statement:** The system shall allow staff users to export the inactive patrons report in CSV format for use by outreach systems.

Staff users need to export inactive patron data for outreach activities. The CSV shall include the mailing address, patron ID, flags, and fines status fields identified for that use. The output shall be suitable for uploading into external outreach systems.

*Priority rationale:* The CSV format has an email agreement and a stated outreach use case, but evidence is limited to one source and two stakeholders.

*Stakeholders:* Latoya Davidson, Katherine Gregory

<details><summary>Evidence</summary>

- D09: "Exportable format (CSV)"

</details>

<a id="req-088"></a>
#### REQ-088 Invalid Patron Branch Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall generate a periodic report of patrons with an invalid branch location.

Staff users need to detect patron records whose branch location is invalid or inconsistent. The report shall identify affected patron records for data-quality correction. It shall be available periodically.

*Priority rationale:* The requirement is only a specification example with two stakeholders and no additional priority evidence.

*Stakeholders:* Staff, Administrators

<details><summary>Evidence</summary>

- D10: "Examples of periodic reports include: - Patrons with invalid home library"

</details>

<a id="req-089"></a>
#### REQ-089 Item-Level Holds

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall generate a periodic report of item-level holds.

Staff users need a report showing holds associated with individual items. The report shall represent holds at the item level rather than only at the bibliographic-record level. It shall be available periodically for circulation and collection-management work.

*Priority rationale:* Item-level holds are listed only as a specification example, with one stakeholder and no explicit priority signal.

*Stakeholders:* Staff

<details><summary>Evidence</summary>

- D10: "Examples of periodic reports include: - Item-level holds"

</details>

<a id="req-090"></a>
#### REQ-090 Items Not Recently Checked Out

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall generate a periodic report of items that have not been checked out for a configurable number of days.

Staff users need to identify items that have not circulated recently for collection-management review. The number of days shall be configurable by an authorized staff user. The report shall be available periodically.

*Priority rationale:* This report is supported only by the specification and one stakeholder, so it is a desirable but nonessential enhancement.

*Stakeholders:* Staff

<details><summary>Evidence</summary>

- D10: "Examples of periodic reports include: - Items that have not been checked out in X days"

</details>

<a id="req-091"></a>
#### REQ-091 Overdue In-Transit Items

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall generate a periodic report of items that have been in transit longer than a configurable number of days.

Staff users need to identify in-transit items that exceed an operational time threshold. The threshold in days shall be configurable. The report shall support scope by branch and by the consortium.

*Priority rationale:* Overdue in-transit reporting is only a specification example with two stakeholders and no formal decision or stronger priority signal.

*Stakeholders:* Front-line staff, Staff

<details><summary>Evidence</summary>

- D10: "Examples of periodic reports include: - Items that have been in-transit for more than X days"

</details>

<a id="req-092"></a>
#### REQ-092 Schedule Multiple Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall allow staff users to select multiple reports for coordinated scheduling or simultaneous execution.

Staff users need to schedule more than one report without configuring each report separately. The system shall allow multiple report definitions to be selected as a batch. The batch shall support coordinated scheduling or execution at the same time.

*Priority rationale:* Coordinated scheduling is supported only by one reference source and two stakeholders, with no formal decision or broader corroboration.

*Stakeholders:* PINES IT Department, staff users

<details><summary>Evidence</summary>

- D14: "No ability to check multiple reports to run at the same time"

</details>

### 6.5 Circulation and transaction reporting

*33 requirements - Must: 5, Should: 16, Could: 12, Won't: 0*

<a id="req-093"></a>
#### REQ-093 Accurate Check-In Timestamp

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall record and expose check-in date and time fields that represent actual check-in events and exclude renewal events.

Both requirements require a distinct check-in timestamp that is not affected by renewals. The system shall record and expose accurate check-in date and time values for check-in transactions. Check-in and renewal timestamps shall remain distinguishable.

*Priority rationale:* Accurate separation of actual check-ins from renewals is foundational to trustworthy transaction reporting, and the issue is supported by two independent sources and three stakeholders.

*Stakeholders:* library staff, PINES IT Department, circulation staff

<details><summary>Evidence</summary>

- D20: ""Checkin date/time should not include renewals""
- D14: "Checkin Date/time not including renewals - checkin and renewal timestamps are stored together"

</details>

<a id="req-094"></a>
#### REQ-094 Check-In Count Reporting

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide check-in count reports, including individual and cumulative counts broken down by check-in method such as book drop, terminal, staff user, and self-service.

The method-specific requirement fully contains the general check-in count requirement. The system shall report check-in counts and shall support both individual and cumulative totals, with breakdowns by check-in method.

*Priority rationale:* Check-in counts by method are a core circulation-reporting capability supported by the specification and survey, with four stakeholders and an explicit 'should' signal.

*Stakeholders:* individual, staff, Staff, library staff

<details><summary>Evidence</summary>

- D10: "CIRCULATION REPORTS: - Check in Count"
- D10: "CIRCULATION REPORTS: - Check in Count"
- D20: ""I need to see check-in counts broken down by method - book drop vs terminal vs self-service""

</details>

<a id="req-095"></a>
#### REQ-095 Checkout and Renewal Count Reporting

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall count checkout and renewal transactions separately and cumulatively by type and provide renewal counts separately from checkout counts.

Both requirements address distinct counting of checkout and renewal transactions. The system shall report checkout and renewal counts independently and cumulatively, including supported transaction types such as staff, self-service, online, and OPAC renewals, while ensuring that renewal totals are available separately from checkout totals.

*Priority rationale:* Separating checkout and renewal counts is essential for accurate circulation reporting and is supported by both the specification and survey.

*Stakeholders:* Staff, library staff, staff

<details><summary>Evidence</summary>

- D10: "The system counts all types of check-out individually and cumulatively: - staff check-out - self check-out - staff renewal - self checkout renewal - online renewal - OPAC renewal"
- D20: ""Check-out types should be counted separately - staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, OPAC renewal""
- D10: "CIRCULATION REPORTS: - Renewals Count"

</details>

<a id="req-096"></a>
#### REQ-096 Checkout Count Report

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report counting checkouts only and excluding renewals and non-cataloged transaction types unless otherwise specified.

The report shall show checkout counts as a distinct circulation measure. Renewals and non-cataloged transaction types shall be excluded from this report unless another specification defines otherwise. Detailed checkout and renewal breakdowns are covered by a separate requirement.

*Priority rationale:* A checkout-only count that excludes renewals is necessary to prevent misleading core circulation totals, although it is documented in one source with three stakeholders.

*Stakeholders:* individual, staff, Staff

<details><summary>Evidence</summary>

- D10: "Checkout Count (includes checkouts only)"
- D10: "CIRCULATION REPORTS: - Checkout Count (includes checkouts only)"

</details>

<a id="req-097"></a>
#### REQ-097 Total Circulation Count Report

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a Total Circulation Count report that includes checkouts, renewals, and uncataloged circulation with a breakdown by circulation type.

Staff users need one circulation report that combines cataloged and uncataloged circulation data into a total. The report shall include checkouts, renewals, and non-cataloged circulation. It shall display both the aggregate total and a breakdown by those circulation types.

*Priority rationale:* A total circulation report combining checkouts, renewals, and uncataloged circulation is central to the system's reporting purpose and explicitly requires a breakdown by transaction type.

*Stakeholders:* staff, Staff

<details><summary>Evidence</summary>

- D10: "Total Circulation Count (Merging both Cat and Non-Cat circulation data)"
- D10: "CIRCULATION REPORTS: - Total Circulation Count (Merging both Cat and Non-Cat circulation data)"
- D10: "Circulation Count - total circ including checkouts, renewals, and noncats"

</details>

<a id="req-098"></a>
#### REQ-098 Branch Holds Count

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml)

**Statement:** The system shall report the number of holds for a given branch.

The system shall provide the number of holds associated with a specified branch. Holds shall be reportable as a separate metric and included in relevant overall breakdowns. This requirement is distinct from annual hold counts and hold-placement-origin counts.

*Priority rationale:* Branch hold counts were requested by multiple stakeholders and agreed in an email, but the agreement is not a formal meeting decision.

*Stakeholders:* Maria Rodriguez, Susan Sexton-Cooley, Katherine Gregory

<details><summary>Evidence</summary>

- D01: "Like total items in library, number of holds, number of adult fiction, number of board books..."

</details>

<a id="req-099"></a>
#### REQ-099 Circulation By Age Demographic

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide circulation count reports grouped by patron age demographic, with definable age groups.

The report shall aggregate circulation counts by patron age demographic categories. Staff users shall be able to define the age groups used for aggregation. The report supports analysis of circulation activity across patron age groups.

*Priority rationale:* Age-based circulation reporting has support from two sources and five stakeholders, but no formal decision or mandatory signal.

*Stakeholders:* staff, patron, PINES IT Department, library staff, Staff

<details><summary>Evidence</summary>

- D10: "Circulation Count by Age Demographic"
- D14: "Circulation Count by Age Demographic (not available)"
- D10: "CIRCULATION REPORTS: - Circulation Count by Age Demographic"

</details>

<a id="req-100"></a>
#### REQ-100 Circulation By County

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a circulation count report cross-tabulated by circulation location and patron county.

The report shall aggregate circulation counts using circulation location and patron county as dimensions. It shall cross-tabulate the two dimensions so staff users can compare activity at circulation locations by patron county. The circulation location is the relevant branch location or shelving/circulation location represented in the source requirements.

*Priority rationale:* County cross-tabulation is supported by the reference and specification and has the broadest stakeholder support in this group, with six stakeholders, but no formal decision.

*Stakeholders:* PINES IT Department, library staff, staff, patron, Staff, Administrators

<details><summary>Evidence</summary>

- D14: "Circulation Count by Circ Location broken down by Patron County (not available)"
- D10: "Circulation Count by Circ Location broken down by Patron County"
- D10: "CIRCULATION REPORTS: - Circulation Count by Circ Location broken down by Patron County"

</details>

<a id="req-101"></a>
#### REQ-101 Circulation By Dewey

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a circulation count report grouped by Dewey classification or Dewey call number ranges.

The report shall aggregate circulation counts by Dewey classification. Staff users shall be able to view counts by Dewey class numbers or call number ranges. This supports analysis of circulation by subject classification.

*Priority rationale:* Dewey-based circulation reporting is supported by two sources and five stakeholders and addresses a reported availability gap, but is not formally mandated.

*Stakeholders:* staff, Staff, Catalogers, PINES IT Department, library staff

<details><summary>Evidence</summary>

- D10: "Circulation Count by Dewey"
- D10: "CIRCULATION REPORTS: - Circulation Count by Dewey"
- D14: "Circulation Count by Dewey (not available)"

</details>

<a id="req-102"></a>
#### REQ-102 Circulation By MARC Fields

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a circulation count report that aggregates counts by specified MARC fields.

The report shall allow staff users to select MARC fields as grouping or filtering criteria. Examples include MARC 650 for subject and MARC 100 for author. The resulting report shall aggregate circulation counts using the selected fields.

*Priority rationale:* MARC-field aggregation is supported by two sources and five stakeholders and is identified as not available, indicating meaningful demand without a formal decision.

*Stakeholders:* staff, Catalogers, Staff, PINES IT Department, library staff

<details><summary>Evidence</summary>

- D10: "Circulation Count by MARC"
- D10: "CIRCULATION REPORTS: - Circulation Count by MARC"
- D14: "Circulation Count by MARC fields (not available)"

</details>

<a id="req-103"></a>
#### REQ-103 Circulation Reporting by Modifier Categories

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide circulation count reports grouped by circulation modifier and, where applicable, by Category 1 and Category 2 modifier categories.

M105 specifies the modifier-category breakdown while encompassing the basic circulation-modifier grouping required by M104. The merged requirement shall report circulation counts by circulation modifier and support additional grouping by Category 1 and Category 2.

*Priority rationale:* Modifier-category reporting is supported by two sources and five stakeholders, with the current capability explicitly described as only partially available.

*Stakeholders:* staff, Staff, PINES IT Department, library staff, individual

<details><summary>Evidence</summary>

- D10: "Circulation Count by Circ Modifier"
- D10: "CIRCULATION REPORTS: - Circulation Count by Circ Modifier"
- D14: "Circulation Count by Circ Modifier (partially available)"

</details>

<a id="req-104"></a>
#### REQ-104 Claims Returned Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a Claims Returned report containing items recorded through the claims-returned workflow and their related transaction details.

The report shall include item and transaction details for claims-returned records. These details shall include relevant dates, patron information, and resolution information. The report shall support staff users who need to review claims-returned records and their associated transaction details.

*Priority rationale:* Claims-returned reporting is supported by both a reference and the specification and addresses a stated availability gap, though it lacks a formal decision.

*Stakeholders:* circulation staff, PINES IT Department, staff

<details><summary>Evidence</summary>

- D14: "Claims Returned report (not available)"
- D14: "Claims Returned report (not available)"
- D10: "Claims returned"

</details>

<a id="req-105"></a>
#### REQ-105 Hold Status Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml), D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide hold reports covering placed, filled, stale, and status-based holds, with breakdowns by category and placement method.

Staff users need reports that show overall hold counts and group them by selected categories such as adult fiction, board books, or format. Reports shall cover placed, filled, and stale holds and support subtotals by hold type or status, including active, frozen, and frozen-until. The reports shall indicate whether each hold was placed at a staff desk, at a public computer, or remotely. A separate Stale Holds report is specified for detailed stale-hold processing.

*Priority rationale:* Hold-status reporting has support from three source types, five stakeholders, a 41% survey signal, and an email agreement, but no formal meeting decision.

*Stakeholders:* library staff, Robert Chen, Susan Sexton-Cooley, Katherine Gregory, Staff

<details><summary>Evidence</summary>

- D20: "Hold reports (placed, filled, stale): 41%"
- D01: "Shows breakdowns with holds count per category"
- D20: ""Holds reports should show how the hold was placed - at staff desk, at public computer, or remotely""

</details>

<a id="req-106"></a>
#### REQ-106 Holds Purchase Alert Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a Holds Purchase Alert report that identifies items with holds warranting purchase consideration.

Staff users need a report that uses hold data to identify high-demand bibliographic records or patterns of holds that may justify purchasing additional items. The report shall support purchase planning by highlighting items with sufficient demand for consideration. No specific threshold for purchase consideration is defined.

*Priority rationale:* The purchase-alert report is supported by two sources and four stakeholders and addresses a stated availability gap, but is not formally mandated.

*Stakeholders:* staff, acquisitions, PINES IT Department, collection development staff

<details><summary>Evidence</summary>

- D10: "Holds Purchase Alert"
- D14: "Holds Purchase Alert (not available)"

</details>

<a id="req-107"></a>
#### REQ-107 Items In Circulation Count

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml)

**Statement:** The system shall report the number of items currently checked out and in circulation for a given branch.

The system shall provide the current count of items that are checked out. The count shall be available as a separate metric and as part of totals and category breakdowns. Checked-out items shall contribute to total holdings for the specified branch.

*Priority rationale:* Branch counts of items in circulation were clarified and agreed in an email and have four stakeholders, but the agreement is not a formal meeting decision.

*Stakeholders:* Susan Sexton-Cooley, George Tuttle, Maria Rodriguez, Katherine Gregory

<details><summary>Evidence</summary>

- D01: "The volume should include: 3. Items out in circulation (checked out)"

</details>

<a id="req-108"></a>
#### REQ-108 Items On Shelf Count

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml)

**Statement:** The system shall report the number of items currently on the shelf and checked in for a given branch.

The system shall provide the current count of items that are on the shelf and checked in. The count shall be available as a separate metric and as part of totals and category breakdowns. The reporting scope is a specified branch.

*Priority rationale:* On-shelf counts were proposed and captured in an email summary with three stakeholders, making them important but not formally mandatory.

*Stakeholders:* Susan Sexton-Cooley, Maria Rodriguez, Katherine Gregory

<details><summary>Evidence</summary>

- D01: "The volume should include: 2. Items on the shelf (checked in)"

</details>

<a id="req-109"></a>
#### REQ-109 Patron Transaction Totals

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall display the number of checkouts and placed holds for each patron in transaction reports.

Transaction reports shall provide per-patron totals for checkouts and holds placed. The information shall allow staff users to review a patron's transaction volume. No additional transaction types are specified for this per-patron view.

*Priority rationale:* Patron transaction totals have an explicit 'should' signal, although they are documented in only one source and supported by one stakeholder.

*Stakeholders:* Staff

<details><summary>Evidence</summary>

- D10: "The system displays the number of check-outs and placed holds per patron."

</details>

<a id="req-110"></a>
#### REQ-110 Stale Holds Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a Stale Holds report identifying holds that meet configured stale-hold criteria.

Staff users need to identify holds that have remained on the hold shelf or otherwise lacked progress beyond the applicable pickup window or threshold. The report shall list stale holds for cleanup and follow-up. The definition of stale shall be configurable or parameterized, such as a hold older than a specified number of days without progress.

*Priority rationale:* The stale-holds report is supported by two sources and addresses a stated availability gap, but lacks a formal decision.

*Stakeholders:* staff, library staff

<details><summary>Evidence</summary>

- D10: "Stale Holds (holds sitting on hold shelf waiting for pickup for too long)"
- D14: "Stale Holds (not available)"

</details>

<a id="req-111"></a>
#### REQ-111 Transaction Grouping Dimensions

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow transaction reports to be grouped by branch, hour, system or ILS, and terminal, and queried by transaction type or all transactions.

Staff users shall be able to group transaction reports by branch, hour, system or ILS, and terminal. These grouping dimensions shall support analysis of transactions by organizational, time, system, and workstation dimensions. Staff users shall be able to query reports for all transactions or select particular transaction types, including check-ins, check-outs, fines collected, and patron registrations. Grouping transactions by hour shall support identification of busy periods.

*Priority rationale:* Grouping transactions by branch, time, system, terminal, and type is supported by the specification and survey and four stakeholders, but is not explicitly mandatory.

*Stakeholders:* Staff, Administrators, library staff, PINES Reports Working Group

<details><summary>Evidence</summary>

- D10: "Transactions can be grouped by hour, terminal, branch, and system. Transactions include check-ins, check-outs, fines collected, patron registrations, etc., and can be queried by all transactions or by type of transaction."
- D20: "Transactions can be grouped by hour, terminal, branch, and system."
- D20: "Group transactions by hour to identify busy periods"

</details>

<a id="req-112"></a>
#### REQ-112 Transactions By Reporting Scope

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide reports showing holds placed, holds filled, and check-outs per patron, branch, selected group of branches, system, and county.

Staff users need transaction reporting at patron, branch, consortium-system, and geographic aggregation levels. The reports shall cover holds placed, holds filled, and check-outs. Reporting shall support an individual branch, a selected group of branches, the system, a county, and an individual patron as applicable.

*Priority rationale:* Reporting by patron, branch, system, and county is supported by two sources and four stakeholders with a 'can generate' signal, but no formal decision.

*Stakeholders:* Staff, Administrators, library staff, PINES Reports Working Group

<details><summary>Evidence</summary>

- D10: "The system can generate a report of transactions (holds placed, holds filled, and check-outs) per patron, per library, per selected group of libraries, per system, per county."
- D20: "Transactions report can show holds placed, holds filled, and check-outs per patron, per library, per group of libraries, per system, per county."

</details>

<a id="req-113"></a>
#### REQ-113 Unfilled Holds Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide an Unfilled Holds report reporting holds that have not been fulfilled.

Staff users need to identify current holds that remain unfilled so they can monitor fulfillment and take corrective action. The report should include the hold placement date and patron information where available. It shall present holds that have not yet been fulfilled.

*Priority rationale:* An unfilled-holds report is supported by the reference and specification and addresses a stated availability gap, but is not formally mandated.

*Stakeholders:* staff, library staff

<details><summary>Evidence</summary>

- D10: "Unfilled Holds"
- D14: "Unfilled Holds (not available)"

</details>

<a id="req-114"></a>
#### REQ-114 Annual Holds Placed Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide an annual report showing the number of holds placed.

The report shall summarize the total number of holds placed during an annual period. It is intended for circulation reporting and annual activity analysis. The requirement does not specify additional dimensions or hold-placement origins.

*Priority rationale:* The annual holds report appears only as an example in the early specification, with no additional priority signal or corroborating source.

*Stakeholders:* staff, management

<details><summary>Evidence</summary>

- D10: "Annual # of holds placed"

</details>

<a id="req-115"></a>
#### REQ-115 Circulation By Home Branch

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a circulation count report cross-tabulated by circulation location and patron home branch.

The report shall aggregate circulation counts using circulation location and the patron's home branch. It shall cross-tabulate these dimensions to show where circulation occurs in relation to patron home branch. The report is intended to support branch-level circulation analysis.

*Priority rationale:* Home-branch cross-tabulation appears only in the specification and has limited support from three stakeholders.

*Stakeholders:* staff, Staff, Administrators

<details><summary>Evidence</summary>

- D10: "Circulation Count by Circ Location broken down by Patron Home Library"
- D10: "CIRCULATION REPORTS: - Circulation Count by Circ Location broken down by Patron Home Library"

</details>

<a id="req-116"></a>
#### REQ-116 Circulation By Shelving Location

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a circulation count report grouped by shelving location.

The report shall aggregate circulation counts by shelving location values. It shall provide a distinct circulation breakdown for the shelving locations represented in the system. No additional grouping dimensions are specified.

*Priority rationale:* Shelving-location reporting is listed only in the specification and has support from just two stakeholders.

*Stakeholders:* staff, Staff

<details><summary>Evidence</summary>

- D10: "Circulation Count by Shelving Location"
- D10: "CIRCULATION REPORTS: - Circulation Count by Shelving Location"

</details>

<a id="req-117"></a>
#### REQ-117 Hold Request Origin Counts

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall count hold requests by placement origin, including staff desk, public computer inside the branch, and remote placement.

The system shall track the origin through which each hold request was placed. Reports shall distinguish staff-desk placement, placement at a public computer inside the branch, and remote placement. Counts shall support comparison of hold activity across placement channels.

*Priority rationale:* Origin counts have only one source and one stakeholder despite the specification's 'should' signal, so they are a desirable enhancement rather than a release essential.

*Stakeholders:* Staff

<details><summary>Evidence</summary>

- D10: "The system counts all hold requests, including how the hold was placed: - at a staff desk - at a public computer inside the library - remotely"

</details>

<a id="req-118"></a>
#### REQ-118 In-House Use Count Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report counting in-house use of cataloged items.

The report shall count in-house uses associated with cataloged items. It shall provide the count as a circulation-related reporting measure. No additional grouping or time period is specified.

*Priority rationale:* In-house-use reporting appears only in the specification and has support from one stakeholder.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "Cataloged In House Use Count"

</details>

<a id="req-119"></a>
#### REQ-119 IntraPINES Loans Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide an IntraPINES Loans report covering all systems and facilities, with loan counts broken down by system and facility.

Staff users need to analyze loans exchanged within the consortium at both system and facility levels. The report shall provide an overall view across all systems and facilities. It shall also present loan counts broken down by each applicable system and facility.

*Priority rationale:* The IntraPINES loans report is specified in only one source and, despite three stakeholders, has no priority signal or formal decision.

*Stakeholders:* staff, facility, system

<details><summary>Evidence</summary>

- D10: "IntraPINES Loans by Facility"
- D10: "IntraPINES Loans by System"
- D10: "IntraPINES Loans for all Facilities"

</details>

<a id="req-120"></a>
#### REQ-120 Items Received For Holds

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report of items received to fulfill holds.

Staff users need to identify items that have arrived at pickup branches or other pickup points for hold fulfillment. The report shall list items received for holds. It supports monitoring and processing of items awaiting pickup or related hold workflows.

*Priority rationale:* Items-received-for-holds reporting is a single-specification example supported by only one stakeholder.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "Items Received for Holds"

</details>

<a id="req-121"></a>
#### REQ-121 Items Sent For Holds

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report of items sent to fulfill holds.

Staff users need to identify items dispatched to fulfill holds. The report shall list items sent for hold fulfillment and support monitoring of movement toward the requesting branch or pickup point. No additional grouping or filtering parameters are specified.

*Priority rationale:* Items-sent-for-holds reporting is a single-specification example supported by only one stakeholder.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "Items Sent for Holds"

</details>

<a id="req-122"></a>
#### REQ-122 Monthly Non-Cat In-House Use

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a NonCat In House Use Count by Month report.

Staff users need to monitor monthly in-house use involving uncataloged or non-cataloged items. The report shall provide counts by month. No additional grouping or filtering parameters are specified.

*Priority rationale:* The monthly non-cataloged in-house-use report appears only in the specification and has no corroborating support.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "NonCat In House Use Count by Month"

</details>

<a id="req-123"></a>
#### REQ-123 Non-Cat Count Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a Non-Cat Count report for uncataloged circulation.

Staff users need counts of circulation involving uncataloged or non-cataloged items. The system shall provide a dedicated Non-Cat Count report for these circulation counts. The report is distinct from the combined Total Circulation Count report.

*Priority rationale:* Non-cataloged circulation counts are supported by only two stakeholders in one specification source and have no priority signal.

*Stakeholders:* Staff, staff

<details><summary>Evidence</summary>

- D10: "CIRCULATION REPORTS: - Non-Cat Count"
- D10: "Non-Cat Count"

</details>

<a id="req-124"></a>
#### REQ-124 Transaction Type Reporting

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D20 (survey_results_2009.txt)

**Statement:** The system shall include check-ins, check-outs, fines collected, and patron registrations in transaction reports.

Staff users need transaction reports that cover the specified circulation, financial, and registration transactions. The reports shall include check-ins, check-outs, fines collected, and patron registrations. These transaction types shall be available for the applicable transaction reporting and analysis.

*Priority rationale:* Transaction-type reporting is supported only by one survey stakeholder and has no additional priority signal or decision.

*Stakeholders:* library staff

<details><summary>Evidence</summary>

- D20: "Transactions include check-ins, check-outs, fines collected, patron registrations, etc."

</details>

<a id="req-125"></a>
#### REQ-125 Transaction Workstation Filters

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall allow staff users to report transactions for a specified date and time on a specified workstation or performed by a specified staff user.

Staff users need to investigate transactions associated with a particular time period and point of operation. The system shall support filtering by specified date and time, workstation identifier, or staff user. This enables analysis and review of transactions performed at a workstation or by an authenticated staff user.

*Priority rationale:* Workstation and staff-user filters appear only in the specification and have limited support from two stakeholders.

*Stakeholders:* staff, security

<details><summary>Evidence</summary>

- D10: "Ability to run a report on transactions that occurred on x date and time on x workstation or by x staff"

</details>

### 6.6 Inventory and collection management

*39 requirements - Must: 4, Should: 15, Could: 20, Won't: 0*

<a id="req-126"></a>
#### REQ-126 Branch Capacity Distribution Analysis

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt)

**Statement:** The system shall provide reporting and analysis to evaluate branch capacity and determine collection distribution across branches.

Staff users need to assess whether branch capacity and shelving or space constraints are suitable for current holdings. The analysis shall support evaluation of collection distribution across branches and recommendations for optimal distribution. It shall address branch capacity, shelving or space constraints, and collection placement decisions.

*Priority rationale:* The requirement was formally agreed and accepted as a scope item in meeting minutes, making it a committed consortium capability.

*Stakeholders:* Local System Administrators, Library Managers, Library Directors

<details><summary>Evidence</summary>

- D17: "Analyzing branch capacity and optimal distribution of the collection"

</details>

<a id="req-127"></a>
#### REQ-127 Collection Usage Analysis

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt)

**Statement:** The system shall provide reports and analysis of collection composition and use by patrons.

Staff users need to evaluate the collection and how patrons use its materials. Analysis shall support collection composition, circulation or usage statistics, and patron interactions with collection items. The results shall inform collection management decisions.

*Priority rationale:* The requirement was formally accepted in meeting minutes as a scope item, providing strong decision evidence for inclusion.

*Stakeholders:* Library Managers, Staff

<details><summary>Evidence</summary>

- D17: "Analyzing the Library collection and its use by patrons"

</details>

<a id="req-128"></a>
#### REQ-128 Consolidated In-Transit Item Reporting

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D05 (conversations/conv_pines019_020_missing_intransit.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide a consolidated in-transit item report combining transit-to and transit-from records, with filtering or grouping by sending and destination branch and views for a branch or the consortium.

Both requirements describe reporting on items moving between branches. The merged report shall combine transit-to and transit-from records, support branch-level or consortium-wide viewing, and allow grouping or filtering by sending and destination branch.

*Priority rationale:* It has the explicit “critical” signal, twelve stakeholders, four source types, and confirmed consolidation agreements, making it essential.

*Stakeholders:* staff, facility, Dana Peeler, Delivery coordination staff, Branch managers, Front-line staff, Staff, Thomas Wright ...

<details><summary>Evidence</summary>

- D10: "List of Items in Transit by both sending library and destination library"
- D18: "In-transit item reports are critical for delivery coordination"
- D10: "The system should generate a list of items that have been in-transit for more than X days (X configurable), per branch and per system."

</details>

<a id="req-129"></a>
#### REQ-129 Missing and Damaged Item Reporting

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D05 (conversations/conv_pines019_020_missing_intransit.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide missing and damaged item reports with filtering and aggregation by branch and time period, including item condition notes and audit-oriented summary counts.

These requirements collectively specify reporting on missing and damaged items. Reports shall support date-range filtering, item condition notes, branch-level views, and summary counts or aggregates by branch and time period for auditing.

*Priority rationale:* Four source types, ten stakeholders, an email agreement, and explicit audit language including “crucial” make this essential for inventory audit and collection management.

*Stakeholders:* Robert Chen, Latoya Davidson, Staff, Dana Peeler, Branch managers, Thomas Wright, Maria Rodriguez, Katherine Gregory ...

<details><summary>Evidence</summary>

- D05: ""The missing/damaged report can include date ranges (e.g., last 30 days, last quarter, etc.) which would be useful for trending.""
- D05: ""Also, can the report include item condition notes? Like "water damage" or "vandalism"?""
- D10: "The system should provide reports of missing and damaged items per branch."

</details>

<a id="req-130"></a>
#### REQ-130 Batch Item Branch-Location Changes

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow staff users to change the branch location of selected items, including changing multiple items in a batch to effect a transfer.

Both requirements cover moving items to a new branch location by changing their records. The merged capability shall support selected-item and batch branch-location changes for transfers, subject to applicable authorization and transaction-safety controls.

*Priority rationale:* Supported by four source types, seven stakeholders, a 31% survey signal, and an email agreement, but no formal meeting decision makes it important rather than essential.

*Stakeholders:* administrators, cataloging staff, Thomas Wright, maria.rodriguez@dalton-whitman.lib.org, robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org, Staff

<details><summary>Evidence</summary>

- D20: "Change records to move items to new location: 31%"
- D15: "Fourth, we need to change records of selected items to move them to a new location."
- D04: "Ability to change records of selected items to move to new location - Mechanisms: changing location field, generating pull lists"

</details>

<a id="req-131"></a>
#### REQ-131 Batch Item Status Conversion

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D06 (conversations/conv_pines021_item_purging.eml), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall allow staff users to change the status of many items in a single batch operation.

Staff users need to update the status of large groups of items to support weeding and purging workflows. The operation shall support selecting many item records, such as 100 items, and changing them from one status to another. Example conversions include changing items from missing to discard or weed, with a utility supporting the batch operation.

*Priority rationale:* Two independent sources, four stakeholders, and two email agreements describe it as “huge” and explicitly requested, although the evidence is not a formal decision.

*Stakeholders:* Maria Rodriguez, Jennifer Durham, Katherine Gregory, Thomas Wright

<details><summary>Evidence</summary>

- D06: "Like changing 100 items from "missing" to "discard/weed" at once."
- D15: "Sometimes I need to change 100 items from "missing" to "discard/weed" in batch."

</details>

<a id="req-132"></a>
#### REQ-132 Collection Price Value Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a report showing the price value of the collection aggregated by call number or call number range.

The report shall calculate and present the price value of the collection or items. It shall aggregate the price value by call number or call number range. The report shall support the applicable collection scope.

*Priority rationale:* Two source types and four stakeholders support this collection-management report, giving it broader support than a specification-only example despite no formal decision.

*Stakeholders:* staff, finance, PINES IT Department, acquisitions managers

<details><summary>Evidence</summary>

- D10: "Price value of collection by call number or shelving location"
- D14: "Price value of collection by call number (not available)"

</details>

<a id="req-133"></a>
#### REQ-133 Configurable Overdue Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide configurable reports for items overdue by a specified number of days.

Staff users shall be able to specify the number of days by which items are overdue as the reporting threshold. The system shall generate reports for items more than the specified number of days overdue. The reports shall include variants for daily work and shelf reading. A patron contact information variant shall be provided where applicable.

*Priority rationale:* It has six stakeholders and two source types, indicating an important expected reporting need even though no formal decision is recorded.

*Stakeholders:* staff, individual, patron, Staff, PINES IT Department, circulation staff

<details><summary>Evidence</summary>

- D10: "Items more than XX days overdue (Overdue Materials Report)"
- D10: "Items overdue by X days (daily, shelf reading, patron contact info)"
- D10: "CIRCULATION REPORTS: - Items overdue by X days (daily, shelf reading, patron contact info)"

</details>

<a id="req-134"></a>
#### REQ-134 Configurable Purge Candidate Criteria

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D06 (conversations/conv_pines021_item_purging.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall identify purge candidates using configurable item-status and time-based criteria that may be combined with logical operators.

Both requirements specify configurable criteria for selecting records or items for purging. The merged capability shall support item-status and time-based conditions and allow applicable criteria to be combined using logical operators.

*Priority rationale:* Three source types, eight stakeholders, multiple email agreements, and an explicit “should” signal show broad and important support, but no meeting decision makes it nonessential.

*Stakeholders:* Maria Rodriguez, Katherine Gregory, Jennifer Durham, Dana Peeler, Thomas Wright, Latoya Davidson, Catalogers, Administrators

<details><summary>Evidence</summary>

- D06: "The system should provide a utility and reports for identifying item records to purge, based on customizable criteria such as:"
- D06: "- That haven't circulated in 5+ years - Activity-based criteria (last circulated X days/months/years ago)"
- D06: ""The system should let us combine criteria.""

</details>

<a id="req-135"></a>
#### REQ-135 Inventory Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide inventory reports for branches that can be run or accessed daily.

Branch managers and other staff users need regular visibility into inventory. The system shall provide reports focused on branch inventory information. Reports shall support daily operational access or execution.

*Priority rationale:* A meeting source identifies daily branch inventory reporting as an operational need, but the absence of a formal decision and broad evidence prevents Must priority.

*Stakeholders:* LaToya Davidson, Branch managers

<details><summary>Evidence</summary>

- D18: "Inventory and capacity reports are used daily"

</details>

<a id="req-136"></a>
#### REQ-136 Item Use Count Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide reports that show item total use counts and use counts for specified date ranges.

Staff users need to analyze item use for collection management and reporting. The system shall provide total use counts and counts segmented by periods such as fiscal years or months. Reports shall support filtering by an exact total use count or by a specified total-use-count range.

*Priority rationale:* Reference and specification sources plus an explicit use-count request from stakeholders make this an important collection-management capability, though not a formal decision.

*Stakeholders:* PINES IT Department, collection managers, staff

<details><summary>Evidence</summary>

- D14: "List of Items with specific Total Use Count (not available)"
- D10: "Ability to have a total use count on items as well as a use count broken down by usage date range such as an FY use count or monthly use count"

</details>

<a id="req-137"></a>
#### REQ-137 Items Added Date Reporting

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide reports counting or listing items created or added within a selected period or date range.

The requirements describe the same reporting need for newly added items. The system shall report the number of items added during a selected period and shall be able to report items created or added within a specified date range.

*Priority rationale:* Two independent source types and three stakeholders support date-range acquisition reporting, but there is no formal decision or critical signal.

*Stakeholders:* staff, PINES IT Department, acquisitions staff

<details><summary>Evidence</summary>

- D10: "Items Added Count"
- D10: "List of Items by Creation Date Range"
- D14: "List of Items by Creation Date Range (not available)"

</details>

<a id="req-138"></a>
#### REQ-138 Low-Labor Uncataloged Material Processing

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall support batch operations and simple workflows for processing uncataloged material while minimizing the labor required from branch staff users.

Both requirements specify minimizing branch labor for uncataloged-material workflows. The system shall provide simple, efficient, and batch-oriented processing capabilities for uncataloged and other items so branch staff users can complete the work with minimal manual effort.

*Priority rationale:* Interview and specification evidence explicitly requires minimal branch labor, making it important for operations even though no formal decision is recorded.

*Stakeholders:* Staff, Thomas Wright

<details><summary>Evidence</summary>

- D10: "Support needed for: - Minimal branch labor"
- D15: "minimal branch labor (we can't spend a lot of time per item)"

</details>

<a id="req-139"></a>
#### REQ-139 Missing MARC Fields Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a report identifying bibliographic records missing specified MARC fields.

Cataloging staff need to find bibliographic records that lack required descriptive data. Users shall be able to specify the MARC fields or tags to check. The report shall list records missing any of the specified fields.

*Priority rationale:* Reference and specification sources plus four stakeholders support this data-quality report as an important capability, though no formal decision is recorded.

*Stakeholders:* cataloger, staff, PINES IT Department, cataloging staff

<details><summary>Evidence</summary>

- D10: "Bib Records missing specific MARC fields"
- D14: "Bib Records missing specific MARC fields (not available)"

</details>

<a id="req-140"></a>
#### REQ-140 New Acquisitions Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D01 (conversations/conv_pines014_material_volume.eml)

**Statement:** The system shall report the number of new acquisitions for a branch during a specified period or at a specified point in time.

Staff users need to measure newly acquired material by branch. The report shall support acquisition date ranges such as the last 30, 60, or 90 days, as well as a point-in-time view. The report shall count acquisitions for the selected branch and period.

*Priority rationale:* Four stakeholders and an email agreement support new-acquisition reporting as an expected capability, but the agreement is not a formal meeting decision.

*Stakeholders:* Susan Sexton-Cooley, Latoya Davidson, Robert Chen, Katherine Gregory

<details><summary>Evidence</summary>

- D01: "The volume should include: 1. New acquisitions (items recently added)"

</details>

<a id="req-141"></a>
#### REQ-141 Quick Uncataloged Distribution

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall provide a quick-distribution workflow for processing uncataloged material and distributing shipments rapidly.

Branch staff need to distribute uncataloged material to branches or programs without extensive per-item processing. The workflow shall support rapid processing of large shipments. It shall enable quick distribution when material must be handled quickly.

*Priority rationale:* Interview and specification evidence consistently identifies quick distribution as needed to process material rapidly, making it important despite limited breadth.

*Stakeholders:* Staff, Thomas Wright

<details><summary>Evidence</summary>

- D10: "Support needed for: - Quick distribution"
- D15: "The requirements are: quick distribution (we need to process these fast), minimal branch labor (we can't spend a lot of time per item), and ability to identify how the material is being used."

</details>

<a id="req-142"></a>
#### REQ-142 Transfer Reversion to Original Branch

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow selected transferred items to be reverted to their original branch location manually or automatically according to configurable elapsed-time, event, or status rules.

M177 specifies manual reversion of selected items, while M184 specifies configurable automatic or manual transfer reversion. The merged requirement shall support returning transferred items to their original branch location through a manual action or configurable rules based on elapsed time, events, or status changes.

*Priority rationale:* Four source types, eleven stakeholders, an 18% survey signal, and email agreements establish broad support for reversion, but no formal decision makes it nonessential.

*Stakeholders:* administrators, cataloging staff, george.tuttle@piedmontlib.org, thomas.wright@augusta-reed.lib.org, robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org, maria.rodriguez@dalton-whitman.lib.org, Thomas Wright ...

<details><summary>Evidence</summary>

- D20: "Revert items to original location: 18%"
- D04: "Ability to revert items to original location after a set period of time and/or based on other criteria ...Revert after X days (date-based) Revert when item status changes to "returned" (event-based) Revert when item is checked out at the destination (event-based)"
- D04: "Ability to revert items to original location after a set period of time"

</details>

<a id="req-143"></a>
#### REQ-143 Uncataloged Inventory Tracking

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall allow staff users to track uncataloged material as inventory without individual bibliographic records.

Staff users need to inventory and manage material that arrives without complete catalog records. The capability shall support material such as paperback books and children's board books. It shall allow large shipments to be tracked as inventory even when individual bibliographic records do not exist.

*Priority rationale:* Interview and specification evidence explicitly says uncataloged material must be tracked as inventory, making this important despite only three stakeholders.

*Stakeholders:* Thomas Wright, Staff, Administrators

<details><summary>Evidence</summary>

- D15: "We need to be able to track these as inventory even though they're not fully cataloged."
- D10: "Ability to control inventory of uncataloged material, such as paperback books and children's board books."

</details>

<a id="req-144"></a>
#### REQ-144 Weeding Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide a Weeding Report that identifies low-use items using a specified total-use threshold and includes last circulation date and circulation counts.

Collection staff need reports to support collection maintenance and weeding decisions. The report shall identify items whose total use count is below a specified threshold. For each item, it shall include the date of last circulation and the number of circulations, with support for other applicable selection criteria.

*Priority rationale:* Three source types, five stakeholders, and a stated partial availability indicate an important and incompletely supported weeding capability, without a formal decision.

*Stakeholders:* staff, PINES IT Department, collection managers, Susan Sexton-Cooley, Branch managers

<details><summary>Evidence</summary>

- D10: "List of Items with a < Total Use Count [Weeding Report]"
- D10: "Weeding report (date of last circulation and number of circs)"
- D14: "Weeding report with date of last circulation (partially available)"

</details>

<a id="req-145"></a>
#### REQ-145 Batch Status Conversion Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report that identifies items and assists staff users in batch-converting their statuses.

Staff users need a report to identify items eligible for conversion from one status to another. The report shall support selective or batch conversion workflows and shall identify candidate items before the conversion is performed. This reporting capability complements the batch status conversion operation.

*Priority rationale:* It appears only in the early specification, with no corroborating source or decision, so it is a desirable adjunct to batch status conversion.

*Stakeholders:* Catalogers, Staff, staff

<details><summary>Evidence</summary>

- D10: "The system should have a report to assist in the conversion of items from one status to another."
- D10: "Items to be Converted (batch converting items from one status to another)"

</details>

<a id="req-146"></a>
#### REQ-146 Bibliographic Records Added Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a report of bibliographic records added, grouped by staff user and branch.

Staff users need to measure bibliographic record creation by the person and branch responsible for adding the records. The report shall provide counts grouped by staff user and branch. It shall support filtering by a date range.

*Priority rationale:* It has reference and specification support but only three stakeholders and no priority signal or formal decision.

*Stakeholders:* staff, PINES IT Department, cataloging managers

<details><summary>Evidence</summary>

- D10: "Bib Records Added by user by library Count"
- D14: "Bib Records Added by user by library Count (not available)"

</details>

<a id="req-147"></a>
#### REQ-147 Bibliographic Records Count

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report counting bibliographic records.

Staff users need a report showing the number of bibliographic records in the system. The report shall provide the overall bibliographic record count. No additional grouping or filtering behavior is specified.

*Priority rationale:* This report is mentioned only in the specification and has no supporting priority signal or decision.

*Stakeholders:* staff, cataloger

<details><summary>Evidence</summary>

- D10: "Bib Records Count"

</details>

<a id="req-148"></a>
#### REQ-148 Bibliographic Records Edited Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a report counting bibliographic records edited within a selected timeframe.

Staff users need to measure bibliographic record editing activity. The report shall count records edited during a selected timeframe and may group or filter results by staff user and branch. This supports monitoring catalog maintenance activity.

*Priority rationale:* Although supported by a reference and the specification, it has no explicit priority signal or formal decision and only four stakeholders.

*Stakeholders:* staff, cataloger, PINES IT Department, cataloging staff

<details><summary>Evidence</summary>

- D10: "Bib Records Edited Count"
- D14: "Bib Records Edited Count (not available)"

</details>

<a id="req-149"></a>
#### REQ-149 Bibliographic Text Item Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report listing items whose bibliographic record contains a specified string.

Staff users need to locate items based on text contained in the bibliographic record. The report shall accept a specified search string and return matching items. This supports collection analysis and catalog maintenance.

*Priority rationale:* It is a single-specification example with one stakeholder and no supporting priority evidence.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "List of items with XXX in bib record"

</details>

<a id="req-150"></a>
#### REQ-150 Branch Capacity Drill-Down

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall allow staff users to drill down from a consortium-wide capacity overview into individual branch capacity details.

Staff users need to move from an overview of capacity to the details for a selected branch. The branch view shall display detailed capacity metrics and capacity history. The drill-down shall begin from the consortium-wide overview.

*Priority rationale:* It has only one email source and two stakeholders; the email agreement indicates support but is not a formal decision.

*Stakeholders:* chris.sharp@gapubliclib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "Ability to drill down into individual branches"

</details>

<a id="req-151"></a>
#### REQ-151 Branch Capacity Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall provide branch capacity reports that can be accessed or run frequently.

Branch managers and other staff users need recurring visibility into branch capacity. Reports shall include measures such as holdings and shelf capacity. The reports shall support frequent use, including daily operational use where needed.

*Priority rationale:* It is recorded in one meeting source without a formal decision, priority signal, or broad stakeholder support.

*Stakeholders:* LaToya Davidson, Branch managers

<details><summary>Evidence</summary>

- D18: "Inventory and capacity reports are used daily"

</details>

<a id="req-152"></a>
#### REQ-152 Collection Age Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a report showing collection age metrics aggregated by call number, call number range, or shelving location.

Collection staff need to assess the age of holdings within different parts of the collection. The report shall aggregate age measures such as average publication year or age distribution. Results shall be organized by call number ranges or shelving locations.

*Priority rationale:* It is supported by a reference and specification but has only three stakeholders and merely indicates that the capability was “not available.”

*Stakeholders:* staff, PINES IT Department, collection managers

<details><summary>Evidence</summary>

- D10: "Age of collection by call number or shelving location"
- D14: "Age of collection by call number (not available)"

</details>

<a id="req-153"></a>
#### REQ-153 Currently Checked-Out Items

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report of items currently checked out at the time of the report run.

Staff users need to identify items that remain checked out. The report shall list all items whose status is checked out when the report runs. This provides a current operational view rather than a historical count.

*Priority rationale:* It is mentioned only in the specification with no priority signal, decision, or broad supporting evidence.

*Stakeholders:* staff, patron

<details><summary>Evidence</summary>

- D10: "Items Currently Checked Out"

</details>

<a id="req-154"></a>
#### REQ-154 Deleted Items Count

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report counting items deleted within a selected date range.

Staff users need to measure item deletions over time. Users shall select a date range for the report. The report shall return the count of items deleted during that range.

*Priority rationale:* This is a specification-only report with one stakeholder and no explicit priority evidence.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "Items Deleted Count"

</details>

<a id="req-155"></a>
#### REQ-155 Deleted Last Copy Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report listing items that were deleted as the last copy owned by the consortium.

Catalogers need to identify items deleted when they were the last copy owned by the consortium. The report shall support updating external services such as WorldCat after those deletions. It is distinct from a report identifying currently held last copies.

*Priority rationale:* The WorldCat-related use case is supported by one specification source and a single example request, without a decision or broader confirmation.

*Stakeholders:* staff, library system

<details><summary>Evidence</summary>

- D10: "Last Copy Report (last copy owned by a library system that was deleted)"

</details>

<a id="req-156"></a>
#### REQ-156 Deleted Last-Item Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report of deleted items that were the last item in a branch or facility.

Staff users need to identify deletions that removed the last remaining item associated with a facility. The report shall list deleted items meeting that condition. The results support updates to external systems.

*Priority rationale:* It has only one specification source and a limited supporting example, with no formal decision or broad stakeholder evidence.

*Stakeholders:* staff, library system

<details><summary>Evidence</summary>

- D10: "Ability to run a report on deleted items that were the last copy in the facility"

</details>

<a id="req-157"></a>
#### REQ-157 Fines-Stopped Item Reporting

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide reports listing items grouped or filtered by fines-stopped reason.

Both requirements describe reporting items according to the reason that fines were stopped. The report shall support listing, grouping, or filtering items by fines-stopped reason.

*Priority rationale:* Although present in both a reference and specification, it has only three stakeholders and no explicit priority or decision.

*Stakeholders:* staff, PINES IT Department, billing staff

<details><summary>Evidence</summary>

- D10: "List of Items by Fines Stopped Reason"
- D14: "List of Items by Fines Stopped Reason (not available)"

</details>

<a id="req-158"></a>
#### REQ-158 High-Use Items Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report listing items whose total use count exceeds a specified threshold.

Staff users need to identify heavily used items for collection management analysis. Users shall specify a threshold for total use count. The report shall list items exceeding that threshold and support total use count data.

*Priority rationale:* It is a single-specification example supported by one stakeholder and lacks a formal decision or stronger priority signal.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "List of Items with a > Total Use Count"

</details>

<a id="req-159"></a>
#### REQ-159 Item Circulation Date

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D20 (survey_results_2009.txt)

**Statement:** The system shall include the last circulation date on item reports.

Staff users need the last circulation date when analyzing items and making collection decisions. Item reports shall be able to display the date on which each item last circulated. This information supports collection analysis, including weeding and inventory review.

*Priority rationale:* It is supported only by one survey stakeholder and has no stated priority signal or formal decision.

*Stakeholders:* library staff

<details><summary>Evidence</summary>

- D20: ""Ability to indicate last circulation date on item reports""

</details>

<a id="req-160"></a>
#### REQ-160 Items Count Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report summarizing the total number of items.

Staff users need to obtain an overall count of items in the system. The report shall support a system-wide total and may aggregate counts according to selected criteria. No specific criteria are prescribed.

*Priority rationale:* The total-items report appears only in the specification and has one stakeholder with no priority signal.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "Items Count"

</details>

<a id="req-161"></a>
#### REQ-161 Items Edited Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a report counting items edited within a selected timeframe.

Staff users need to measure item record editing activity. The report shall count items edited during a chosen timeframe and may group or filter results by staff user and branch. This supports monitoring inventory maintenance activity.

*Priority rationale:* It has reference and specification support but only two stakeholders and no explicit priority or decision.

*Stakeholders:* PINES IT Department, staff

<details><summary>Evidence</summary>

- D14: "Items Edited Count (not available)"
- D10: "Items Edited Count"

</details>

<a id="req-162"></a>
#### REQ-162 Long-Overdue Item Reporting

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide reports listing items designated or marked by the system as Long Overdue.

Both requirements identify the same class of items for reporting: items whose status is Long Overdue or that have been marked long overdue by the system. The merged requirement shall list those items in a report.

*Priority rationale:* This is a specification-only example with one stakeholder and no supporting priority evidence.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "List of Long Overdue"
- D10: "Items marked longoverdue by system"

</details>

<a id="req-163"></a>
#### REQ-163 Manual and Scheduled Purge and Cleanup

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D06 (conversations/conv_pines021_item_purging.eml)

**Statement:** The system shall support manual and scheduled execution of purge and cleanup operations, including configuring specified execution times and frequencies for the purge utility.

The scheduled purge utility requirement is contained within the broader manual-and-scheduled cleanup requirement. Staff users shall be able to run purge and cleanup operations manually or schedule them automatically at specified times and frequencies.

*Priority rationale:* It is supported by only one email source and two stakeholders, with no priority signal or formal decision.

*Stakeholders:* Latoya Davidson, Robert Chen

<details><summary>Evidence</summary>

- D06: "can the purging utility be scheduled? Like, run automatically at the end of each year?"
- D06: ""Should it be automated or manual?""

</details>

<a id="req-164"></a>
#### REQ-164 Missing Damaged Title Frequencies

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D05 (conversations/conv_pines019_020_missing_intransit.eml)

**Statement:** The system shall provide title-level aggregation and frequency counts of missing and damaged items.

Staff users need to identify titles that are repeatedly lost or damaged. The system shall aggregate missing and damaged item occurrences at the title level and show frequency counts. This supports decisions about changing the number of items or relocating titles.

*Priority rationale:* The title-frequency idea appears in one email from one stakeholder and has no formal decision or broader support.

*Stakeholders:* George Tuttle

<details><summary>Evidence</summary>

- D05: ""if we keep losing the same titles, maybe we need different copies or to move them to a different location""

</details>

### 6.7 Transfers and transit management

*7 requirements - Must: 0, Should: 6, Could: 1, Won't: 0*

<a id="req-165"></a>
#### REQ-165 Item Transfer Utility

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall provide a utility for transferring batches of items between branches, mobile units, outreach collections, and other supported destinations.

Staff users shall be able to use the utility to move batches of items for purposes such as mobile library service, outreach collections, and just-in-time warehouses. The utility shall support transfer mechanisms including changing item location fields and generating pull lists. It shall support transfers between branches, mobile units, and outreach program collections.

*Priority rationale:* It is explicitly marked “Should,” described as crucial, and supported by an interview and the specification across three stakeholders.

*Stakeholders:* Staff, Administrators, Thomas Wright

<details><summary>Evidence</summary>

- D10: "System should provide a utility for transferring batches of items between branches."
- D15: "The item transfer utility is crucial for us. We often need to move batches of items between branches - for example, sending books to a mobile library unit or to an outreach program collection."
- D10: "The utility should include: - Mechanisms for moving items: changing location field, generating pull lists"

</details>

<a id="req-166"></a>
#### REQ-166 Overdue In-Transit Detection Threshold

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D05 (conversations/conv_pines019_020_missing_intransit.eml)

**Statement:** The system shall allow staff users to configure the number of days used to identify an item as overdue in transit and shall apply that threshold when the item has a null arrival date and its departure date exceeds the threshold.

Both requirements define the configurable rule for detecting overdue in-transit items. The system shall support a configurable day threshold, defaulting to seven days when no other value is configured, and shall identify an item as overdue in transit when its arrival date is a null value and its departure date is older than the threshold.

*Priority rationale:* The email records stakeholder agreement that the threshold be configurable, with four stakeholders supporting an important overdue-transit control, although no meeting decision makes it Must.

*Stakeholders:* Dana Peeler, Susan Sexton-Cooley, Katherine Gregory, Robert Chen

<details><summary>Evidence</summary>

- D05: ""System generates a list of items in-transit for more than X days (X configurable)""
- D05: ""I need to see what's been in-transit for more than X days (X should be configurable, probably 7 days default).""
- D05: ""For in-transit items, we need to check the transit table for items where the arrival date is null and the departure date is more than X days ago.""

</details>

<a id="req-167"></a>
#### REQ-167 Printable Transfer Pull Lists

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall generate printable pull lists of items selected for transfer.

Staff users shall be able to print a list of items that need to be located and moved. The pull list shall support the physical preparation of a transfer batch. It shall be usable with items selected through the transfer utility.

*Priority rationale:* An email agreement identifies printable pull lists as a required transfer mechanism, supported by three stakeholders, but the evidence is not a formal meeting decision.

*Stakeholders:* maria.rodriguez@dalton-whitman.lib.org, robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "Mechanisms: changing location field, generating pull lists"

</details>

<a id="req-168"></a>
#### REQ-168 Query Transfer Candidates

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt)

**Statement:** The system shall allow staff users to query for candidate materials to include in a transfer batch using flexible selection criteria.

Queries shall support identifying candidate items using criteria such as branch location, collection or section, circulation history, and other metadata. A supported example is finding items in a children's section that have not circulated in six months. The query results shall provide candidate materials for review and selection for transfer.

*Priority rationale:* Candidate querying is identified as a desired utility mechanism and appears in both an interview and the specification, indicating expected functionality despite only two stakeholders.

*Stakeholders:* Thomas Wright, Staff

<details><summary>Evidence</summary>

- D15: "First, we need to query for candidate materials. Maybe we want all items in the children's section that haven't circulated in 6 months."
- D10: "The utility should include: - Ability to query for candidate materials"

</details>

<a id="req-169"></a>
#### REQ-169 Sort In-Transit by Due Date

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D05 (conversations/conv_pines019_020_missing_intransit.eml)

**Statement:** The system shall allow staff users to sort the in-transit report by due date.

The in-transit report shall provide due-date sorting for front-line staff users. This shall help them identify and follow up on the oldest outstanding in-transit items first. Sorting shall apply to the merged in-transit report.

*Priority rationale:* Sorting by due date was agreed in an email, supported by two stakeholders, and justified by frontline staff needing to chase the oldest items first, but it lacks a formal meeting decision.

*Stakeholders:* Susan Sexton-Cooley, Front-line staff

<details><summary>Evidence</summary>

- D05: ""For the in-transit report - can we sort by due date? Front-line staff need to chase the oldest items first.""

</details>

<a id="req-170"></a>
#### REQ-170 Undo Transfer Operation

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall provide an undo function to reverse a transfer operation performed in error.

Staff users shall be able to reverse a mistakenly applied transfer. The undo function shall restore the transfer to its prior state or otherwise reverse its operational effect. The exact scope, such as a single batch or a defined time window, remains to be determined during design.

*Priority rationale:* An email agreement includes undo in the consolidated transfer requirements and two stakeholders support it, making it important error recovery without evidence of a mandatory decision.

*Stakeholders:* susansexton-cooley@saraboblib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "And we need an undo function! What if someone clicks the wrong button?"

</details>

<a id="req-171"></a>
#### REQ-171 Printable Transit Labels

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall generate printable transit labels with barcodes for items being transferred.

Staff users shall be able to print labels for items involved in physical transfers. Labels shall include barcodes to support scanning during transit and receipt. The labels are intended to assist physical transport between branches or other destinations.

*Priority rationale:* Printable barcode labels have support from only one email and two stakeholders, with no explicit priority signal or agreement, so they are a useful enhancement rather than essential functionality.

*Stakeholders:* george.tuttle@piedmontlib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "Also, can we generate transit labels? Like, printable barcodes for the items being transferred?"

</details>

### 6.8 Patron and demographic reporting

*13 requirements - Must: 1, Should: 5, Could: 7, Won't: 0*

<a id="req-172"></a>
#### REQ-172 Provide Demographic Analysis Reports

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D17 (meeting_minutes/meeting_2009-03-15_minutes.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide patron demographic analysis reports, including aggregated statistics by age range and geographic region, to support program, service, and collection planning.

Reports shall support demographic analysis of patron data and related transactions for planning programs and services. Results shall include aggregated statistics by age range and geographic fields such as county and zip code, with anonymized aggregates where applicable. The reporting capability shall also support analysis of patron interests and provide patron reports that include demographic and inactive-account information.

*Priority rationale:* The requirement was formally agreed in meeting minutes, is supported by four sources and seven stakeholders, and was accepted as part of scope despite the survey indicating 52% and a 'should' signal.

*Stakeholders:* Susan Sexton-Cooley, Program planners, Staff, Administrators, Library Managers, Library Directors, library staff

<details><summary>Evidence</summary>

- D18: "Demographic analysis for program planning"
- D10: "The system should produce useful demographic statistics, including transactions by geographical regions, age ranges, etc."
- D17: "Analyzing demographics and interests of patrons"

</details>

<a id="req-173"></a>
#### REQ-173 Calculate Configurable Age Brackets

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D08 (conversations/conv_pines023_patron_characteristics.eml)

**Statement:** The system shall calculate a patron's age from birth_date at query time and allow configurable age brackets for filtering and grouping reports.

The system shall derive current patron age from the birth_date field rather than requiring stored age ranges. Staff users or report authors shall be able to define custom age brackets, such as 0-5, 6-10, and 11-15, and save them for report use. Reports and queries shall support filtering and grouping patrons by these configured age brackets.

*Priority rationale:* Configurable age calculation is supported by two stakeholder agreements in one email source and three stakeholders, making it important but not a formal meeting decision.

*Stakeholders:* Robert Chen, Katherine Gregory, Susan Sexton-Cooley

<details><summary>Evidence</summary>

- D08: "The "age range" is calculated from the birth_date field, which means we need to compute it at query time."
- D08: "The age ranges need to be configurable too. Like, 0-5, 6-10, 11-15, etc. Or 0-6, 7-12, 13-17, 18-24, 25-34... Whatever makes sense for the report."

</details>

<a id="req-174"></a>
#### REQ-174 Provide Patron Count Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide patron count reports that can be aggregated by demographic, geographic, profile, home branch, and survey-answer categories.

The reports shall provide total patron counts and counts grouped by age demographic, county, city, zip code, home branch, profile group, and selected survey answers. Geographic aggregation shall support individual fields and combinations of county, city, and zip code, and age groups shall be definable for counting patrons. Staff users shall be able to filter the overall patron count and select a survey when counting patrons by survey answer.

*Priority rationale:* Patron count aggregation is supported by two source types and five stakeholders, making it broadly useful, although there is no formal meeting decision and the 'not available' signal suggests a current gap rather than a mandate.

*Stakeholders:* staff, patron, PINES IT Department, library planners, planning staff

<details><summary>Evidence</summary>

- D10: "Patron Count"
- D10: "Patron Count by Age Demographic"
- D10: "Patron Count by County"

</details>

<a id="req-175"></a>
#### REQ-175 Report Patron Behavior Statistics

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall produce patron behavior statistics, including return-time, renewal-likelihood, and branch-renewal metrics.

The system shall provide statistics that help staff users understand and predict patron behavior and use of materials. Metrics shall include the average time taken to return a specified book or title, the likelihood that a specified book or title will be renewed, and the percentage of check-outs at a branch that are renewals. These metrics shall support analysis of return timeliness, renewal behavior, and material use.

*Priority rationale:* Patron behavior statistics are supported by both the specification and survey and carry an explicit 'should' signal, though they lack a formal meeting decision.

*Stakeholders:* Staff, Administrators, library staff

<details><summary>Evidence</summary>

- D10: "The system should produce statistics that can be used to understand and predict patron behavior and use of materials."
- D10: "For example: - How quickly is a particular book returned, on average?"
- D10: "For example: - How likely is a particular book to be renewed?"

</details>

<a id="req-176"></a>
#### REQ-176 Report Patron Inactivity

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml), D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall generate reports identifying patrons with no circulation or electronic activity during a configurable number of days.

The report shall identify patrons whose last recorded circulation or electronic activity is older than the configured inactivity threshold. The threshold shall accept any number of days and provide common presets of 30, 90, 180, and 365 days. Electronic activity shall include OPAC or patron-account logins, online hold placements, online renewals, and access to digital collections when the relevant integration and logging exist. Staff users shall be able to scope the report by the consortium, branch, county, or similar grouping.

*Priority rationale:* Inactivity reporting has eight stakeholders, support across email and specification sources, multiple recorded email agreements, and explicit demand for configurable activity definitions, but no formal meeting decision.

*Stakeholders:* Maria Rodriguez, pines-reports-working-group, Katherine Gregory, Susan Sexton-Cooley, Robert Chen, Dana Peeler, Staff, Administrators

<details><summary>Evidence</summary>

- D09: "We need a report that shows patrons with no circulation or electronic activity in the last X days."
- D09: "X should be configurable - we usually use 365 days but it would be nice to adjust."
- D09: ""Electronic activity" should include: 1. Logging into OPAC/patron account 2. Placing holds online 3. Renewing items online 4. Accessing digital collections (if integrated)"

</details>

<a id="req-177"></a>
#### REQ-177 Use Patron Table Demographics

**Priority:** Should &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D08 (conversations/conv_pines023_patron_characteristics.eml)

**Statement:** The system shall use the existing patron table as the authoritative data source for patron demographic fields in reports.

Reports shall read age or birth_date, zip code, county, home branch, patron type, and preferred language from the existing patron table. Using this authoritative source shall keep demographic filtering, grouping, and analysis aligned with the patron data maintained by the ILS.

*Priority rationale:* Using the existing patron table is a technically confirmed data-source constraint with an email agreement and verified field availability, making it important for consistent reporting even without a formal meeting decision.

*Stakeholders:* Robert Chen, Katherine Gregory

<details><summary>Evidence</summary>

- D08: "All the fields mentioned (age range, zip code, county, home branch, patron type, preferred language) exist in the patron table."

</details>

<a id="req-178"></a>
#### REQ-178 List Patrons by Survey Answer

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report listing patrons by selected survey answer.

Staff users shall be able to select a survey by name and identify patron records associated with each selected answer. The report shall not require staff users to enter an internal survey ID when selecting the survey. Results shall list the matching patrons rather than only providing aggregate counts.

*Priority rationale:* This appears only as an example in the early specification with one stakeholder and no formal decision or broader supporting evidence.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "List of patrons by survey answer"

</details>

<a id="req-179"></a>
#### REQ-179 Monthly Patron Addition Reporting

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall report patrons added during selected months, including monthly totals and, where required, breakdowns by demographic category.

The requirements describe monthly reporting of new patron additions. The system shall report patron additions grouped by month and shall support a report for patrons added during the previous month with results broken down by demographic category.

*Priority rationale:* Monthly patron additions are mentioned only in the early specification with no priority signal, agreement, or corroborating source.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "New Patron Count (patrons added the previous month by Demographic Category)"
- D10: "Patron Added Count by Month"

</details>

<a id="req-180"></a>
#### REQ-180 Report Barred Patrons

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report listing patrons whose account status is BARRED.

Staff users shall be able to generate a report of patrons with the BARRED account status. The report shall identify the patrons currently subject to that status for operational review.

*Priority rationale:* Barred-patron reporting appears only in the early specification with one stakeholder and no priority signal or corroborating evidence.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "List of patrons who are BARRED"

</details>

<a id="req-181"></a>
#### REQ-181 Report Inactive Status Patrons

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a report listing patrons with inactive status.

Staff users shall be able to generate a report based on the patron status field to identify patrons whose accounts are inactive. The report shall support filtering by patron status and include contact and account metadata. This status-based report is distinct from the report identifying patrons with no activity during a configurable period.

*Priority rationale:* Inactive-status reporting has limited support from a reference and specification and three stakeholders, with no formal decision and a 'not available' signal.

*Stakeholders:* staff, PINES IT Department, circulation staff

<details><summary>Evidence</summary>

- D10: "List of Patrons with inactive status"
- D14: "List of Patrons with inactive status (not available)"

</details>

<a id="req-182"></a>
#### REQ-182 Report Patrons by Expiration

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report listing patrons by account expiration date or date range.

Staff users shall be able to specify expiration dates or date ranges and generate a report of patrons whose accounts expire within the selected period. The report shall support operational planning for account renewal and follow-up.

*Priority rationale:* Expiration-date reporting is listed only in the early specification for one stakeholder, without a priority signal, agreement, or additional source support.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "List of Patrons by Expiration Date"

</details>

<a id="req-183"></a>
#### REQ-183 Report Patrons by Notes

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report listing patrons whose notes contain specified wording.

Staff users shall be able to enter or select text to search patron notes. The report shall list patron records whose notes contain the specified wording.

*Priority rationale:* Searching patron notes is an isolated early-specification example with one stakeholder and no corroboration or priority signal.

*Stakeholders:* staff

<details><summary>Evidence</summary>

- D10: "List of Patrons with specific wording in notes"

</details>

<a id="req-184"></a>
#### REQ-184 Report Voter Survey Responses

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide reports of voter survey responses, including weekly totals and weekly counts by county.

Staff users shall be able to generate a report counting voter registration survey responses by week. The reporting capability shall also provide weekly voter survey response counts broken down by county. It shall support voter-related survey responses stored in patron records or related structures.

*Priority rationale:* Voter survey response reporting is supported only by a reference and specification with four stakeholders and a 'not available' signal, but lacks survey, interview, or meeting confirmation.

*Stakeholders:* staff, community, PINES IT Department, library administration

<details><summary>Evidence</summary>

- D10: "Voter Survey Responses County by Week"
- D10: "Voter Reg Survey Responses Count by Week"
- D14: "Voter Survey Responses (not available)"

</details>

### 6.9 Financial reporting and accounts

*16 requirements - Must: 2, Should: 9, Could: 5, Won't: 0*

<a id="req-185"></a>
#### REQ-185 Accounting Audit Compliance

**Priority:** Must &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall ensure that reports, archived data, and financial record-keeping comply with standard accounting practices and applicable state, county, and municipal auditing requirements.

Both requirements impose the same accounting and governmental audit-compliance obligation. The merged requirement covers reports, archived data, and related financial records, including compliance with applicable standard accounting practices and state, county, and municipal auditing requirements.

*Priority rationale:* Accounting and audit compliance is a legal/policy constraint, and the requirement is explicitly marked “must,” so it is essential despite the agreement being recorded only in email.

*Stakeholders:* Auditors, Administrators, Legal / Compliance, LaToya Davidson, Katherine Gregory, finance.committee@gapl.org

<details><summary>Evidence</summary>

- D10: "All reports and data archiving must comply with standard accounting practice and state, county, and municipal auditing requirements."
- D11: "All reports and data archiving must comply with standard accounting practice and state, county, and municipal auditing requirements."

</details>

<a id="req-186"></a>
#### REQ-186 Financial Reporting Verification

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide financial reports and verification features for tracking and verifying financial transactions, including reports suitable for director-level use.

Staff users and directors need financial reporting capabilities covering areas such as fines and payments. The system shall support tracking and verification of financial transactions to support financial management and auditing. Reports shall be appropriate for director-level review and decision-making.

*Priority rationale:* Financial Reporting Verification was formally agreed in meeting minutes as included in the accepted scope, making it a Must despite the survey support being 34%.

*Stakeholders:* LaToya Davidson, Library directors, library staff, Library Managers, Local System Administrators, Library Directors

<details><summary>Evidence</summary>

- D18: "Financial report needs are understood at the director level"
- D20: "Financial reports (fines, payments): 34%"
- D17: "Tracking and verifying financial transactions"

</details>

<a id="req-187"></a>
#### REQ-187 Aged Debt Reporting

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide an Aged Debt report with detailed aging and patron-level debt information.

The report shall summarize outstanding debt using granular aging buckets, including 30-, 60-, and 90-plus-day categories. It shall provide debt details per patron. Where supported, it shall also provide historical snapshots of aged debt. The enhancement addresses limitations in the currently available report.

*Priority rationale:* Aged Debt Reporting is supported by two sources and four stakeholders, with an explicit signal that the existing capability “needs enhancement,” making it important but not formally mandatory.

*Stakeholders:* finance, staff, PINES IT Department, billing staff

<details><summary>Evidence</summary>

- D10: "Aged Debt"
- D14: "Aged Debt detailed report (partially available, needs enhancement)"

</details>

<a id="req-188"></a>
#### REQ-188 Balance Threshold Query

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall allow staff users to query patron accounts whose balances exceed a configurable monetary threshold.

Staff users shall be able to specify the threshold amount used to identify patron accounts requiring attention. The query shall return accounts with balances greater than that amount. The threshold is configurable rather than fixed to a particular dollar value.

*Priority rationale:* The requirement is supported by two sources and four stakeholders and has an email agreement, but its “For example” signal indicates it is not a formal Must decision.

*Stakeholders:* Susan Sexton-Cooley, Dana Peeler, LaToya Davidson, Staff

<details><summary>Evidence</summary>

- D11: "For fines and charges, the staff should be able to query patron accounts with balances greater than X dollars."
- D10: "As an example, a staff user can easily query patron accounts with balances greater than X dollars."

</details>

<a id="req-189"></a>
#### REQ-189 Branch Payment and Waiver Tracking

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall track and provide reports of payments collected and fines waived by branch.

Both requirements cover branch-level financial activity involving payments. The merged capability shall track and allow staff users to view payments collected at each branch, together with fines waived and related payment activity by branch.

*Priority rationale:* Branch Payment and Waiver Tracking has support from two sources and five stakeholders, an email agreement, and an explicit “should” signal.

*Stakeholders:* Dana Peeler, LaToya Davidson, Katherine Gregory, Administrators, Staff

<details><summary>Evidence</summary>

- D11: "Payments tracking by library is important for our end-of-month reports. Each branch needs to be able to see what payments were collected at their location."
- D10: "System tracks fines waived and payments made per library."

</details>

<a id="req-190"></a>
#### REQ-190 Financial Transaction Associations

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall record fines, charges, waivers, and ecommerce transactions and associate them with applicable patron and item records for financial reporting.

Financial transactions must be recorded against patron records and item records when applicable. The transaction types include fines, charges, waivers, and ecommerce transactions. Using a common association model allows these transactions to be included in financial reports and related account analysis.

*Priority rationale:* Financial Transaction Associations is supported by two sources and four stakeholders, has an email agreement, and is explicitly signaled as “should,” but lacks a formal meeting decision.

*Stakeholders:* Staff, Administrators, Katherine Gregory, LaToya Davidson

<details><summary>Evidence</summary>

- D10: "Fines, charges, waivers, and ecommerce transactions are attached to patron and item records."
- D11: "Fines, charges, waivers, and ecommerce transactions are attached to patron and item records."

</details>

<a id="req-191"></a>
#### REQ-191 Fines Charges Accrual Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall provide reports of fines and charges accrued by selectable time period and charge type.

Reports shall support predefined periods including the last 12 months, year-to-date, and last month. They shall also support custom date ranges where applicable. Results shall be broken down by charge type, such as overdue fines, damaged item charges, and lost item charges. This supports analysis of accrued financial obligations over time and by category.

*Priority rationale:* Fines Charges Accrual Reports has two-source support, five stakeholders, and two email agreements, making it important though not formally mandated.

*Stakeholders:* Staff, Administrators, LaToya Davidson, Katherine Gregory, finance.committee@gapl.org

<details><summary>Evidence</summary>

- D10: "The system provides financial reports including: - fines and charges accrued per time period (e.g., last twelve months, YTD, last month) and per type of charge (overdue fines, damaged item charges, lost item charges, etc.)"
- D11: "Fines and charges accrued per time period (last 12 months, YTD, last month)"
- D11: "Fines and charges accrued per time period ... and per type of charge (overdue fines, damaged item charges, lost item charges, etc.)"

</details>

<a id="req-192"></a>
#### REQ-192 Fines Waived Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall provide reports of fines waived by selectable time period and branch.

The reports shall attribute waived fines to individual branches. They shall support selection of the reporting time period. Branch-level attribution supports budgeting and review because each branch has its own budget for waived fines.

*Priority rationale:* Fines Waived Reports is supported by two sources and five stakeholders and has an email agreement, warranting Should rather than Must because no meeting decision or legal constraint is recorded.

*Stakeholders:* Administrators, Staff, Susan Sexton-Cooley, Katherine Gregory, finance.committee@gapl.org

<details><summary>Evidence</summary>

- D10: "The system provides financial reports including: - fines waived per time period and per branch"
- D11: "Fines waived per time period and per branch"

</details>

<a id="req-193"></a>
#### REQ-193 Item Value Report

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall generate a report of item values for the entire collection or a selected subset.

The report shall calculate value using data in item records, such as purchase price. Staff users shall be able to report on the entire collection or select a subset. Example subsets include items with a longoverdue status and DVDs in the children's collection. This supports valuation of specific portions of the collection as well as the collection overall.

*Priority rationale:* Item Value Report has two-source support, six stakeholders, and an email agreement, making it an important expected capability without a formal Must decision.

*Stakeholders:* Staff, Administrators, Twin Lakes finance department, LaToya Davidson, Katherine Gregory, pines-reports-working-group@gapl.org

<details><summary>Evidence</summary>

- D10: "The system can generate a report of the value of items (based on data in item record) in the entire collection or a portion."
- D11: "Value of items report - staff should be able to get the value of items based on data in item records. This could be the entire collection, or a portion."

</details>

<a id="req-194"></a>
#### REQ-194 Patron Balance Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall provide reports of patron account balances grouped by patron, branch location, and the consortium.

Reports shall support balances for an individual patron, aggregation by the patron's branch location, and aggregation across the consortium. These views allow staff users to review account balances at detailed and organizational levels. The reports support financial oversight and account management.

*Priority rationale:* Patron Balance Reports is supported by two sources and five stakeholders and has an email agreement, indicating broad importance but not a formal mandatory decision.

*Stakeholders:* Staff, Administrators, LaToya Davidson, Katherine Gregory, finance.committee@gapl.org

<details><summary>Evidence</summary>

- D10: "The system provides financial reports including: - patron account balances by patron, home library, and system"
- D11: "Patron account balances by patron, home library, and system"

</details>

<a id="req-195"></a>
#### REQ-195 Payments Time Method Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall provide reports of payments made by selectable time period, payment method, point of service, and branch.

Reports shall support predefined or selected reporting periods and breakdowns by payment method. They shall also identify the point of service, such as a staff desk, self-check station, or OPAC. Payment methods may include cash, credit card, and check. Branch-level breakdowns shall support reconciliation.

*Priority rationale:* Payments Time Method Reports has the broadest support among the detailed reports—two sources, six stakeholders, and an email agreement—but no formal meeting decision or mandatory constraint.

*Stakeholders:* Administrators, Staff, LaToya Davidson, Susan Sexton-Cooley, Dana Peeler, Katherine Gregory

<details><summary>Evidence</summary>

- D10: "The system provides financial reports including: - payments made per time period and per payment method (e.g., staff desk, self-check station, OPAC)"
- D11: "Payments made per time period and per payment method (staff desk, self-check, OPAC)"

</details>

<a id="req-196"></a>
#### REQ-196 Bills Owed Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a report of bills currently owed by patrons.

The report shall summarize outstanding bills or fees for each patron. It shall also provide totals to support review of currently owed amounts. This report addresses current outstanding obligations rather than historical billing states.

*Priority rationale:* Bills Owed Report appears only in the early specification, with no priority signal or formal decision, so it is a desirable but weakly supported feature.

*Stakeholders:* staff, patron, finance

<details><summary>Evidence</summary>

- D10: "Bills currently Owed by Patrons"

</details>

<a id="req-197"></a>
#### REQ-197 Detailed Payment Reporting

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide detailed reports of payments received, including forgiveness, work, and goods payments.

The detailed payments requirement encompasses reporting on the specified special payment types. The system shall report payments received with sufficient detail and shall include forgiveness, work, and goods payments in the reported payment information.

*Priority rationale:* Detailed Payment Reporting is mentioned only in the specification, has no priority signal or decision, and has support from just two stakeholders.

*Stakeholders:* finance, staff

<details><summary>Evidence</summary>

- D10: "Detailed Forgive, Work, and Goods Payments Received"
- D10: "Detailed Payments Received"

</details>

<a id="req-198"></a>
#### REQ-198 Detailed Voids Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall provide a detailed report of voided bill and payment transactions.

The report shall list voided bill and payment transactions. It shall include the reasons for voiding and the staff user information associated with each void. This supports review and verification of changes to financial transactions.

*Priority rationale:* Detailed Voids Report is supported only by the specification and two stakeholders, without a priority signal or formal decision.

*Stakeholders:* finance, staff

<details><summary>Evidence</summary>

- D10: "Detailed Voids"

</details>

<a id="req-199"></a>
#### REQ-199 Easy Financial Updates

**Priority:** Could &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall allow staff users to update financial information easily.

Staff users need straightforward workflows for editing and updating financial data. The update process should be easy to understand and operate. This requirement concerns usability of financial-data maintenance rather than the content of financial reports.

*Priority rationale:* Easy Financial Updates is a single-source usability request from one stakeholder, and the wording “easily” provides no evidence of a higher priority.

*Stakeholders:* Staff

<details><summary>Evidence</summary>

- D10: "Financial information can be updated easily."

</details>

<a id="req-200"></a>
#### REQ-200 Historical Snapshot Bills

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide a Snapshot Bills report that shows billing states as of specified past dates.

Staff users shall be able to query historical billing snapshots going back in time. The report shall reconstruct the state of bills for specified past dates. This supports historical reporting and review of prior billing conditions.

*Priority rationale:* Historical Snapshot Bills has reference and survey support and identifies a capability gap, but only three stakeholders and no formal decision support a Could priority.

*Stakeholders:* PINES IT Department, billing staff, library staff

<details><summary>Evidence</summary>

- D14: "Snapshot bills report going back in time - does not exist"
- D20: ""Need a snapshot bills report going back in time""

</details>

### 6.10 Data governance, audit, and retention

*17 requirements - Must: 5, Should: 5, Could: 7, Won't: 0*

<a id="req-201"></a>
#### REQ-201 Anonymize Demographic Statistics

**Priority:** Must &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide demographic statistics using anonymized data that contains no personally identifiable information about patrons.

The system shall remove information that could identify a patron before producing demographic statistics. The resulting statistics must contain no personally identifiable information. This protects patron privacy while preserving the ability to perform demographic analysis.

*Priority rationale:* The requirement is explicitly marked "must" and protects personally identifiable patron information, making it a privacy-critical constraint despite support from only two sources.

*Stakeholders:* Legal / Compliance, Administrators, library staff

<details><summary>Evidence</summary>

- D10: "The data used to produce these statistics must be anonymized - information that could be used to identify a patron is deleted."
- D20: "Demographic statistics (must be anonymized - no personally identifiable info)"

</details>

<a id="req-202"></a>
#### REQ-202 Financial Retention Enforcement

**Priority:** Must &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D11 (email_financial_reports.eml)

**Statement:** The system shall enforce applicable data retention policies, including retaining specified financial and audit data for seven years where required.

Retention enforcement shall follow applicable state and local auditing requirements. Where those requirements specify a seven-year period, the system shall retain the relevant financial and audit data for that period. The requirement applies to data covered by those legal or regulatory obligations.

*Priority rationale:* The requirement enforces applicable retention policies, including a seven-year legal retention period, and has an agreed decision even though it is documented in an email.

*Stakeholders:* George Tuttle, LaToya Davidson, Katherine Gregory

<details><summary>Evidence</summary>

- D11: "Some data needs to be retained for 7 years for audit purposes. The system needs to enforce retention policies."

</details>

<a id="req-203"></a>
#### REQ-203 Include Null and Blank Records

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D08 (conversations/conv_pines023_patron_characteristics.eml), D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall allow staff users to request that records containing null values or blank fields be included in report results and represented explicitly.

Reports shall not silently exclude records because a field contains a null value or is blank. Staff users shall be able to request inclusion of these records regardless of what is being filtered or displayed. Report results shall represent null values and blank fields explicitly and distinguish those values appropriately to prevent misleading results.

*Priority rationale:* The requirement is explicitly marked "must" and was formally agreed in meeting minutes, with support from five source types and concern about incomplete reporting of null and blank data.

*Stakeholders:* library staff, staff, data, Robert Chen, Dana Peeler, Katherine Gregory, PINES IT Department, report consumers

<details><summary>Evidence</summary>

- D20: ""All nulls and blank fields must be included in results""
- D10: "All nulls and blank fields must be included in the results no matter what is being filtered or displayed"
- D19: ""All nulls and blank fields must be included in the results," Robert noted."

</details>

<a id="req-204"></a>
#### REQ-204 Payment Reconciliation Ledger

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D11 (email_financial_reports.eml)

**Statement:** The system shall maintain a ledger of patron payments that records the charges to which each payment was applied and supports tracing each payment to its originating charge.

The ledger shall support financial reconciliation and auditability of patron payments. It shall record the payment, amount, date, applied charge or charges, and supporting identifiers needed to trace the payment to its origin. Staff users shall be able to determine which charges each payment settled.

*Priority rationale:* The requirement is explicitly marked "CRITICAL" and multiple participants agreed it was critical for payment reconciliation.

*Stakeholders:* George Tuttle, finance.committee@gapl.org, pines-reports-working-group@gapl.org, Auditors, Administrators

<details><summary>Evidence</summary>

- D11: "The financial audit trail is CRITICAL for our finance department. They need to be able to trace every payment back to the specific charge it was applied to."
- D10: "The system maintains a ledger of patron payments, including which charges payments are applied to, to facilitate reconciliation."

</details>

<a id="req-205"></a>
#### REQ-205 Privacy-Protected Transaction Archive

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml)

**Statement:** The system shall archive transaction data for the legally required period while protecting patron privacy and preserving useful anonymized demographic statistics.

The transaction archive shall comply with applicable State Law retention and privacy requirements. Personally identifiable information shall be removed or avoided as required while retaining transaction information useful for compliance and demographic reporting. The archive shall preserve the required data for the legally specified period.

*Priority rationale:* The requirement is needed for legally required transaction archiving and privacy protection, with evidence explicitly stating compliance and State Law obligations.

*Stakeholders:* admins, legal/compliance, directors, Administrators, Legal / Compliance

<details><summary>Evidence</summary>

- D12: "Transactions archived protecting patron privacy per State Law, while providing useful demographic statistics. State law requires us to retain transaction data for X years, but patron privacy means we can't keep personally identifiable information."
- D10: "Transactions should be archived in a form that protects patron privacy as defined by State Law, while providing useful demographic statistics."

</details>

<a id="req-206"></a>
#### REQ-206 Deletion Audit Logging

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D06 (conversations/conv_pines021_item_purging.eml), D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall maintain an append-only audit log of purge and deletion operations, recording the affected record, responsible staff user, timestamp, branch location, and operation details, independently of the deleted record.

Deletion and purge actions must remain auditable after the primary record is removed. Each deletion audit entry shall identify the record type and record ID, the staff user who performed the action, the deletion timestamp, the relevant branch location, the records affected, and the operation performed. Database triggers shall capture deletion events in an audit table so that the audit entry cannot be lost with the deleted record. Deletion audit records shall be retained permanently or for a configurable retention period.

*Priority rationale:* Deletion auditing has four agreed email conclusions, five stakeholders, and explicit concerns that deletions currently leave no record, but the agreements are not formal meeting decisions.

*Stakeholders:* Robert Chen, George Tuttle, Katherine Gregory, Dana Peeler, Maria Rodriguez

<details><summary>Evidence</summary>

- D07: "Fields: record_type, record_id, deleted_by, deleted_at, location"
- D06: "Audit trail for all purges"
- D07: "To implement this, we'd need: 1. A trigger in the database that logs deletions to an audit table"

</details>

<a id="req-207"></a>
#### REQ-207 Deletion Compliance Reports

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall provide deletion reports suitable for compliance and retention audits, including deletion counts and dates for specified dates or date ranges.

Staff users and auditors need evidence that records are handled according to retention schedules. Reports shall show how many records were deleted and when, including results for selected dates or date ranges. The reports shall support external compliance reviews.

*Priority rationale:* An email agreement and two stakeholders identify deletion reports as important for compliance audits, but the requirement has support from only one source document.

*Stakeholders:* Latoya Davidson, Katherine Gregory

<details><summary>Evidence</summary>

- D07: "Some libraries need to prove they're handling data according to retention schedules. Being able to show "we deleted 500 patron records on X date" is important for audits."

</details>

<a id="req-208"></a>
#### REQ-208 Deletion Counts Tracking

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml), D10 (early_draft_srs_galecia.txt), D15 (interview_cataloging_2009-05-08.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall count and track record deletions by branch location and for the consortium, including the reason for each deletion.

The system shall track deletions of records such as item records and patron records. Staff users shall be able to obtain deletion counts scoped to a branch location and to the consortium as a whole. The tracking shall support audit and reporting activities and include the reason associated with each deletion.

*Priority rationale:* Deletion tracking is supported by four source types, twelve stakeholders, an email agreement, and audit/accountability statements, although the survey signal is only 27% rather than a mandatory decision.

*Stakeholders:* Maria Rodriguez, George Tuttle, Katherine Gregory, Robert Chen, Dana Peeler, Susan Sexton-Cooley, Latoya Davidson, administrators ...

*Note:* Conflict with M208 (contradiction): M207 requires a reason for each deletion, while M208 describes capturing a deletion reason or pre-deletion status as optional. Resolution: Keep M207: it is an agreed, consolidated requirement supported by D07, D10, D15, and D20. M208 is based only on D07 and makes the capture optional, so it is superseded by the stronger agreed requirement.

<details><summary>Evidence</summary>

- D07: "Quick question: Is there a way to track when records are deleted? We need to be able to count and track record deletions (item records, patron records) per location and per system. This is for auditing purposes."
- D20: "Count and track record deletions: 27%"
- D10: "Ability to count and track record deletions (e.g., item records, patron records) per location and per system."

</details>

<a id="req-209"></a>
#### REQ-209 Destructive Operation Safeguards

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D06 (conversations/conv_pines021_item_purging.eml)

**Statement:** The system shall safeguard destructive operations by presenting purge candidates in read-only reports and requiring a separate confirmation step before deletion.

Purge candidate reports shall be non-destructive and separate from the operation that performs deletion. Before any actual deletion or other destructive operation, the system shall require an explicit confirmation step. These safeguards shall reduce the risk of accidentally deleting an entire collection and shall work with deletion audit logging.

*Priority rationale:* Three email agreements and three stakeholders support read-only candidates and confirmation as important safeguards against accidental destructive operations, though no formal meeting decision is recorded.

*Stakeholders:* Robert Chen, Katherine Gregory, Dana Peeler

<details><summary>Evidence</summary>

- D06: "A separate confirmation step for actual deletions"
- D06: "Reports show candidates for purging (read-only)"
- D06: ""we don't want someone accidentally deleting their entire collection.""

</details>

<a id="req-210"></a>
#### REQ-210 Transaction Retention Aggregates

**Priority:** Should &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall retain detailed transaction history for a configurable number of days and retain monthly and annual transaction aggregates indefinitely.

The retention period for detailed transaction history shall be configurable to support differing organizational policies. Monthly and annual aggregates shall remain available indefinitely. This requirement applies to transaction history and its summarized forms.

*Priority rationale:* Configurable detailed retention and indefinite aggregate retention are supported by both the specification and survey, making them important governance needs despite no formal decision.

*Stakeholders:* PINES Reports Working Group, administrators, Administrators, Auditors

<details><summary>Evidence</summary>

- D20: "Transaction history maintained for X days (configurable), with monthly and annual aggregates retained indefinitely."
- D10: "Transaction history is maintained for X days (X is configurable). Monthly and annual aggregate information is maintained indefinitely."

</details>

<a id="req-211"></a>
#### REQ-211 Denied Deletion Attempt Logging

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D07 (conversations/conv_pines022_deletions.eml)

**Statement:** The system shall log denied deletion attempts, including the staff user, timestamp, branch location, targeted record, and denial result.

Attempts to delete records without authorization must remain available for compliance review and troubleshooting. Each denied attempt shall identify who attempted it, when and from which branch location, and which record was targeted. The log shall indicate that the deletion was denied.

*Priority rationale:* Denied-attempt logging has one email source and two stakeholders, with an agreement describing it as helpful for compliance and troubleshooting rather than essential.

*Stakeholders:* Latoya Davidson, Katherine Gregory

<details><summary>Evidence</summary>

- D07: "Can we also track attempted deletions that were denied? That would tell us if someone is trying to delete things they shouldn't."

</details>

<a id="req-212"></a>
#### REQ-212 Report Run Audit History

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall maintain a queryable and exportable history of report runs, including the staff user, parameters, timestamps, status, and delivery destinations.

The history shall record who ran or scheduled each report run and the parameters used. It shall also record start and end timestamps, execution status, and delivery destinations. Staff users and compliance reviewers shall be able to query and export this history for operational and audit purposes.

*Priority rationale:* Report-run history is supported only by one reference document and two stakeholders, with no priority signal or decision evidence.

*Stakeholders:* PINES IT Department, auditors

<details><summary>Evidence</summary>

- D14: "No query queue visibility (staff can't see where their report is in queue)"

</details>

<a id="req-213"></a>
#### REQ-213 Report Template Integrity

**Priority:** Could &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall prevent report template modifications that would compromise the accuracy or integrity of report results.

Report templates shall be protected from changes that could produce misleading or invalid results. For example, a template shall not be alterable in a way that causes deleted items to appear as valid current data. This protects the reliability of reports generated from shared report templates.

*Priority rationale:* Template integrity appears only in the early specification with two stakeholders and no decision or priority signal, so it is a desirable quality improvement rather than an established essential.

*Stakeholders:* System administrators, Library Managers

<details><summary>Evidence</summary>

- D10: "Changes to templates should not compromise the accuracy of results... they should not be able to alter the template to display deleted items."

</details>

<a id="req-214"></a>
#### REQ-214 Staff Login Audit Logging

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D13 (email_staff_login.eml)

**Statement:** The system shall record login events and associate each event with the individual staff user for audit purposes.

Login audit records shall identify the staff user associated with each login and the time of the event. This supports accountability and investigation of shared-password or unattended-terminal incidents. The requirement applies to staff user authentication events.

*Priority rationale:* Login audit logging has only one email source, two stakeholders, and no explicit priority or decision evidence.

*Stakeholders:* Susan Sexton-Cooley, Dana Peeler

<details><summary>Evidence</summary>

- D13: "The system must track WHICH staff member is logged in for audit purposes."

</details>

<a id="req-215"></a>
#### REQ-215 Transfer History Display

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall record and display item transfer history, including transfer counts and timestamps.

Staff users shall be able to review the transfer history of an item. The history shall show how many times the item was transferred and when those transfers occurred. This supports identification of problematic items and misplaced items, including analysis over a selected period such as the past year.

*Priority rationale:* Transfer history display is mentioned in one email for three stakeholders without a priority signal or recorded decision.

*Stakeholders:* latoya.davidson@twinlakeslib.org, robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "Can we track transfer history? Like, "this item has been transferred 5 times in the past year.""

</details>

<a id="req-216"></a>
#### REQ-216 Transfer Operation Audit Log

**Priority:** Could &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall log all item transfer operations for audit purposes, including who initiated each transfer, which items were moved, and when.

Transfer operations must be recorded to support auditing and troubleshooting. Each log entry shall identify the initiating staff user, the items involved, and the time of the transfer. The requirement applies to all transfer operations.

*Priority rationale:* Transfer audit logging has one stakeholder and one email source with no priority signal or decision, so it is a limited-scope improvement.

*Stakeholders:* robert.chen@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "Logging - track all transfers for audit purposes."

</details>

<a id="req-217"></a>
#### REQ-217 Unique Excel Export Rows

**Priority:** Could &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D20 (survey_results_2009.txt)

**Statement:** The system shall ensure that exported Excel data contains no duplicate rows.

Excel exports shall not contain unintended duplicate rows. The system shall de-duplicate or correctly aggregate exported data as necessary to preserve accurate results. This supports reliable downstream analysis of report data.

*Priority rationale:* Duplicate-free Excel exports are supported only by one survey stakeholder and have no explicit priority or decision evidence.

*Stakeholders:* library staff

<details><summary>Evidence</summary>

- D20: ""I need to export to Excel but the data has too many duplicate rows""

</details>

### 6.11 Security and access control

*11 requirements - Must: 4, Should: 6, Could: 1, Won't: 0*

<a id="req-218"></a>
#### REQ-218 Local System Configuration

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt)

**Statement:** The system shall allow authorized local system administrators to configure the system locally.

Local system administrators need to perform configuration related to local reporting and management processes. The system shall provide this capability according to the permissions associated with the local system administrator role. Local configuration access shall be distinguished from unrestricted global administration.

*Priority rationale:* Local system configuration was explicitly agreed in meeting C550 as part of the Local System Administrator role, providing a formal decision and essential administrative capability.

*Stakeholders:* Local System Administrators

<details><summary>Evidence</summary>

- D17: "Local System Administrators: Management staff who oversee Library processes. They configure the system locally."

</details>

<a id="req-219"></a>
#### REQ-219 Predefined Staff Role Support

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D16 (interview_sysadmin_2009-05-10.txt), D17 (meeting_minutes/meeting_2009-03-15_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall support predefined staff roles with role-appropriate access levels for patron, staff, local administrative, management, and global administrative responsibilities.

The system shall provide predefined roles for Patron, Staff, Local System Administrator or Local Admin, Library Manager or Library Administrator, Library Director where applicable, and Global System Administrator or Global Admin. Patrons shall have indirect public access through OPAC displays, while Staff shall perform basic circulation functions and run reports within assigned permissions. Local Admins shall have branch-level reporting and configuration capabilities, and Library Managers shall run approved reports with limited report template modification. Global Admins shall have full system access, while the identified Library Administrator and Library Director roles shall be supported where applicable.

*Priority rationale:* Predefined role-based access was accepted in two meeting decisions and an interview agreement, with 12 stakeholders across four sources, making it a core access-control requirement.

*Stakeholders:* Robert Chen, PINES IT Department, Branch managers, IT staff, Katherine Gregory, Patron, Staff, Local System Administrators ...

<details><summary>Evidence</summary>

- D16: "We have different levels of access: - Patron (public access through OPAC) - Staff (basic circulation functions) - Local Admin (branch manager - can run reports, configure local settings) - Global Admin (IT staff - full system access)"
- D19: "Key points: - Global Admin: Full system access - Local Admin: Branch-level reporting and configuration - Library Manager: Run approved reports, limited template modification - Staff: Run reports within assigned permissions - Patron: Indirect access through OPAC displays"
- D17: "The group discussed the different types of users who would interact with Management Processes: Patron... Staff... Local System Administrators... Library Managers... Library Directors... Global System Administrator"

</details>

<a id="req-220"></a>
#### REQ-220 Role and Permission Administration

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D13 (email_staff_login.eml), D16 (interview_sysadmin_2009-05-10.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall provide an easy administration interface for creating and managing staff roles, security groups, and permissions, with permission changes taking effect when a staff user's role assignment changes.

Authorized administrators need to create, edit, and delete security groups and staff roles and manage their associated permissions. A staff user's permissions shall update automatically when the user's role assignment changes, without requiring individual permission edits. The administration workflow shall be straightforward and shall support managing report-related permissions. This requirement covers both the underlying management capability and the usability of the administrative interface.

*Priority rationale:* Role and permission administration was agreed in meeting C599 and supported by four additional source documents, and it is necessary to operate and maintain the agreed security model.

*Stakeholders:* Susan Sexton-Cooley, Katherine Gregory, System administrators, Local System Administrators, George Tuttle, Robert Chen, admins, managers ...

<details><summary>Evidence</summary>

- D13: "Administrators should be able to create and manage these groups."
- D10: "All permissions should be easy to administer."
- D13: "The system should make it easy to administer these roles - changing someone's permissions should be a simple matter of changing their role assignment, not modifying individual permissions."

</details>

<a id="req-221"></a>
#### REQ-221 Role-Based Permission Assignment

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D13 (email_staff_login.eml), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall determine and control a staff user's permissions through the staff role assigned to that individual, including when the staff user logs in or the role assignment changes.

Both requirements require permissions to be based on assigned staff roles. The merged capability shall assign permissions through staff roles and apply the resulting authorization to the individual staff user at login and when the role assignment changes, while supporting assignment to individuals, workgroups, or arbitrary staff groups as applicable.

*Priority rationale:* Role-based permission assignment has multiple formal meeting agreements, 13 stakeholders, and explicit signals of '[* High Priority]' and 'essential'.

*Stakeholders:* George Tuttle, Katherine Gregory, Robert Chen, PINES IT Department, Local Admins, Local System Administrators, Global System Administrator, Susan Sexton-Cooley ...

<details><summary>Evidence</summary>

- D13: "Access control for individuals, workgroups, and arbitrary staff groups."
- D16: "The permission system needs to be controlled through security groups and/or "roles." This allows access control for individuals, workgroups, and arbitrary staff groups."
- D10: "CO-4: User rights and privileges will be controlled through security groups and or "roles" that allow access control for individuals, workgroups, and arbitrary staff groups. [* High Priority]"

</details>

<a id="req-222"></a>
#### REQ-222 Fine-Grained Report Permissions

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall provide fine-grained permissions for creating, editing, cloning, running, scheduling, sharing, and otherwise managing reports and report templates.

Separate permissions shall govern the report and report-template actions available to staff users. These permissions shall control who can create, edit, and clone reports and report templates. Separate permissions shall also control who can run, schedule, share, and otherwise manage reports and report templates. This fine-grained control shall allow the consortium to limit staff users to the reporting actions authorized for them.

*Priority rationale:* Supported by four source documents, 10 stakeholders, and a 76% survey result, making fine-grained report permissions important and broadly expected but not formally decided as mandatory.

*Stakeholders:* staff, administrators, library staff, System administrators, Local System Administrators, admins, managers, directors ...

<details><summary>Evidence</summary>

- D10: "Ability to add more canned reports via permission level"
- D20: "Fine-grained permissions (who can create/run what): 76%"
- D10: "The system should provide distinct, fine-grained permission levels that limit who can create and clone reports."

</details>

<a id="req-223"></a>
#### REQ-223 Item Transfer Authorization

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall restrict item transfer capabilities to authorized staff roles.

Item transfers shall not be available to every staff user. The system shall authorize transfer functions based on assigned permissions or staff roles. Appropriate authorized roles may include managers, administrators, or transfer coordinators, as configured by the organization.

*Priority rationale:* Restricting item transfers to authorized roles is supported by two stakeholders and an email agreement, but the agreement is not a formal meeting decision and comes from only one source.

*Stakeholders:* susansexton-cooley@saraboblib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "We need to be careful about permissions here. Not every staff member should be able to transfer items between branches. This should be limited to certain roles (managers, administrators, transfer coordinators)."

</details>

<a id="req-224"></a>
#### REQ-224 Session Security Controls

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D13 (email_staff_login.eml)

**Statement:** The system shall provide session management features that reduce security risks from shared passwords and unattended terminals.

The system needs controls for staff terminals that may be left logged in or used with shared passwords. Session management may include automatic logout or quick re-authentication to reduce unauthorized use. The controls shall help ensure that access remains associated with the appropriate authenticated staff user. The specific session behavior shall be configurable or otherwise suitable for public service environments, as supported by the system.

*Priority rationale:* Session controls address security risks from shared passwords and unattended terminals, but the requirement is supported by only one email and has no explicit mandatory or formal decision signal.

*Stakeholders:* Dana Peeler

<details><summary>Evidence</summary>

- D13: "It leads to security issues - staff get in a hurry and sometimes share passwords or leave terminals logged in."

</details>

<a id="req-225"></a>
#### REQ-225 Shared Report Folders

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D12 (email_report_features.eml), D20 (survey_results_2009.txt)

**Statement:** The system shall allow authorized administrators to create shared report folders that control which staff users can run specific reports or sets of ad hoc reports.

Shared report folders shall provide an additional mechanism for granting or denying execution access to reports. Administrators need to organize reports into shared folders and allow or disallow staff users from running specific reports. Folder access shall also support managing access to sets of ad hoc reports. This complements role-based permissions with report-level or folder-level control.

*Priority rationale:* Shared report folders are supported by three source documents, seven stakeholders, and a stated administrative access-control need, although no formal decision makes them mandatory.

*Stakeholders:* System administrators, Staff, admins, staff, directors, administrators, library staff

<details><summary>Evidence</summary>

- D10: "System administrators should be able to create shared folders to allow or disallow staff from running specific reports..."
- D12: "Admins can create shared folders to allow or disallow staff from running specific reports, and/or to run ad hoc reports on specific sets of data."
- D20: "Shared folders to allow/disallow staff from running specific reports."

</details>

<a id="req-226"></a>
#### REQ-226 Staff Identity Authentication

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D13 (email_staff_login.eml), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall support streamlined staff login methods such as card-swipe authentication while associating each session with the individual staff user.

Staff users need a convenient login method for staff terminals, including card-swipe or RFID badge authentication. A streamlined login shall identify and authenticate the individual staff user rather than bypassing individual accountability. The identified staff user shall be available for authorization decisions and audit purposes. Card-swipe login is intended to improve service speed and security at staff terminals.

*Priority rationale:* Individual staff identification is supported by three sources and an email agreement, with the explicit signal that the system 'must track WHICH staff member,' but the card-swipe method itself is not formally mandated.

*Stakeholders:* Susan Sexton-Cooley, Dana Peeler, Branch staff, Staff, Katherine Gregory

<details><summary>Evidence</summary>

- D13: "Even with card swipe, we need individual authentication. The system must track WHICH staff member is logged in for audit purposes. The card is just a convenient way to identify the person, but it shouldn't bypass individual authentication entirely."
- D18: "Staff login needs (card swipe) - already discussed via email"
- D10: "The system should support streamlined methods of logging into terminals. For example, a staff member could swipe a card (like an RFID employee badge) to log in..."

</details>

<a id="req-227"></a>
#### REQ-227 Username Password Fallback

**Priority:** Should &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D13 (email_staff_login.eml)

**Statement:** The system shall support individual username and password login as an alternative to card-based staff authentication.

Card-based login shall not be mandatory for staff users. Staff users who do not have an identification card or who cannot use card-swipe authentication shall be able to authenticate with individual credentials. Username and password login shall remain available as a fallback method. The fallback shall identify the individual staff user for authorization and accountability.

*Priority rationale:* Username/password fallback is supported by the specification and an email agreement, making it an important alternative authentication method, though the evidence does not establish it as a formal must.

*Stakeholders:* Staff, Local System Administrators, Dana Peeler, Katherine Gregory

<details><summary>Evidence</summary>

- D10: "The system should not REQUIRE card-based login - traditional username/password should also be available as a fallback."
- D13: "However, we also need to support the traditional username/password method - not all staff may have ID cards, and we need a fallback."
- D10: "...or alternatively use individual login credentials (username and password)."

</details>

<a id="req-228"></a>
#### REQ-228 Staff Password Change Report

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a report of staff accounts that includes the date of the last password change.

Authorized staff need a report of staff accounts for security auditing. Each account entry shall include the timestamp or date of its most recent password change. The report shall support review of account-maintenance practices and password recency. Access to the report shall be governed by the system's authorization controls.

*Priority rationale:* The password-change report appears only in one reference source with the signal 'not available,' so it is a useful security-reporting enhancement but lacks breadth or a decision.

*Stakeholders:* PINES IT Department, system administrators

<details><summary>Evidence</summary>

- D14: "Staff Accounts with date of last password change (not available)"

</details>

### 6.12 Integration and data architecture

*13 requirements - Must: 7, Should: 2, Could: 3, Won't: 1*

<a id="req-229"></a>
#### REQ-229 Centralized Multi-Branch Operation

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall consolidate management processes and data at a central location while accepting input from and providing services to multiple branches.

The system shall operate across multiple branches through centralized data and services. The centralized data and services shall serve as the single source of truth for consortium-wide management and reporting. The system shall support management processes and report runs across the participating branches.

*Priority rationale:* Two meeting records formally agree on centralized multi-branch operation, and seven stakeholders support consolidating data and services across branches.

*Stakeholders:* Katherine Gregory, Technical Subcommittee, Library Administrators, Global System Administrator, Local System Administrators, Working Group, Network administrators

<details><summary>Evidence</summary>

- D19: "AS-2: Management Processes are consolidated at a central location, and accept input and provide services to multiple locations."
- D10: "The Management Processes are consolidated at a central location and accept input from and provide services to multiple library locations."
- D18: "Management Processes are consolidated at a central location, and accept input and provide services to multiple locations."

</details>

<a id="req-230"></a>
#### REQ-230 OPAC Feature Independence

**Priority:** Must &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall not constrain the functionality or features of the OPAC.

Management-process and reporting requirements must remain separate from the public-facing OPAC. Changes or integrations provided by the system must not limit OPAC functionality or affect patron access. This constraint preserves the OPAC’s independent feature set.

*Priority rationale:* The requirement is explicitly marked high priority and was formally agreed in a meeting as a system constraint protecting OPAC independence.

*Stakeholders:* OPAC team, Local System Administrators, Working Group, OPAC stakeholders

<details><summary>Evidence</summary>

- D10: "CO-5: These requirements must not constrain functionality or features of the Online Public Access Catalog (OPAC) module. [* High Priority]"
- D18: "These requirements shall not constrain functionality or features of the Online Public Access Catalog (OPAC) module."

</details>

<a id="req-231"></a>
#### REQ-231 PostgreSQL 8.3 Compatibility

**Priority:** Must &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D16 (interview_sysadmin_2009-05-10.txt)

**Statement:** The system shall be compatible with and operate against the existing PostgreSQL 8.3 database.

The system must work with the existing PostgreSQL 8.3 installation. It must support the SQL features used by the current ILS environment. The implementation must not require replacing PostgreSQL with a different database engine.

*Priority rationale:* Compatibility with the existing PostgreSQL 8.3 database is a hard technical constraint, despite the agreement being recorded only in an interview.

*Stakeholders:* Robert Chen, PINES IT Department

<details><summary>Evidence</summary>

- D16: "It runs PostgreSQL 8.3 for the database."

</details>

<a id="req-232"></a>
#### REQ-232 Read-Only ILS Integration

**Priority:** Must &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall rely on and read data from the ILS, including its Acquisitions and Cataloging modules, without managing or modifying their data.

The system operates as part of an enterprise-level ILS and depends on its data structures and functionality for reporting data. The relevant modules include Acquisitions and Cataloging. The system must query this data without managing or modifying acquisitions or cataloging data.

*Priority rationale:* Two meeting records formally agree that the system must read ILS data without modifying it, and six stakeholders support this integration dependency.

*Stakeholders:* Acquisitions, Cataloging, Global System Administrator, Robert Chen, Working Group, ILS maintainers

<details><summary>Evidence</summary>

- D10: "DE-1: Management Processes rely on the data structures and functionality of an enterprise-level Library Automation System, including Acquisitions and Cataloging modules."
- D10: "The Management Processes are consolidated at a central location and accept input from and provide services to multiple library locations. They rely on the data structures and functionality of the broader ILS, including Acquisitions and Cataloging modules."
- D19: ""All our data comes from the ILS," Robert said. "The reporting system doesn't manage acquisitions or cataloging - it just reads the data.""

</details>

<a id="req-233"></a>
#### REQ-233 Read-Only OPAC Integration

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall query patron-created data in the OPAC, including holds and circulation transactions, without modifying OPAC data.

The system must interact with the patron interface, or OPAC, to access data generated through patron activity. Reports and related functions must be able to query holds and circulation transactions created in the OPAC. The integration is read-only and must not change OPAC data.

*Priority rationale:* Two meeting records formally agree that reports must access OPAC-generated data without modifying it, with support from six stakeholders.

*Stakeholders:* OPAC, Patron, Working Group, OPAC users, Circulation staff, Robert Chen

<details><summary>Evidence</summary>

- D10: "DE-3: Management Processes interact with a patron interface, also known as an Online Public Access Catalog (OPAC)."
- D18: "Management Processes interact with a patron interface, also known as an Online Public Access Catalog (OPAC)."
- D19: ""The reporting system queries this data, but doesn't modify it.""

</details>

<a id="req-234"></a>
#### REQ-234 Relational Reporting Backend

**Priority:** Must &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall use a fully relational database back-end and support reporting against the existing normalized relational schema, including complex joins, without requiring denormalized reporting copies.

The reporting capability must operate with a fully relational database structure. Queries must support complex joins across normalized tables and should avoid maintaining separate denormalized copies that require frequent synchronization with the live database. This approach is intended to preserve consistency with the source data and work with the existing relational architecture.

*Priority rationale:* The relational backend is marked high priority and explicitly as a must, with formal meeting decisions and interview support for reporting against the existing schema.

*Stakeholders:* Global System Administrator, Developers, George Tuttle, IT staff, Robert Chen, PINES Technical Subcommittee, PINES IT Department

<details><summary>Evidence</summary>

- D10: "CO-1: The system must use a fully relational database back-end. [* High Priority]"
- D19: "Robert confirmed that the system must use a fully relational database back-end."
- D16: "The reporting system needs to work with the relational structure, not fight against it... Some systems try to use denormalized reporting schemas, but that creates sync issues."

</details>

<a id="req-235"></a>
#### REQ-235 Vendor Data Interfaces

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall interface with vendor websites through published APIs and/or automated transfers of standard-format data files such as USMARC21 and EDIFACT.

The system must exchange data with external vendor websites using published APIs or automated file transfers. Supported standard formats include USMARC21 and EDIFACT. The integration must not assume that vendor data is available at every branch.

*Priority rationale:* Two meeting records formally agree that vendor interfaces are a dependency, and six stakeholders support integration through APIs or standard-format file transfers.

*Stakeholders:* Acquisitions, Developers, Vendor systems, Robert Chen, Working Group, Libraries using external vendors

<details><summary>Evidence</summary>

- D10: "DE-2: Management Processes interface with a variety of vendor websites, via published APIs and/or automated transfer of standard-format data files (e.g., USMARC21, EDIFACT)."
- D19: "DE-2: Management Processes interface with a variety of vendor websites, via published APIs and/or automated transfer of standard-format data files (e.g., USMARC21, EDIFACT)."

</details>

<a id="req-236"></a>
#### REQ-236 Combined Financial Data

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D11 (email_financial_reports.eml)

**Statement:** The system shall support joining financial data attached to patron records and items when generating financial reports.

Financial reports must combine financial information that may be stored on patron records and item records. Supported data may include fines, charges, waivers, and e-commerce transactions. The joins must allow these sources to be reported together where relevant.

*Priority rationale:* Three stakeholders support combining financial data, but the requirement appears in only one email and has no formal meeting decision.

*Stakeholders:* Susan Sexton-Cooley, LaToya Davidson, Katherine Gregory

<details><summary>Evidence</summary>

- D11: "The financial data is attached to patron records AND item records. So when we query for financial reports, we need to be able to join these data sources."

</details>

<a id="req-237"></a>
#### REQ-237 Documented Technical Constraints

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall document and respect technical constraints, including supported server operating systems and browser versions, in its technical architecture documentation.

The technical architecture documentation must identify the supported server operating systems and browser versions. System design and implementation must respect these documented constraints. This provides IT staff with clear compatibility and deployment expectations.

*Priority rationale:* A meeting record raises the need to document and respect technical constraints, making this important for implementation governance, but there is no recorded formal decision.

*Stakeholders:* George Tuttle, IT staff

<details><summary>Evidence</summary>

- D18: "Technical constraints (server OS, browser support)"

</details>

<a id="req-238"></a>
#### REQ-238 Reportable Record Types

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall support reporting on bibliographic records, items, patrons, circulation transactions, hold transactions, money records, and staff users or accounts.

Reports must be able to reference the specified record types and their common fields. These fields include information such as titles, barcodes, status, patron type, fines, and staff accounts. The supported record types provide the data foundation for operational and management reporting.

*Priority rationale:* The record types are listed in only one reference document, with no formal decision, priority signal, or broader source support.

*Stakeholders:* PINES IT Department, report authors

<details><summary>Evidence</summary>

- D14: "The following record types are available for reporting: - bibliographic_record ... - item ... - patron ... - action_circulation ... - action_hold ... - money ... - actor"

</details>

<a id="req-239"></a>
#### REQ-239 Reusable Transfer Query Tool

**Priority:** Could &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall reuse the existing report query tool where feasible as the query builder for transfers.

The transfer query-builder capability should reuse existing report query tool components when practical. Reuse is intended to reduce duplicate functionality and implementation effort. The constraint applies where the existing tool can support transfer candidate-selection needs.

*Priority rationale:* Reusing the existing transfer query tool is supported by only one email and is qualified by 'where feasible,' indicating a desirable implementation convenience rather than a necessity.

*Stakeholders:* robert.chen@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "Query builder for candidate selection - we can reuse the report query tool for this."

</details>

<a id="req-240"></a>
#### REQ-240 Unified Patron Activity Query

**Priority:** Could &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml)

**Statement:** The system shall combine activity data from transactions, OPAC login events, holds, renewals, and digital access logs into a unified query or view for determining each patron’s most recent activity.

Activity data is stored across multiple source tables and must be combined for reporting and patron analysis. The query or view must support determining the latest activity timestamp for each patron. The required activity sources include transactions, OPAC login events, holds, renewals, and digital access logs.

*Priority rationale:* Only one email identifies the need for a combined query across activity tables, with no formal decision or broader stakeholder evidence.

*Stakeholders:* Robert Chen, Susan Sexton-Cooley

<details><summary>Evidence</summary>

- D09: "These are stored in different tables, so we'd need a combined query."

</details>

<a id="req-241"></a>
#### REQ-241 Separate Reporting Database

**Priority:** Won't &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D14 (evergreen_reference_2009.txt)

**Statement:** The system shall not require a separate reporting database or read-only replica for report execution instead of the production OLTP database.

Reports shall be able to run against the production OLTP database without requiring a separate reporting database or read-only replica. Staff users may optionally run reports against a separate reporting database or read-only replica when available. This allows report execution without mandating a separate environment while supporting optional offloading of heavy reporting queries from operational processing.

*Priority rationale:* The source explicitly states 'No separate reporting database/replica,' indicating that this approach is rejected or deferred for the release.

*Stakeholders:* PINES IT Department, operations

<details><summary>Evidence</summary>

- D14: "No separate reporting database/replica (reports run on production database)"

</details>

### 6.13 Deployment and environments

*8 requirements - Must: 3, Should: 2, Could: 2, Won't: 1*

<a id="req-242"></a>
#### REQ-242 Client Access Options

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall be accessible through a web browser or a Windows-compatible desktop client.

Staff users shall be able to access the system through either a web browser or a Windows-compatible desktop client. Browser access avoids client installation where preferred, while a dedicated client supports environments that require it. Both access methods are needed to accommodate differing branch deployment preferences.

*Priority rationale:* The meeting recorded formal agreement that supporting both browser and Windows desktop access was critical, reinforced by a high-priority signal.

*Stakeholders:* Staff, Patron, Working Group, Library staff

<details><summary>Evidence</summary>

- D10: "OE-3: The system must be accessible through a web browser or a Windows-compatible client. [* High Priority]"
- D18: "Management Processes shall be accessible through a web-browser or a Windows-compatible client. [Discussion: This is critical - some libraries prefer browser-based access (no client install), others prefer the dedicated client for better performance.]"

</details>

<a id="req-243"></a>
#### REQ-243 Environment Separation and Migration

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall provide separate development, training, and production environments that isolate development and training activities from production and support migration of reporting configurations between them.

Developers need a separate development environment for testing new reports and system changes without affecting production. Staff users need a separate training environment for practicing report runs and configurations safely, with no risk to production data. The system shall support export and import of report templates, schedules, permission settings, saved queries, and other reporting configuration between development, training, and production, including migration to production.

*Priority rationale:* Environment isolation and configuration migration have broad support across five documents and nine stakeholders, with multiple meeting agreements and explicit safety concerns.

*Stakeholders:* PINES IT Department, Katherine Gregory, Developers, System administrators, Local System Administrators, Global System Administrator, Robert Chen, Trainers ...

<details><summary>Evidence</summary>

- D14: "No configuration migration between environments"
- D18: "Management Processes shall provide a development and training environment with the ability to migrate configurations to a production environment."
- D10: "CO-3: The system must provide a development and training environment with the ability to migrate configurations to a production environment. [* Medium Priority]"

</details>

<a id="req-244"></a>
#### REQ-244 Supported Server Platforms

**Priority:** Must &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall operate on Linux or Solaris server environments, including Red Hat Enterprise Linux 5 and Solaris 10 on SPARC hardware.

The system shall support deployment on the consortium's existing Linux or Solaris server environments. The detailed target platforms include Red Hat Enterprise Linux 5 and Solaris 10 running on SPARC hardware. This supports both the primary production environment and a secondary disaster-recovery or reporting environment.

*Priority rationale:* Linux and Solaris support are established technical platform constraints with consensus, high-priority evidence, and agreement in both an interview and a meeting.

*Stakeholders:* Robert Chen, PINES IT Department, George Tuttle, IT staff, Working Group, Global System Administrator

<details><summary>Evidence</summary>

- D16: "So any reporting system needs to work on both Linux and Solaris."
- D10: "OE-2: The system must operate on a Linux or Solaris server environment. [* High Priority]"

</details>

<a id="req-245"></a>
#### REQ-245 Browser Compatibility

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall support Microsoft Internet Explorer version 6.0 and later and Mozilla Firefox version 2.0 and later when accessed through a web browser.

Staff users accessing the system through a web browser need support for the specified browser versions. The system interface and outputs shall remain usable in Microsoft Internet Explorer 6.0 and later and Mozilla Firefox 2.0 and later. This accommodates branch computers using different browser standards.

*Priority rationale:* This has support from three source documents and seven stakeholders, with interview and meeting agreement, but is explicitly marked medium priority rather than critical.

*Stakeholders:* Staff, Patron, Working Group, Library IT staff, Robert Chen, PINES IT Department, Branch libraries

<details><summary>Evidence</summary>

- D10: "OE-4: If web-browser based, the system must be accessible through Microsoft Internet Explorer (version 6.0 and later) and Mozilla Firefox (version 2.0 and later). [* Medium Priority]"
- D18: "If web-browser based, Management Processes shall be accessible through Microsoft Internet Explorer (v.6.0 and later) and Mozilla Firefox (v.2.0 and later)."
- D16: "So we need to support IE 6.0+ and Firefox 2.0+."

</details>

<a id="req-246"></a>
#### REQ-246 Enterprise ILS Deployment Context

**Priority:** Should &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall be designed for use as part of an enterprise-level ILS; it may rely on enterprise infrastructure such as redundant servers, backup systems, and network connectivity.

The management and reporting processes are expected to operate as components of an enterprise-level ILS. This deployment context permits reliance on enterprise-grade infrastructure, including redundant servers, backup systems, and network connectivity. The context establishes how the system is expected to be deployed.

*Priority rationale:* The enterprise-level infrastructure assumption was agreed in two meeting records, making it important for deployment design although it is not itself a mandatory user-facing capability.

*Stakeholders:* Robert Chen, Project stakeholders, Working Group, PINES / Evergreen

<details><summary>Evidence</summary>

- D19: "AS-1: Management Processes are part of an enterprise-level Library Automation System."
- D10: "AS-1: Management Processes are part of an enterprise-level Library Automation System."
- D18: "Management Processes are part of an enterprise-level Library Automation System. [Discussion: This means we can rely on the infrastructure being enterprise-grade. Evergreen is that system for PINES.]"

</details>

<a id="req-247"></a>
#### REQ-247 Optional Card-Reader Deployment

**Priority:** Could &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D13 (email_staff_login.eml)

**Statement:** The system shall operate in environments without card-reader hardware and shall not mandate installation of such hardware.

Some branches may not have the infrastructure needed to install card readers. The system shall remain fully operable without card-reader hardware. Card-reader installation therefore shall not be a deployment prerequisite.

*Priority rationale:* Only one email and one stakeholder support avoiding mandatory card-reader hardware, with no formal decision or broader evidence.

*Stakeholders:* Susan Sexton-Cooley

<details><summary>Evidence</summary>

- D13: "Some of our smaller branches may not have the infrastructure for card readers. So the requirement should be: "The system supports (but does not require) streamlined staff login methods.""

</details>

<a id="req-248"></a>
#### REQ-248 Optional Streamlined Login

**Priority:** Could &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D13 (email_staff_login.eml)

**Statement:** The system shall make streamlined staff login methods optional and shall not require their deployment.

The system may support streamlined staff login methods for environments that can use them. Deployment of these methods shall remain optional because some branches may lack the required infrastructure. Staff users must still be able to use the system without deploying a streamlined login method.

*Priority rationale:* An email agreement supports making streamlined login optional, but the requirement has limited source breadth and no meeting decision.

*Stakeholders:* Susan Sexton-Cooley, Katherine Gregory

<details><summary>Evidence</summary>

- D13: "Also - and this is important - the system should not REQUIRE the streamlined login. Some of our smaller branches may not have the infrastructure for card readers."

</details>

<a id="req-249"></a>
#### REQ-249 Patron-Facing Scope Exclusion

**Priority:** Won't &nbsp;|&nbsp; **Type:** constraint &nbsp;|&nbsp; **Sources:** D17 (meeting_minutes/meeting_2009-03-15_minutes.txt)

**Statement:** The system shall not include day-to-day patron-facing functions that are provided by the OPAC and circulation client.

The system is limited to management and reporting processes rather than day-to-day patron-facing operations. Patron-facing functions provided by the OPAC and circulation client are explicitly outside this system's scope. This prevents overlap with those separate components.

*Priority rationale:* The meeting formally agreed that patron-facing functions are excluded from this system's scope, so they are explicitly rejected for this release.

*Stakeholders:* PINES Services Specialist, Working Group

<details><summary>Evidence</summary>

- D17: "She clarified that this does NOT include day-to-day patron-facing functions (those are part of the OPAC and circulation client)."

</details>

### 6.14 Usability, accessibility, and documentation

*8 requirements - Must: 3, Should: 2, Could: 3, Won't: 0*

<a id="req-250"></a>
#### REQ-250 Accessibility Support

**Priority:** Must &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall provide accessible interfaces and outputs that support screen readers, screen magnification, other assistive technologies, and applicable accessibility requirements.

Accessibility shall apply to the reporting interface, report output, web-based components, and the online help system. The system shall support screen-reading software such as JAWS and NVDA and screen-magnification software such as ZoomText, while remaining usable when magnified. Keyboard navigation and compatibility with other assistive technologies shall be supported. The system shall comply with applicable accessibility standards and legal requirements, including Section 508 or WCAG as required by the organization.

*Priority rationale:* This is a Must because two meeting decisions explicitly identify accessibility as a legal, mandatory, non-negotiable requirement for public institutions, supported by five source documents and 12 stakeholders.

*Stakeholders:* PINES IT Department, accessibility officers, staff users with disabilities, Susan Sexton-Cooley, Working Group, Public institution staff, Patron, Staff ...

<details><summary>Evidence</summary>

- D18: "Management Processes shall be accessible with screen-reading software, screen-magnification software, and other software programs designed to increase accessibility. ... Section 508 compliance is mandatory."
- D16: "The system needs to work with: - Screen magnification software like ZoomText"
- D16: "The system needs to work with: - Screen readers like JAWS and NVDA"

</details>

<a id="req-251"></a>
#### REQ-251 Integrated Hierarchical Help

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall provide an online, hierarchical, cross-linked, searchable HTML help system integrated with the reporting interface and covering all system functions.

The help system shall be available within the system so staff users do not need to leave the application to find documentation. It shall describe and illustrate system functions and provide contextual guidance, examples, and links to relevant documentation, including report definitions, fields, and scheduling. The content shall be organized hierarchically, cross-linked, searchable, and easy to navigate. Help content shall be provided in HTML and support the accessibility requirements applicable to the system.

*Priority rationale:* The requirement has five sources, eight stakeholders, and a formal meeting decision describing integrated context-sensitive help as critical, supported by a High Priority signal.

*Stakeholders:* PINES IT Department, staff users, Katherine Gregory, Library staff, Robert Chen, Staff, Local System Administrators, Patron

<details><summary>Evidence</summary>

- D14: "No online help system integrated with reports"
- D19: "The system shall provide an online, hierarchical, and cross-linked help system in HTML."
- D10: "UD-3: The system must provide an online, hierarchical, and cross-linked help system in HTML that describes and illustrates all system functions. [* High Priority]"

</details>

<a id="req-252"></a>
#### REQ-252 Standards-Compliant HTML

**Priority:** Must &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D16 (interview_sysadmin_2009-05-10.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall produce valid, standards-compliant HTML for web-based interfaces, report displays and outputs, and help system pages.

All applicable web output shall conform to relevant HTML standards and validate as standards-compliant HTML. The output shall include semantic HTML structure, appropriate alternative text attributes, and ARIA labels or roles where appropriate. These practices shall support compatibility across browsers and assistive technologies. The requirement applies to the web-based interface, report output, and help system.

*Priority rationale:* Standards-compliant HTML has formal meeting decisions, four source documents, and explicit 'must' and High Priority signals, making it essential for the system.

*Stakeholders:* Robert Chen, Katherine Gregory, Developers, Local System Administrators, PINES IT Department, Accessibility users, George Tuttle, Web developers

<details><summary>Evidence</summary>

- D19: ""We need to make sure all HTML output validates against W3C standards," Robert noted."
- D10: "CO-2: The system must produce standards-compliant HTML output for web-based components. [* High Priority]"
- D16: "The HTML output needs to be properly structured with alt tags, ARIA labels, and proper semantic HTML. And the system needs to produce standards-compliant HTML."

</details>

<a id="req-253"></a>
#### REQ-253 Detailed Error Feedback

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall provide high-level error reporting and low-level query-specific feedback through the front-end interface for authorized staff users.

Error messages shall provide meaningful feedback when reports or queries fail rather than only generic failure notifications. Detailed diagnostics shall identify information such as the affected table, field, and kind of error. The detailed feedback shall be available to Local and Global System Administrators or equivalent staff users with the required permissions.

*Priority rationale:* Detailed error feedback was agreed in two meeting records and appears in three sources, but its explicit Medium Priority signal indicates it is important rather than essential.

*Stakeholders:* Local System Administrators, Global System Administrator, Katherine Gregory, Global System Administrators, Support staff, Robert Chen

<details><summary>Evidence</summary>

- D10: "UD-4: The system must provide thorough high-level error reporting and feedback, and shall allow low-level query-specific feedback for Local and Global System Administrators from the front-end interface. [* Medium Priority]"
- D18: "The system shall provide thorough high-level error reporting and feedback and shall allow low-level query-specific feedback for Local and Global System Administrators from the front-end interface."
- D19: ""When a report fails, we need to know WHY... which table, which field, what kind of error.""

</details>

<a id="req-254"></a>
#### REQ-254 Usable Reporting Interfaces

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D12 (email_report_features.eml), D20 (survey_results_2009.txt)

**Statement:** The system shall provide user-friendly reporting interfaces that make reports easy to find, create, administer, and use.

The reporting interface shall improve navigation and make it easy for staff users to locate needed reports. Query design and report-related workflow information, including visible queueing where applicable, shall reduce confusion and support self-service. Permission administration shall be easy to manage when staff roles or assignments change. The overall design shall minimize support calls and administrative overhead.

*Priority rationale:* Usable reporting interfaces are supported by both an email and a survey and address ease of administration, making them important and expected despite having no formal decision or mandatory signal.

*Stakeholders:* staff, admins, IT/help desk, library staff

<details><summary>Evidence</summary>

- D12: "We need a user-friendly interface for designing queries ... The permissions need to be easy to administer."
- D20: ""The interface is confusing - I can't find the reports I need""

</details>

<a id="req-255"></a>
#### REQ-255 Batch Transfer Preview

**Priority:** Could &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall present a preview and confirmation screen before committing batch transfers.

The preview shall show the number of items affected and the source and destination details. It shall allow the staff user to confirm the operation before any batch transfer is committed. The confirmation should make the consequences of the operation clear, such as indicating how many items will move between named branches.

*Priority rationale:* The preview was agreed in one email involving two stakeholders, but there is no priority signal or formal meeting decision, so it is a desirable safeguard rather than essential for this release.

*Stakeholders:* susansexton-cooley@saraboblib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "The utility should show a preview before making changes. "If you run this now, 25 items will be moved from Dalton-Whitman to Mobile Library Unit 3. Confirm?""

</details>

<a id="req-256"></a>
#### REQ-256 Branch Grouping

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall allow staff users to group branches by consortium or region when displaying many branches.

Grouping shall reduce visual crowding in overviews that include a large number of branches. The grouping capability shall support higher-level organizational or regional units. The requirement is intended to keep displays usable when as many as 286 branches are represented.

*Priority rationale:* Branch grouping is suggested in one email to address possible crowding across 286 locations, but it has no formal decision, priority signal, or broader source support.

*Stakeholders:* robert.chen@gapubliclib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "One consideration: with 286 locations, the overview might get crowded. Maybe we should group by system/region? Or allow filtering?"

</details>

<a id="req-257"></a>
#### REQ-257 Quick-Access Report Guidance

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt)

**Statement:** The system shall provide a quick-access interface with brief descriptions or hover tooltips explaining the purpose of each report and report template.

Staff users shall obtain concise usage guidance directly from the quick-access reporting interface. The interface shall provide a brief description or hover tooltip for each report and report template. Staff users shall be able to hover over a report or report template title to view its description and purpose.

*Priority rationale:* Quick-access descriptions and hover tooltips appear only in a reference and the early specification, with no agreement or priority signal, so they are desirable usability enhancements.

*Stakeholders:* PINES IT Department, staff users, individual, staff

<details><summary>Evidence</summary>

- D14: "No quick access interface with pop-up descriptions"
- D10: "Ability to hover over each title of canned report/template with pop-up box with description"
- D14: "No hover tooltips for report titles"

</details>

### 6.15 Performance, scalability, and reliability

*8 requirements - Must: 2, Should: 3, Could: 3, Won't: 0*

<a id="req-258"></a>
#### REQ-258 Consortium Capacity Support

**Priority:** Must &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D18 (meeting_minutes/meeting_2009-07-20_minutes.txt)

**Statement:** The system shall support a consortium with at least 286 branches, approximately 17 million annual circulations, and purchasing or processing more than 900,000 items per year.

The system shall remain capable of supporting consortium-wide reporting and search workloads at the stated scale. Capacity shall include at least 286 branches, approximately 17 million annual circulations, and purchasing or processing over 900,000 items annually. These figures represent the expected scale of a consortium deployment.

*Priority rationale:* The meeting records a formal agreement that consortium-scale support is a must, reinforced by the high-priority signal and specification evidence covering 286 branches and major transaction volumes.

*Stakeholders:* Library Administrators, Global System Administrator, PINES Services Specialist (Katherine Gregory), George Tuttle, Working Group, Library directors, Branch managers

<details><summary>Evidence</summary>

- D10: "OE-1: The system must support a library consortium with 286 locations, 17 million annual circulations, and purchasing/processing over 900,000 items per year. [* High Priority]"
- D18: "Management Processes must support the needs of a large, multiple-system library consortium. Specifically, the system must support a library consortium with 286 locations, 17 million annual circulations, purchasing and processing over 900,000 items per year."

</details>

<a id="req-259"></a>
#### REQ-259 Interactive Service Protection

**Priority:** Must &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D16 (interview_sysadmin_2009-05-10.txt), D19 (meeting_tech_subcommittee_2009-06-30.txt)

**Statement:** The system shall isolate reporting and query workloads so that they do not constrain or slow down the OPAC, circulation, or other interactive services during open hours.

Reporting activities shall be separated from the OPAC and other patron-facing services so those services remain responsive while reports are running. Queries and reports shall be usable during open hours without disrupting circulation or OPAC access. The system shall preserve interactive performance during heavy reporting workloads, using scheduling, queuing, or other suitable techniques as needed.

*Priority rationale:* Isolation of reporting workloads has a formal meeting agreement, support from three document types and six stakeholders, and explicit critical signals including 'absolutely cannot' and 'key requirement'.

*Stakeholders:* Robert Chen, PINES IT Department, Patrons, Staff, Local System Administrators, Library Managers

<details><summary>Evidence</summary>

- D19: ""We absolutely cannot constrain the OPAC," Robert emphasized. "If a report is running, it should not slow down the OPAC.""
- D16: "The key requirement is that searches and reports can be processed during open hours without disrupting other system functions."
- D10: "It is highly desirable that searches and reports can be processed during open hours without disrupting other system functions."

</details>

<a id="req-260"></a>
#### REQ-260 Immediate Financial Updates

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D11 (email_financial_reports.eml)

**Statement:** The system shall update financial information immediately when a payment is made so that balances and reports reflect the payment without delay.

When a patron makes a payment at a front desk or other point-of-sale system, the payment shall be reflected immediately in the relevant account balance. The updated financial information shall also be available for querying and reporting without a material delay. This ensures staff users have current financial information when serving patrons or reviewing reports.

*Priority rationale:* Immediate financial updates are important and supported by two stakeholders plus an email agreement, but the agreement is not a formal meeting decision and does not establish Must priority.

*Stakeholders:* Dana Peeler, LaToya Davidson

<details><summary>Evidence</summary>

- D11: "When a patron makes a payment at the front desk, we need the system to reflect that immediately."

</details>

<a id="req-261"></a>
#### REQ-261 Report Performance Under Load

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt), D14 (evergreen_reference_2009.txt), D20 (survey_results_2009.txt)

**Statement:** The system shall execute reports within a reasonable time during busy hours and support real-time reporting where applicable.

Staff users shall be able to obtain reports with current or near-real-time data when reporting needs require it. Report execution shall provide acceptable performance during busy periods rather than becoming unreasonably slow under load. The system shall support low-latency reporting modes where applicable while maintaining the required operational performance.

*Priority rationale:* Report performance is supported by three independent sources and four stakeholders, but the conflicting survey signals about real-time reporting prevent treating the full requirement as Must.

*Stakeholders:* staff, PINES IT Department, management, library staff

<details><summary>Evidence</summary>

- D10: "Ability to have real time reporting"
- D14: "No real-time reporting (all reports are run on current data)"
- D20: ""Reports take too long to run during busy hours""

</details>

<a id="req-262"></a>
#### REQ-262 Transaction-Safe Batch Updates

**Priority:** Should &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall perform batch branch-location updates atomically and recoverably to prevent partial or inconsistent updates.

Batch updates to branch locations shall use transaction safety mechanisms so that changes are applied consistently. If an update cannot be completed, the system shall avoid leaving a partial or inconsistent result. The requirement applies to large or ordinary batch updates where data integrity must be preserved.

*Priority rationale:* Atomic and recoverable updates protect against inconsistent data and are important for reliability, but the requirement appears in only one email without an explicit critical signal or formal decision.

*Stakeholders:* robert.chen@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "Batch update of location field - straightforward database update with transaction safety."

</details>

<a id="req-263"></a>
#### REQ-263 Efficient Batch Transfers

**Priority:** Could &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall process large batch transfers efficiently by using smaller sub-batches when necessary to avoid database locking and performance problems.

Staff users shall be able to process transfers involving very large collections without causing excessive database contention. The system shall support splitting large transfer workloads into smaller sub-batches when needed. The approach shall account for collections of approximately 9.6 million items and preserve acceptable system performance during processing.

*Priority rationale:* Efficient sub-batching is mentioned by only one stakeholder in one email, with no explicit priority signal or formal decision.

*Stakeholders:* robert.chen@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "One concern: with 9.6 million items, batch updates need to be efficient. We should process in smaller batches to avoid locking the database."

</details>

<a id="req-264"></a>
#### REQ-264 Read-Only Reporting Replicas

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D16 (interview_sysadmin_2009-05-10.txt)

**Statement:** The system shall be able to execute reports and searches against read-only replicas to avoid impacting the production database.

The system shall support reporting workloads on standby or read-only replica instances that are periodically synchronized from production. Staff users shall be able to use these replicas for reports and searches when doing so reduces load on the primary database. This capability is intended to preserve production performance, particularly during open hours.

*Priority rationale:* Read-only replicas are a proposed implementation approach supported only by one interview and two stakeholders, without a formal decision or explicit priority signal.

*Stakeholders:* Robert Chen, PINES IT Department

<details><summary>Evidence</summary>

- D16: "Or we need read-only reporting replicas."

</details>

<a id="req-265"></a>
#### REQ-265 Scalable Capacity Overview

**Priority:** Could &nbsp;|&nbsp; **Type:** non-functional &nbsp;|&nbsp; **Sources:** D02 (conversations/conv_pines015_capacity_interface.eml)

**Statement:** The system shall remain usable when displaying capacity for the full set of branches by providing suitable grouping, filtering, paging, or aggregation.

Staff users shall be able to view capacity across a consortium containing approximately 286 branches without the overview becoming unwieldy or unresponsive. The interface shall support one or more techniques such as grouping, filtering, paging, or aggregation to manage the volume of branch information. These techniques shall preserve the usability and responsiveness of the capacity overview.

*Priority rationale:* Scalable capacity presentation is raised in only one email by one stakeholder as a concern that the overview 'might get crowded,' with no formal decision or stronger priority evidence.

*Stakeholders:* robert.chen@gapubliclib.org

<details><summary>Evidence</summary>

- D02: "One consideration: with 286 locations, the overview might get crowded."

</details>

### 6.16 Notifications and workflow automation

*3 requirements - Must: 0, Should: 1, Could: 2, Won't: 0*

<a id="req-266"></a>
#### REQ-266 Configure Transfer Alert Recipients

**Priority:** Should &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D04 (conversations/conv_pines018_item_transfer.eml)

**Statement:** The system shall allow staff users to configure who receives alerts and notifications when a transfer is delayed or encounters issues.

Staff users need alerts when a transfer is delayed or has other issues. The system shall support configurable recipients, such as the staff user who initiated the transfer or designated staff users. This ensures transfer problems reach the people responsible for follow-up.

*Priority rationale:* Supported by two stakeholders and an email-thread agreement to include transfer delay alerts, making it important and expected, although the agreement is not a formal meeting decision.

*Stakeholders:* jennifer.durham@statesboro.lib.org, katherine.gregory@gapubliclib.org

<details><summary>Evidence</summary>

- D04: "If an item transfer is delayed or has issues, notify me."
- D04: "And can we set up alerts? If an item transfer is delayed or has issues, notify me."

</details>

<a id="req-267"></a>
#### REQ-267 Assign Cleanup Tasks

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D09 (conversations/conv_pines024_inactive_patrons.eml)

**Statement:** The system shall allow staff users to assign cleanup or follow-up tasks for inactive patrons to specific branches or staff users at the home branch level.

Staff users need to allocate or mark inactive patron records for branch-level cleanup so local staff can act on assigned lists. The assignment shall support specific branches or staff users and operate at the home branch level. This enables follow-up work to be distributed to the appropriate branch or staff user.

*Priority rationale:* Raised by one stakeholder in a single email, with no formal decision or corroborating source, so it is a desirable but limited-impact improvement.

*Stakeholders:* George Tuttle

<details><summary>Evidence</summary>

- D09: "At the home library level, I can assign cleanup tasks to specific branches."

</details>

<a id="req-268"></a>
#### REQ-268 Run Notice Reports

**Priority:** Could &nbsp;|&nbsp; **Type:** functional &nbsp;|&nbsp; **Sources:** D10 (early_draft_srs_galecia.txt)

**Statement:** The system shall allow staff users to run reports for pre-overdue notices, overdue notices, and holds notices that have been or will be sent.

Staff users need reports showing notices that have been sent or are scheduled to be sent. The reports shall cover pre-overdue notices, overdue notices, and holds notices. This supports monitoring and follow-up of patron notification activity.

*Priority rationale:* Listed only as an example in the early specification, with no supporting survey, interview, or meeting evidence, so it is a candidate for implementation if resources allow.

*Stakeholders:* staff, patron

<details><summary>Evidence</summary>

- D10: "Ability to run reports for pre-overdue, overdue, and holds notices sent"

</details>

## 7. Blacklist

Items identified in the sources but excluded from the specification, with the reason. Nothing was dropped silently: every extracted candidate is either part of a requirement above or listed here.

### 7.1 Removed because of conflicts

| Removed item | Sources | Conflicts with | Explanation |
|---|---|---|---|
| Deletion Reason Capture: The system shall optionally capture a record's status or a staff-supplied reason at the time of deletion. | D07 | M207 Deletion Counts Tracking | M207 requires a reason for each deletion, while M208 describes capturing a deletion reason or pre-deletion status as optional. Resolution: Keep M207: it is an agreed, consolidated requirement supported by D07, D10, D15, and D20. M208 is based only on D07 and makes the capture optional, so it is superseded by the stronger agreed requirement. |

### 7.2 Removed as invalid or in review

| Removed item | Sources | Reason | Explanation |
|---|---|---|---|
| Batch Cataloging Operations: The system shall support batch operations for cataloging tasks and data-quality maintenance. | D15 | out-of-scope | M126 is explicitly about cataloging operations, while the agreed scope in D17 excludes Cataloging because it is covered by a separate specification. |
| Hierarchical Volume and Item Deletion: The system shall provide a quick and effective method to delete a volume entry together with its associated item entries. | D06, D15 | out-of-scope | Deleting volume and item entries is a cataloging operation, which the agreed scope in D17 assigns to a separate specification. |
| Orphaned Record Cleanup: The system shall provide a safeguarded and efficient utility to identify and delete orphaned records, including bibliographic records with no associated item records and orphaned item or volume records. | D06, D10, D15 | out-of-scope | Cleaning up orphaned bibliographic, item, and volume records is cataloging functionality, which the agreed scope in D17 excludes from this specification. |
| Management Scope Limitation: The SRS shall specify only requirements that directly or indirectly relate to management activities. | D17 | not-a-system-requirement | M250 defines what the SRS should cover rather than specifying behavior or a quality of the system. |
| Iterative UI Prototyping: The system's user interface and related data structure specifications shall be developed through an iterative, prototype-oriented methodology with multiple opportunities for end-user review. | D17 | not-a-system-requirement | M261 prescribes a prototype-oriented development and review process rather than a system capability or constraint. |
| Library Terminology Assumption: The SRS shall assume that its readers have a general understanding of common library terminology. | D17 | not-a-system-requirement | M262 is an assumption about the knowledge of SRS readers, not a requirement on the system. |
| Readable Precise Documentation: The SRS and related documentation shall be readable for non-technical staff users while providing sufficient specificity for software project managers and developers. | D17 | not-a-system-requirement | M265 specifies qualities of the SRS and related documentation rather than requirements on the system. |
| WorldCat Editing Assistance: The system shall provide information or links to assist catalogers in editing WorldCat entries for items identified as last copies. | D15 | out-of-scope | M279 provides assistance for catalogers editing WorldCat entries, a cataloging activity excluded from this specification by the agreed scope in D17. |
| Data Specifications Deliverable: The developer shall provide complete data specifications for the records maintained or accessed by the system. | D10, D18, D19 | not-a-system-requirement | This states a developer documentation deliverable rather than a capability or constraint of the system. |
| Process Documentation Deliverable: The developer shall provide thorough high-level descriptions of major system processes. | D10, D18, D19 | not-a-system-requirement | This states a developer documentation deliverable rather than a capability or constraint of the system. |

### 7.3 Candidates discarded while merging

| Candidate | Source | Reason | Explanation |
|---|---|---|---|
| Staff accounts password audit: The system shall provide a report listing Staff Accounts with date of last password change and account expiration. | D10 | off-topic | The staff account password audit report concerns staff security administration rather than patron and demographic reporting. |
| Tested and proven output: The system shall provide tested and proven report outputs. | D10 | too-vague | The phrase 'tested and proven report outputs' provides no actionable quality criteria or measurable system behavior. |
| Per-library and per-system runs: The system shall allow the Shelf Space Report to be run at the branch (per-library) level and at the entire system (per-system) level. | D03 | off-topic | This candidate specifies a report's branch and consortium run scope rather than a security or access-control capability. |

### 7.4 Statements not taken as requirements

During extraction, these statements were recognised as not being requirements: 67 off-topic, 50 not-a-requirement, 14 existing-functionality.

| Source | Reason | Statement | Explanation |
|---|---|---|---|
| D01 | existing-functionality | Yes, the database tracks acquisition date for items. | Statement describing current system data (acquisition date exists); extracted requirements reference using this data, but the statement itself is documentation of current functionality. |
| D02 | existing-functionality | The data is centralized in our database | Statement describing current system architecture; treated as background context rather than a new requirement. |
| D03 | existing-functionality | Currently I pull reports manually and make spreadsheets. | Description of current manual process; used as motivation for automation requirement but is not itself a new system requirement. |
| D05 | existing-functionality | The system currently tracks item status as "missing" or "long overdue" or various other statuses. We can query for items with status "missing" or "lost" and group by branch. | Describes current system behavior; not a new requirement unless gaps/limitations are stated (none explicitly stated here). |
| D07 | existing-functionality | Currently, Evergreen does not log deletions - once something is deleted, it's gone. | Statement about the current system's behavior; used to infer requirements but not itself a new requirement. |
| D13 | existing-functionality | Adding to this - we need user rights and privileges to be controlled through security groups and/or "roles." | This sentence duplicates a proposed requirement later summarized by Katherine; included as a requirement already and thus not repeated here as ignored. (The ignored list only includes background and off-topic; duplicates are represented in requirements.) |
| D14 | existing-functionality | Report writer features: Drag-and-drop field selection; Basic filtering and sorting; Multiple output formats (CSV, HTML, sometimes Excel); Ability to save and reuse report definitions | These describe current capabilities of Evergreen's report writer rather than a new requirement; extract only gaps/desired improvements. |
| D14 | existing-functionality | Canned reports list (Checkout Count, Renewals Count, Items Added Count, etc.) | This enumerates pre-defined reports in the current system; it documents existing functionality rather than requirements for the new system. |
| D14 | existing-functionality | Scheduling note: Some reports can be scheduled to run at regular intervals (daily, weekly, monthly). | Describes current scheduling capability; missing scheduling features were extracted instead. |
| D14 | existing-functionality | Current permission model: Staff can run any report they can access | Describes current permissions; the requirements extracted focus on needed fine-grained permissions rather than restating current state. |
| D14 | existing-functionality | 3.2 KEY RELATIONSHIPS - bibliographic_record -> item ... (list of relationships) | This is documentation of the current data model relationships; where gaps implied requirements were extracted, but the plain listing is not itself a requirement. |
| D16 | existing-functionality | Our main server is a Red Hat Enterprise Linux 5 box with dual quad-core processors and 32GB of RAM. | This describes current hardware specifications rather than a requirement; the OS requirement was extracted but specific hardware details are descriptive. |
| D16 | existing-functionality | When someone runs a complex report, it can tie up the database and slow down the circulation client. | This describes a current problem; the underlying needs (background processing / replicas / no disruption) have been extracted as requirements. |
| D19 | existing-functionality | "We have a dev server, a training server, and production," | This describes the current environment rather than stating a requirement for the new system. |
| D01 | not-a-requirement | Also, Robert - any idea if the database tracks acquisition date? | A question about existing data; the fact that the database tracks acquisition date was asserted later and is documentation of existing functionality rather than a new system requirement. |
| D01 | not-a-requirement | Latoya (note: typo in your email address) - | An administrative note about an email address typo, not a system requirement. |
| D02 | not-a-requirement | Robert will look into technical constraints around displaying 286 locations. Chris will draft initial mockups. | These are actions/tasks assigned to people (project activities), not system capabilities or constraints. |
| D03 | not-a-requirement | Robert will investigate how to estimate shelf space from existing data | This is an action item/task assigned to a person, not a system capability request; the underlying need (estimate shelf space) was extracted as requirements. |
| D03 | not-a-requirement | Susan will coordinate with branch managers for testing | Project coordination action item, not a system requirement. |
| D04 | not-a-requirement | Action: Robert will investigate technical constraints. Thomas will coordinate testing with cataloging staff. | These are project action items/assignments, not functional or non-functional system requirements. |
| D04 | not-a-requirement | We need this in cataloging all the time. We transfer items between our branches for collection balancing and for special programs. | Background justification / use-case context rather than a specific system requirement; relevant needs extracted separately. |
| D05 | not-a-requirement | Do you also need the in-transit items report? I think Maria mentioned something about delivery issues in her interview notes. | A question seeking clarification rather than a stated requirement or need. |
| D07 | not-a-requirement | Robert will implement the database triggers. Katherine will draft the report interface requirements. | Project task assignments and who will implement or draft requirements are actions, not system requirements. |
| D08 | not-a-requirement | Action: ... Jenny will provide test cases from her summer reading program planning. | This is an action item/person task, not a system capability or constraint. |
| D10 | not-a-requirement | This document presents a draft set of requirements for the management and reporting processes of an Integrated Library System. The requirements cover functional aspects only; data structures and user interfaces will require further specification and development using an iterative, prototype-oriented methodology. | Descriptive statement about the document scope and methodology; does not specify a system capability or constraint. |
| D10 | not-a-requirement | King County serves over 2.3 million residents across 49 libraries with an annual circulation of approximately 8 million items. The system maintains over 4 million bibliographic records and serves over 650,000 active borrower accounts. | Contextual background about KCLS scale and current system; useful context but not a standalone requirement beyond the explicit OE-1 scale requirement. |
| D10 | not-a-requirement | The Management Processes facilitate the management of Library services, programs, and policies. Specifically, the Management Processes support: - Analyzing the Library collection and its use by patrons. - Analyzing branch capacity and optimal distribution of the collection. - Analyzing the demographics and interests of patrons. - Analyzing staff productivity and workflow. - Tracking and verifying financial transactions. | High-level goals and capabilities are descriptive aims; specific functional requirements for these analyses are not detailed in this part and so this paragraph is background rather than an explicit requirement. |
| D10 | not-a-requirement | that have been identified as necessary. | Generic sentence fragment without a concrete system need or capability. |
| D10 | not-a-requirement | This document represents the initial requirements gathering phase. | Statement about the document's purpose rather than a system capability. |
| D10 | not-a-requirement | Feedback due: February 15, 2009 | Administrative note about feedback deadline, not a software requirement. |
| D10 | not-a-requirement | Contact: Lori Ayre, Lori.Ayre@galecia.com Lucien Kress, Lucien.Kress@galecia.com | Document contact information, not a system requirement. |
| D11 | not-a-requirement | Thoughts? | This is a closing prompt asking for feedback, not a requirement. |
| D11 | not-a-requirement | These are spot on. | Agreement/endorsement comment, not a system requirement. |
| D11 | not-a-requirement | I agree with everything. | Agreement statement from a participant, not a requirement. |
| D11 | not-a-requirement | I'll add these to the master requirements list. | Administrative note about process, not a requirement for the system. |
| D12 | not-a-requirement | The key benefit of templates is consistency. We want to make sure that when the director asks for "the weeding report," everyone runs the same report with the same criteria. Templates ensure this. | This is rationale/benefit explaining why templates are useful, not a separate system capability. |
| D12 | not-a-requirement | I can confirm the importance of report queuing from the IT side. Without queue visibility, staff call the help desk thinking reports are "broken" when they're just waiting in line. | This statement provides rationale and consequences, not a new functional requirement beyond queue visibility already extracted. |
| D12 | not-a-requirement | These are all being added to the requirements matrix. | Administrative note about requirements tracking, not a system need. |
| D13 | not-a-requirement | Following up on yesterday's call, I wanted to share what we're seeing at the front lines regarding staff login. | Contextual background statement about why the sender is writing; does not state a system need. |
| D13 | not-a-requirement | Dana, I second this request. At Sara Hightower, we've had similar issues. | Agreement and contextual remark; not a distinct system requirement beyond the requests that follow. |
| D13 | not-a-requirement | Thanks everyone for the input. I'm summarizing the key requirements from this thread and will add them to our growing list: | Administrative note about process; not a system capability or constraint. |
| D14 | not-a-requirement | PINES currently operates Evergreen across 286 library locations, serving approximately 3.5 million patrons with a collection of 9.6 million items. | Usage statistics describing current deployment scale; not a functional or non-functional requirement. |
| D15 | not-a-requirement | Thomas provided very specific, actionable requirements | This is the interviewer's summary/commentary, not a system requirement. |
| D15 | not-a-requirement | He mentioned several requirements that overlap with other interviews, confirming their validity | Summary/comment about cross-validation; not a direct requirement for the system. |
| D16 | not-a-requirement | Most of our libraries standardize on Microsoft Internet Explorer, but many have moved to Firefox. | This is contextual background supporting the browser compatibility requirement; the actual browser support requirement is extracted separately. |
| D16 | not-a-requirement | Robert's technical perspective confirms many requirements from other sources - Server environment (Linux/Solaris) is validated ... | Interviewer's summary notes confirm and restate requirements but do not add new system needs. |
| D17 | not-a-requirement | Katherine explained that King County Library System (WA) had previously worked with Galecia Group to develop a comprehensive Software Requirements Specification for a reports interface. PINES staff decided to use that as a foundation and adapt it for our specific needs. She mentioned that Lori Ayre and Lucien Kress from Galecia Group had been contacted and were willing to share their draft. | Background information about using an existing draft/specification; not a direct system requirement. |
| D17 | not-a-requirement | Each member will conduct at least one interview with staff at their library system to gather report needs (due by April 15, 2009) | An action item for working group members, not a requirement of the software system. |
| D17 | not-a-requirement | Katherine will circulate the King County / Galecia Group draft for reference | An administrative action item, not a system requirement. |
| D17 | not-a-requirement | A follow-up meeting is scheduled for July 20, 2009 to review findings | Meeting scheduling information, not a system requirement. |
| D17 | not-a-requirement | A technical subcommittee meeting will be held in late June to discuss architectural constraints | Administrative/planning item about project process, not a direct system requirement. |
| D18 | not-a-requirement | Technical subcommittee meeting: June 30, 2009 (Katherine to send agenda) | This is a meeting action item (organizational task), not a system requirement. |
| D18 | not-a-requirement | Complete draft of requirements document: by September 1, 2009 | This is a project schedule/action item rather than a software requirement. |
| D18 | not-a-requirement | All members to continue gathering detailed report requirements | This is a working-group task, not a feature or constraint of the system. |
| D18 | not-a-requirement | Become the Reports testing group, through which all new Reports development would be filtered. | This is an organizational role for the working group, not a software/system requirement. |
| D18 | not-a-requirement | Minutes prepared by: Katherine Gregory, PINES Services Specialist; Minutes distributed: July 22, 2009 | Document metadata / administrative information, not a system requirement. |
| D19 | not-a-requirement | Meeting logistics: Date, time, location, attendees, and note taker | Meeting metadata and attendee list are context for the meeting, not system requirements. |
| D19 | not-a-requirement | Action items (Robert to research reporting warehouse options; Katherine to compile technical requirements document; George to draft architecture; attendees to review; follow-up meeting scheduled) | These are project tasks and meeting follow-ups rather than system requirements or constraints. |
| D19 | not-a-requirement | "Modern SQL databases can handle complex analytical queries if they're written properly." | This is a rationale/opinion rather than a specific system requirement. |
| D20 | not-a-requirement | Survey Period: April 1 - April 20, 2009 | Survey metadata (dates) is a fact about the survey, not a system requirement. |
| D20 | not-a-requirement | Respondents: 142 library staff members from 58 PINES member libraries | Survey participation statistics are contextual information, not a requirement. |
| D20 | not-a-requirement | Response Rate: 34% (expected ~30%) | Survey response rate is informational and does not express a system need. |
| D20 | not-a-requirement | Survey conducted by: Katherine Gregory, PINES Services Specialist | Authorship/attribution of the survey is metadata, not a system requirement. |
| D20 | not-a-requirement | Report distributed to: PINES Reports Working Group | Distribution list of the survey report is contextual and does not express a system need. |
| D01 | off-topic | Also - did anyone see that Pies 'n' Thighs is opening a second location? My wife is already planning our anniversary dinner there. | Personal small talk about restaurants unrelated to system requirements. |
| D01 | off-topic | My daughter has her recital tomorrow and I'm trying not to think about work but here we are. :P | Personal comment, not a system requirement. |
| D01 | off-topic | I'm heading to the Braves game tonight with some colleagues. Go Braves! | Personal comment, not a system requirement. |
| D01 | off-topic | Also, I need coffee. Real coffee. Not the office sludge. | Personal aside unrelated to requirements. |
| D01 | off-topic | BTW, anyone know a good restaurant in Athens? I'm taking my mom out for her birthday dinner this weekend. | Personal small talk unrelated to system requirements. |
| D02 | off-topic | I'm also dealing with a mouse problem in the staff area. Anyone have a good exterminator recommendation? | Request for an exterminator is unrelated to system requirements or features. |
| D02 | off-topic | My kid's soccer practice got rained out again. Third time this week. | Personal comment not related to system requirements. |
| D02 | off-topic | My cat has started sleeping on my keyboard while I work. | Personal anecdote with no bearing on system requirements. |
| D02 | off-topic | My mom sent me cookies in the mail today. Chocolate chip. | Personal comment not relevant to requirements. |
| D02 | off-topic | Now someone please tell me where I can buy a decent cup of coffee around here. | Personal question not related to system requirements. |
| D03 | off-topic | P.S. Does anyone know if the new Marvel movie is any good? | Personal/non-system chatter unrelated to reporting requirements. |
| D03 | off-topic | My kid is obsessed with dinosaur books... Apparently T-Rex could bite through a car. | Personal anecdote not relevant to system requirements. |
| D03 | off-topic | I just got back from the farmer's market. Got some amazing heirloom tomatoes. Anyone tried making a tomato sandwich with just basil, salt, and bread? | Personal anecdote not a system requirement. |
| D03 | off-topic | My cat Mittens keeps knocking plants off my windowsill. | Personal anecdote not a system requirement. |
| D03 | off-topic | Going to try that pesto recipe I found. Using the basil from my garden. | Personal anecdote not a system requirement. |
| D03 | off-topic | My sister is visiting from Atlanta this weekend. She's been begging me to take her to Callaway Gardens. | Personal anecdote not a system requirement. |
| D03 | off-topic | I need to buy new running shoes. These old ones are falling apart. | Personal remark not relevant to the system. |
| D04 | off-topic | My neighbor's fence fell down in the storm. I loaned them my ladder. Good fences make good neighbors... but broken fences make good neighborly interactions. | Personal small talk unrelated to system requirements. |
| D04 | off-topic | My cat has started bringing me "gifts" - namely, socks he's stolen from the laundry. He's very proud of himself. | Personal anecdote not related to system functionality. |
| D04 | off-topic | My coffee maker broke this morning. Had to use the office coffee. Survival mode activated. | Personal comment not a system requirement. |
| D04 | off-topic | Watching "Chef's Table" again. That episode with the Danish pastry chef is mesmerizing. | Personal comment not relevant to requirements. |
| D04 | off-topic | My daughter's goldfish died. She's devastated. We're getting a new one named Bubbles II. | Personal anecdote unrelated to the software requirements. |
| D04 | off-topic | My mom bought a new vacuum cleaner. It's so powerful it picked up our cat's tail. He ran around the house like a tumbleweed. | Personal anecdote unrelated to requirements. |
| D04 | off-topic | My cat ran around the house like a tumbleweed (vacuum anecdote). | Duplicate personal anecdote; off-topic to system requirements. |
| D05 | off-topic | BTW, has anyone seen "The West Wing" reruns on Netflix? I'm binge-watching it again. Such a great show. | Personal/off-topic chatter not related to system requirements. |
| D05 | off-topic | My neighbor's dog barks at everything. Including my mailbox. The dog has issues. | Personal/off-topic chatter not related to system requirements. |
| D05 | off-topic | Taking my mom to lunch today. She wants to try that new Italian place downtown. I hope it's not too noisy. | Personal/off-topic chatter not related to system requirements. |
| D05 | off-topic | My garden tomatoes are finally ripening. The squirrels keep stealing them though. I've named one "Bandit." | Personal/off-topic chatter not related to system requirements. |
| D05 | off-topic | Watching "The Great British Baking Show" while I work. It's the most comforting show ever created. | Personal/off-topic chatter not related to system requirements. |
| D05 | off-topic | Coffee. I need coffee. | Personal/off-topic chatter not related to system requirements. |
| D06 | off-topic | Also, does anyone know if Costco is open on Sundays? Need to buy snacks for staff meeting. | Personal small talk unrelated to system requirements. |
| D06 | off-topic | I just finished reading "The Seven Husbands of Evelyn Hugo" and I'm not ready to talk about anything else. | Personal comment with no relevance to system functionality. |
| D06 | off-topic | My sister just texted me that she's engaged. I'm so excited! | Personal news not related to system requirements. |
| D06 | off-topic | Going to see "Endgame" tonight. Anyone else plan to? | Casual conversation, not a requirement. |
| D06 | off-topic | My dog ate my library card. I have no idea how. | Personal anecdote unrelated to the software needs. |
| D06 | off-topic | Took my kids to the zoo yesterday. The penguins were very active. | Personal comment not relevant to requirements. |
| D06 | off-topic | (P.S. Costco is open Sunday. Confirmed.) | Follow-up personal confirmation unrelated to system requirements. |
| D07 | off-topic | My neighbor just got a new puppy. It's a golden doodle named Biscuit. Apparently Biscuit has a taste for garden hose. | Personal chatter unrelated to system requirements. |
| D07 | off-topic | My laptop battery is at 2%. I need to plug in before I lose this draft. | Personal comment not a system requirement. |
| D07 | off-topic | Taking my daughter to ballet class. She has a recital next week and is very nervous. | Personal chatter unrelated to system requirements. |
| D07 | off-topic | I'm reading 'Where the Crawdads Sing' right now. The marsh descriptions are beautiful. | Personal comment not a system requirement. |
| D07 | off-topic | Trying out a new recipe for chicken tikka masala tonight. Fingers crossed. | Personal chatter unrelated to system requirements. |
| D08 | off-topic | P.S. Does anyone else's cat sit on their keyboard when you're trying to work? Mine does it on purpose, I'm convinced. | Personal anecdote unrelated to system requirements. |
| D08 | off-topic | My son has his science fair project due next week. He's building a volcano that erupts with baking soda and vinegar. Classic. | Personal anecdote unrelated to system requirements. |
| D08 | off-topic | Got my haircut yesterday. Finally got rid of that awkward growing-out phase. Feels so much better. | Personal anecdote unrelated to system requirements. |
| D08 | off-topic | My mom just asked me to help her set up FaceTime on her new iPhone. She's 72 and technology is... an adventure. | Personal anecdote unrelated to system requirements. |
| D08 | off-topic | I spilled coffee on my shirt this morning. It's going to be one of those days. | Personal anecdote unrelated to system requirements. |
| D08 | off-topic | My new monitor arrived today. Dual screens, here I come! | Personal anecdote unrelated to system requirements. |
| D09 | off-topic | Also, anyone have a good eye cream recommendation? I'm starting to see fine lines and it's freaking me out. | Personal/health/cosmetic question unrelated to system requirements. |
| D09 | off-topic | My son just got accepted to Georgia Tech. I'm so proud! | Personal announcement not relevant to system requirements. |
| D09 | off-topic | My daughter's first piano recital is this weekend. She's been practicing Chopin for months. I'm nervous just watching her practice. | Personal anecdote unrelated to the report requirements. |
| D09 | off-topic | I just realized I've been pronouncing "espresso" wrong my whole life. I've been saying "expresso." Mind blown. | Personal comment unrelated to the system. |
| D09 | off-topic | The power went out for 2 hours this morning. I had to work on my laptop on battery. Very slow going. | Personal status update unrelated to requirements; no need implied. |
| D09 | off-topic | My garden is finally blooming. The peonies are enormous this year. | Personal anecdote, not a system need. |
| D09 | off-topic | (P.S. "Italian" is "ee-tal-EE-an." You're welcome, Susan.) | Personal aside/clarification unrelated to requirements. |
| D09 | off-topic | Subject: Re: Inactive patrons report needed (note typo correction) | Email subject / note about a typo; not a system requirement. |
| D10 | off-topic | DRAFT SOFTWARE REQUIREMENTS SPECIFICATION FOR THE MANAGEMENT PROCESSES OF AN INTEGRATED LIBRARY SYSTEM (document header and metadata) | Document title, authors, version, date and status are metadata about the document, not functional requirements for the system. |
| D10 | off-topic | TABLE OF CONTENTS (list of sections) | Table of contents is structural to the document and not itself a system requirement. |
| D10 | off-topic | ================================================================================ | Document formatting separator, not a requirement. |
| D10 | off-topic | END OF DRAFT DOCUMENT | Document footer text not a system requirement. |
| D12 | off-topic | Jenny === From: susansexton-cooley@saraboblib.org ... - Susan | Email salutations, signatures and separators are not requirements. |
| D12 | off-topic | Jenny, this is great. | Praise or small-talk that does not contain a system need. |
| D13 | off-topic | Thanks, Dana Peeler Systems Librarian, Ohoopee Regional Library | Email signature and sign-off; personal/off-topic content not a system requirement. |
| D14 | off-topic | Evergreen is an open-source Integrated Library System (ILS) originally developed by the Georgia Public Library Service for use in PINES. The current version in production at PINES is 1.4.0.4. | Background/context information about the product and its version; not a system requirement. |
| D15 | off-topic | COMPLETED BY: Jennifer Durham DATE: May 10, 2009 | Document metadata and completion note, not a system requirement. |
| D16 | off-topic | Interviewee years in IT: 15; PINES experience: 3 years; Technical expertise: Linux systems, PostgreSQL, network infrastructure, accessibility compliance | Personal background and expertise of the interviewee are context but not system requirements. |
| D17 | off-topic | Meeting logistics: Date, Time, Location, Attendees, Approval of agenda, Call to order and introductions, Minutes prepared/distributed | Administrative meeting metadata and attendee list; not requirements for the software system. |

## 8. Conflict resolution log

- **contradiction** between M207, M208 (pipeline IDs): M207 requires a reason for each deletion, while M208 describes capturing a deletion reason or pre-deletion status as optional. Kept M207, removed M208. *Rationale:* Keep M207: it is an agreed, consolidated requirement supported by D07, D10, D15, and D20. M208 is based only on D07 and makes the capture optional, so it is superseded by the stronger agreed requirement.

## 9. Quality assurance

Final automatic validation: **passed** - 0 errors, 47 warnings; 20 of 20 source documents traced.

Remaining warnings (each was reviewed and judged acceptable, or is listed as open below):

- possible-duplicate - REQ-005, REQ-222: 'Fine-Grained Reporting' and 'Fine-Grained Report Permissions' are very similar (overlap 0.67)
- possible-duplicate - REQ-014, REQ-160: 'Material Item Count Report' and 'Items Count Report' are very similar (overlap 0.67)
- possible-duplicate - REQ-015, REQ-129: 'Missing Item Reports' and 'Missing and Damaged Item Reporting' are very similar (overlap 0.67)
- possible-duplicate - REQ-022, REQ-151: 'Branch Capacity Trends' and 'Branch Capacity Reports' are very similar (overlap 0.67)
- possible-duplicate - REQ-035, REQ-036: 'Filter Branches' and 'Filter by Branch Location' are very similar (overlap 0.67)
- possible-duplicate - REQ-052, REQ-151: 'Branch Capacity Overview' and 'Branch Capacity Reports' are very similar (overlap 0.67)
- possible-duplicate - REQ-077, REQ-156: 'Last Item Report' and 'Deleted Last-Item Report' are very similar (overlap 0.67)
- possible-duplicate - REQ-095, REQ-096: 'Checkout and Renewal Count Reporting' and 'Checkout Count Report' are very similar (overlap 0.67)
- possible-duplicate - REQ-100, REQ-115: 'Circulation By County' and 'Circulation By Home Branch' are very similar (overlap 0.67)
- possible-duplicate - REQ-107, REQ-108: 'Items In Circulation Count' and 'Items On Shelf Count' are very similar (overlap 0.70)
- possible-duplicate - REQ-107, REQ-160: 'Items In Circulation Count' and 'Items Count Report' are very similar (overlap 0.67)
- possible-duplicate - REQ-108, REQ-160: 'Items On Shelf Count' and 'Items Count Report' are very similar (overlap 0.67)
- possible-duplicate - REQ-120, REQ-121: 'Items Received For Holds' and 'Items Sent For Holds' are very similar (overlap 0.60)
- possible-duplicate - REQ-131, REQ-145: 'Batch Item Status Conversion' and 'Batch Status Conversion Report' are very similar (overlap 0.75)
- possible-duplicate - REQ-136, REQ-160: 'Item Use Count Report' and 'Items Count Report' are very similar (overlap 0.67)
- possible-duplicate - REQ-148, REQ-161: 'Bibliographic Records Edited Report' and 'Items Edited Report' are very similar (overlap 0.62)
- possible-duplicate - REQ-154, REQ-160: 'Deleted Items Count' and 'Items Count Report' are very similar (overlap 0.67)
- possible-duplicate - REQ-232, REQ-233: 'Read-Only ILS Integration' and 'Read-Only OPAC Integration' are very similar (overlap 0.60)
- unverified-evidence - REQ-075: None of the supporting quotes was found verbatim in the sources
- unverified-evidence - REQ-212: None of the supporting quotes was found verbatim in the sources
- vocabulary - REQ-020: Uses 'activity' instead of the glossary term 'transaction'
- vocabulary - REQ-077: Uses 'copy' instead of the glossary term 'item'
- vocabulary - REQ-093: Uses 'event' instead of the glossary term 'transaction'
- vocabulary - REQ-134: Uses 'operator' instead of the glossary term 'staff user'
- vocabulary - REQ-137: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-142: Uses 'event' instead of the glossary term 'transaction'
- vocabulary - REQ-149: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-155: Uses 'copy' instead of the glossary term 'item'
- vocabulary - REQ-155: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-157: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-158: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-162: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-174: Uses 'profile' instead of the glossary term 'staff role'
- vocabulary - REQ-176: Uses 'activity' instead of the glossary term 'transaction'
- vocabulary - REQ-178: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-180: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-181: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-182: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-183: Uses 'listing' instead of the glossary term 'report'
- vocabulary - REQ-203: Uses 'blank' instead of the glossary term 'null value'
- vocabulary - REQ-214: Uses 'event' instead of the glossary term 'transaction'
- vocabulary - REQ-229: Uses 'process' instead of the glossary term 'report run'
- vocabulary - REQ-240: Uses 'activity' instead of the glossary term 'transaction'
- vocabulary - REQ-240: Uses 'event' instead of the glossary term 'transaction'
- vocabulary - REQ-246: Uses 'network' instead of the glossary term 'consortium'
- vocabulary - REQ-263: Uses 'process' instead of the glossary term 'report run'
- vocabulary - REQ-264: Uses 'search' instead of the glossary term 'query'

Review rounds (validate - review - revise loop):

| Round | Errors | Warnings | Actions | Warnings dismissed | Reviewer summary |
|---|---|---|---|---|---|
| 1 | 26 | 61 | 40 | 28 | The specification has many clear, coherent requirements, but the validator identified numerous descriptions that need to be expanded into the required paragraph form. The flagged vocabulary and statement-form issues also need correction; the possible duplicates and evidence warnings are acceptable as distinct capabilities or are covered by the source-tracing process. |
| 2 | 0 | 47 | 1 | 3 | The flagged similar report names refer to distinct needs: collection counts versus an overall item total, and current last-copy items versus deleted last items. The vocabulary warning was already addressed in an earlier review; the current requirement details do not show the flagged term. One additional priority and statement mismatch remains in the Won’t requirement about a separate reporting database. |
| 3 | 0 | 47 | 1 | 0 | The specification is generally coherent, with no validator issues reported and no further significant duplicates or priority mismatches apparent. One statement could be clearer about the system’s enterprise deployment context versus the infrastructure it may rely on. |
| 4 | 0 | 47 | 1 | 0 | No validator issues were reported, and the requirements are generally coherent with no significant new duplicates or priority mismatches apparent. One statement is unclear about what staff users may modify and run. |

Open review items (proposed in the last round, not applied because the round limit was reached):

- rewrite REQ-063: Replace “run a permitted modifiable item” with wording that clearly refers to modifying and running a report template when the staff user's permissions allow it. For example: “The system shall allow staff users to run a report template as-is or modify and run it when their permissions allow.” Ensure the description uses the same meaning.

## Appendix: traceability matrix

| Document | Requirements derived from it |
|---|---|
| D01 `conversations/conv_pines014_material_volume.eml` | [REQ-013](#req-013), [REQ-014](#req-014), [REQ-029](#req-029), [REQ-036](#req-036), [REQ-053](#req-053), [REQ-054](#req-054), [REQ-098](#req-098), [REQ-105](#req-105), [REQ-107](#req-107), [REQ-108](#req-108), [REQ-140](#req-140) |
| D02 `conversations/conv_pines015_capacity_interface.eml` | [REQ-016](#req-016), [REQ-022](#req-022), [REQ-023](#req-023), [REQ-035](#req-035), [REQ-042](#req-042), [REQ-052](#req-052), [REQ-066](#req-066), [REQ-084](#req-084), [REQ-150](#req-150), [REQ-256](#req-256), [REQ-265](#req-265) |
| D03 `conversations/conv_pines016_shelf_space.eml` | [REQ-009](#req-009), [REQ-016](#req-016), [REQ-018](#req-018), [REQ-037](#req-037) |
| D04 `conversations/conv_pines018_item_transfer.eml` | [REQ-038](#req-038), [REQ-039](#req-039), [REQ-041](#req-041), [REQ-130](#req-130), [REQ-142](#req-142), [REQ-167](#req-167), [REQ-170](#req-170), [REQ-171](#req-171), [REQ-215](#req-215), [REQ-216](#req-216), [REQ-223](#req-223), [REQ-239](#req-239), [REQ-255](#req-255), [REQ-262](#req-262), [REQ-263](#req-263), [REQ-266](#req-266) |
| D05 `conversations/conv_pines019_020_missing_intransit.eml` | [REQ-128](#req-128), [REQ-129](#req-129), [REQ-164](#req-164), [REQ-166](#req-166), [REQ-169](#req-169) |
| D06 `conversations/conv_pines021_item_purging.eml` | [REQ-077](#req-077), [REQ-131](#req-131), [REQ-134](#req-134), [REQ-163](#req-163), [REQ-206](#req-206), [REQ-209](#req-209) |
| D07 `conversations/conv_pines022_deletions.eml` | [REQ-011](#req-011), [REQ-024](#req-024), [REQ-025](#req-025), [REQ-026](#req-026), [REQ-027](#req-027), [REQ-031](#req-031), [REQ-206](#req-206), [REQ-207](#req-207), [REQ-208](#req-208), [REQ-211](#req-211) |
| D08 `conversations/conv_pines023_patron_characteristics.eml` | [REQ-012](#req-012), [REQ-034](#req-034), [REQ-173](#req-173), [REQ-177](#req-177), [REQ-203](#req-203) |
| D09 `conversations/conv_pines024_inactive_patrons.eml` | [REQ-008](#req-008), [REQ-030](#req-030), [REQ-044](#req-044), [REQ-056](#req-056), [REQ-057](#req-057), [REQ-076](#req-076), [REQ-081](#req-081), [REQ-087](#req-087), [REQ-176](#req-176), [REQ-240](#req-240), [REQ-267](#req-267) |
| D10 `early_draft_srs_galecia.txt` | [REQ-001](#req-001), [REQ-002](#req-002), [REQ-005](#req-005), [REQ-010](#req-010), [REQ-012](#req-012), [REQ-013](#req-013), [REQ-014](#req-014), [REQ-015](#req-015), [REQ-017](#req-017), [REQ-018](#req-018), [REQ-020](#req-020), [REQ-021](#req-021), [REQ-033](#req-033), [REQ-034](#req-034), [REQ-038](#req-038), [REQ-040](#req-040), [REQ-041](#req-041), [REQ-043](#req-043), [REQ-045](#req-045), [REQ-046](#req-046), [REQ-048](#req-048), [REQ-049](#req-049), [REQ-051](#req-051), [REQ-052](#req-052), [REQ-053](#req-053), [REQ-055](#req-055), [REQ-058](#req-058), [REQ-059](#req-059), [REQ-060](#req-060), [REQ-063](#req-063), [REQ-064](#req-064), [REQ-065](#req-065), [REQ-069](#req-069), [REQ-070](#req-070), [REQ-072](#req-072), [REQ-073](#req-073), [REQ-077](#req-077), [REQ-078](#req-078), [REQ-079](#req-079), [REQ-080](#req-080), [REQ-081](#req-081), [REQ-082](#req-082), [REQ-083](#req-083), [REQ-085](#req-085), [REQ-086](#req-086), [REQ-088](#req-088), [REQ-089](#req-089), [REQ-090](#req-090), [REQ-091](#req-091), [REQ-094](#req-094), [REQ-095](#req-095), [REQ-096](#req-096), [REQ-097](#req-097), [REQ-099](#req-099), [REQ-100](#req-100), [REQ-101](#req-101), [REQ-102](#req-102), [REQ-103](#req-103), [REQ-104](#req-104), [REQ-105](#req-105), [REQ-106](#req-106), [REQ-109](#req-109), [REQ-110](#req-110), [REQ-111](#req-111), [REQ-112](#req-112), [REQ-113](#req-113), [REQ-114](#req-114), [REQ-115](#req-115), [REQ-116](#req-116), [REQ-117](#req-117), [REQ-118](#req-118), [REQ-119](#req-119), [REQ-120](#req-120), [REQ-121](#req-121), [REQ-122](#req-122), [REQ-123](#req-123), [REQ-125](#req-125), [REQ-128](#req-128), [REQ-129](#req-129), [REQ-130](#req-130), [REQ-132](#req-132), [REQ-133](#req-133), [REQ-134](#req-134), [REQ-136](#req-136), [REQ-137](#req-137), [REQ-138](#req-138), [REQ-139](#req-139), [REQ-141](#req-141), [REQ-142](#req-142), [REQ-143](#req-143), [REQ-144](#req-144), [REQ-145](#req-145), [REQ-146](#req-146), [REQ-147](#req-147), [REQ-148](#req-148), [REQ-149](#req-149), [REQ-152](#req-152), [REQ-153](#req-153), [REQ-154](#req-154), [REQ-155](#req-155), [REQ-156](#req-156), [REQ-157](#req-157), [REQ-158](#req-158), [REQ-160](#req-160), [REQ-161](#req-161), [REQ-162](#req-162), [REQ-165](#req-165), [REQ-168](#req-168), [REQ-172](#req-172), [REQ-174](#req-174), [REQ-175](#req-175), [REQ-176](#req-176), [REQ-178](#req-178), [REQ-179](#req-179), [REQ-180](#req-180), [REQ-181](#req-181), [REQ-182](#req-182), [REQ-183](#req-183), [REQ-184](#req-184), [REQ-185](#req-185), [REQ-187](#req-187), [REQ-188](#req-188), [REQ-189](#req-189), [REQ-190](#req-190), [REQ-191](#req-191), [REQ-192](#req-192), [REQ-193](#req-193), [REQ-194](#req-194), [REQ-195](#req-195), [REQ-196](#req-196), [REQ-197](#req-197), [REQ-198](#req-198), [REQ-199](#req-199), [REQ-201](#req-201), [REQ-203](#req-203), [REQ-204](#req-204), [REQ-205](#req-205), [REQ-208](#req-208), [REQ-210](#req-210), [REQ-213](#req-213), [REQ-219](#req-219), [REQ-220](#req-220), [REQ-221](#req-221), [REQ-222](#req-222), [REQ-225](#req-225), [REQ-226](#req-226), [REQ-227](#req-227), [REQ-229](#req-229), [REQ-230](#req-230), [REQ-232](#req-232), [REQ-233](#req-233), [REQ-234](#req-234), [REQ-235](#req-235), [REQ-242](#req-242), [REQ-243](#req-243), [REQ-244](#req-244), [REQ-245](#req-245), [REQ-246](#req-246), [REQ-250](#req-250), [REQ-251](#req-251), [REQ-252](#req-252), [REQ-253](#req-253), [REQ-257](#req-257), [REQ-258](#req-258), [REQ-259](#req-259), [REQ-261](#req-261), [REQ-268](#req-268) |
| D11 `email_financial_reports.eml` | [REQ-185](#req-185), [REQ-188](#req-188), [REQ-189](#req-189), [REQ-190](#req-190), [REQ-191](#req-191), [REQ-192](#req-192), [REQ-193](#req-193), [REQ-194](#req-194), [REQ-195](#req-195), [REQ-202](#req-202), [REQ-204](#req-204), [REQ-236](#req-236), [REQ-260](#req-260) |
| D12 `email_report_features.eml` | [REQ-001](#req-001), [REQ-010](#req-010), [REQ-017](#req-017), [REQ-020](#req-020), [REQ-034](#req-034), [REQ-040](#req-040), [REQ-051](#req-051), [REQ-059](#req-059), [REQ-063](#req-063), [REQ-067](#req-067), [REQ-080](#req-080), [REQ-205](#req-205), [REQ-220](#req-220), [REQ-222](#req-222), [REQ-225](#req-225), [REQ-254](#req-254) |
| D13 `email_staff_login.eml` | [REQ-214](#req-214), [REQ-220](#req-220), [REQ-221](#req-221), [REQ-224](#req-224), [REQ-226](#req-226), [REQ-227](#req-227), [REQ-247](#req-247), [REQ-248](#req-248) |
| D14 `evergreen_reference_2009.txt` | [REQ-013](#req-013), [REQ-017](#req-017), [REQ-028](#req-028), [REQ-032](#req-032), [REQ-034](#req-034), [REQ-040](#req-040), [REQ-046](#req-046), [REQ-048](#req-048), [REQ-055](#req-055), [REQ-058](#req-058), [REQ-060](#req-060), [REQ-061](#req-061), [REQ-062](#req-062), [REQ-065](#req-065), [REQ-072](#req-072), [REQ-074](#req-074), [REQ-075](#req-075), [REQ-076](#req-076), [REQ-077](#req-077), [REQ-078](#req-078), [REQ-080](#req-080), [REQ-081](#req-081), [REQ-092](#req-092), [REQ-093](#req-093), [REQ-099](#req-099), [REQ-100](#req-100), [REQ-101](#req-101), [REQ-102](#req-102), [REQ-103](#req-103), [REQ-104](#req-104), [REQ-106](#req-106), [REQ-110](#req-110), [REQ-113](#req-113), [REQ-132](#req-132), [REQ-133](#req-133), [REQ-136](#req-136), [REQ-137](#req-137), [REQ-139](#req-139), [REQ-144](#req-144), [REQ-146](#req-146), [REQ-148](#req-148), [REQ-152](#req-152), [REQ-157](#req-157), [REQ-161](#req-161), [REQ-174](#req-174), [REQ-181](#req-181), [REQ-184](#req-184), [REQ-187](#req-187), [REQ-200](#req-200), [REQ-203](#req-203), [REQ-212](#req-212), [REQ-222](#req-222), [REQ-228](#req-228), [REQ-238](#req-238), [REQ-241](#req-241), [REQ-243](#req-243), [REQ-250](#req-250), [REQ-251](#req-251), [REQ-257](#req-257), [REQ-261](#req-261) |
| D15 `interview_cataloging_2009-05-08.txt` | [REQ-014](#req-014), [REQ-018](#req-018), [REQ-021](#req-021), [REQ-038](#req-038), [REQ-041](#req-041), [REQ-061](#req-061), [REQ-077](#req-077), [REQ-079](#req-079), [REQ-083](#req-083), [REQ-128](#req-128), [REQ-129](#req-129), [REQ-130](#req-130), [REQ-131](#req-131), [REQ-134](#req-134), [REQ-138](#req-138), [REQ-141](#req-141), [REQ-142](#req-142), [REQ-143](#req-143), [REQ-165](#req-165), [REQ-168](#req-168), [REQ-208](#req-208) |
| D16 `interview_sysadmin_2009-05-10.txt` | [REQ-076](#req-076), [REQ-219](#req-219), [REQ-220](#req-220), [REQ-221](#req-221), [REQ-231](#req-231), [REQ-234](#req-234), [REQ-243](#req-243), [REQ-244](#req-244), [REQ-245](#req-245), [REQ-250](#req-250), [REQ-251](#req-251), [REQ-252](#req-252), [REQ-259](#req-259), [REQ-264](#req-264) |
| D17 `meeting_minutes/meeting_2009-03-15_minutes.txt` | [REQ-003](#req-003), [REQ-004](#req-004), [REQ-006](#req-006), [REQ-019](#req-019), [REQ-047](#req-047), [REQ-049](#req-049), [REQ-126](#req-126), [REQ-127](#req-127), [REQ-172](#req-172), [REQ-186](#req-186), [REQ-218](#req-218), [REQ-219](#req-219), [REQ-249](#req-249) |
| D18 `meeting_minutes/meeting_2009-07-20_minutes.txt` | [REQ-001](#req-001), [REQ-004](#req-004), [REQ-009](#req-009), [REQ-017](#req-017), [REQ-018](#req-018), [REQ-047](#req-047), [REQ-076](#req-076), [REQ-079](#req-079), [REQ-128](#req-128), [REQ-129](#req-129), [REQ-135](#req-135), [REQ-144](#req-144), [REQ-151](#req-151), [REQ-172](#req-172), [REQ-186](#req-186), [REQ-221](#req-221), [REQ-226](#req-226), [REQ-229](#req-229), [REQ-230](#req-230), [REQ-232](#req-232), [REQ-233](#req-233), [REQ-234](#req-234), [REQ-235](#req-235), [REQ-237](#req-237), [REQ-242](#req-242), [REQ-243](#req-243), [REQ-244](#req-244), [REQ-245](#req-245), [REQ-246](#req-246), [REQ-250](#req-250), [REQ-251](#req-251), [REQ-252](#req-252), [REQ-253](#req-253), [REQ-258](#req-258) |
| D19 `meeting_tech_subcommittee_2009-06-30.txt` | [REQ-013](#req-013), [REQ-045](#req-045), [REQ-048](#req-048), [REQ-050](#req-050), [REQ-078](#req-078), [REQ-203](#req-203), [REQ-219](#req-219), [REQ-220](#req-220), [REQ-221](#req-221), [REQ-229](#req-229), [REQ-232](#req-232), [REQ-233](#req-233), [REQ-234](#req-234), [REQ-235](#req-235), [REQ-243](#req-243), [REQ-246](#req-246), [REQ-250](#req-250), [REQ-251](#req-251), [REQ-252](#req-252), [REQ-253](#req-253), [REQ-259](#req-259) |
| D20 `survey_results_2009.txt` | [REQ-007](#req-007), [REQ-013](#req-013), [REQ-015](#req-015), [REQ-017](#req-017), [REQ-019](#req-019), [REQ-032](#req-032), [REQ-038](#req-038), [REQ-039](#req-039), [REQ-041](#req-041), [REQ-043](#req-043), [REQ-048](#req-048), [REQ-049](#req-049), [REQ-051](#req-051), [REQ-055](#req-055), [REQ-068](#req-068), [REQ-071](#req-071), [REQ-078](#req-078), [REQ-081](#req-081), [REQ-093](#req-093), [REQ-094](#req-094), [REQ-095](#req-095), [REQ-105](#req-105), [REQ-111](#req-111), [REQ-112](#req-112), [REQ-124](#req-124), [REQ-130](#req-130), [REQ-142](#req-142), [REQ-159](#req-159), [REQ-172](#req-172), [REQ-175](#req-175), [REQ-186](#req-186), [REQ-200](#req-200), [REQ-201](#req-201), [REQ-203](#req-203), [REQ-208](#req-208), [REQ-210](#req-210), [REQ-217](#req-217), [REQ-222](#req-222), [REQ-225](#req-225), [REQ-254](#req-254), [REQ-261](#req-261) |
