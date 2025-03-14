# Kolmogorov-Loveland betting strategies lose the Betting game on open sets 

Tomislav Petrović<br>March 6, 2025


#### Abstract

Whether Kolmogorov-Loveland randomness (KLR) is the same as MartinLöf randomness (MLR) is a major open problem in the study of algorithmic randomness. More general classes of betting strategies than Kolmogorov-Loveland ones have been studied in [8, 13, 12]. In each case it was proven that the class induces a notion of randomness equivalent to MLR. In all of those proofs, it was shown that the class contains a finite set of betting strategies such that for any given bound, when betting on a binary sequence contained in an effective open set of small enough measure, at least one of the betting strategies in the set earns capital larger than the bound. We show that the class of Kolmogorov-Loveland betting strategies does not have this property.


## 1 Introduction

Kolmogorov-Loveland randomness was first defined in [10] in terms of betting strategies that bet on the values of bits of an infinite binary sequence. Based on the values of bits it has seen so far, a betting strategy makes a bet by choosing a position to bet on next and placing some fraction of its capital on a guessed value of the bit at the chosen position as a wager. The value of the bit is then revealed, and the capital is updated. If the guess was wrong the wager is lost. If the guess was correct, the capital is increased by the wagered amount. A monotonic betting strategy must choose the positions on which to bet in increasing order, while the non-monotonic betting strategies can choose the positions in any order, adaptively (depending on the bits that were revealed so far). A betting strategy wins on the binary sequence if the supremum of capital over the sequence of bets is unbounded. A sequence is Kolmogorov-Loveland random (KLR) if no computable non-monotonic betting strategy wins on the sequence.

Computable non-monotonic betting strategies are also called KolmogorovLoveland betting strategies. Both Kolmogorov in [3] and Loveland in [5] considered non-monotonic choice of positions. However, they looked at the frequency

of 1 s over the chosen positions to define a version of randomness that is nowadays called Kolmogorov-Loveland stochasticity.

In this paper, we will consider only Martin-Löf randomness ([6]) with respect to the uniform (Lebesgue) measure, $\lambda$. With this in mind, we give a brief definition. An effective open set is a set of sequences that have a prefix in a computable enumeration of strings. A Martin-Löf randomness test is a computable enumeration of effective open sets called levels of the Martin-Löf test. The $k$ th level of the test has measure less than $2^{-k}$, and a sequence fails the test if it is contained in every level of the test. A sequence is Martin-Löf random (MLR) if it passes every Martin-Löf randomness test.

Whether the set of KLR sequences is the same as the set of MLR sequences is a well studied open question in the field of algorithmic randomness [4].

A set of betting strategies is called universal if for every non-MLR sequence it contains a strategy that wins on the sequence. We can now restate "is $\mathrm{KLR}=\mathrm{MLR}$ ?" as "is the set of Kolmogorov-Loveland betting strategies universal?". In fact, by a result in [9], we can consider just the total computable non-monotonic betting strategies since every partial strategy can be replaced by two total ones that win on the same sequences as the partial one.

For any betting strategy, making a bet consists of partitioning a set of sequences into two subsets and placing a wager on one of them. The outcome of a bet determines which subset contains the sequence the strategy is betting on. A non-monotonic strategy, when making a bet, partitions a set of sequences into two sets according to the value of the bit at a chosen position. In [8], more general betting strategies than the non-monotonic ones have been studied. A general betting strategy has more freedom in partitioning sets. When making a bet, the set determined by the outcome of a previous bet, $v$, can be split into any two chosen clopen sets $v_{0}, v_{1}$. The outcome of the bet determines in which of the two sets the sequence is, and the capital is updated in the following way. Suppose that the betting strategy wagers amount $w$ of current capital $c$ on $v_{0}$. If the sequence the strategy is betting on is in $v_{1}$, the updated capital is $c_{1}=c-w$. If the sequence is in $v_{0}$, the updated capital is $c_{0}=c+w \frac{\lambda\left(v_{1}\right)}{\lambda\left(v_{0}\right)}$. Note that the measure of $v_{0}, v_{1}$ does not have to be equal. It was shown in [8] that there is a single total computable general betting strategy that is universal.

The outcomes of an infinite sequence of successive bets determine an infinite sequence of nested sets. If the measure over the sequence of sets for some infinite succession of bets does not go to zero, we say that a betting strategy has atoms. It is easy to see that a universal betting strategy necessarily has atoms. An atomless computable betting strategy cannot be universal, since the sequence of outcomes of bets where wager was lost each time (to wit, the losing streak) then defines a ML-test - the sequences that fail the test at every level are non-MLR by definition, but the betting strategy does not win on them.

However, we can use van Lambalgen's theorem [14] to show that there are two atomless computable general betting strategies $A$ and $B$ that are universal (by Alexander Shen, personal communication). Let us encode a pair of sequences $(\alpha, \beta)$ as a single sequence $\gamma$ with $\alpha$ at even positions and $\beta$ at odd positions.

The betting strategy $B$ bets on odd positions like the universal betting strategy and, to be atomless, ocasionaly reads (wagers 0 capital on) even positions. The betting strategy $A$ bets on the even positions like the universal betting strategy with an oracle $\beta$, with the bits of the oracle obtained by reading from the odd positions. By van Lambalgen's theorem, $\gamma$ is non-MLR if $\beta$ is non-MLR (in which case strategy $B$ wins on $\gamma$ ), or, if $\alpha$ is non-MLR with $\beta$ as an oracle (in which case strategy $A$ wins on $\gamma$ ).

Furthermore, if we look more closely at the proof of Theorem 5.9. in [14], there is a pair of computable betting strategies $A$ and $B$ such that, given $n$, for every sequence in the $n$th level of the universal Martin-Löf test, $O_{n}$ (or any other given effective open set of measure less than $2^{-n}$ ), either strategy $A$ has supremum of capital larger than $(n+1)^{2}$ when betting on the sequence or strategy $B$ has supremum of capital larger than $2^{n} /(n+1)^{2}$.

Thus, the class of atomless betting strategies (called exhaustive betting strategies in [13]) contains a pair that, for a given bound on capital, when betting on a binary sequence in an effective open set of small enough measure, at least one of the betting strategies earns capital larger than the bound. Similarly, one can show the same for the class of balanced ([13]) or half-betting strategies ([12]). The class of general betting strategies, and, similarly, martingale processes of [2], [8], contains a single betting strategy with this property.

We contrast this with the main result of this paper. For every KolmogorovLoveland betting strategy we can compute a bound on the capital and construct an effective open set of arbitrarily small measure that contains a sequence such that every Kolmogorov-Loveland betting strategy, while betting on the sequence, will always have capital below its bound.

# 2 Notation 

The set of (finite binary) strings is denoted with $\{0,1\}^{*}$, the set of strings of length $\ell$ with $\{0,1\}^{\ell}$, and the set of (infinite binary) sequences with $\{0,1\}^{\infty}$. The length of string $s$ is denoted with $|s|$. The empty string, $\epsilon$, has length 0 . That is, $|\epsilon|=0$. If a string $s$ is a prefix of string (or sequence) $s^{\prime}$ we write $s \preceq s^{\prime}$. The binary value of a sequence $\sigma$ at position $p$ is denoted with $\sigma_{p}$. A set of sequences prefixed by some string $s$ is called a basic set and is denoted with $\widetilde{s}$. A union of basic sets is called an open set, its complement a closed set, and a union of finitely many basic sets is a clopen set (both open and closed). A union of disjoint sets is denoted with symbol $\sqcup$.

A restriction $r$ is a sequence of symbols 0,1 or $*$. The set of restrictions is denoted with $\{0,1, *\}^{\infty}$. We denote the symbol at position $p$ in restriction $r$ with $r_{p}$. An infinite binary sequence $\sigma$ is consistent with a restriction $r$ if at every position $p$ where $r_{p} \neq *, \sigma_{p}=r_{p}$. We denote the set of sequences consistent with restriction $r$ with $\widetilde{r}$, it is a closed set. For a set of restrictions $R, \widetilde{R}$ denotes the set of sequences that are consistent with any restriction in $R$.

If the restriction $r$ has $*$ at all but finitely many positions, we say that $r$ is a finite restriction. Note that in this case $\widetilde{r}$ is clopen. The empty restriction, $\zeta$,

has $*$ at all positions, and is consistent with every sequence.
Definition 2.1. We denote with $\lambda$ uniform (Lebesgue) measure on $\{0,1\}^{\infty}$. Furthermore, we will be measuring only basic sets and their unions. Let $s$ be a string, the measure of the basic set $\widetilde{s}$ is $2^{-|s|}$. Let $X$ be a union of disjoint basic sets, the measure of $X$ is the sum of measures of the basic sets.

Definition 2.2. Let $\rho$ be a partial function from strings to finite restrictions with these properties:

- The empty string, $\epsilon$, is mapped to the empty restriction, $\zeta$.
- If for some string $s$ and bit $b, \rho(s b)$ is defined then both $\rho(s)$ and $\rho(s \bar{b})$ are defined. These three restrictions are the same except at one position $p$ where $\rho(s)_{p}=*, \rho(s 0)_{p}=0$ and $\rho(s 1)_{p}=1$.

We will call $\rho$ a restriction function.
Let $\mu$ be a partial function from strings to non-negative reals such that:

- The empty string, $\epsilon$, is mapped to 1.
- If for some string $s$ and a bit $b, \mu(s b)$ is defined then both $\mu(s)$ and $\mu(s \bar{b})$ are defined, and $\mu(s)=\mu(s b)+\mu(s \bar{b})$.

We will call $\mu$ a mass function. If $\mu$ is defined on all strings on which $\rho$ is defined, we call the pair $(\rho, \mu)$ a non-monotonic betting strategy. We will say that the strategy is finite if the restriction function is defined for only finitely many strings. The strategy is computable if both $\rho$ and $\mu$ are computable. The Kolmogorov-Loveland betting strategies are precisely the computable nonmonotonic betting strategies.

For a string $s$, and a betting strategy $(\rho, \mu)$ we call the pair $(\rho(s), \mu(s))$ the betting outcome for $s$. A pair of betting outcomes for $s 0, s 1$ is called $a$ bet for $s$.

Sometimes it is more convenient to look at the ratio between mass assigned to $s$ and the measure of the set of sequences consistent with the restriction assigned to $s$, called the capital for $s$ and denoted with $c$. That is, $c(s)=$ $\mu(s) / \lambda(\hat{\rho}(s))=2^{|s|} \mu(s)$.

The maximum of capital over all prefixes of $s$ is the maximum of capital for $s$ and we denote it with $\bar{c}$. That is,

$$
\bar{c}(s)=\max _{s^{\prime} \leq s} c\left(s^{\prime}\right)
$$

The maximal capital that the strategy achieves when betting on $\gamma$, denoted $\hat{c}(\gamma)$, is the supremum of capital over the bets the strategy makes when betting on $\gamma$, that is,

$$
\hat{c}(\gamma)=\sup _{\{s: \gamma \in \hat{\rho}(s)\}} \bar{c}(s)
$$

. We say that the strategy wins on $\gamma$ if $\hat{c}(\gamma)$ is unbounded.
We can define a betting strategy incrementaly, bet by bet.

Definition 2.3. Let $B$ be a non-monotonic betting strategy. Let $s$ be a string for which the outcome is defined and the outcomes for $s 0, s 1$ are not defined. We will call $s$ a leaf-string of $B$ and the restriction $\rho(s)$ a leaf-restriction. Let $B^{\prime}$ be a non-monotonic betting strategy that is the same as $B$ for all strings, except that, additionally, it has defined outcomes for strings $s 0, s 1$. We will say that $B^{\prime}$ is obtained from $B$ by defining a bet for the leaf-string $s$. Let $B^{\prime}$ be a strategy obtained from $B$ by successively defining finitely many bets, we will denote this with $B \rightarrow B^{\prime}$.

We call a betting strategy that has a defined outcome only for the empty string an initial betting strategy.

Note that any betting strategy can be defined by starting with an initial betting strategy, and then successively defining bets.

