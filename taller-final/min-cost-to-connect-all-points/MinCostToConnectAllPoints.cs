public class Solution
{
    private int[] parent;
    private int[] rank;

    private int Find(int x)
    {
        while (parent[x] != x)
        {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    private bool Union(int a, int b)
    {
        int ra = Find(a), rb = Find(b);
        if (ra == rb) return false;
        if (rank[ra] < rank[rb]) (ra, rb) = (rb, ra);
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
        return true;
    }

    public int MinCostConnectPoints(int[][] points)
    {
        int n = points.Length;

        // Todas las aristas (peso Manhattan, extremos)
        var edges = new List<(int w, int a, int b)>();
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
            {
                int w = Math.Abs(points[i][0] - points[j][0])
                      + Math.Abs(points[i][1] - points[j][1]);
                edges.Add((w, i, j));
            }

        // Ordenar por peso
        edges.Sort((x, y) => x.w.CompareTo(y.w));

        // Union-Find
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        int total = 0, used = 0;
        foreach (var (w, a, b) in edges)
        {
            if (Union(a, b))
            {
                total += w;
                if (++used == n - 1) break;
            }
        }
        return total;
    }
}