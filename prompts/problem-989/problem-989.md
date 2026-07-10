# Problem 989: Fibonacci Sum

Write $F_n$ for the $n$-th **Fibonacci number**, with $F_1 = F_2 = 1$ and $F\_{n+1} = F_n + F\_{n-1}$.

It is known that $F_n$ is very well approximated by $\varphi^n / \sqrt 5$, where $\varphi$, the golden ratio, is the positive root of the equation $x^2 = x+1$.

Let $G(n)$ be the number of distinct integers $0 \leq x \< n$ such that $x^2 \equiv x+1 \pmod n$.

You are given $\displaystyle\sum\_{n=1}^{10^3}F_nG(n)\equiv 190950976\bmod(10^9+9)$.

Find $\displaystyle\sum\_{n=1}^{10^{14}}F_nG(n)$, giving your answer modulo $10^9+9$.

---

[Source: projecteuler.net/problem=989](https://projecteuler.net/problem=989)
