# Problem 529: $10$-substrings

A <span class="dfn">$10$-substring</span> of a number is a substring of its digits that sum to $10$. For example, the $10$-substrings of the number $3523014$ are:

- **<u>352</u>**3014
- 3**<u>523</u>**014
- 3**<u>5230</u>**14
- 35**<u>23014</u>**

A number is called <span class="dfn">$10$-substring-friendly</span> if every one of its digits belongs to a $10$-substring. For example, $3523014$ is $10$-substring-friendly, but $28546$ is not.

Let $T(n)$ be the number of $10$-substring-friendly numbers from $1$ to $10^n$ (inclusive).  
For example $T(2) = 9$ and $T(5) = 3492$.

Find $T(10^{18}) \bmod 1\\000\\000\\007$.

---

[Source: projecteuler.net/problem=529](https://projecteuler.net/problem=529)
