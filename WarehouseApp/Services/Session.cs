using WarehouseApp.Models;

namespace WarehouseApp.Services
{
    // Глобальное хранилище текущего пользователя
    public static class Session
    {
        public static User CurrentUser { get; set; }

        public static void Logout()
        {
            CurrentUser = null;
        }
    }
}