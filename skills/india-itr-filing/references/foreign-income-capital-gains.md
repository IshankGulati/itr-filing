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
- If exact dated rates can be recovered from local workpapers or checked-in helper outputs, do that before asking the user whether placeholder precision is acceptable.
- If a fresh historical `SBI TT` lookup is needed, the helper repo `skbly7/sbi-tt-rates-historical` can assist in fetching historical TT rates for foreign-capital-gains work; still document the exact source, dates, and method used in the case notes.
- Do not assume `Rule 115` or `SBI TTBR` is the universal answer for every foreign-income type.
- Named anti-pattern: `Rule 115` and `Rule 115A` are not the same provision. `Rule 115A` is the averaging mechanism for the first proviso to section 48, which applies to **non-residents** on shares or debentures of an Indian company. A **resident** selling **foreign** shares is normally outside that proviso, so the gain is computed under the main section-48 route and converted under `Rule 115`. Do not apply the non-resident `115A` mechanics to a resident's foreign-share gain.
- Keep the conversion method explicit, the source explicit, and the relevant date logic explicit.
- Write the method into the case notes before using the numbers in scenario comparisons.
- Before presenting an FX-converted gain as final, compute a rough independent estimate such as foreign-currency gain times a representative sale-date rate. If the detailed INR answer diverges materially, re-check the rate dates and mechanics before sending it.
- If the method is still provisional, mark the resulting INR values as provisional too.

Do not bury the FX assumption inside a spreadsheet without explaining it in prose.

### Resident foreign-share gains: two live conversion methods

For a resident selling foreign shares there are **two methods seen in real practice**, and they produce materially different taxable gains once the rupee has moved. Do not silently pick one and call the other an error. This is a genuine interpretive fork, not a settled rule.

- **Per-leg conversion (mainstream).** Convert cost at the `SBI TTBR` for the month-end **before the purchase** and proceeds at the `SBI TTBR` for the month-end **before the sale**; the taxable gain is the INR difference. This is the method practitioner sources such as Zerodha Varsity illustrate. It **deliberately captures rupee movement inside the taxable gain**, which is the normal treatment for a resident's foreign asset (residents do not get the non-resident `115A` FX protection). When the rupee has weakened, this yields the **larger** gain, and that is expected, not a bug.
- **Single-rate-on-net-gain (minority reading).** Compute the gain in foreign currency first, then convert the net gain once at the month-end `TTBR` before sale. This treats the whole capital-gains head as converting at one specified date. It yields a **lower** gain when the rupee has depreciated.

Rules for handling this fork:

- Pick the method deliberately, name it, and cite the source you relied on. Do not switch methods just because a number "feels" too high or because a prior tool or the user reported a different figure.
- When the two methods diverge materially, present **both** numbers and surface the choice to the user or their CA rather than quietly adopting the lower one. A large gap is usually the FX method, not a data error.
- A rupee-depreciation component showing up in a resident's gain is normal under the mainstream method; do not "correct" it away without a stated legal basis.
- Run the rough sanity bound in both cases, but remember the bound only catches arithmetic slips, not the method choice itself.

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

### Schedule FA is calendar-year and lists holdings, not this year's trades

`Schedule FA` reports foreign assets on a **calendar-year basis** (the relevant accounting period, not the Indian `FY`), and it lists the **peak and closing position of every holding**, not just the current year's transactions. Two failure modes follow directly:

- Do not read a `Schedule FA` line as a current-`FY` sale. A platform-generated `FA` draft (for example from Vested or a similar service) can show a position that was actually **closed in a prior year**, or show a calendar-year event that belongs in a **different Indian FY**. Cross-check the trade against the transaction export and the prior-year filed return before treating it as a taxable event this year.
- When an asset was disposed of near a year boundary, place the closure in the correct period. A sale or company dissolution dated in **January–March** falls in one Indian `FY` but the **next** calendar year for `FA` purposes; confirm the exact date before deciding which year's `FA` it belongs in.

If a platform's `FA` figures appear to contradict the transaction export, treat the mismatch as a reconciliation task, not as evidence the user's records are incomplete. The prior-year filed return and the raw transaction file are the anchors; the platform `FA` draft is a convenience, not the truth.

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
