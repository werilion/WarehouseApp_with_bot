using System;
using System.Collections.ObjectModel;
using System.Windows;
using Microsoft.Data.SqlClient;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class InventoryViewModel : ViewModelBase
    {
        private string _searchText = "";
        public ObservableCollection<Product> Products { get; set; } = new ObservableCollection<Product>();

        public string SearchText 
        { 
            get => _searchText; 
            set { _searchText = value; OnPropertyChanged(); LoadData(); } 
        }

        public RelayCommand SaveChangesCommand { get; }

        public InventoryViewModel()
        {
            LoadData();
            SaveChangesCommand = new RelayCommand(o => ExecuteSave());
        }

        public void LoadData()
        {
            Products.Clear();
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    var cmd = new SqlCommand("SELECT * FROM Products WHERE Name LIKE @s", conn);
                    cmd.Parameters.AddWithValue("@s", $"%{SearchText}%");
                    using (var r = cmd.ExecuteReader())
                        while (r.Read())
                            Products.Add(new Product { 
                                Id = (int)r["Id"], 
                                Name = r["Name"].ToString(), 
                                Quantity = (decimal)r["Quantity"], 
                                Unit = r["Unit"].ToString() 
                            });
                }
            } catch (Exception ex) { MessageBox.Show(ex.Message); }
        }

        private void ExecuteSave()
        {
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    foreach (var p in Products) {
                        string sql = "UPDATE Products SET Quantity = @q WHERE Id = @id";
                        using (var cmd = new SqlCommand(sql, conn)) {
                            // Используем явные типы для исключения ошибок конвертации
                            cmd.Parameters.Add(new SqlParameter("@q", System.Data.SqlDbType.Decimal) { Value = p.Quantity });
                            cmd.Parameters.Add(new SqlParameter("@id", System.Data.SqlDbType.Int) { Value = p.Id });
                            cmd.ExecuteNonQuery();
                        }
                    }
                }
                MessageBox.Show("Остатки успешно обновлены в базе данных!");
                LoadData(); // Перезагружаем, чтобы подтвердить сохранение
            } catch (Exception ex) { MessageBox.Show("Ошибка сохранения: " + ex.Message); }
        }
    }
}