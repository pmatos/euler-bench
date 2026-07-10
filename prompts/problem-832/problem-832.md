# Problem 832: Mex Sequence

In this problem $\oplus$ is used to represent the bitwise **exclusive or** of two numbers.  
Starting with blank paper repeatedly do the following:

1.  Write down the smallest positive integer $a$ which is currently not on the paper;
2.  Find the smallest positive integer $b$ such that neither $b$ nor $(a \oplus b)$ is currently on the paper. Then write down both $b$ and <span style="white-space:nowrap;">$(a \oplus b)$.</span>

After the first round $\\1,2,3\\$ will be written on the paper. In the second round $a=4$ and because <span style="white-space:nowrap;">$(4 \oplus 5)$,</span> $(4 \oplus 6)$ and $(4 \oplus 7)$ are all already written $b$ must be <span style="white-space:nowrap;">$8$.</span>

After $n$ rounds there will be $3n$ numbers on the paper. Their sum is denoted by <span style="white-space:nowrap;">$M(n)$.</span>  
For example, $M(10) = 642$ and <span style="white-space:nowrap;">$M(1000) = 5432148$.</span>

Find <span style="white-space:nowrap;">$M(10^{18})$.</span> Give your answer modulo <span style="white-space:nowrap;">$1\\000\\000\\007$.</span>

---

[Source: projecteuler.net/problem=832](https://projecteuler.net/problem=832)
