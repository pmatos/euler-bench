# Problem 219: Skew-cost Coding

Let <span style="font-weight:bold;">A</span> and <span style="font-weight:bold;">B</span> be bit strings (sequences of 0's and 1's).  
If <span style="font-weight:bold;">A</span> is equal to the <span style="text-decoration:underline;">left</span>most length(<span style="font-weight:bold;">A</span>) bits of <span style="font-weight:bold;">B</span>, then <span style="font-weight:bold;">A</span> is said to be a <span style="font-style:italic;">prefix</span> of <span style="font-weight:bold;">B</span>.  
For example, 00110 is a prefix of <span style="text-decoration:underline;">00110</span>1001, but not of 00111 or 100110.

A <span style="font-style:italic;">prefix-free code of size</span> `n` is a collection of `n` distinct bit strings such that no string is a prefix of any other. For example, this is a prefix-free code of size 6:

0000, 0001, 001, 01, 10, 11

Now suppose that it costs one penny to transmit a '0' bit, but four pence to transmit a '1'.  
Then the total cost of the prefix-free code shown above is 35 pence, which happens to be the cheapest possible for the skewed pricing scheme in question.  
In short, we write Cost(6) = 35.

What is Cost(10<sup>9</sup>) ?

---

[Source: projecteuler.net/problem=219](https://projecteuler.net/problem=219)
