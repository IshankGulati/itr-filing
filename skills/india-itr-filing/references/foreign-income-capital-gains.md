# Foreign Income And Capital Gains

## Contents

1. When to read this file
2. Required inputs
3. Lot reconstruction workflow
4. FX and Rule-115 handling
5. FTC and foreign schedules
6. Carry-forward loss usage
7. Output expectations

## 1. When to read this file

Read this file when the case includes any of the following:

- foreign-broker activity
- employer equity plans routed through a foreign platform
- foreign dividends or interest
- foreign withholding tax
- foreign assets or account reporting
- current-year or brought-forward foreign-share capital gains or losses

This file is for Indian taxpayers who hold foreign investments or receive foreign income. It is not a guide to filing non-Indian tax returns.

## 2. Required inputs

- annual activity statements
- transaction export with trade dates, quantities, proceeds, basis, and fees
- prior-year statement if the FY starts with open lots
- dividend, interest, and withholding-tax lines
- any platform-provided `FA`, `FSI`, `TR`, or `Form 67` support
- prior-year filed-return schedules if loss carry forward matters
- any local `SBI TTBR` or `Rule 115` workpapers already present in the workspace

If broker-specific exports are hard to find, read [broker-playbooks.md](broker-playbooks.md) and request the generic export pattern first.

## 3. Lot reconstruction workflow

Use this order:

1. Confirm whether records support a defensible specific-lot method.
2. If not, choose a clearly stated fallback method that fits the instrument and records.
3. For broker-routed equity and ETF positions, `FIFO` is a common working fallback when no better lot evidence exists.
4. For mutual funds, pooled products, or other instruments where another method may be more appropriate, verify the current-law treatment instead of forcing `FIFO`.
5. Rebuild realized sales lot by lot.
6. Separate holding-period classification from the broker's own tax labels.
7. Keep a visible record of:
   - acquisition date
   - sale date
   - quantity
   - cost basis
   - proceeds
   - fees
   - gain or loss
   - tax bucket under the current working interpretation

Do not skip this workflow merely because the broker already shows total realized gain.

## 4. FX and Rule-115 handling

- Search the workspace first for local files like:
  - `*ttbr*`
  - `*rule115*`
  - `*sbi_tt*`
- Reuse reliable local rate workpapers before building a new rate table.
- Do not assume `Rule 115` or `SBI TTBR` is the universal answer for every foreign-income type.
- Keep the conversion method explicit.
- Keep the source explicit.
- Keep the relevant date logic explicit.
- Write the method into the case notes before using the numbers in scenario comparisons.
- If the method is still provisional, mark the resulting INR values as provisional too.

Do not bury the FX assumption inside a spreadsheet without explaining it in prose.

## 5. FTC and foreign schedules

Foreign tax suffered is not the same as foreign tax credit finally usable in the Indian return.

Track separately:

- foreign income amount
- foreign tax withheld or paid
- source country
- source type
- support document
- likely Indian schedule destination

Expect to touch some or all of these, depending on the case:

- `FA`
- `FSI`
- `TR`
- `Form 67`

Keep the mapping evidence, not just the final totals.

## 6. Carry-forward loss usage

When brought-forward capital losses matter:

- prefer filed ITR JSON or utility output over raw broker summaries
- inspect `CFL`, `CG`, `BFLA`, and `CYLA`
- use CPC intimation or processed-return support when available
- state clearly whether the working figure is:
  - raw source summary
  - filed-return figure
  - processed-return supported figure

Treat the filed-return or processed-return figure as the default planning anchor unless the user is deliberately preparing a correction or litigation-style review.

## 7. Output expectations

Aim to produce:

- a lot-level realized-gain file
- a cashflow or income conversion file for dividends, interest, and withholding
- a short note documenting the FX method and date logic
- a clean summary in `itr_working.md`
- a line-by-line explanation in `itr_line_by_line.md`
- a final mapping into `outputs/itr-draft.json` only when the broader case is materially complete and current AY validation work is actually feasible
