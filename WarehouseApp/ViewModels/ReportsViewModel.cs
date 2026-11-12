using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Text;
using System.Windows;
using Microsoft.Data.SqlClient;
using Microsoft.Win32;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class ReportsViewModel : ViewModelBase
    {
        private DateTime _startDate = DateTime.Now.AddMonths(-1);
        private DateTime _endDate = DateTime.Now;
        private ObservableCollection<ReportItem> _reportData;

        public DateTime StartDate { get => _startDate; set { _startDate = value; OnPropertyChanged(); } }
        public DateTime EndDate { get => _endDate; set { _endDate = value; OnPropertyChanged(); } }
        
        public ObservableCollection<ReportItem> ReportData 
        { 
            get => _reportData; 
            set { _reportData = value; OnPropertyChanged(); } 
        }

        public RelayCommand LoadStockReportCommand { get; }
        public RelayCommand LoadMovementReportCommand { get; }
        public RelayCommand ExportCommand { get; }

        public ReportsViewModel()
        {
            ReportData = new ObservableCollection<ReportItem>();
            LoadStockReportCommand = new RelayCommand(o => LoadStockReport());
            LoadMovementReportCommand = new RelayCommand(o => LoadMovementReport());
            ExportCommand = new RelayCommand(o => ExportToCSV(), o => ReportData.Count > 0);
        }

        private void LoadStockReport()
        {
            ReportData.Clear();
            string query = @"SELECT p.Name as ProductName, c.Name as CategoryName, p.Quantity, p.Price, (p.Quantity * p.Price) as TotalSum 
                             FROM Products p JOIN Categories c ON p.CategoryId = c.Id";
            ExecuteQuery(query);
        }

        private void LoadMovementReport()
        {
            ReportData.Clear();
            string query = @"SELECT p.Name as ProductName, d.DocType, di.Quantity, di.Price, (di.Quantity * di.Price) as TotalSum, d.DocDate as Date
                             FROM DocumentItems di
                             JOIN Documents d ON di.DocumentId = d.Id
                             JOIN Products p ON di.ProductId = p.Id
                             WHERE d.DocDate BETWEEN @start AND @end";
            ExecuteQuery(query, true);
        }

        private void ExecuteQuery(string query, bool useDates = false)
        {
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    var cmd = new SqlCommand(query, conn);
                    if (useDates) {
                        cmd.Parameters.AddWithValue("@start", StartDate);
                        cmd.Parameters.AddWithValue("@end", EndDate);
                    }
                    using (var r = cmd.ExecuteReader()) {
                        while (r.Read()) {
                            ReportData.Add(new ReportItem {
                                ProductName = r["ProductName"].ToString(),
                                Quantity = (decimal)r["Quantity"],
                                TotalSum = (decimal)r["TotalSum"],
                                // Проверка на наличие колонок (зависит от типа отчета)
                                CategoryName = r.HasColumn("CategoryName") ? r["CategoryName"].ToString() : "",
                                DocType = r.HasColumn("DocType") ? r["DocType"].ToString() : ""
                            });
                        }
                    }
                }
            } catch (Exception ex) { MessageBox.Show(ex.Message); }
        }

        private void ExportToCSV()
        {
            SaveFileDialog sfd = new SaveFileDialog { Filter = "CSV Files (*.csv)|*.csv", FileName = "Report.csv" };
            if (sfd.ShowDialog() == true) {
                var sb = new StringBuilder();
                sb.AppendLine("Товар;Кол-во;Сумма;Тип");
                foreach (var item in ReportData)
                    sb.AppendLine($"{item.ProductName};{item.Quantity};{item.TotalSum};{item.DocType}");
                
                File.WriteAllText(sfd.FileName, sb.ToString(), Encoding.UTF8);
                MessageBox.Show("Экспорт завершен!");
            }
        }
    }

    // Хелпер для проверки наличия колонок
    public static class SqlExtensions {
        public static bool HasColumn(this SqlDataReader reader, string columnName) {
            for (int i = 0; i < reader.FieldCount; i++)
                if (reader.GetName(i).Equals(columnName, StringComparison.InvariantCultureIgnoreCase)) return true;
            return false;
        }
    }
}