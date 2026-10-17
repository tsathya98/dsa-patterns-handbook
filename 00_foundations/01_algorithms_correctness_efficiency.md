# Algorithmic foundations: correctness, efficiency, and scaling

> **Topic:** Foundations of problem solving  
> **Cohort lecture:** Airtribe DSA, Session 1 (Aakash Verma)  
> **Core comparison:** Stopwatch time vs. elementary operation count  

## 1. What an algorithm is

An algorithm is a finite, step-by-step recipe that turns an input into the right output.

A working algorithm needs four things:
1. Accepts valid input.
2. Produces the right output for every valid input.
3. Terminates in a finite number of steps without getting stuck in an infinite loop.
4. Scales cleanly when input size $N$ grows large.

## 2. Correctness vs. efficiency

* **Correctness:** Does it return the right answer?
* **Efficiency:** Does it still finish in reasonable time when the dataset grows by orders of magnitude?

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   THE PAYROLL PROCESSING ANALOGY                       │
├────────────────────────────────────────────────────────────────────────┤
│ Input:  Employee attendance, hourly rate, leaves, overtime, and taxes. │
│ Output: Exact paycheck credited to the bank account.                   │
├────────────────────────────────────────────────────────────────────────┤
│ • A naive algorithm works fine for 10 employees (takes 0.01 sec).      │
│ • When the company scales to 100,000 employees:                        │
│   - A slow O(N²) algorithm takes 3 hours to calculate payday.          │
│   - A linear O(N) algorithm takes 0.2 seconds.                         │
└────────────────────────────────────────────────────────────────────────┘
```

## 3. Why we never measure speed in milliseconds

Suppose two engineers run the exact same Python script:
* **Person A (New M-series Mac):** Finishes in 20 ms.
* **Person B (Older laptop):** Finishes in 44 ms.

The algorithm did not change speed. Wall-clock time shifts based on hardware and environment:
* Processor clock speed and core count
* Operating system and background processes
* CPU temperature and thermal throttling
* Programming language and interpreter overhead

```text
Wall-Clock Time (Stopwatch)   ──> Measures your laptop at this exact second.
Time Complexity (Big O)       ──> Measures how operation count grows with N.
```

Instead of timing with a stopwatch, we count **elementary operations** (single CPU steps):
* Variable assignments (`x = 5`) $\to \mathcal{O}(1)$
* Arithmetic (`a + b`, `a * b`) $\to \mathcal{O}(1)$
* Array index lookups (`arr[i]`) $\to \mathcal{O}(1)$
* Comparisons (`a > b`) $\to \mathcal{O}(1)$
* Swapping two variables (`a, b = b, a`) $\to \mathcal{O}(1)$
