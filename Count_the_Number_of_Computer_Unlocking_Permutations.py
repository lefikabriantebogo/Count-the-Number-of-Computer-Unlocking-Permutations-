class Solution(object):
    def countPermutations(self, complexity):
        """
        :type complexity: List[int]
        :rtype: int
        """
        MOD = 10**9 + 7
        n = len(complexity)
        if n == 1:
            return 1

        # List of (label, complexity) for computers 1 to n-1
        computers = [(i, complexity[i]) for i in range(1, n)]
        computers.sort(key=lambda x: x[1])  # sort by complexity ascending

        # Precompute factorial and invfactorial
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD

        invfact = [0] * (n + 1)
        invfact[n] = pow(fact[n], MOD - 2, MOD)
        for i in range(n - 1, -1, -1):
            invfact[i] = invfact[i + 1] * (i + 1) % MOD

        def binom(N, K):
            if K < 0 or K > N:
                return 0
            return fact[N] * invfact[K] % MOD * invfact[N - K] % MOD

        ans = 1
        placed = 1  # computer 0 is placed
        max_comp = complexity[0]  # current maximum complexity among unlocked

        i = 0
        while i < n - 1:
            curr_comp = computers[i][1]

            # If this complexity is not strictly greater than current max → impossible
            if curr_comp <= max_comp:
                return 0

            # Collect entire group with same complexity
            j = i
            while j < n - 1 and computers[j][1] == curr_comp:
                # Check labels are in increasing order within group
                if j > i and computers[j][0] < computers[j - 1][0]:
                    return 0  # labels not increasing → impossible
                j += 1

            size = j - i
            # Ways to interleave this group of size 'size' into 'placed' existing positions
            ans = ans * binom(placed + size - 1, size) % MOD

            placed += size
            max_comp = curr_comp  # now this complexity is achievable
            i = j

        return ans