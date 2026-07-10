# Problem 541: Divisibility of Harmonic Number Denominators

The $n$<sup>th</sup> **harmonic number** $H_n$ is defined as the sum of the multiplicative inverses of the first $n$ positive integers, and can be written as a **reduced fraction** $a_n/b_n$.  
$H_n = \displaystyle \sum\_{k=1}^n \frac 1 k = \frac {a_n} {b_n}$, with $\gcd(a_n, b_n)=1$.

Let $M(p)$ be the largest value of $n$ such that $b_n$ is not divisible by $p$.

For example, $M(3) = 68$ because $H\_{68} = \frac {a\_{68}} {b\_{68}} = \frac {14094018321907827923954201611} {2933773379069966367528193600}$, $b\_{68}=2933773379069966367528193600$ is not divisible by $3$, but all larger harmonic numbers have denominators divisible by $3$.

You are given $M(7) = 719102$.

Find $M(137)$.

---

[Source: projecteuler.net/problem=541](https://projecteuler.net/problem=541)
