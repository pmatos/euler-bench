# Problem 955: Finding Triangles

A sequence $(a_n)\_{n \ge 0}$ starts with $a_0 = 3$ and for each $n \ge 0$,

- if $a_n$ is a **triangle number<span class="tooltiptext">A triangle number is a number of the form $m(m + 1)/2$ for some integer $m$.</span>**, then $a\_{n + 1} = a_n + 1$;
- otherwise, $a\_{n + 1} = 2a_n - a\_{n - 1} + 1$.

The sequence begins: $${\color{red}3}, 4, {\color{red}6}, 7, 9, 12, 16, {\color{red}21}, 22, 24, 27, 31, {\color{red}36}, 37, 39, 42, \dots$$ where triangle numbers are marked red.

The $10$th triangle number in the sequence is $a\_{2964} = 1439056$.  
Find the index $n$ such that $a_n$ is the $70$th triangle number in the sequence.

---

[Source: projecteuler.net/problem=955](https://projecteuler.net/problem=955)