We next define effective open sets.
Definition 2.4. An open set $O \subseteq\{0,1\}^{\infty}$ is effective if $O=\bigcup_{i} \tilde{f}(i)$, where $f$ is a computable map from natural numbers to strings.

# 3 Preliminaries 

We can now state the main result of this paper.
Theorem 1 (Main Theorem). For each Kolmogorov-Loveland betting strategy there is a computable bound and for all $k$ there is an effective open set of measure less than $2^{-k}$ such that the set contains a sequence on which the maximal achieved capital of any Kolmogorov-Loveland betting strategy is below the strategy's bound.

We will prove the main result by introducing a game called the Betting game on open sets that is played between two players, the Chooser and the Gambler. We show that if there is a computable winning strategy in the game for the Chooser then this implies the main result.

Definition 3.1. The Betting game on open sets is played between two players called the Chooser and the Gambler and has two parameters, a set of bounds on the maximal capital $H=\left\{h_{1}, h_{2}, \ldots\right\}$ and a size parameter $k$.

The Chooser will be choosing clopen sets, and in the entire game, the Chooser must choose a sequence of clopen sets such such that their union (an open set) has measure less than $2^{-k}$.

The Gambler starts the game with a countable set of initial non-monotonic betting strategies, denoted $\mathbf{B}_{0}=\left\{B_{1}^{0}, B_{2}^{0}, \ldots\right\}$. As the game progresses, the Gambler will be defining bets for the betting strategies with the goal to define strategies so that, for every sequence in the chosen clopen sets, there is at least one $n$ such that the $n$th betting strategy achieves a maximal capital of strictly more than the bound $h_{n}$ when betting on the sequence.

The game is played in turns. Let $B_{n}^{i-1}$ denote the Gambler's $n$th betting strategy at the beginning of $i$ th turn, and let $\mathbf{B}_{i-1}$ denote the entire set of

Gambler's betting strategies at the beginning of $i$ th turn, that is, $\mathbf{B}_{i-1}=$ $\left\{B_{1}^{i-1}, B_{2}^{i-1}, \ldots\right\}$. We write $\mathbf{B}_{i-1} \rightarrow \mathbf{B}_{i}$ to denote that for all $n$, we have $B_{n}^{i-1} \rightarrow B_{n}^{\prime}$.

In $i$ th turn of the game, the Chooser chooses a clopen set $C_{i}$ (can be empty) and reveals it to the Gambler. The Gambler then decides if he will define a new bet for one of his strategies and if so reveals this strategy and the new bet to the Chooser. Alternatively, the Gambler decides to define no new bets, and reveals this to the Chooser (in this case $\mathbf{B}_{i-1}=\mathbf{B}_{i}$ ).

We will say that the Gambler achieves the $i$ th goal if in some turn (say $j$ th), for every sequence in the chosen set $C_{i}$ there is some $n$ such that the betting strategy $B_{n}^{j}$ achieves maximal capital larger than $h_{n}$ when betting on the sequence.

The Gambler wins the game if every goal is eventually achieved, otherwise the Chooser wins.

The Chooser has a winning strategy for the Betting game, if there is some $H$ such that for any Gambler and every parameter $k$ the Chooser wins the game. We will say that the Chooser has a computable winning strategy for the Betting game if it has a winning strategy and for every $n$ the capital bound $h_{n}$ is computable and for all $i$ the clopen set of sequences $C_{i}$ is computable from $\mathbf{B}_{i-1}$.

Lemma 3.2. If the Chooser has a computable winning strategy in the Betting game, this implies the main result, Theorem 1.

Proof. Let $K=\left\{B_{1}, B_{2}, \ldots\right\}$ be the set of Kolmogorov-Loveland betting strategies. From $K$, we will define a Gambler $G$. The Gambler $G$ starts the game with initial betting strategies $\left\{B_{1}^{\prime}, B_{2}^{\prime}, \ldots\right\}$. In each turn, the Gambler $G$ runs the dovetailed computation of strategies in $K$ for one step and if in that step a betting strategy (say $B_{n}$ ) defines a bet then $B_{n}^{\prime}$ defines that same bet, and if not then $G^{\prime}$ does not define any new bets in this turn.

To prove the lemma we show that
Claim 3.3. If the Gambler $G^{\prime}$ loses the Betting game with parameters $H=$ $\left\{h_{1}, h_{2}, \ldots\right\}$ and $k$ against a Chooser, then there is a sequence in some chosen basic set such that for all $n$ the maximal achieved capital of $B_{n} \in K$ is less than $h_{n}$.

Proof by compactness. Let $\left(\rho_{n}, \mu_{n}\right)$ denote the restriction and mass function of the $n$th strategy, $B_{n}$, and let $c_{n}, \bar{c}_{n}, \bar{c}_{n}$ denote its capital, maximum capital and maximal achieved capital functions, respectively.

If for some sequence $\gamma, \bar{c}_{n}(\gamma)>h_{n}$ then there is a shortest string $s$ such that $\gamma$ is consistent with $\rho_{n}(s)$ and $\bar{c}_{n}(s)\left(=c_{n}(s)\right)$ is strictly larger than the capital bound for the $n$th strategy, $h_{n}$. Let $s_{1}, s_{2}, \ldots$ be the effective enumeration of such strings and let $O_{n}$ be the effective open set that contains sequences from clopen sets $\widetilde{\rho}_{n}\left(s_{1}\right), \widetilde{\rho}_{n}\left(s_{2}\right), \ldots$ Let $O$ be the (effective) open set that is the union of $O_{1}, O_{2}, \ldots$

By compactness, for any clopen set $C$ that is a subset of $O$ there are finitely many basic sets in the enumeration of $O$ such that their union contains $C$. In particular this is also true for the chosen clopen sets. Let $C_{i}$ be the clopen set chosen in the $i$ th turn. If for every sequence in $C_{i}$, some strategy from $K$ achieves maximum capital higher than its bound, then this happens after finitely many betting strategies have made finitely many bets, and the Gambler $G$ will in some turn define all of those bets for all of those strategies and achieve the $i$ th goal.

Therefore, the Gambler $G$ loses only if there is some turn $i$ and a sequence in $C_{i}$ such that for all $n$ the maximal achieved capital of the $n$th betting strategy in $K$ is less than $h_{n}$.

If the Chooser has a computable winning strategy, there is some computable set of capital bounds $H$ such that for any $k$, the set of chosen sequences is an effective open set of size less than $2^{-k}$. This set, by Claim 3.3, contains a sequence for which the maximal achieved capital of the $n$th strategy in $K$ is less than $n$th bound in $H$, for all $n$.

Definition 3.4. Let a non-monotonic betting strategy $(\rho, \mu)$ have the following property: for all strings $s$, if the betting outcome is defined for $s$ then the difference between maximal capital for $s$ and capital for $s$ is less than 2 , that is, $c(s) \geq \bar{c}(s)-2$. We say that such a betting strategy is conservative.

We will say that the Gambler in the Betting game is conservative if he defines bets so that the betting strategies defined by those bets are conservative.

For every betting strategy $B$, we can construct a conservative betting strategy $B^{\prime}$ that has the same restriction function, and has a mass function such that the maximum of capital of $B^{\prime}$ is logarithmic in the maximum of capital of $B$. The construction is in [1] attributed to [7], and in other papers is often referred to as winning "slowly-but-surely", and the strategy $B^{\prime}$ as $B$ "with savings". For completeness we will also give the definition here.

Definition 3.5. Let $B=(\rho, \mu)$ be a betting strategy and let $c$ denote its capital function, that is, for any $s$ for which the outcome is defined we have $\mu(s)=c(s) \lambda(\tilde{\rho}(s))$.

From $B$ we will construct a strategy $B^{\prime}$, that has a different capital function, $c^{\prime}$. The capital $c^{\prime}$ is defined as a sum of two functions, $c_{B}$ (the capital "in the bank") and $c_{P}$ (the capital "for play"). For the empty string the capital "for play" is 1 , and the capital "in the bank" is 0 . That is, $c_{P}(\epsilon)=1, c_{B}(\epsilon)=0$. The capital in the bank is never used for betting, the wagered capital comes out of the capital "for play". The fraction of the capital "for play" that is wagered in a bet is the same as the fraction of the entire capital, $c$, of the original strategy that gets wagered in a bet, and then, depending on the outcome, the "for play" capital gets increased or decreased. As soon as the "for play" capital becomes larger than 2, half of it is transfered to "the bank".

More formally, for any $s$ for which a bet is defined in the original betting strategy $B$, let $f$ denote the fraction of capital that is wagered, $w$ the wagered amount, and $b$ the guessed value of the bit, $f=w / c(s), w=c(s b)-c(s)$. Then

$$
\begin{gathered}
c_{P}(s b)= \begin{cases}\frac{(1+f)}{2} c_{P}(s) & \text { if }(1+f) c_{P}(s) \geq 2 \\
(1+f) c_{P}(s) & \text { otherwise }\end{cases} \\
c_{B}(s b) \begin{cases}c_{B}(s)+\frac{(1+f)}{2} c_{P}(s) & \text { if }(1+f) c_{P}(s) \geq 2 \\
c_{B}(s) & \text { otherwise }\end{cases}
\end{gathered}
$$

and

$$
\begin{gathered}
c_{P}(s \tilde{b})=(1-f) c_{P}(s) \\
c_{B}(s \tilde{b})=c_{B}(s)
\end{gathered}
$$

Let $c^{\prime}(s)=c_{P}(s)+c_{B}(s)$ and $\mu^{\prime}(s)=c^{\prime}(s) \lambda(\tilde{\mu}(s))$. We will say that the betting strategy $B^{\prime}=\left(\rho, \mu^{\prime}\right)$ is the betting strategy $B=(\rho, \mu)$ with savings.

For any $s$ for which a bet is defined in the original strategy $B$, we will say that the pair of betting outcomes $\left(\rho(s 0), \mu^{\prime}(s 0)\right),\left(\rho(s 1), \mu^{\prime}(s 1)\right)$ is a conservative version of the original bet $\left(\rho(s 0), \mu(s 0)),(\rho(s 1), \mu(s 1)\right)$.
Lemma 3.6. Let $B$ be a betting strategy and let $B^{\prime}$ be $B$ with savings. The strategy $B^{\prime}$ is conservative, and for all strings $s$ for which the outcome is defined in $B$, we will have that $c^{\prime}(s)>\log \bar{c}(s)-2$.
Proof. Let the capital of strategy $B^{\prime}$ be $c^{\prime}(s)=c_{P}(s)+c_{B}(s)$ as in Definition 3.5. We have that $c^{\prime}(s) \geq c_{B}(s)$. From the Definition 3.5, we have that for any $s, c_{P}(s) \in[0,2)$. Furthermore, since $c_{B}$ is non-decreasing, we have that for the maximum capital for $s, \bar{c}^{\prime}(s)<c_{B}(s)+2$. Therefore $\bar{c}^{\prime}(s)<c^{\prime}(s)+2$. That is, the strategy $B^{\prime}$ is conservative.

For the original strategy, $B$, and any sequence $\sigma$, let $s_{k}$ denote the shortest prefix of $\sigma$ such that $c\left(s_{k}\right) \geq 2^{k}$ (if such prefix exists). Since $s_{k}$ is the shortest prefix for which the capital is larger than the bound, $\bar{c}\left(s_{k}\right)=c\left(s_{k}\right)$.

For $s \prec s_{1}$ we will have that $c_{P}(s)=c(s)$ and $c_{B}(s)=0$. Assume that for some $k$ we have $c_{P}\left(s_{k}\right)=c\left(s_{k}\right) 2^{-k}$ and $c_{B}\left(s_{k}\right)=\sum_{i \leq k} c_{P}\left(s_{i}\right)$. For all $s_{k} \preceq s \prec s_{k+1}$ we will have $c_{P}(s)=c_{P}\left(s_{k}\right) \frac{c(s)}{c\left(s_{k}\right)}=c(s) 2^{-k}$ and $c_{B}(s)=c_{B}\left(s_{k}\right)$. For $s_{k+1}$, the capital $c\left(s_{k+1}\right) \geq 2^{k+1}$, the "for play" capital becomes larger than 2 , and half of it is transferred to "the bank", that is $c_{P}\left(s_{k+1}\right)=\frac{1}{2} c\left(s_{k+1}\right) 2^{-k}$ and $c_{B}\left(s_{k}\right)=c_{B}\left(s_{k}\right)+c_{P}\left(s_{k+1}\right)$. By induction, for all $k$ we have $c_{P}\left(s_{k}\right)=c\left(s_{k}\right) 2^{-k}$ and $c_{B}\left(s_{k}\right)=\sum_{i \leq k} c_{P}\left(s_{i}\right)$.

