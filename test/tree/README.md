We need to build re-order atoms in product molecule
    to match order of that in reactant

We have mapping such that
Mapping[ReactantIndex] = ProductIndex
where
Mapping = [0, 2, 3, 4, 5, 6, 7, 8]

So it looks something like this:

P = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]
R = [a0, a2, a3, a4, a5, a6, a7, a8]
