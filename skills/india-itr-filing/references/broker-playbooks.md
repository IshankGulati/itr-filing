# Broker Playbooks

## Contents

1. Why this file exists
2. Generic export pattern for any broker or platform
3. Common categories by platform type
4. How to add a provider-specific mini-playbook

## 1. Why this file exists

Do not overfit the skill to one broker.

Use this file when:

- the user has a broker or platform the skill does not explicitly know yet
- the user needs help finding the right exports
- a contributor wants to add a provider-specific mini-guide later

The goal is to request the right raw artifacts first, then add provider-specific knowledge over time.

## 2. Generic export pattern for any broker or platform

Ask for the smallest set that can support Indian-tax reconstruction.

### Capital gains

- realized gain or tax P&L report
- full transaction export with trade date, quantity, proceeds, basis, and fees
- holdings or opening-position statement if the FY starts with open lots

### Income

- dividend report
- interest report
- corporate-actions or vesting report if employer equity is involved

### Tax and withholding

- withholding-tax report
- broker tax statement
- local tax certificates if the platform issues them

### Continuity

- prior-year closing statement or next-year opening statement when lot continuity matters

If the platform provides both a summary report and a raw activity export, prefer the raw activity export for reconstruction and use the summary only as a reconciliation aid.

## 3. Common categories by platform type

### Indian equity or F&O broker

Common useful exports:

- tax P&L
- contract notes
- tradebook
- holdings statement
- annual report

### Mutual-fund platform

Common useful exports:

- capital-gains statement
- CAS
- transaction statement
- folio-wise account statement

### Foreign broker

Common useful exports:

- annual activity statement
- trade export
- dividend report
- interest report
- withholding report
- opening-position statement

### Employer equity platform

Common useful exports:

- vesting history
- release confirmations
- sell-to-cover details
- transfer-to-broker history
- broker sale confirmations

### VDA exchange

Common useful exports:

- trade history
- deposit and withdrawal history
- wallet transfers
- realized-gain report if available

## 4. How to add a provider-specific mini-playbook

If a broker or platform keeps coming up, add a mini-guide that records:

- provider name
- where the user usually finds reports
- exact report names to request
- best export formats
- known field quirks
- whether summaries are reliable or only directional
- which artifacts are enough for Indian-tax reconstruction

Keep provider-specific knowledge additive. Do not rewrite the whole skill around one platform.