We have $c_{B}\left(s_{k}\right)=\sum_{i \leq k} c\left(s_{i}\right) 2^{-i} \geq k>\log \bar{c}\left(s_{k}\right)-1$. Since for all $s_{k} \prec s \prec$ $s_{k+1}, \bar{c}(s)<2 \bar{c}\left(s_{k}\right)$, we have that $\log \bar{c}(s)<\log \bar{c}\left(s_{k}\right)+1$, and therefore, for all $s$ we have $c^{\prime}(s) \geq c_{B}(s)>\log \bar{c}(s)-2$.

Lemma 3.7. If the Chooser has a computable winning strategy in the Betting game when playing against conservative Gamblers, then the Chooser also has a computable winning strategy in the Betting game (that is, against any kind of Gambler).

Proof. Let $G$ be any Gambler, and let $G^{\prime}$ be a Gambler that defines the same strategies as $G$ but with savings. Suppose that the Chooser has a computable winning strategy in the Betting game when playing against a conservative Gambler. Then there is some computably enumerable set of bounds $H^{\prime}=$ $\left\{h_{1}^{\prime}, h_{2}^{\prime}, \ldots\right\}$ assigned to strategies defined by $G^{\prime}, \mathbf{B}^{\prime}=\left\{B_{1}^{\prime}, B_{2}^{\prime}, \ldots\right\}$, such that the Chooser chooses a set in the game against $G^{\prime}$ with some size parameter $k$, that contains a sequence on which none of the strategies constructed by $G^{\prime}$ achieve maximal capital larger than their bound. For every $n$ the $n$th strategy of $G, B_{n}$, by Lemma 3.6, achieves on that same sequence a maximal capital smaller than $h_{n}=2^{h_{n}^{\prime}+2}$. Let $H=\left\{h_{1}, h_{2}, \ldots\right\}$ and for all $n, h_{n}=2^{h_{n}^{\prime}+2}$. The set of bounds $H$ is computably enumerable, and the Chooser wins in the game against $G$ with any size parameter $k$. That is, the Chooser has the same computable winning strategy in the Betting game when playing against any Gambler as the Chooser that plays against the conservative Gamblers, except that the capital bounds are exponentially larger.

Definition 3.8. The Chooser has a winning strategy with residue for the Betting game on open sets, if for some set of capital bounds $H=\left\{h_{1}, h_{2}, \ldots\right\}$ and every size parameter $k$ there is some $n$ such that for every Gambler the Chooser wins the game when only the first $n$ of Gambler's betting strategies are considered. That is, the chosen open set in the game has a subset, on which none of the first $n$ of Gamblers betting strategies achieve capital larger then their bounds when betting on any sequence in the subset. Additionally, this subset has measure that is larger than the sum $\sum_{i>n} 1 / h_{i}$.

Let $\mathbf{B}_{i}=\left\{B_{1}^{\prime}, B_{2}^{\prime}, \ldots\right\}$ denote the Gambler's betting strategies at the end of $i$ th turn, and let $\mathbf{B}_{i}^{1: n}=\left\{B_{1}^{\prime}, \ldots, B_{n}^{\prime}\right\}$ the first $n$ of those strategies. The Chooser's strategy is computable if $H$ is computable, $n$ is computable from $k$, and the chosen set in the $i$ th turn is computable from Gambler's first $n$ betting strategies at the end of the $(i-1)$ th turn, $\mathbf{B}_{i-1}^{1: n}$.

Lemma 3.9. Suppose that for some set of capital bounds $H$ and the size parameter $k$, the Chooser chooses an open set $C$ in the Betting game that has a subset $C^{\prime}$ that contains sequences on which the first $n$ Gambler's betting strategies do not achieve capital larger than their capital bounds and the measure of $C^{\prime}$ is larger than the sum $\sum_{i>n} 1 / h_{i}$. Then $C$ contains a sequence on which none of the Gambler's betting strategies achieve capital larger then their capital bound.

Proof. By assumption, the first $n$ betting strategies do not achieve capital larger than their bounds on any sequence in $C^{\prime}$. The size of a set of sequences on which the $i$ th betting strategy achieves capital larger than $h_{i}$ is at most $1 / h_{i}$, and the size of the set of sequences on which at least one of the strategies after the $n$th achieves capital larger than its bound is then at most $\sum_{i>n} 1 / h_{i}$. Since $\lambda\left(C^{\prime}\right)>\sum_{i>n} 1 / h_{i}, C^{\prime}$ must contain a sequence on which none of the strategies achieve capital larger than their bound.

In the next chapter we will prove a key proposition that will allow us to prove the main result.

# 4 Proof of the main theorem 

Proposition 4.1 (Key Proposition). The Chooser has a computable winning strategy with residue in the Betting game against conservative Gamblers.

We will construct a strategy for the Chooser that chooses clopen sets consisting of sequences that on a set of positions $I$ have the number of ones that has remainder $o$ when divided by natural number $m$. We will call such clopen sets modulo sets. The modulus $m$ remains the same throughout the Betting game, while set of positions $I$ and the remainder $o$ change.

Definition 4.2 (Modulo set). For any subset of positions $I$, modulus $m$ and remainder $o$, the set of strings whose number of ones on positions in $I$ modulo $m$ is $o$ is denoted with $\operatorname{Mod}(I, m, o)$, that is,
$\operatorname{Mod}(I, m, o)=\bigsqcup_{\{s: s \bmod m=o\}}\left\{\sigma \in\{0,1\}^{\infty}: \sum_{p \in I} \sigma_{p}=s\right\}$.
The modulo sets have the property that if the restriction has enough unrestricted positions in $I$, then the set of sequences consistent with the restriction is approximately independent of the modulo set (Corollary 4.10).

Definition 4.3. We will say that two reals $x, y$ are $\xi$-approximate, and write $x \approx_{\xi} y$ when $(1-\xi) y \leq x \leq \frac{1}{1-\xi} y$.

Definition 4.4. We say that a restriction $r$ is $\xi$-approximately independent of a set of sequences $M$ when $\lambda(M \cap \tilde{r}) \approx_{\xi} \lambda(M) \lambda(\tilde{r})$
Definition 4.5. For any restriction $r$ and any set of positions $I$ we denote the number of positions in $I$ that are not restricted by $r$ with $\mathrm{N}^{*}(r, I)$, that is,
$\mathrm{N}^{*}(r, I)=\left|\left\{p \in I: r_{p}=*\right\}\right|$.
Proposition 4.6. For any restriction $r$, modulus $m$ and $\xi<1$, if $N^{s}(r, I) \geq$ $\left(\frac{m}{\xi}\right)^{2}$ then for every remainder $o \in[0, m-1], \lambda(\operatorname{Mod}(I, m, o) \mid \tilde{r}) \approx_{\xi} \frac{1}{m}$.
Proof. Let $u$ be the number of positions in $I$ unrestricted by $r$ and let $j$ be the number of positions in $I$ that are restricted by $r$ to 1 . Let $S_{i}$ be the set of sequences that have value 1 in $j+i$ positions in $I$. Clearly,

$$
\widetilde{r} \text { intersects } S_{i} \text { if and only if } i \in[0, u]
$$

Furthermore, the measure of $S_{i}$, conditional on $\widetilde{r}$, is proportional to the number of ways we can restrict $u$ many positions so that $i$ many are restricted to value 1 and the rest, $u-i$ many, to 0 . More precisely,

$$
\lambda\left(S_{i} \mid \widetilde{r}\right)=\binom{u}{i} 2^{-u}
$$

For the central binomial coefficient we can find an upper bound in [11]:

$$
\binom{2 n}{n}<\frac{4^{n}}{\sqrt{\pi n}}
$$

Denote the measure of $S_{i}$, conditional on $\widetilde{r}$, with $f(i)$. By (1), for $i \notin[0, u]$, $f(i)=0$. By properties of binomial coefficents, for $i \in[0, u]$ :

$$
f(i) \text { is non-decreasing on }\left[0,\left\lfloor\frac{1}{2} u\right\rfloor\right] \text { and non-increasing on }\left[\left\lfloor\frac{1}{2} u\right\rfloor, u\right]
$$

. For the maximal value of $f$ we have:
Claim 4.7. $f\left(\left\lfloor\frac{1}{2} u\right\rfloor\right)<1 / \sqrt{u}$
Proof. If $u$ is even, $f\left(\left\lfloor\frac{1}{2} u\right\rfloor\right)=f\left(\frac{1}{2} u\right)=\binom{u}{u / 2} 2^{-u}$. By (3) this is less than $\frac{1}{\sqrt{\pi u}}<1 / \sqrt{u}$.

On the other hand, if $u$ is odd, $\left\lfloor\frac{1}{2} u\right\rfloor=(u-1) / 2$. From definition of binomial coefficient, $\binom{u}{(u-1) / 2}=\frac{1}{2}\binom{u+1}{(u+1) / 2}$ and we have $f((u-1) / 2)=\binom{u}{(u-1) / 2} 2^{-u}=$ $\frac{1}{2}\binom{u+1}{(u+1) / 2} 2^{-u}$. By (3) this is less than $\frac{1}{2} \frac{4^{(u+1) / 2}}{\sqrt{\pi(u+1)}} 2^{-u}=\frac{1}{\sqrt{\pi(u+1)}}<1 / \sqrt{u}$
Claim 4.8. Let $n_{1}, \ldots, n_{d}, \ldots, n_{z}$ be a sequence of $z$ non-negative numbers that is non-decreasing up to dth number, $n_{d}$, and non-increasing afterwards. That is, $n_{1} \leq \cdots \leq n_{d} \geq \cdots \geq n_{z}$. The difference between the sum of numbers with even indices and the numbers with odd indices is at most $n_{d}$.

Proof. We prove for the case when $d$ is odd and $z$ is even. The difference is then: $\sum_{i \in[1, z / 2]} n_{2 i-1}-n_{2 i}$ $=\left(\sum_{i \in[1,(d-1) / 2]} n_{2 i-1}-n_{2 i}\right)+n_{d}+\left(\sum_{i \in[(d+1) / 2, z / 2-1]} n_{2 i+1}-n_{2 i}\right)-n_{z}$. Both sums are at most 0 , and so is $n_{z}$, therefore the difference is at most $n_{d}$.

The other cases, when $d$ is even or $z$ is odd, can be reduced to the previous case by prepending 0 at the beginning of the number sequence or appending 0 at the end (or both).

Denote with $M_{o}$ the modulo set defined on set of positions $I$ with modulus $m$ and remainder $o$, that is, $M_{o}=\operatorname{Mod}(I, m, o)$. Let $N_{o}$ denote the set of all $i \in[0, u]$ such that $S_{i}$ intersects $M_{o}$, that is $(j+i) \bmod m=o$. We have that $\lambda\left(M_{o} \mid \widetilde{r}\right)=\sum_{i \in N_{o}} f(i)$.

Let $o, o^{\prime}$ be any two distinct remainders in $[0, m)$ and let $N$ be the sequence of numbers in $N_{o} \sqcup N_{o^{\prime}}$, in increasing order. For any two consecutive elements in $N$, one will be from $N_{o}$ and the other one from $N_{o^{\prime}}$, and since $N$ is a subsequence of $[0, u]$, by (4) and claims 4.7 and 4.8 , the difference between the sum of $f$ over $N_{o}$ and the sum of $f$ over $N_{o^{\prime}}$ is at most $1 / \sqrt{u}$. This implies that there is some real $g$ such that for every $o$ in $[0, m)$ the sum of $f$ over $N_{o}$ is in $[g, g+1 / \sqrt{u}]$.

