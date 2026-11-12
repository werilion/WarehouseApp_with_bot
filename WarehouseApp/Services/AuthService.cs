using System;
using Microsoft.Data.SqlClient;
using WarehouseApp.Models;
using WarehouseApp.Infrastructure;

namespace WarehouseApp.Services
{
    public class AuthService
    {
        /// <summary>
        /// Авторизация пользователя с использованием хеширования пароля
        /// </summary>
        public User Login(string login, string password)
        {
            // 1. Хешируем введенный пользователем пароль
            string hashedInput = SecurityHelper.HashPassword(password);

            using (var conn = DatabaseHelper.GetConnection())
            {
                conn.Open();
                
                // 2. Ищем в базе пользователя, у которого совпадает логин И ХЕШ пароля
                string query = @"
                    SELECT u.*, r.Name as RoleName 
                    FROM Users u 
                    JOIN Roles r ON u.RoleId = r.Id 
                    WHERE u.Login = @login AND u.Password = @password";

                using (var cmd = new SqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@login", login);
                    cmd.Parameters.AddWithValue("@password", hashedInput); // Сравниваем хеш из БД с новым хешем

                    using (var reader = cmd.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            return new User
                            {
                                Id = (int)reader["Id"],
                                Login = reader["Login"].ToString(),
                                FullName = reader["FullName"].ToString(),
                                RoleId = (int)reader["RoleId"],
                                Role = new Role { Name = reader["RoleName"].ToString() }
                            };
                        }
                    }
                }
            }
            return null;
        }
    }
}