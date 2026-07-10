# Problem 742: Minimum Area of a Convex Grid Polygon

A <span class="dfn">symmetrical convex grid polygon</span> is a polygon such that:

- All its vertices have integer coordinates.
- All its internal angles are strictly smaller than $180^\circ$.
- It has both horizontal and vertical symmetry.

For example, the left polygon is a convex grid polygon which has neither horizontal nor vertical symmetry, while the right one is a valid symmetrical convex grid polygon with six vertices:

<div style="text-align:center;">

<img src="assets/0742_hexagons.jpg" class="dark_img" />

</div>

Define $A(N)$, the minimum area of a symmetrical convex grid polygon with $N$ vertices.

You are given $A(4) = 1$, $A(8) = 7$, $A(40) = 1039$ and $A(100) = 17473$.

Find $A(1000)$.

---

[Source: projecteuler.net/problem=742](https://projecteuler.net/problem=742)
