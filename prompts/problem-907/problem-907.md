# Problem 907: Stacking Cups

An infant's toy consists of $n$ cups, labelled $C_1,\dots,C_n$ in increasing order of size.

<img src="assets/0907_four_cups.png" height="162" alt="0907_four_cups.png" />

The cups may be stacked in various combinations and orientations to form towers. The cups are shaped such that the following means of stacking are possible:

- Nesting: $C_k$ may sit snugly inside $C\_{k+1}$.  
  <img src="assets/0907_nesting.png" height="150" alt="0907_nesting.png" />
- Base-to-base: $C\_{k+2}$ or $C\_{k-2}$ may sit, right-way-up, on top of an up-side-down $C_k$, with their bottoms fitting together snugly.  
  <img src="assets/0907_base_to_base.png" height="198" alt="0907_base_to_base.png" />
- Rim-to-rim: $C\_{k+2}$ or $C\_{k-2}$ may sit, up-side-down, on top of a right-way-up $C_k$, with their tops fitting together snugly.  
  <img src="assets/0907_rim_to_rim.png" height="198" alt="0907_rim_to_rim.png" />
- For the purposes of this problem, it is **not** permitted to stack **both** $C\_{k+2}$ and $C\_{k-2}$ rim-to-rim on top of $C_k$, despite the schematic diagrams appearing to allow it:  
  <img src="assets/0907_rim_to_rim_counter_example.png" height="267" alt="0907_rim_to_rim_counter_example.png" />  

Define $S(n)$ to be the number of ways to build a single tower using all $n$ cups according to the above rules.  
You are given $S(4)=12$, $S(8)=58$, and $S(20)=5560$.

Find $S(10^7)$, giving your answer modulo $1\\000\\000\\007$.

---

[Source: projecteuler.net/problem=907](https://projecteuler.net/problem=907)
