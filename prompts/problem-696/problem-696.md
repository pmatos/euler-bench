# Problem 696: Mahjong

The game of Mahjong is played with tiles belonging to $s$ <span class="dfn">suits</span>. Each tile also has a <span class="dfn">number</span> in the range $1\ldots n$, and for each suit/number combination there are exactly four indistinguishable tiles with that suit and number. (The real Mahjong game also contains other bonus tiles, but those will not feature in this problem.)

A <span class="dfn">winning hand</span> is a collection of $3t+2$ Tiles (where $t$ is a fixed integer) that can be arranged as $t$ <span class="dfn">Triples</span> and one <span class="dfn">Pair</span>, where:

- A <span class="dfn">Triple</span> is either a <span class="dfn">Chow</span> or a <span class="dfn">Pung</span>
- A <span class="dfn">Chow</span> is three tiles of the same suit and consecutive numbers
- A <span class="dfn">Pung</span> is three identical tiles (same suit and same number)
- A <span class="dfn">Pair</span> is two identical tiles (same suit and same number)

For example, here is a winning hand with $n=9$, $s=3$, $t=4$, consisting in this case of two Chows, two Pungs, and one Pair:

<div class="center">

![A winning Mahjong hand](assets/0696_mahjong_1.png)

</div>

Note that sometimes the same collection of tiles can be represented as $t$ Triples and one Pair in more than one way. This only counts as one winning hand. For example, this is considered to be the same winning hand as above, because it consists of the same tiles:

<div class="center">

![Alternative arrangement of the same hand](assets/0696_mahjong_2.png)

</div>

Let $w(n, s, t)$ be the number of distinct winning hands formed of $t$ Triples and one Pair, where there are $s$ suits available and tiles are numbered up to $n$.

For example, with a single suit and tiles numbered up to $4$, we have $w(4, 1, 1) = 20$: there are $12$ winning hands consisting of a Pung and a Pair, and another $8$ containing a Chow and a Pair. You are also given that $w(9, 1, 4) = 13259$, $w(9, 3, 4) = 5237550$, and $w(1000, 1000, 5) \equiv 107662178 \pmod{1\\000\\000\\007}$.

Find $w(10^8, 10^8, 30)$. Give your answer modulo $1\\000\\000\\007$.

---

[Source: projecteuler.net/problem=696](https://projecteuler.net/problem=696)
