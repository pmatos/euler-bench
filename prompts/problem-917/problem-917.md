# Problem 917: Minimal Path Using Additive Cost

The sequence $s_n$ is defined by $s_1 = 102022661$ and $s_n = s\_{n-1}^2 \bmod {998388889}$ for $n \> 1$.

Let $a_n = s\_{2n - 1}$ and $b_n = s\_{2n}$ for $n=1,2,...$

Define an $N \times N$ matrix whose values are $M\_{i,j} = a_i + b_j$.

Let $A(N)$ be the minimal path sum from $M\_{1,1}$ (top left) to $M\_{N,N}$ (bottom right), where each step is either right or down.

You are given $A(1) = 966774091$, $A(2) = 2388327490$ and $A(10) = 13389278727$.

Find $A(10^7)$.

---

[Source: projecteuler.net/problem=917](https://projecteuler.net/problem=917)