Since the modulo sets $M_{0}, \ldots, M_{m-1}$ partition the set of sequences, we have $\sum_{o \in[0, m), i \in N_{o}} f(i)=1$. If $g<\frac{1}{m}-1 / \sqrt{u}$ then the sum $\sum_{o \in[0, m), i \in N_{o}} f(i)$ would be strictly less than 1 (a contradiction), and if $g>\frac{1}{m}$ this sum would be strictly more than 1 (a contradiction). Therefore $g \in\left[\frac{1}{m}-1 / \sqrt{u}, \frac{1}{m}\right]$, and we have that for every $o$ in $[0, m)$ the sum of $f$ over $N_{o}$ is between $\frac{1}{m}-1 / \sqrt{u}$ and $\frac{1}{m}+1 / \sqrt{u}$.

Since the sum of $f$ over $N_{o}$ is $\lambda\left(M_{o} \mid \widetilde{r}\right)$, and from the condition $\mathrm{N}^{*}(r, I) \geq$ $\left(\frac{m}{\xi}\right)^{2}$, we have $1 / \sqrt{u} \leq \frac{\xi}{m}$. Therefore $\lambda\left(M_{o} \mid \widetilde{r}\right)$ is between $\frac{1}{m}(1-\xi)$ and $\frac{1}{m}(1+\xi)$. This implies the result as $1+\xi \leq 1 /(1-\xi)$ for any $\xi<1$.

Corollary 4.9. Let $M$ be a modulo set defined on a set of positions $I$, with modulus $m$ and remainder o. That is, $M=\operatorname{Mod}(I, m, o)$. For any positive $\xi<1$, if $|I| \geq\left(\frac{m}{\xi}\right)^{2}$ then $\lambda(M) \approx_{\xi} \frac{1}{m}$
Proof. Let $r$ be the empty restriction, $r=\zeta$. Then $\tilde{r}$ is the set of all sequences and $\mathrm{N}^{*}(r, I)=|I|$. We have that $\mathrm{N}^{*}(r, I) \geq\left(\frac{m}{\xi}\right)^{2}$.

By Proposition 4.6, for any remainder $o$, we have $\lambda(\operatorname{Mod}(I, m, o)) \approx_{\xi} \frac{1}{m}$.
Corollary 4.10. Let $M$ be a modulo set defined on a set of positions $I$, with modulus $m$ and remainder o. That is, $M=\operatorname{Mod}(I, m, o)$. Let $r$ be a restriction that has more than $\left(\frac{m}{\xi}\right)^{2}$ unrestricted positions in $I$, for some positive $\xi<1 / 2$. Then $\tilde{r}$ is $2 \xi$-approximately independent of $M$.

Proof. By Proposition 4.6 we have that $\lambda(M \cap \tilde{r})$ is between $\frac{\lambda(\tilde{r})}{m}(1-\xi)$ and $\frac{\lambda(\tilde{r})}{m} \frac{1}{(1-\xi)}$. From Corollary 4.9 we have that the measure of $M$ is between $\frac{1}{m}(1-\xi)$ and $\frac{1}{m} \frac{1}{(1-\xi)}$. This implies that $\lambda(M \cap \tilde{r})$ is at least $\lambda(\tilde{r}) \lambda(M)(1-\xi)^{2}$ and at most $\lambda(\tilde{r}) \lambda(M) \frac{1}{(1-\xi)^{2}}$. Since $(1-2 \xi)$ is less than $(1-\xi)^{2}$, the result follows.

For a subset of positions $I$ we classify the restrictions according to the number of unrestricted positions in $I$.

Definition 4.11. A restriction $r$ is $(I, \phi)$-chubby if it has more than $\phi$ unrestricted positions in $I$, that is, $\mathrm{N}^{*}(r, I) \geq \phi$.

A restriction is $(I, \phi)$-slim if it is not $(I, \phi)$-chubby.
We will say that an $(I, \phi)$-slim restriction restricts $I$ entirely if it restricts all of the positions in $I$.

A restriction is $(I, \phi)$-lean if it is $(I, \phi)$-slim but does not restrict $I$ entirely.
We will also say that the set of sequences $\tilde{r}$ is $(I, \phi)$-chubby (or slim, or lean) if the restriction $r$ is is $(I, \phi)$-chubby (or slim, or lean).

Note that for a modulo set $M$ defined for positions $I$, modulus $m$ and a remainder $o$, if $\phi>\left(\frac{m}{\xi}\right)^{2}$, then the $(I, \phi)$-chubby restrictions are $2 \xi$-approximately independent of the modulo set $M$, and the restrictions that restrict $I$ entirely are either contained in $M$ or disjoint from it.

Let us look at the case when conservative Gambler defines bets of just one non-monotonic betting strategy. For a set of sequences $X$ and a finite betting strategy $B$, we will consider the expectation of capital, with respect to $\lambda$, conditional on $X$, over the leaf-restrictions of a betting strategy, or shortly, the expected capital of $B$ on $X$. That is, denoting the leaf-strings of $B$ with $L$, the expected capital of $B$ on $X$ is $\sum_{s \in L} \lambda(\widetilde{\rho}(s) \mid X) c(s)$. We can use the expected capital of $B$ on $X$ to upper bound the smallest capital over leaf-strings whose restriction intersects $X$.

If $B$ is conservative, we have that the expected capital of $B$ on $X$ also upper bounds the smallest maximum capital the finite betting strategy $B$ achieves when betting on sequences in $X$. Namely, if the expected capital of $B$ for $X$ is $c$ then there is a leaf-string $s$ for which the maximum of capital is less than $c+2$ and $\widetilde{\rho}(s)$ intersects $X$.

Let $B, B^{\prime}$ be finite conservative non-monotonic betting strategies and $B \rightarrow$ $B^{\prime}$. That is, $B^{\prime}$ is obtained from $B$ by defining some additional bets that are also conservative. Let $s$ be a leaf-string of $B$, and $S$ the set of leaf-strings of $B^{\prime}$ that have prefix $s$.

Suppose $\rho(s)$ is $(I, \phi)$-chubby. If restrictions $\rho^{\prime}\left(s^{\prime}\right)$ are also $(I, \phi)$-chubby for all $s^{\prime} \in S$, the modulo set $M$ is (approximately) independent of $\widetilde{\rho}^{\prime}\left(s^{\prime}\right)$ and the expected capital on sequences in $M \cap \widetilde{\rho}(s)$ remains (approximately) $c(s)$. In order to increase the expected capital on $M \cap \widetilde{\rho}(s)$ to (approximately) $\frac{1}{1-d} c(s)$, the Gambler must define new bets so that the measure of leaf-strings in $S$ that are assigned $(I, \phi)$-slim restrictions is at least $d \lambda(\widetilde{\rho}(s))$.

On the other hand, suppose $\rho(s)$ restricts $I$ entirely, and $\widetilde{\rho}(s)$ is a subset of $M$. Regardless of how the additional bets are defined, the expected capital of $B^{\prime}$ on $M \cap \rho(s)$ remains $c(s)$.

We can see that if the betting strategy $B$ has no $(I, \phi)$-lean restrictions, and $B^{\prime}$ with new bets increases the expected capital on $M$ by a factor of (approximately) $\frac{1}{1-d}$, then it must be that the measure of $(I, \phi)$-slim leaf-restrictions is increased by at least (approximately) $d$.

We can use essentially the same argument to show this is also true for the expectation of expected capitals when the Gambler has more than one betting strategy, the $i$ th one having probability of $2^{-i}$, and the set of sequences contained in $(I, \phi)$-lean restrictions can be non-empty, but small (Lemma 4.19).

Definition 4.12. Let $X$ be a set of sequences. For a betting strategy $B$, the expectation of capital, conditional on $X$, for the leaf-restrictions we will call in short the expected capital of $B$ on $X$. That is, denoting the leaf-strings of $B$ with $S_{B}$, the expected capital of $B$ on $X$ is $\sum_{s \in S_{B}} c_{B}(s) \lambda(\hat{\rho}(s) \mid X)$.

Let $\mathbf{B}=\left\{B_{1}, B_{2}, \ldots\right\}$ be a set of betting strategies that have finitely many bets defined and let the probability of the $i$ th betting strategy in $\mathbf{B}$ be $2^{-i}$. The expectation over the betting strategies in $\mathbf{B}$ of their expected capital on $X$, we call the expected earning for $\boldsymbol{B}$ on $X$ and denote it with $\operatorname{earn}_{\mathbf{B}}(X)$.

That is,

$$
\operatorname{earn}_{\mathbf{B}}(X)=\sum_{B_{i} \in \mathbf{B}, s \in S_{B_{i}}} 2^{-i} c_{B_{i}}(s) \lambda\left(\rho_{B_{i}}^{-}(s) \mid X\right)
$$

In the next four lemmas $(4.13,4.14,4.15,4.16)$ we prove some properties of the expected earning that we will use later.

Lemma 4.13. For any set of finite betting strategies $\boldsymbol{B}$ the expected earning on the entire set of sequences is less than 1.

Proof. For strategy $B$, the expected capital on the set of all sequences is $\sum_{s \in S_{B}} c_{B}(s) \lambda(\tilde{\rho}(s))=\sum_{s \in S_{B}} \mu_{B}(s)=1$.
The expected earning is the expectation of expected capitals, $\operatorname{earn}_{\mathbf{B}}\left(\{0,1\}^{\infty}\right)=\sum_{B_{i} \in \mathbf{B}} \sum_{s \in S_{B_{i}}} 2^{-i}$.

Lemma 4.14. For any set of finite betting strategies $\boldsymbol{B}$, and any set of sequences $X$ and its subset $X^{\prime}$, earn $_{B}\left(X^{\prime}\right) \leq \frac{\lambda(X)}{\lambda\left(X^{\prime}\right)} \operatorname{earn}_{B}(X)$.

Proof. We have $\operatorname{earn}_{\mathbf{B}}\left(X^{\prime}\right)=\frac{1}{\lambda\left(X^{\prime}\right)} \sum_{B_{i} \in \mathbf{B}} \sum_{s \in S_{B_{i}}} 2^{-i} c_{B_{i}}(s) \lambda\left(\tilde{\rho}(s) \cap X^{\prime}\right)$ $\leq \frac{1}{\lambda\left(X^{\prime}\right)} \sum_{B_{i} \in \mathbf{B}} \sum_{s \in S_{B_{i}}} 2^{-i} c_{B_{i}}(s) \lambda(\tilde{\rho}(s) \cap X)=\frac{\lambda(X)}{\lambda\left(X^{\prime}\right)} \operatorname{earn}_{\mathbf{B}}(X)$
Lemma 4.15. For every set of sequences $X$, any finite partition of $X$ and any set of finite betting strategies $\boldsymbol{B}$ there is a part in the partition such that the expected earning of $\boldsymbol{B}$ on the part is less than the expected earning of $\boldsymbol{B}$ on the set $X$.

Proof. The result immediately follows from the law of total expectation.
Lemma 4.16. Let $\boldsymbol{B}=\left\{B_{1}, B_{2}, \ldots\right\}$ be a countable set of finite betting strategies. Every set of sequences $X$ for any $d$ smaller than the measure of $X$ contains a subset $Y$ of measure more than $d$ such that for every strategy $B_{i} \in \boldsymbol{B}$ and every sequence in $Y$ the leaf-restriction that contains the sequence has capital less than $2^{q} \frac{\lambda(X)}{\lambda(X)-d} \operatorname{earn}_{B}(X)$.

Proof. Let $q=\frac{\lambda(X)}{\lambda(X)-d}$ and let $Z$ be the set of sequences in $X$ for which there is some betting strategy $B_{i} \in \mathbf{B}$ whose leaf-restriction that contains the sequence has capital strictly larger than $q 2^{i} \operatorname{earn}_{\mathbf{B}}(X)$.

We have that $\operatorname{earn}_{\mathbf{B}}(Z) \geq q \operatorname{earn}_{\mathbf{B}}(X)$. By Lemma 4.14, $\operatorname{earn}_{\mathbf{B}}(Z) \leq \frac{\lambda(X)}{\lambda(Z)} \operatorname{earn}_{\mathbf{B}}(X)$, and we have $\lambda(Z) \leq \frac{\lambda(X)}{q}=\lambda(X)-d$.

