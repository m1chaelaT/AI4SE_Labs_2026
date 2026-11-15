# Task 5 run summary (2026-11-15T19:24:34)

Model: `gpt-5-mini`, retrieved chunks per task: 5, vector store: `minilm`

## Unit tests

| | run | passed | failed | errors |
|---|---|---|---|---|
| before (stubs) | 481 | 429 | 35 | 17 |
| after (generated) | 481 | 467 | 1 | 13 |

Fixed tests: 40, newly failing: 2, still failing: 12

Still failing:

- `tests.test_inventory.InventoryLedgerContainsLenIterTests.test_contains_present_even_if_zero_on_hand_after_commit`
- `tests.test_orders.OrderAdvanceTests.test_advance_from_terminal_raises`
- `tests.test_orders.OrderAdvanceTests.test_advance_to_same_status_raises`
- `tests.test_orders.OrderAdvanceTests.test_illegal_advance_raises_and_keeps_status`
- `tests.test_orders.OrderStateMachineTests.test_call_is_alias_for_transition`
- `tests.test_orders.OrderStateMachineTests.test_transition_illegal_raises`
- `tests.test_orders.OrderTotalTests.test_total_reflects_merged_quantities_for_bulk_discount`
- `tests.test_pricing.BulkDiscountPriceTests.test_at_threshold_applies_discount`
- `tests.test_pricing.BulkDiscountPriceTests.test_discount_uses_floor_division`
- `tests.test_pricing.BulkDiscountPriceTests.test_full_discount_yields_zero`
- `tests.test_pricing.BulkDiscountPriceTests.test_quantity_summed_across_lines`
- `tests.test_pricing.BulkDiscountPriceTests.test_wraps_base_with_tax`

Newly failing:

- `tests.test_orders.OrderLogTests.test_by_status_non_status_raises_on_first_next`
- `tests.test_pricing.BulkDiscountPriceTests.test_call_matches_price`

## Tasks and token usage

| Task | Status | Calls | Prompt | Completion | (reasoning) | Total |
|---|---|---|---|---|---|---|
| `OrderStatus.is_terminal` | written | 1 | 639 | 178 | 128 | 817 |
| `InventoryLedger.__contains__` | written | 1 | 800 | 290 | 192 | 1090 |
| `Warehouse.stock_report` | written | 1 | 753 | 358 | 256 | 1111 |
| `OrderStateMachine.transition` | written | 1 | 854 | 307 | 192 | 1161 |
| `OrderLog.by_status` | written | 1 | 672 | 123 | 64 | 795 |
| `Customer.can_afford` | written | 1 | 771 | 186 | 128 | 957 |
| `Order.__len__` | written | 1 | 606 | 102 | 64 | 708 |
| `BulkDiscountPricing.price` | written | 1 | 830 | 554 | 448 | 1384 |
| `EventBus.__contains__` | written | 1 | 728 | 199 | 128 | 927 |
| `Money.__bool__` | written | 1 | 720 | 43 | 0 | 763 |
| **total** | | 10 | 7373 | 2340 | 1600 | **9713** |
