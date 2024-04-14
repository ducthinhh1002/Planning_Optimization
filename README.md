# Planning Optimization Project, HUST, 20232

# Problem description

There are K trucks 1,2,…,K to transport N items (2D shape) 1, 2, …, N. Truck k  has the container size W[k] x  L[k]. Item i has size w[i] x  l[i] .  Items loaded in a truck can not overlap. The cost of using truck k is c[k]. Find a solution that load N items into K trucks such that the total cost of trucks used is minimal.
A solution is represented by t[i], x[i], y[i], and o[i] in which (x[i], y[i]) is the coordinate of item i loaded in truck t[i], o[i] = 1, if the item i is rotated 90 degree.
Input
Line 1: contains N and K (1 <= N, K <= 1000)
Line i+1 (i = 1,2,…,N) contains 2 integers  w[i] and l[i]  (1 <= w[i], l[i] <= 1000)
Line  1+N+k (k = 1,…, K) contains W[k], L[k] and c[k] (1 <= W[k], L[k] <= 1000, 1 <= c[k] <= 1000)
Output
Line i (i = 1, 2, . . ., N): write 4 integers i, t[i], x[i], y[i], o[i]

# Algorithms