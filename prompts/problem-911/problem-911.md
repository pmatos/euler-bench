# Problem 911: Khinchin Exceptions

An irrational number $x$ can be uniquely expressed as a **continued fraction** $\[a_0; a_1,a_2,a_3,\dots\]$: $$ x=a\_{0}+\cfrac{1}{a_1+\cfrac{1}{a_2+\cfrac{1}{a_3+{\_\ddots}}}} $$where $a_0$ is an integer and $a_1,a_2,a_3,\dots$ are positive integers.

Define $k_j(x)$ to be the **geometric mean** of $a_1,a_2,\dots,a_j$.  
That is, $k_j(x)=(a_1a_2 \cdots a_j)^{1/j}$.  
Also define $k\_\infty(x)=\lim\_{j\to \infty} k_j(x)$.

Khinchin proved that **almost all** irrational numbers $x$ have the same value of $k\_\infty(x)\approx2.685452\dots$ known as **Khinchin's constant**. However, there are some exceptions to this rule.

For $n\geq 0$ define $$\rho_n = \sum\_{i=0}^{\infty} \frac{2^n}{2^{2^i}} $$For example $\rho_2$, with continued fraction beginning $\[3; 3, 1, 3, 4, 3, 1, 3,\dots\]$, has $k\_\infty(\rho_2)\approx2.059767$.

Find the geometric mean of $k\_{\infty}(\rho_n)$ for $0\leq n\leq 50$, giving your answer rounded to six digits after the decimal point.

---

[Source: projecteuler.net/problem=911](https://projecteuler.net/problem=911)
