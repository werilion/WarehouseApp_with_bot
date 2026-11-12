using System;
using System.Collections.ObjectModel;
using System.Windows;
using Microsoft.Data.SqlClient;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class AddProductViewModel : ViewModelBase
    {
        // Поля для нового товара
        public string Name { get; set; }
        public string Description { get; set; }
        public decimal Price { get; set; }
        public string Unit { get; set; } = "шт.";
        public Category SelectedCategory { get; set; }

        public ObservableCollection<Category> Categories { get; set; } = new ObservableCollection<Category>();
        public RelayCommand SaveCommand { get; }

        public AddProductViewModel()
        {
            LoadCategories();
            SaveCommand = new RelayCommand(o => ExecuteSave(o), o => !string.IsNullOrEmpty(Name) && SelectedCategory != null);
        }

        private void LoadCategories()
        {
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    var cmd = new SqlCommand("SELECT * FROM Categories", conn);
                    using (var r = cmd.ExecuteReader())
                        while (r.Read()) 
                            Categories.Add(new Category { Id = (int)r["Id"], Name = r["Name"].ToString() });
                }
            } catch (Exception ex) { MessageBox.Show(ex.Message); }
        }

        private void ExecuteSave(object window)
        {
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    string sql = @"INSERT INTO Products (Name, CategoryId, Description, Price, Unit, Quantity) 
                                 VALUES (@n, @c, @d, @p, @u, 0)";
                    var cmd = new SqlCommand(sql, conn);
                    cmd.Parameters.AddWithValue("@n", Name);
                    cmd.Parameters.AddWithValue("@c", SelectedCategory.Id);
                    cmd.Parameters.AddWithValue("@d", (object)Description ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("@p", Price);
                    cmd.Parameters.AddWithValue("@u", Unit);
                    cmd.ExecuteNonQuery();
                }
                
                // Закрываем окно после сохранения
                if (window is Window w) {
                    w.DialogResult = true; // Сигнализируем об успехе
                    w.Close();
                }
            } catch (Exception ex) { MessageBox.Show("Ошибка сохранения: " + ex.Message); }
        }
    }
}