Let $Y=X \backslash Z$. The measure of $Y$ is larger than $d$, and for every sequence in $Y$ and every strategy $B_{i} \in \mathbf{B}$ the leaf-restriction that contains the sequence has capital less than $q 2^{i} \operatorname{earn}_{\mathbf{B}}(X)$.

Definition 4.17. A set where we allow multiple instances of elements is called a multi-set. The number of instances for an element in a multi-set is called the multiplicity of the element in the multi-set. A set is then a multi-set where each element has multiplicity 1 . We will be considering only multi-sets of finite restrictions.

The sum of measures of sets of sequences consistent with restrictions in the multi-set $R$ is denoted with $\lambda^{+}(R)$ and called the sum-size of $R$, that is,
$\lambda^{+}(R)=\sum_{r \in R} \lambda(\widetilde{r})$. The set of sequences that are consistent with any restriction in $R$ is denoted with $\widetilde{R}$.

A union of two multi-sets is called a join. The multiplicity of an element in the join of two multi-sets is the sum of multiplicities of the element in the two multi-sets.

For example, let $R$ be the join of leaf-restrictions of $n$ finite non-monotonic betting strategies. Then $\lambda^{+}(R)=n$ and $\lambda(\widetilde{R})=1$.

Definition 4.18. Let $B=(\rho, \mu)$ be a finite Kolmogorov-Loveland betting strategy, and $B^{\prime}=\left(\rho^{\prime}, \mu^{\prime}\right)$ a Kolmogorov-Loveland betting strategy obtained from $B$ by defining finitely many new bets, that is, $B \rightarrow B^{\prime}$. Let $s, s^{\prime}$ be leaf-strings of $B, B^{\prime}$ such that $s$ is a prefix of $s^{\prime}$. Denote with $r, r^{\prime}$ the restrictions $\rho(s), \rho^{\prime}\left(s^{\prime}\right)$.

If for some set of positions $I$ and number $\phi$ the restriction $r$ is $(I, \phi)$-chubby and the restriction $r^{\prime}$ is $(I, \phi)$-slim we will say that $r^{\prime}$ was $(I, \phi)$-slimmed down by new bets of $B^{\prime}$.

Lemma 4.19. Let $M=\operatorname{Mod}(I, m, o)$ be some modulo set and let $\phi>m^{2}$, $\xi=m / \sqrt{\phi}$.

Let $\boldsymbol{B}$ be a finite set of finite Kolmogorov-Loveland betting strategies, and let $\boldsymbol{B}^{\prime}$ be a set of Kolmogorov-Loveland betting strategies obtained from $\boldsymbol{B}$ by defining finitely many new bets, that is, $\boldsymbol{B} \rightarrow \boldsymbol{B}^{\prime}$.

Denote with $\Theta$ the multi-set of $(I, \phi)$-lean leaf-restrictions of strategies in $\boldsymbol{B}$.
Denote with $\Delta$ the multi-set of restrictions that were slimmed down by newly defined bets of strategies in $\boldsymbol{B}^{\prime}$.

Denote with $M^{\prime}$ the sequences in $M$ that are not consistent with any restriction in $\Delta$ or $\Theta$.

The expected earning for $\boldsymbol{B}^{\prime}$ on $M^{\prime}$, earn $\boldsymbol{B}^{\prime}\left(M^{\prime}\right)$ is at most $\frac{1}{(1-2 \xi)(1-\lambda(\Theta|M))-\lambda^{+}(\Delta)} \operatorname{earn}_{\boldsymbol{B}}(M)$.

Proof. Let $\mathbf{B}=\left\{B_{1}, \ldots, B_{n}\right\}, \mathbf{B}^{\prime}=\left\{B_{1}^{\prime}, \ldots, B_{n}^{\prime}\right\}$. Since $\mathbf{B} \rightarrow \mathbf{B}^{\prime}$, we also have $B_{i} \rightarrow B_{i}^{\prime}$. For $i \leq|\mathbf{B}|$, denote the restriction functions of $B_{i}, B_{i}^{\prime}$ with $\rho_{i}, \rho_{i}^{\prime}$, their mass functions with $\mu_{i}, \mu_{i}^{\prime}$ and capitals with $c_{i}, c_{i}^{\prime}$.

Let $S_{i}$ denote the leaf-strings of the betting strategy $B_{i}$ and let $S_{i}^{\prime}$ denote the leaf-strings of the betting strategy $B_{i}^{\prime}$.

Let $\Psi_{i}$ be the strings in $S_{i}$ that are assigned by $\rho_{i}$ restrictions that restrict $I$ entirely. Let $\Psi_{i}^{\prime}$ be the strings in $S_{i}^{\prime}$ that have a prefix in $\Psi_{i}$.
Claim 4.20. $\sum_{s^{\prime} \in \Psi_{i}^{\prime}} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M\right)=\sum_{s \in \Psi_{i}} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M)$.
Proof. A restriction $\rho(s), s \in \Psi_{i}$ restricts all positions in $I$ and $\tilde{\rho}(s)$ is either contained in $M$ or disjoint from it. This is also true for any restriction $\rho^{\prime}\left(s^{\prime}\right), s^{\prime} \in$ $\Psi_{i}^{\prime}$ and both values $\lambda\left(M \mid \tilde{\rho}^{\prime}\left(s^{\prime}\right)\right)$ and $\lambda\left(M \mid \tilde{\rho}(s)\right)$ are the same (they are either 0 or 1 ) when $s \preceq s^{\prime}$. Therefore,

$$
\begin{aligned}
& \sum_{s^{\prime} \in \Psi_{i}^{\prime}} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M\right) \\
= & \sum_{s^{\prime} \in \Psi_{i}^{\prime}} \mu_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(M \mid \tilde{\rho}^{\prime}\left(s^{\prime}\right)\right) \\
= & \sum_{s \in \Psi_{i}} \lambda\left(M \mid \tilde{\rho}(s)\right) \sum_{s^{\prime} \in \Psi_{i}^{\prime}, s \preceq s^{\prime}} \mu_{i}^{\prime}\left(s^{\prime}\right) \\
= & \sum_{s \in \Psi_{i}} \mu_{i}(s) \lambda\left(M \mid \tilde{\rho}(s)\right)=\sum_{s \in \Psi_{i}} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M)
\end{aligned}
$$

Let $\Phi_{i}, \Phi_{i}^{\prime}$ be the strings in $S_{i}, S_{i}^{\prime}$ that are assigned $(I, \phi)$-chubby restrictions by $\rho_{i}, \rho_{i}^{\prime}$, respectfully.
Claim 4.21. $\sum_{s^{\prime} \in \Phi_{i}^{\prime}} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M\right) \leq \frac{1}{(1-2 \xi)} \sum_{s \in \Phi_{i}} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M)$.

Proof. A string $s^{\prime} \in \Phi_{i}^{\prime}$ has a prefix $s \in \Phi_{i}$, and by Proposition 4.6, both values $\lambda\left(M \mid \tilde{\rho}^{\prime}\left(s^{\prime}\right)\right)$ and $\lambda(M \mid \tilde{\rho}(s))$ are $\xi$-approximately $\frac{1}{m}$. At the most extreme, one value is $1 /(1-\xi)$ times larger than $\frac{1}{m}$, and the other one is $1-\xi$ times smaller, implying the two values are $2 \xi-\xi^{2}$ (and therefore also $2 \xi$ ) approximate. We have:

$$
\begin{aligned}
& \sum_{s^{\prime} \in \Phi_{i}^{\prime}} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M\right) \\
= & \sum_{s^{\prime} \in \Phi_{i}^{\prime}} \mu_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(M \mid \tilde{\rho}^{\prime}\left(s^{\prime}\right)\right) \\
\approx & 2 \xi \sum_{s \in \Phi_{i}} \sum_{s^{\prime} \in \Phi_{i}^{\prime}, s \leq s^{\prime}} \mu_{i}^{\prime}\left(s^{\prime}\right) \lambda(M \mid \tilde{\rho}(s)) \\
= & \sum_{s \in \Phi_{i}} \lambda(M \mid \tilde{\rho}(s)) \sum_{s^{\prime} \in \Phi_{i}^{\prime}, s \leq s^{\prime}} \mu_{i}^{\prime}\left(s^{\prime}\right) \\
\leq & \sum_{s \in \Phi_{i}} \mu_{i}(s) \lambda(M \mid \tilde{\rho}(s)) \\
= & \sum_{s \in \Phi_{i}} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M)
\end{aligned}
$$

By claims $4.20,4.21$, for all $i \leq|\mathbf{B}|$,

$$
\sum_{s^{\prime} \in \Phi_{i}^{\prime} \cup \Psi_{i}^{\prime}} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M\right) \leq \frac{1}{(1-2 \xi)} \sum_{s \in \Phi_{i} \cup \Psi_{i}} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M)
$$

Let $\Delta_{i}$ denote the strings in $S_{i}^{\prime}$ that are assigned by $\rho_{i}^{\prime}$ a restriction that was slimmed down by new bets.

Let $\Theta_{i}$ be the leaf-strings that are assigned $(I, \phi)$-lean restrictions by $\rho_{i}$. Let $\Theta_{i}^{\prime}$ be the leaf-strings of $B_{i}^{\prime}$ that have a prefix in $\Theta_{i}$.

Since the restrictions are either $(I, \phi)$-chubby, $(I, \phi)$-lean or restrict $I$ entirely, we have $S_{i}=\Phi_{i} \sqcup \Theta_{i} \sqcup \Psi_{i}$.

A leaf-string in $\Phi_{i}$ has successors in $S_{i}^{\prime}$ that are assigned by $\rho_{i}^{\prime}$ restrictions that are either $(I, \phi)$-chubby or were slimmed down by new bets, therefore $S_{i}^{\prime}=\Phi_{i}^{\prime} \sqcup \Delta_{i} \sqcup \Theta_{i}^{\prime} \sqcup \Psi_{i}^{\prime}$.

The multi-set $\Delta$ is the join of $\bigcup_{s^{\prime} \in \Delta_{i}} \rho^{\prime}\left(s^{\prime}\right)$ over all $i \leq|\mathbf{B}|$, the multi-set $\Theta$ is the join of $\bigcup_{s \in \Theta_{i}} \rho_{i}(s)$ over all $i \leq|\mathbf{B}|$ and $M^{\prime}=M \backslash(\bar{\Delta} \cup \bar{\Theta})$.

The sequences in $M^{\prime}$ are consistent only with chubby leaf-restrictions of $B_{i}^{\prime}$ and the leaf-restrictions of $B_{i}$ that restrict $I$ entirely, that is, for any leaf-string $s^{\prime}$ in $\Delta_{i} \cup \Theta_{i}^{\prime}, \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M^{\prime}\right)=0$, and we have
$\lambda\left(M^{\prime}\right) \operatorname{earn}_{\mathbf{B}^{\prime}}\left(M^{\prime}\right)=\sum_{i \leq|\mathbf{B}|} \sum_{s^{\prime} \in \Phi_{i}^{\prime} \cup \Psi_{i}^{\prime}} 2^{-i} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M^{\prime}\right)$
Since $M^{\prime} \subseteq M$,
$\lambda\left(M^{\prime}\right) \operatorname{earn}_{\mathbf{B}^{\prime}}\left(M^{\prime}\right) \leq \sum_{i \leq|\mathbf{B}|} \sum_{s^{\prime} \in \Phi_{i}^{\prime} \cup \Psi_{i}^{\prime}} 2^{-i} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M\right)$
By (5):
$\sum_{s^{\prime} \in \Phi_{i}^{\prime} \cup \Psi_{i}^{\prime}} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M\right) \leq \frac{1}{1-2 \xi} \sum_{s \in \Phi_{i} \cup \Psi_{i}} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M)$
Since $\Phi_{i} \sqcup \Psi_{i}$ is a subset of all leaf-strings of strategy $B_{i}$ we have
$\sum_{s \in \Phi_{i} \cup \Psi_{i}} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M) \leq \sum_{s \in S_{i}} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M)$
Summing over $i$ we get:
$\leq \frac{\sum_{i \leq|\mathbf{B}|} \sum_{s^{\prime} \in \Phi_{i}^{\prime} \cup \Psi_{i}^{\prime}} 2^{-i} c_{i}^{\prime}\left(s^{\prime}\right) \lambda\left(\tilde{\rho}^{\prime}\left(s^{\prime}\right) \cap M\right)}{\frac{1}{1-2 \xi} \sum_{i \leq|\mathbf{B}|} \sum_{s \in S_{i}} 2^{-i} c_{i}(s) \lambda(\tilde{\rho}(s) \cap M)}$
$=\frac{1}{1-2 \xi} \lambda(M) \operatorname{earn}_{\mathbf{B}}(M)$. Therefore

