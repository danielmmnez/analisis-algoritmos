public class Solution
{
    public int NetworkDelayTime(int[][] times, int n, int k)
    {
        // Lista de adyacencia (índices 1..n)
        var graph = new List<(int to, int w)>[n + 1];
        for (int i = 1; i <= n; i++) graph[i] = new List<(int, int)>();
        foreach (var t in times)
            graph[t[0]].Add((t[1], t[2]));

        // Distancias: infinito salvo el origen
        var dist = new int[n + 1];
        Array.Fill(dist, int.MaxValue);
        dist[k] = 0;

        // Heap: elemento = nodo, prioridad = distancia tentativa
        var pq = new PriorityQueue<int, int>();
        pq.Enqueue(k, 0);

        while (pq.TryDequeue(out int u, out int d))
        {
            if (d > dist[u]) continue;          // entrada vieja: ya hay una mejor

            foreach (var (v, w) in graph[u])
            {
                int nd = d + w;
                if (nd < dist[v])
                {
                    dist[v] = nd;
                    pq.Enqueue(v, nd);
                }
            }
        }

        // El que más tarda manda; si alguno quedó en infinito, -1
        int ans = 0;
        for (int i = 1; i <= n; i++)
        {
            if (dist[i] == int.MaxValue) return -1;
            ans = Math.Max(ans, dist[i]);
        }
        return ans;
    }
}