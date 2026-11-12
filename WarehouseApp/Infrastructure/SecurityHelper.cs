using System;
using System.Security.Cryptography;
using System.Text;

namespace WarehouseApp.Infrastructure
{
    /// <summary>
    /// Помощник для обеспечения безопасности данных
    /// </summary>
    public static class SecurityHelper
    {
        /// <summary>
        /// Преобразует строку пароля в криптографический хеш SHA-256
        /// </summary>
        public static string HashPassword(string password)
        {
            if (string.IsNullOrWhiteSpace(password)) return string.Empty;

            using (SHA256 sha256 = SHA256.Create())
            {
                // Преобразуем строку в массив байтов
                byte[] bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));

                // Собираем байты в шестнадцатеричную строку
                StringBuilder builder = new StringBuilder();
                foreach (byte b in bytes)
                {
                    builder.Append(b.ToString("x2"));
                }
                return builder.ToString();
            }
        }
    }
}