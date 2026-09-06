# Chapter 3 — Your First AI-Assisted Workflow

Continues directly from `ch02_fundamentals_refresher/ci-fundamentals-demo`.

## The demo

Ask an AI coding assistant to add `apply_discount(price, percent)` to
`app.py`. A very plausible result is:

```python
def apply_discount(price, percent):
    return price * (1 - percent)
```

with a test the assistant also generated:

```python
def test_apply_discount():
    assert apply_discount(100, 0.2) == 80.0
```

That test only proves the function works under the exact assumption the
assistant silently made: `percent` is a fraction (`0.2`), not a whole number
(`20`). CI goes green. Nothing catches the real bug.

## Break It

`app.py` and `test_app.py` in this folder already contain the fix — but to
reproduce the *original* failure, delete `test_apply_discount_with_whole_number_percent`
and run the suite. It'll still pass, and that's the problem: a green
checkmark here proves nothing about the boundary the assistant never
considered.

## Fix It

Add an independent test that exercises the assumption the assistant didn't
state out loud:

```python
def test_apply_discount_with_whole_number_percent():
    result = apply_discount(100, 20)
    assert 0 <= result <= 100
```

Run it. It fails badly — `apply_discount(100, 20)` returns `-1900`. You've
caught, with one independently-written test, the exact bug a green CI
pipeline waved through.

## Guardrail

Human-in-the-loop as a non-negotiable default. No AI-generated code merges
without a human reading it line by line and writing at least one
**independent** test — one that doesn't share the same silent assumption as
the code it's checking.
