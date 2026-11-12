using System;
using System.Collections.ObjectModel;
using System.Windows;
using Microsoft.Data.SqlClient;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class SettingsViewModel : ViewModelBase
    {
        private string _warehouseName;
        private string _warehouseAddress;
        private string _newCategoryName;

        public string WarehouseName { get => _warehouseName; set { _warehouseName = value; OnPropertyChanged(); } }
        public string WarehouseAddress { get => _warehouseAddress; set { _warehouseAddress = value; OnPropertyChanged(); } }
        public string NewCategoryName { get => _newCategoryName; set { _newCategoryName = value; OnPropertyChanged(); } }

        public ObservableCollection<Category> Categories { get; set; } = new ObservableCollection<Category>();

        public RelayCommand SaveGeneralSettingsCommand { get; }
        public RelayCommand AddCategoryCommand { get; }
        public RelayCommand DeleteCategoryCommand { get; }

        public SettingsViewModel()
        {
            LoadSettings();
            LoadCategories();

            SaveGeneralSettingsCommand = new RelayCommand(o => ExecuteSaveGeneral());
            AddCategoryCommand = new RelayCommand(o => ExecuteAddCategory(), o => !string.IsNullOrEmpty(NewCategoryName));
            DeleteCategoryCommand = new RelayCommand(o => ExecuteDeleteCategory(o));
        }

        private void LoadSettings()
        {
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    var cmd = new SqlCommand("SELECT * FROM SystemSettings WHERE Id = 1", conn);
                    using (var r = cmd.ExecuteReader())
                        if (r.Read()) {
                            WarehouseName = r["WarehouseName"].ToString();
                            WarehouseAddress = r["WarehouseAddress"].ToString();
                        }
                }
            } catch { /* Если таблицы нет, просто проигнорируем */ }
        }

        private void LoadCategories()
        {
            Categories.Clear();
            using (var conn = DatabaseHelper.GetConnection()) {
                conn.Open();
                var cmd = new SqlCommand("SELECT * FROM Categories", conn);
                using (var r = cmd.ExecuteReader())
                    while (r.Read()) Categories.Add(new Category { Id = (int)r["Id"], Name = r["Name"].ToString() });
            }
        }

        private void ExecuteSaveGeneral()
        {
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    var cmd = new SqlCommand("UPDATE SystemSettings SET WarehouseName = @n, WarehouseAddress = @a WHERE Id = 1", conn);
                    cmd.Parameters.AddWithValue("@n", WarehouseName);
                    cmd.Parameters.AddWithValue("@a", WarehouseAddress);
                    cmd.ExecuteNonQuery();
                    MessageBox.Show("Настройки организации обновлены!");
                }
            } catch (Exception ex) { MessageBox.Show(ex.Message); }
        }

        private void ExecuteAddCategory()
        {
            using (var conn = DatabaseHelper.GetConnection()) {
                conn.Open();
                new SqlCommand($"INSERT INTO Categories (Name) VALUES (N'{NewCategoryName}')", conn).ExecuteNonQuery();
            }
            NewCategoryName = ""; OnPropertyChanged(nameof(NewCategoryName));
            LoadCategories();
        }

        private void ExecuteDeleteCategory(object obj)
        {
            if (obj is Category c) {
                try {
                    using (var conn = DatabaseHelper.GetConnection()) {
                        conn.Open();
                        new SqlCommand($"DELETE FROM Categories WHERE Id = {c.Id}", conn).ExecuteNonQuery();
                    }
                    LoadCategories();
                } catch { MessageBox.Show("Нельзя удалить категорию, в которой есть товары!"); }
            }
        }
    }
}