using System;
using System.Collections.ObjectModel;
using System.Windows;
using Microsoft.Data.SqlClient;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class DashboardViewModel : ViewModelBase
    {
        private decimal _totalQuantity;
        private decimal _receivedToday;
        private decimal _soldToday;
        private ObservableCollection<Product> _topProducts;

        // Свойства для привязки к карточкам
        public decimal TotalQuantity { get => _totalQuantity; set { _totalQuantity = value; OnPropertyChanged(); } }
        public decimal ReceivedToday { get => _receivedToday; set { _receivedToday = value; OnPropertyChanged(); } }
        public decimal SoldToday { get => _soldToday; set { _soldToday = value; OnPropertyChanged(); } }

        // Список товаров для таблицы на главной
        public ObservableCollection<Product> TopProducts { get => _topProducts; set { _topProducts = value; OnPropertyChanged(); } }

        public DashboardViewModel()
        {
            TopProducts = new ObservableCollection<Product>();
            LoadStatistics();
        }

        public void LoadStatistics()
        {
            try
            {
                using (var conn = DatabaseHelper.GetConnection())
                {
                    conn.Open();

                    // 1. Считаем общее кол-во товаров на складе
                    var cmdTotal = new SqlCommand("SELECT SUM(Quantity) FROM Products", conn);
                    var resultTotal = cmdTotal.ExecuteScalar();
                    TotalQuantity = resultTotal != DBNull.Value ? Convert.ToDecimal(resultTotal) : 0;

                    // 2. Поступило за сегодня (Income)
                    var cmdIn = new SqlCommand(@"
                        SELECT SUM(di.Quantity) 
                        FROM DocumentItems di 
                        JOIN Documents d ON di.DocumentId = d.Id 
                        WHERE d.DocType = 'Income' AND CAST(d.DocDate AS DATE) = CAST(GETDATE() AS DATE)", conn);
                    var resultIn = cmdIn.ExecuteScalar();
                    ReceivedToday = resultIn != DBNull.Value ? Convert.ToDecimal(resultIn) : 0;

                    // 3. Реализовано за сегодня (Outcome)
                    var cmdOut = new SqlCommand(@"
                        SELECT SUM(di.Quantity) 
                        FROM DocumentItems di 
                        JOIN Documents d ON di.DocumentId = d.Id 
                        WHERE d.DocType = 'Outcome' AND CAST(d.DocDate AS DATE) = CAST(GETDATE() AS DATE)", conn);
                    var resultOut = cmdOut.ExecuteScalar();
                    SoldToday = resultOut != DBNull.Value ? Convert.ToDecimal(resultOut) : 0;

                    // 4. Загружаем топ-5 товаров с наибольшим остатком
                    TopProducts.Clear();
                    var cmdTop = new SqlCommand("SELECT TOP 5 * FROM Products ORDER BY Quantity DESC", conn);
                    using (var reader = cmdTop.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            TopProducts.Add(new Product
                            {
                                Id = (int)reader["Id"],
                                Name = reader["Name"].ToString(),
                                Quantity = (decimal)reader["Quantity"],
                                Unit = reader["Unit"].ToString()
                            });
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка загрузки статистики: " + ex.Message);
            }
        }
    }
}