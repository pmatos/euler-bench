# Problem 996: Overtakes

There are $n$ tennis players on a leader board, from rank $1$ (highest) to rank $n$ (lowest).

Every day, a match is held between a pair of players with **adjacent** ranks. When the higher rank player wins, nothing happens; otherwise, their ranks are exchanged, and we call that match an *overtake* by the winning player.

After $k$ days, the players find that all of them are back to their initial ranks. They then count the number of overtakes by each player.

Here is an example with $3$ players, named $A, B, C$ from highest to lowest initial rank.

<div class="center">

<table class="grid center" style="width:100%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th>Match</th>
<th>Winner</th>
<th>Loser</th>
<th>Rank $1, 2, 3$<br />
after match</th>
<th colspan="3">Overtake counts</th>
</tr>
</thead>
<tbody>
<tr>
<th>$A$</th>
<th>$B$</th>
<th>$C$</th>
<th></th>
<th></th>
<th></th>
<th></th>
</tr>
&#10;<tr>
<td>$1*$</td>
<td>$C$</td>
<td>$B$</td>
<td>$A, C, B$</td>
<td>$0$</td>
<td>$0$</td>
<td>$1$</td>
</tr>
<tr>
<td>$2$</td>
<td>$C$</td>
<td>$B$</td>
<td>$A, C, B$</td>
<td>$0$</td>
<td>$0$</td>
<td>$1$</td>
</tr>
<tr>
<td>$3*$</td>
<td>$C$</td>
<td>$A$</td>
<td>$C, A, B$</td>
<td>$0$</td>
<td>$0$</td>
<td>$2$</td>
</tr>
<tr>
<td>$4$</td>
<td>$A$</td>
<td>$B$</td>
<td>$C, A, B$</td>
<td>$0$</td>
<td>$0$</td>
<td>$2$</td>
</tr>
<tr>
<td>$5*$</td>
<td>$A$</td>
<td>$C$</td>
<td>$A, C, B$</td>
<td>$1$</td>
<td>$0$</td>
<td>$2$</td>
</tr>
<tr>
<td>$6*$</td>
<td>$B$</td>
<td>$C$</td>
<td>$A, B, C$</td>
<td>$1$</td>
<td>$1$</td>
<td>$2$</td>
</tr>
</tbody>
</table>

</div>

The matches marked with $\*$ are overtakes.  
After $6$ days, all players are back to initial ranks with overtake counts $1, 1, 2$.

Let $F(n, k)$ be the number of possible $n$-tuples of overtake counts after $k$ days, assuming that all players are back to initial ranks.  
You are given $F(3, 4) = 8$ and $F(12, 34) = 2457178250$.

Find $F(123, 4567891) \bmod 1234567891$.

---

[Source: projecteuler.net/problem=996](https://projecteuler.net/problem=996)
