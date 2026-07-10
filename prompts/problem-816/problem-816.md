# Problem 816: Shortest Distance Among Points

We create an array of points $P_n$ in a two dimensional plane using the following random number generator:  
$s_0=290797$  
$s\_{n+1}={s_n}^2 \bmod 50515093$  
  
$P_n=(s\_{2n},s\_{2n+1})$

Let $d(k)$ be the shortest distance of any two (distinct) points among $P_0, \cdots, P\_{k - 1}$.  
E.g. $d(14)=546446.466846479$.

Find $d(2000000)$. Give your answer rounded to $9$ places after the decimal point.

---

[Source: projecteuler.net/problem=816](https://projecteuler.net/problem=816)