$$
\lambda\left(M^{\prime}\right) \operatorname{earn}_{\mathbf{B}^{\prime}}\left(M^{\prime}\right) \leq \frac{1}{1-2 \xi} \lambda(M) \operatorname{earn}_{\mathbf{B}}(M)
$$

Since $\lambda\left(M^{\prime}\right) \geq \lambda(M)-\lambda(M \cap \bar{\Theta})-\lambda(M \cap \bar{\Delta})$, we have

$$
\frac{\lambda(M)}{\lambda\left(M^{\prime}\right)} \leq \frac{1}{1-\lambda(\bar{\Theta}|M|-\lambda(\bar{\Delta}|M)}
$$

Finally, $\operatorname{earn}_{\mathbf{B}^{\prime}}\left(M^{\prime}\right) \leq \frac{1}{(1-2 \xi)} \frac{1}{1-\lambda(\bar{\Theta}|M|-\lambda(\bar{\Delta}|M)} \operatorname{earn}_{\mathbf{B}}(M)$. The only thing left to prove is that

$$
\lambda(\bar{\Delta}|M) \leq \lambda^{+}(\Delta) /(1-2 \xi)
$$

Suppose that for some string $v$ that is a prefix of a slimmed-down leaf-string, the restriction $\rho_{i}^{\prime}(v)$ has exactly $\phi$ unrestricted positions. This restriction is still chubby, and if the strategy then bets on a position in $I$, both of its immediate successors $\rho^{\prime}(v 0), \rho^{\prime}(v 1)$ are slim. The sum over leaf-strings $s^{\prime}$ of $B_{i}^{\prime}$ that extend $v$ of $\lambda\left(\rho_{i}^{\prime}\left(s^{\prime}\right) \cap M\right)$ is equal to $\lambda\left(\rho_{i}^{\prime}(v) \cap M\right)$.

By Corollary 4.10, the restriction $\rho_{i}^{\prime}(v)$ is $2 \xi$-independent of $M$. Let $D_{i}$ denote the set of sequences consistent with the leaf-restrictions that were slimmeddown by new bets of strategy $B_{i}^{\prime}$. That is, $D_{i}=\bigsqcup_{s^{\prime} \in \Delta_{i}} \rho^{\prime}\left(s^{\prime}\right)$. The measure of $D_{i}$ conditional on $M$ is at most $\lambda\left(D_{i}\right) /(1-2 \xi)$. Since $\bar{\Delta}=\bigcup_{i \leq|\mathbf{B}|} D_{i}$, we have that $\lambda(\bar{\Delta}|M) \leq \sum_{i \leq|\mathbf{B}|} \lambda\left(D_{i} \mid M\right)$ which is less than $\lambda^{+}(\Delta) /(1-2 \xi)$.

In Lemma 4.19, we have shown that the Gambler, starting a turn of the betting game with a finite set of Komlogorov-Loveland betting strategies $\mathbf{B}$, in order to increase the expected earning on sequences in a modulo set defined on the set of positions $I$ with modulus $m<\sqrt{\phi}$, has to define new bets for the strategies that slim down a large multi-set of $(I, \phi)$-chubby leaf-restrictions of strategies in $\mathbf{B}$, under the condition that the multi-set of $(I, \phi)$-lean leafrestrictions of strategies in $\mathbf{B}$ is small.

Suppose that, to the contrary, the multi-set of $(I, \phi)$-lean leaf-restrictions of strategies in $\mathbf{B}$ is not small. We will show that, if $\phi$ is small compared to $I$, we can find a large subset of $I, I^{\prime}$, such that most of those $(I, \phi)$-lean leaf-restrictions restrict $I^{\prime}$ entirely.

Lemma 4.22. For any multi-set $R$ of $(I, \phi)$-slim restrictions and any positive $q<1$, there is some $I^{\prime} \subseteq I$ such that $\left|I^{\prime}\right| \geq q|I|$ and the sum-size of restrictions in $R$ that restrict $I^{\prime}$ is at least $\left(1-\phi q^{\prime}\right) \lambda^{+}(R)$, where $q^{\prime}=1 /\left(\left\lfloor\frac{|I|}{|q| I|!}\right\rfloor\right)$.

Proof. Let $\ell=\lceil q|I|\rceil, n=\left\lfloor\frac{|I|}{r}\right\rfloor$, and let $I_{1}, \ldots, I_{n}$ be disjoint consecutive subsets of $I$ with $\left|I_{i}\right|=\ell$.

For a set of positions $J$, let $L(J)$ denote the sum over all restrictions in the multiset $R$ of the product of the number of unrestricted positions in $J$ and the measure of the restriction. That is,
$L(J)=\sum_{r \in R} N^{*}(r, J) \lambda(\widetilde{r})$.
Suppose that the proposition is not true and for every subset of $I$ with $\ell$ elements, the sum-size of restrictions that have one (or more) unrestricted positions in the subset is more than $\phi q^{\prime} \lambda^{+}(R)$. This is also true for every $I^{\prime} \in\left\{I_{1} \ldots I_{n}\right\}$.

The sum-size of restrictions that have one (or more) positions in $I^{\prime}$ unrestricted is a lower bound for $L\left(I^{\prime}\right)$. Since $\left\{I_{1} \ldots I_{n}\right\}$ are disjoint subsets of $I$, $L(I) \geq \sum_{i \in[1, n]} L\left(I_{i}\right)$, and we have that $L(I) \geq n \phi q^{\prime} \lambda^{+}(R)$.

Since $q^{\prime}=\frac{1}{n}, L(I) \geq \phi \lambda^{+}(R)$. This implies that there is some restriction in $R$ with at least $\phi$ unrestricted positions, and $R$ therefore contains an $(I, \phi)$ chubby restriction, contrary to the assumption.

It will be easier to use the following corollary of the previous lemma as it does not have rounding.

Corollary 4.23. For any multi-set $R$ of $(I, \phi)$-slim restrictions and any $q$ between $\frac{3}{|I|}$ and $\frac{1}{4}$ there is some $I^{\prime} \subseteq I$ such that $\left|I^{\prime}\right| \geq q|I|$ and the sum-size of restrictions in $R$ that restrict $I^{\prime}$ is at least $(1-2 q \phi) \lambda^{+}(R)$.

Proof. It is enough to show that if $q \leq 1 / 4$ and $|I| \geq 3 / q$ then $1 /\left\lfloor\frac{|I|}{|q| I|!}\right\rfloor=q^{\prime} \leq$ $2 q$. The result then follows from Lemma 4.22.

We have:
$1 /\left\lfloor\frac{|I|}{|q| I|!}\right\rfloor<1 /\left(\frac{|I|}{q|I|+1}-1\right)=\frac{q|I|+1}{|I|-(q|I|+1)}$. We will find a bound on $|I|$ and $q$ so that this last term, $\frac{q|I|+1}{|I|-(q|I|+1)}$, is less than $2 q$.

We have:
$\frac{q|I|+1}{|I|-(q|I|+1)} \leq 2 q \Longleftrightarrow q|I|+1 \leq 2 q|I|-2 q^{2}|I|-2 q \Longleftrightarrow 1+2 q \leq q|I|-2 q^{2}|I|$ $\Longleftrightarrow \frac{1}{q} \frac{1+2 q}{1-2 q} \leq|I|$.

It is easy to see that this last inequality is true for any $|I| \geq 3 / q$ and $q \leq 1 / 4$.

Suppose that the sum-size of $(I, \phi)$-lean leaf-restrictions of a finite set of finite Kolmogorov-Loveland betting strategies is above some desired bound $\delta$. We can use Corollary 4.23 , setting $q=\delta / \phi$, to find a set of positions $I^{\prime} \subseteq I$ where most of the $(I, \phi)$-lean leaf-restrictions restrict $I^{\prime}$ entirely. The sum-size of the leaf-restrictions that restrict $I^{\prime}$ entirely is larger than the sum-size of the leaf-restrictions that restrict $I$ entirely by at least $\delta^{\prime}=\delta(1-2 \delta)$.

It could be that a lot of the $(I, \phi)$-chubby leaf-restrictions are $\left(I^{\prime}, \phi\right)$-lean. In this case we can again use Corollary 4.23 to find $I^{\prime \prime} \subset I^{\prime}$ where most of the $\left(I^{\prime}, \phi\right)$-lean leaf-restrictions restrict $I^{\prime \prime}$ entirely, and so on. However, this cannot go on forever as each time we find a new subset, the sum-size of the leaf-restrictions that restrict the entire subset is incremented by $\delta^{\prime}$ and at some point we would find a set of positions that is entirely restricted by all of the leaf-restrictions.

Lemma 4.24. Let $R$ be a multi-set of finite restrictions, $I$ a set of positions, and $\phi$ a bound on the number of unrestricted positions with $\phi \geq 2$. Let $x$ be the sum-size of restrictions in $R$ that restrict $I$ entirely. Let $\delta<1 / 2$ and $\delta^{\prime}=\delta(1-2 \delta)$. Let $g$ be the smallest integer such that $g \delta^{\prime}+x \geq \lambda^{+}(R)$. Let $q=\delta / \phi$.

If $|I|$ is larger than $(1 / q)^{q+2}$ then there is some positive integer $k \leq g$ and $I^{\prime} \subseteq I$ such that $\left|I^{\prime}\right| \geq q^{k}|I|$ and the sum-size of restrictions in $R$ that are $\left(I^{\prime}, \phi\right)$-lean is at most $\delta$, while the sum-size of restrictions in $R$ that restrict $I^{\prime}$ entirely is at least $x+k \delta^{\prime}$.

Proof. Let $\Theta$ be the multi-set of $(I, \phi)$-lean restrictions from $R$. If $\Theta$ already has sum-size smaller than $\delta$, then $I^{\prime}=I$. On the other hand, if $\Theta$ has sum-size larger than $\delta$, since $q=\delta / \phi \leq 1 / 4,|I| \geq(1 / q)^{2}$, and $\frac{3}{|I|} \leq 3 q^{2} \leq q$, we can use Corollary 4.23 to find some $I^{\prime}$ with $\left|I^{\prime}\right| \geq q|I|$, such that the sum-size of restrictions in $\Theta$ that restrict $I^{\prime}$ is at least $(1-2 \delta) \lambda^{+}(\Theta)$ which is larger than $\delta^{\prime}$. Let $x^{\prime}$ be the sum-size of restrictions that restrict $I^{\prime}$ entirely. Since the restrictions that restrict $I$ entirely, also restrict $I^{\prime}$ entirely, $x^{\prime} \geq x+\delta^{\prime}$.

Some of the $(I, \phi)$-chubby restrictions might be $\left(I^{\prime}, \phi\right)$-slim. If the multi-set of $\left(I^{\prime}, \phi\right)$-lean restrictions from $R$ has sum-size larger than $\delta$ we can repeat the same argument on $I^{\prime}$. This adds another $\delta^{\prime}$ to the sum-size of restrictions that restrict the set $I^{\prime \prime}$ with size larger than $q^{2}|I|$. We can keep repeating this until we find a subset with less than $\delta$ slim restrictions that do not restrict it. We are guaranteed that we will eventually find such subset, as after applying the argument $g$ many times, we find a set of positions such that the sum-size of restrictions that restrict it is $\lambda^{+}(R)$ and therefore the sum-size of the rest of the slim restrictions is zero.

Suppose that for some finite set of finite Kolmogorov-Loveland betting strategies $\mathbf{B}$, set of positions $I$ and the bound on the number of unrestricted positions $\phi$, the set of sequences consistent with $(I, \phi)$-lean leaf-restrictions of strategies in $\mathbf{B}$ is small. Then for any modulus $m$, the modulo sets defined on $I$ with remainders $0, \ldots, m-1$ partition the set of infinite binary sequences, and there must be some remainder $o$, such that the modulo set $\operatorname{Mod}(I, m, o)$ has both low earning and small intersection with the set of sequences consistent with $(I, \phi)$-lean leaf-restrictions.

Lemma 4.25. For any finite set of finite Kolmogorov-Loveland betting strategies $\boldsymbol{B}$, any set of sequences $\Theta$ with measure less than $\delta$, every modulus $m$ and bound $c>1$, there is a remainder o such that the expected earning for $\boldsymbol{B}$ on the modulo set $M=\operatorname{Mod}(I, m, o)$ is less than $1 /\left(1-\frac{1}{c}\right)$ and the measure of the intersection of $M$ with $\Theta$ is less than $c \delta \lambda(M)$. That is,
$\operatorname{earn}_{\boldsymbol{B}}(M) \leq 1 /\left(1-\frac{1}{c}\right)$, and
$\lambda(\Theta \mid M) \leq c \delta$
Proof. The family of modulo sets with different remainders partitions the set of sequences. The sum of measures of modulo sets for which the measure of $\Theta$, conditional on the modulo set, is larger than $c \lambda(\Theta)$ is at most $\frac{1}{c}$. Let $X$ denote the union of modulo sets for which the measure of $\Theta$, conditional on the modulo set is less than $c \delta$. We have that the measure of $X$ is at least $1-\frac{1}{c}$. By lemmas $4.13,4.14$ we have that $\operatorname{earn}_{\mathbf{B}}(X) \leq 1 /\left(1-\frac{1}{c}\right)$, and by Lemma 4.15 , for at least one of these modulo sets the expected earning is smaller than $1 /\left(1-\frac{1}{c}\right)$.

We will construct a computable winning strategy with residue for the Chooser in the Betting game against conservative Gamblers called the Modulo Chooser. We fix the set of capital bounds $H=\left\{h_{1}, h_{2}, \ldots\right\}$ so that $h_{i}=2^{i+5}$. Given the size parameter $k$, we will pick a large enough modulus $m$ and large enough number of strategies $n$. We will show that the Modulo Chooser, throughout the entire game chooses an open set of measure less than $2^{-k}$, and the measure of chosen sequences on which none of the first $n$ of Gambler's betting strategies achieve capital larger their respective capital bounds is more than $2^{-n}$, satisfying Definition 3.8 .

At the beginning of the first turn of the Betting game, the Chooser picks large enough $\phi, I_{1}$, and chooses the modulo set $M_{1}=\operatorname{Mod}\left(I_{1}, m, 0\right)$. Note that the leaf-restriction of the initial betting strategy is $\left(I_{1}, \phi\right)$-chubby since it is the empty restriction and does not restrict any positions, also the set of $\left(I_{1}, \phi\right)$-lean leaf-restrictions is empty. Therefore, before the Gambler has defined any bets, the expected earning on $M_{1}$ is less than 1 .

We can use Lemma 4.19, to show that the Gambler must define some additional bets for the betting strategies that bet on at least $\left|I_{1}\right|-\phi+1$ positions in $I_{1}$ to slim down the empty restriction, and furthermore, the sum-size of the multi-set of $\left(I_{1}, \phi\right)$-slim leaf-restrictions must be large.

If this does not happen, then by Lemma 4.16 there is a subset of $M_{1}$ of measure larger than $2^{-n}$ on which none of the Gambler's betting strategies achieve capital larger than their bound, and already with the first chosen set the Chooser wins the game.

On the other hand, if the Gambler does define new bets so that the the multiset of $\left(I_{1}, \phi\right)$-slim leaf-restrictions is large, then by Lemma 4.24 the Chooser can find a large $I_{2} \subseteq I_{1}$ such that the sum-size of $\left(I_{2}, \phi\right)$-lean leaf-restrictions is small enough, and the sum-size of leaf-restrictions that restrict $I_{2}$ entirely is larger than some amount $d$.

Next, by Lemma 4.25 the Chooser can find some remainder $o_{2}$, so that the modulo set $M_{2}=\operatorname{Mod}\left(I_{2}, m, o_{2}\right)$ has small intersection with sequences consistent with $\left(I_{2}, \phi\right)$-lean leaf-restrictions and has low expected earning. Again, low earning implies that there are sequences in $M_{2}$ on which the Gambler's betting strategies at the beginning of the second turn do not achieve capital higher than their bounds. Then, again by Lemma 4.19, the Gambler must define some additional bets so that the sum-size of the multi-set of $\left(I_{1}, \phi\right)$-slim leaf-restrictions is large, and so on.

After the Chooser chooses the $i$ th (nonempty) set we are guaranteed that either the Chooser wins the game or, when the Gambler has defined additional bets, we find some large set of positions on which the sum-size of the leafrestrictions that restrict this entire set is at least $i \cdot d$.

The game cannot go on forever as after the $(n / d)$ th set was chosen there would be some set of positions that is entirely restricted by all of the leafrestrictions, implying that the Gambler cannot increase earning on the modulo set chosen in the $(n / d+1)$ st turn and the Chooser certainly wins the game. Since $I_{1}$ was chosen large enough, and all of the $I_{1} \supseteq I_{2} \supseteq \cdots \supseteq I_{n / d+1}$ are large compared to the modulus $m$, all of the chosen modulo sets have measure

approximately $1 / m$. Since $m$ was chosen large enough the total size of the chosen sets is smaller than $2^{-k}$ (the bound given by the size parameter $k$ ).

We now give a formal definition of the Modulo Chooser.
Definition 4.26. We define a strategy for the Chooser in the Betting Game on open sets against conservative Gamblers called the Modulo Chooser.

Let the capital parameter be $H=\left\{h_{1}, h_{2}, \ldots\right\}$, with $h_{i}=2^{i+5}$, and let $k$ be the size parameter.

Let modulus $m$ be $2^{2(k+4)}$. Let the number of Gambler's strategies that are considered be $n=4+\log m$. Let the bound on the number of unrestricted positions be $\phi=64 m^{2}$. Let $\ell=(4 \phi)^{8 n+3}$.

The Modulo Chooser will be choosing modulo sets defined on some subset of the first $\ell$ positions with modulus $m$ and some remainder. In the first turn, the chosen modulo set is defined on entire interval of positions $I_{1}=[1, \ell]$ with modulus $m$ and remainder $o_{1}=0$, we denote this modulo set $M_{1}$.

Let $j_{i}$ denote the turn when the $i$ th modulo set, $M_{i}=\operatorname{Mod}\left(I_{i}, m, o_{i}\right)$, is chosen. Suppose that in turn $j_{i}$ and subsequent turns the Gambler defines new bets, and by the end of turn $t$ the sum-size of the restrictions that were $\left(I_{i}, \phi\right)$ slimmed down by the new bets for the first $n$ strategies becomes more than $3 / 8$. If, and only if, this happens the Modulo Chooser will choose the next modulo set, $M_{i+1}$, at the beginning of turn $j_{i+1}=t+1$, otherwise $j_{i+1}$ is undefined, and the Modulo Chooser does not choose any more (nonempty) sets. When choosing the $(i+1)$ st modulo set, the Modulo Chooser finds a subset of the first $\ell$ positions, $I_{i+1}$, with properties:
I. 1 Let $\Psi_{i}$ denote the multiset of leaf restrictions of strategies in $\mathbf{B}_{t}^{1: n}$ that restrict $I_{i+1}$ entirely. Let $z_{i}=8 \lambda^{+}\left(\Psi_{i}\right)$. The sum-size of $\Psi_{i}$ is more than $i / 8$ and the number of positions in $I_{i+1}$ is more than $\left(\frac{1}{4 \phi}\right)^{z_{i}} \ell$.
I. 2 Let $\Theta_{i}$ denote the multiset of leaf restrictions of strategies in $\mathbf{B}_{t}^{1: n}$ that are $\left(I_{i+1}, \phi\right)$-lean. The sum-size of $\Theta_{i}$ is less than $1 / 4$.

The Modulo Chooser then chooses a modulo set $M_{i+1}$ defined on the interval $I_{i+1}$, with modulo $m$ and a remainder $o_{i+1}$ with properties:
M. 1 The size, conditional on $M_{i+1}$, of the set of sequences contained in an $\left(I_{i+1}, \phi\right)$-lean leaf-restriction of any of the Gambler's betting strategies, after the bets have been made in turn $t$, is less than $3 / 8$. That is $\lambda\left(\widetilde{\Theta}_{i} \mid M_{i+1}\right) \leq$ $3 / 8$.
M. 2 The expected earning for $\mathbf{B}_{t}^{1: n}$ on the sequences in $M_{i+1}$ that are contained only in $\left(I_{i+1}, \phi\right)$-chubby leaf-restrictions of the Gambler's betting strategies is less than 3 .

We will now prove that the Modulo Chooser is a computable winning strategy with residue in the Betting game on open sets against conservative gamblers.

Proof of Proposition 4.1. We begin with the following claim.
Claim 4.27. For any Gambler, at the beginning of the turn $j_{i}$, when $i$ th modulo set is to be chosen, there is a modulo set $M_{i}=\left(I_{i}, m, o_{i}\right)$ such that the set of positions $I_{i}$ has properties I.1,I.2 and the remainder $o_{i}$ has properties M.1,M.2.

Proof. We prove by induction. In the first turn $I_{1}=[1, \ell], o_{1}=0$ and the chosen modulo set is $M_{1}=\operatorname{Mod}\left(I_{1}, m, o_{1}\right)$. Since the Gambler did not define any bets yet, all of the Kolmogorov-Loveland betting strategies are initial, and both $\Psi_{0}$ and $\Theta_{0}$ are empty. We have that I. 2 is satisfied since $\lambda^{+}\left(\Theta_{0}\right)=0$ I. 1 is satisfied since $\lambda^{+}\left(\Psi_{0}\right)=0, z_{0}=0$ and $\left|I_{i}\right|=\ell$. Properties M. 1 and M. 2 are also satisfied since $\lambda\left(\bar{\Theta}_{0} \mid M_{1}\right)=0$ and $\operatorname{earn}_{\mathbf{B}_{2}^{1 / n}}<1$.

For turns $t \in\left[j_{i}, j_{i+1}\right)$, denote with $\Delta_{t}$ the multi-set of leaf restrictions of strategies in $\mathbf{B}_{t}^{1 / n}$ that were $\left(I_{i}, \phi\right)$-slimmed down by bets defined in turns $j_{i}, \ldots, t$. If the $(i+1)$ st modulo set is to be chosen in turn $j_{i+1}$, then by definition, the sum-size of $\Delta_{j_{i+1}-1}$ is more than $3 / 8$. For brevity, denote with $\Delta^{i}$ the multi-set $\Delta_{j_{i+1}-1}$.

Assume that in turn $j_{i}$ the $i$ th chosen modulo set $M_{i}$ is defined on $I_{i}$ that has properties I.1,I.2, with a remainder $o_{i}$ that has properties M.1, M.2.

We next show that there is $I_{i+1}$ with properties I.1,I.2.
In case $\Theta_{i} \leq 1 / 4$ then the subset of restrictions in $\Delta^{i}$ that restrict $I_{i}$ entirely has sum-size at least $1 / 8$. The set of positions $I_{i+1}=I_{i}$ has property I. 2 since $\Theta_{i} \leq 1 / 4$, and property I. 1 since $\lambda^{+}\left(\Psi_{i}\right) \geq \lambda^{+}\left(\Psi_{i-1}\right)+1 / 8$.

In the other case, when $\Theta_{i}>1 / 4$, we can use Lemma 4.24. Let the sumsize of restrictions in $\Delta^{i}$ that restrict $I_{i}$ entirely be $y$. Let $R$ be the multiset of leaf restrictions of strategies in $\mathbf{B}_{t}^{1 / n}$. We have that $\lambda^{+}(R)=n$. Let $I=I_{i}, x=\lambda^{+}\left(\Psi_{i-1}\right)+y, \delta=1 / 4, \delta^{\prime}=\delta(1-2 \delta)=1 / 8 g=\lceil 8(n-x)\rceil$, $q=\delta / \phi=\frac{1}{4 \phi}$. By assumption, $I_{i}$ has property I. 1 and we have $x \geq \lambda^{+}\left(\Psi_{i-1}\right)=$ $z_{i-1} / 8 \geq(i-1) / 8$ and $|I| \geq\left(\frac{1}{4 \phi}\right)^{z_{i-1}} \ell \geq\left(\frac{1}{4 \phi}\right)^{8 x} \ell$. Since $\ell=(4 \phi)^{8 n+3}$ we have $|I| \geq(4 \phi)^{8(n-x)+3}$, and since $g \leq 8(n-x)+1$, we have $|I| \geq(1 / q)^{g+2}$. We have that $R, I, \phi, \delta, \delta^{\prime}, x, g, q$ satisfy the properties of Lemma 4.24. We also have that there is some positive integer $k \leq g$ and $I^{\prime} \subseteq I$ such that $\left|I^{\prime}\right| \geq q^{k}|I|$ and the sum-size of restrictions in $R$ that are $\left(I^{\prime}, \phi\right)$-lean is at most $\delta$, while the sum-size of restrictions in $R$ that restrict $I^{\prime}$ is at least $x+k / 8$. Let $I_{i+1}=I^{\prime}$. Since $\delta=1 / 4, I_{i+1}$ has property I.2. We have $z_{i} \geq 8 x+k \geq z_{i-1}+k$, and since $k \geq 1$, and $z_{i-1} \geq i-1, z_{i} \geq i$, that is, $\lambda^{+}\left(\Psi_{i}\right) \geq i / 8$. Furthermore, $\left|I_{i+1}\right| \geq\left(\frac{1}{4 \phi}\right)^{k}\left|I_{i}\right| \geq\left(\frac{1}{4 \phi}\right)^{k+z_{i-1}} \ell \geq\left(\frac{1}{4 \phi}\right)^{z_{i}} \ell$, and $I_{i+1}$ has property I.1.

We conclude that in both cases we can find $I_{i+1}$ with properties I.1,I.2.
Let $c=3 / 2$. By Lemma 4.25 there is some remainder $o_{i+1}$ such that for the modulo set $M_{i+1}=\operatorname{Mod}\left(I_{i+1}, m, o_{i+1}\right)$ we have $\operatorname{earn}_{\mathbf{B}_{1}^{1 / n}}\left(M_{i+1}\right) \leq 3$ and $\lambda\left(\tilde{\Theta}_{i} \mid M_{i+1}\right) \leq 3 / 8$. That is, $M_{i+1}$ has properties M.1,M.2.

Claim 4.28. The Modulo Chooser chooses at most $8 n+1$ modulo sets.

Proof. Suppose that the modulo set chooses $8 n+1$ modulo sets. For the modulo set $M_{8 n+1}=\operatorname{Mod}\left(I_{8 n+1}, m, o_{8 n+1}\right)$, by property $\mathbf{I . 1}$ the sum-size of the multiset of leaf restrictions that restrict $I_{8 n+1}$ entirely is $n$. That is, all of the leaf restrictions of strategies in $\mathbf{B}_{j 8 n+1-1}^{1: n}$ restrict $I_{8 n+1}$ entirely. But then, it is not possible to slim down any of those restrictions, and the condition for the next modulo set to be chosen can never be fulfilled.

Claim 4.29. The measure of every chosen modulo set is $1 / 8$-approximately $\frac{1}{m}$
Proof. For all $i$, the $i$ th modulo set $\operatorname{Mod}\left(I_{i}, m, o_{i}\right)$ is defined on set of positions $I_{i}$ that by property I. 1 has size of more than $\left(\frac{1}{4 \phi}\right)^{z_{i}} \ell$. Since the sum-size of leaf restrictions of $\mathbf{B}_{i}^{1: n}$, for any $t$, is at most $n, z_{i}$ is at most $8 n$, and we have that $\left|I_{i}\right| \geq\left(\frac{1}{4 \phi}\right)^{8 n} \ell=(4 \phi)^{3} \geq \phi=64 m^{2}$. Let $\xi=1 / 8$ so that $\left|I_{i}\right| \geq\left(\frac{m}{\xi}\right)^{2}$. We can now use Corollary 4.9 to bound the measure of the chosen modulo sets.

Claim 4.30. The sum of measures of the sets chosen by the Modulo Chooser with size parameter $k$ is less than $2^{-k}$

Proof. By Claim 4.28 the Modulo Chooser chooses at most $8 n+1$ modulo sets. By Claim 4.29, the measure of every chosen modulo set is less than $\frac{8}{m} \frac{1}{m}$. The sum of measures of the chosen sets is then less than $(8 n+1) \frac{7}{8} \frac{1}{m}$. By definition $n=4+\log m$ and $m=2^{2(k+4)}$, therefore

$$
\begin{aligned}
& (8 n+1) \frac{8}{2} \frac{1}{m} \\
= & \frac{8\left(8(4+2(k+4))+1\right)}{2} 2^{-2(k+4)} \\
= & \frac{2^{3} k+2^{8} \cdot 2^{2^{2}} \cdot 2^{3}}{4} 2^{-2(k+4)} \\
< & \frac{2^{3} k+2^{12}}{4} 2^{-2(k+4)}=\left[\left(2^{5} k+2^{8}\right) 2^{-k-8}\right] 2^{-k} . \text { This is less than } 2^{-k} \text {, for all } k .
\end{aligned}
$$

Claim 4.31. For any conservative Gambler, if the Modulo Chooser chooses finitely many modulo sets in the entire Betting game, the last chosen modulo set contains a subset of size $2^{-n}$ on which none of the first $n$ betting strategies achieve capital larger than the bound determined by the capital parameter $H$.

Proof. Let $M_{i}=\operatorname{Mod}\left(I_{i}, m, o_{i}\right)$ be the last chosen modulo set, chosen in turn $j_{i}$. Since the Modulo Chooser would choose another modulo set if in some turn $t \geq j_{i}$ the sum-size of $\Delta_{t}$ was larger than $3 / 8$ we have that for all $t \geq j_{i}$, $\lambda^{+}\left(\Delta_{t}\right)<3 / 8$.

For some $t \geq j_{i}$, let $M_{i}^{\prime}=M_{i} \backslash\left(\tilde{\Delta}_{t} \cup \tilde{\Theta}_{i-1}\right)$, that is, $M_{i}^{\prime}$ is the modulo set $M_{i}$ without sequences contained in leaf restrictions of strategies in $B_{t}^{1: n}$ that were slimmed down by bets defined in turns $j_{i}, \ldots, t$ and without sequences in leaf restrictions of strategies in $B_{j_{i-1}}^{1: n}$ that are $\left(I_{i}, \phi\right)$-lean. By Lemma 4.19, since $\phi>m^{2}, \operatorname{earn}_{\mathbf{B}_{1}^{1: n}}\left(M_{i}^{\prime}\right) \leq \frac{1}{(1-2 \xi)\left(1-\lambda\left(\tilde{\Theta}_{i-1}\left|M_{i}\right|\right)-\lambda^{+}\left(\Delta_{t}\right)}\operatorname{earn}_{\mathbf{B}_{j_{i-1}}^{1: n}}\left(M_{i}\right)\right.$, where $\xi=m / \sqrt{\phi}=1 / 8$. We have $\lambda^{+}\left(\Delta_{t}\right)<3 / 8$, by property M. $1 \lambda\left(\tilde{\Theta}_{i-1} \mid M_{i}\right) \leq$ $3 / 8$ and by property M. $2 \operatorname{earn}_{\mathbf{B}_{j_{i-1}}^{1: n}}\left(M_{i}\right) \leq 3$. Therefore, $\operatorname{earn}_{\mathbf{B}_{1}^{1: n}}\left(M_{i}^{\prime}\right) \leq$ $\frac{3}{3 / 4(1-3 / 8)-3 / 8}=32$. Furthermore, by inequalities (6),(7) in Lemma 4.19, the measure of $M_{i}^{\prime}$ is more than $\frac{1}{8} \lambda\left(M_{i}\right)$. Then by Claim $4.29, \lambda\left(M_{i}^{\prime}\right) \geq \frac{1}{8} \frac{7}{8} \frac{1}{m}=\frac{7}{64 m}$.

By Lemma 4.16, $M_{i}^{\prime}$ has a subset of size $2^{-n}$ such that for every $j \leq n$ and every sequence in the subset, the leaf restriction of the $j$ th betting strategy at the end of turn $t$ that contains the sequence has capital less than $2^{j} \frac{\pi T_{m}}{\pi T_{m}-2-n} 32$. As $n=4+\log m$, this is equal to $2^{j} \cdot \frac{3}{7} \cdot 32$ which is less than $2^{j+4}$. Finally, since the Gambler is conservative, this implies that $M_{i}$ contains a subset of size $2^{-n}$ such that for any sequence in the subset and for every $t$ and every $j \leq n$, the $j$ th betting strategy after turn $t$, achieves maximal capital smaller than $2^{j+4}+2$ when betting on the sequence. This is less than $h_{j}=2^{j+5}$.

We have shown in Claim 4.30 that the Modulo Chooser chooses a set of sequences that is smaller than $2^{-k}$. By Claim 4.28 only finitely many modulo sets are chosen throughout the game. Then by Claim 4.31 and Definition 3.8, the Modulo Chooser has a computable winning strategy with residue in the Betting game on open sets against conservative Gamblers.

We can now prove the main result.
Proof of Theorem 1. The main result, Theorem 1, follows from the key proposition, Proposition 4.1, by lemmas 3.9, 3.7, 3.2.

# References 

[1] Harry Buhrman, Dieter van Melkebeek, Kenneth W. Regan, Martin Strauss, and D. Sivakumar. A generalization of resource-bounded measure, with application to the BPP vs. EXP problem. Electron. Colloquium Comput. Complex., TR98-058, 1998.
[2] John M. Hitchcock and Jack H. Lutz. Why computational complexity requires stricter martingales. Theory Comput. Syst., 39(2):277-296, 2006.
[3] Andrei N. Kolmogorov. On tables of random numbers (reprinted from "Sankhya: The Indian Journal of Statistics", Series A, Vol. 25 Part 4, 1963). Theor. Comput. Sci., 207(2):387-395, 1998.
[4] Ming Li and Paul M. B. Vitányi. An Introduction to Kolmogorov Complexity and Its Applications, 4th Edition. Texts in Computer Science. Springer, 2019 .
[5] Donald Loveland. A new interpretation of the von Mises' concept of random sequence. Zeitschrift fur mathematische Logik und Grundlagen der Mathematik, 12(1):279-294, 1966.
[6] Per Martin-Löf. The definition of random sequences. Inf. Control., $9(6): 602-619,1966$.
[7] Elvira Mayordomo. Contributions to the study of resource-bounded measure. PhD thesis, Universitat Politècnica de Catalunya (UPC), 1994.

[8] Wolfgang Merkle, Nenad Mihailovic, and Theodore A. Slaman. Some results on effective randomness. Theory Comput. Syst., 39(5):707-721, 2006.
[9] Wolfgang Merkle, Joseph S. Miller, André Nies, Jan Reimann, and Frank Stephan. Kolmogorov-Loveland randomness and stochasticity. Ann. Pure Appl. Log., 138(1-3):183-210, 2006.
[10] Andrei A. Muchnik, Alexei L. Semenov, and Vladimir A. Uspensky. Mathematical metaphysics of randomness. Theor. Comput. Sci., 207(2):263-317, 1998.
[11] Noam D. Elkies. Upper limit on the central binomial coefficient. https://mathoverflow.net/questions/133732/upper-limit-on-the-central-binomial-coefficient. 2013. [Online; accessed 15-March-2024].
[12] Tomislav Petrović. A universal pair of $1 / 2$-betting strategies. Inf. Comput., 281:104703, 2021.
[13] Jason Rute. Computable randomness and betting for computable probability spaces. Math. Log. Q., 62(4-5):335-366, 2016.
[14] Michiel van Lambalgen. The axiomatization of randomness. J. Symb. Log., $55(3): 1143-1167,1990$.