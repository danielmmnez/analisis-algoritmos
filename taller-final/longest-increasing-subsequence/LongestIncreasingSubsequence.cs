public class Solution
{
    public int LengthOfLIS(int[] nums)
    {
        int n = nums.Length;
        var dp = new int[n];
        Array.Fill(dp, 1);
        int best = 1;

        for (int i = 1; i < n; i++)
        {
            for (int j = 0; j < i; j++)
            {
                if (nums[j] < nums[i])
                    dp[i] = Math.Max(dp[i], dp[j] + 1);
            }
            best = Math.Max(best, dp[i]);
        }
        return best;
    }
}