namespace WarehouseApp.Services
{
    /// <summary>
    /// Контакты техподдержки. Замените значения на реальные данные вашей организации.
    /// </summary>
    public static class SupportInfo
    {
        public const string Phone = "+7 (000) 000-00-00";
        public const string Email = "support@example.com";
        public const string WorkingHours = "Пн-Пт, 9:00-18:00";

        public static readonly string[] Statuses = { "Новое", "В работе", "Закрыто" };

        public static string NextStatus(string current)
        {
            int i = Array.IndexOf(Statuses, current);
            return Statuses[(i + 1) % Statuses.Length];
        }
    }
}
