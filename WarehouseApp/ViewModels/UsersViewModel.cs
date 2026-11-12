using System;
using System.Collections.ObjectModel;
using System.Windows;
using Microsoft.Data.SqlClient;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class UsersViewModel : ViewModelBase
    {
        // Поля поиска и списков
        private ObservableCollection<User> _users = new ObservableCollection<User>();
        private ObservableCollection<Role> _roles = new ObservableCollection<Role>();
        private string _searchText = "";
        
        // Поля формы создания
        public string NewLogin { get; set; }
        public string NewPassword { get; set; }
        public string NewFullName { get; set; }
        public Role SelectedRole { get; set; }

        public ObservableCollection<User> Users { get => _users; set { _users = value; OnPropertyChanged(); } }
        public ObservableCollection<Role> Roles { get => _roles; set { _roles = value; OnPropertyChanged(); } }
        
        public string SearchText 
        { 
            get => _searchText; 
            set { _searchText = value; OnPropertyChanged(); LoadData(); } 
        }

        public RelayCommand AddUserCommand { get; }
        public RelayCommand DeleteUserCommand { get; }

        public UsersViewModel()
        {
            AddUserCommand = new RelayCommand(o => ExecuteAddUser(), o => !string.IsNullOrEmpty(NewLogin) && !string.IsNullOrEmpty(NewPassword) && SelectedRole != null);
            DeleteUserCommand = new RelayCommand(o => ExecuteDeleteUser(o));
            LoadData();
        }

        public void LoadData()
        {
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    if (Roles.Count == 0) {
                        var cmdR = new SqlCommand("SELECT * FROM Roles", conn);
                        using (var r = cmdR.ExecuteReader())
                            while (r.Read()) Roles.Add(new Role { Id = (int)r["Id"], Name = r["Name"].ToString() });
                    }

                    Users.Clear();
                    string sql = @"SELECT u.*, r.Name as RoleName FROM Users u 
                                 JOIN Roles r ON u.RoleId = r.Id 
                                 WHERE u.Login LIKE @s OR u.FullName LIKE @s";
                    var cmdU = new SqlCommand(sql, conn);
                    cmdU.Parameters.AddWithValue("@s", $"%{SearchText}%");
                    using (var r = cmdU.ExecuteReader())
                        while (r.Read())
                            Users.Add(new User {
                                Id = (int)r["Id"], Login = r["Login"].ToString(),
                                FullName = r["FullName"].ToString(),
                                Role = new Role { Name = r["RoleName"].ToString() }
                            });
                }
            } catch (Exception ex) { MessageBox.Show(ex.Message); }
        }

        private void ExecuteAddUser()
        {
            try {
                // ВАЖНО: Хешируем пароль перед сохранением в базу данных
                string hashedPassword = SecurityHelper.HashPassword(NewPassword);

                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    string sql = "INSERT INTO Users (Login, Password, FullName, RoleId) VALUES (@l, @p, @f, @r)";
                    var cmd = new SqlCommand(sql, conn);
                    cmd.Parameters.AddWithValue("@l", NewLogin);
                    cmd.Parameters.AddWithValue("@p", hashedPassword); // Сохраняем хеш
                    cmd.Parameters.AddWithValue("@f", NewFullName);
                    cmd.Parameters.AddWithValue("@r", SelectedRole.Id);
                    cmd.ExecuteNonQuery();
                }
                
                // Очистка полей
                NewLogin = NewPassword = NewFullName = "";
                OnPropertyChanged(nameof(NewLogin)); 
                OnPropertyChanged(nameof(NewPassword)); 
                OnPropertyChanged(nameof(NewFullName));
                
                LoadData();
                MessageBox.Show("Пользователь успешно создан!");
            } catch (Exception ex) { MessageBox.Show("Ошибка при создании: " + ex.Message); }
        }

        private void ExecuteDeleteUser(object obj)
        {
            if (obj is User user && user.Login != "admin") {
                if (MessageBox.Show($"Удалить пользователя {user.Login}?", "Подтверждение", MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.Yes) {
                    using (var conn = DatabaseHelper.GetConnection()) {
                        conn.Open();
                        new SqlCommand($"DELETE FROM Users WHERE Id = {user.Id}", conn).ExecuteNonQuery();
                    }
                    LoadData();
                }
            }
        }
    }
}