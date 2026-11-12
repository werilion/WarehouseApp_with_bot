using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Windows;
using Microsoft.Data.SqlClient;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class HistoryViewModel : ViewModelBase
    {
        private ObservableCollection<Document> _documents = new ObservableCollection<Document>();
        public ObservableCollection<Document> Documents { get => _documents; set { _documents = value; OnPropertyChanged(); } }

        public RelayCommand DeleteDocumentCommand { get; }

        public HistoryViewModel()
        {
            LoadDocuments();
            DeleteDocumentCommand = new RelayCommand(o => ExecuteDelete(o));
        }

        public void LoadDocuments()
        {
            Documents.Clear();
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    string sql = @"SELECT d.*, c.Name as ContractorName, u.FullName as UserName 
                                 FROM Documents d 
                                 JOIN Contractors c ON d.ContractorId = c.Id 
                                 JOIN Users u ON d.UserId = u.Id 
                                 ORDER BY d.DocDate DESC";
                    using (var r = new SqlCommand(sql, conn).ExecuteReader())
                        while (r.Read())
                            Documents.Add(new Document {
                                Id = (int)r["Id"],
                                DocType = r["DocType"].ToString(),
                                DocDate = (DateTime)r["DocDate"],
                                ContractorName = r["ContractorName"].ToString(),
                                TotalAmount = (decimal)r["TotalAmount"],
                                UserName = r["UserName"].ToString()
                            });
                }
            } catch (Exception ex) { MessageBox.Show(ex.Message); }
        }

        private void ExecuteDelete(object obj)
        {
            if (obj is Document doc)
            {
                var result = MessageBox.Show($"Удаление документа №{doc.Id} приведет к пересчету остатков. Продолжить?", 
                    "Внимание", MessageBoxButton.YesNo, MessageBoxImage.Warning);

                if (result == MessageBoxResult.Yes)
                {
                    using (var conn = DatabaseHelper.GetConnection())
                    {
                        conn.Open();
                        var trans = conn.BeginTransaction();
                        try {
                            // 1. Сначала выкачиваем позиции документа в список (чтобы закрыть ридер)
                            var items = new List<DocumentItem>();
                            using (var cmd = new SqlCommand("SELECT ProductId, Quantity FROM DocumentItems WHERE DocumentId = @id", conn, trans)) {
                                cmd.Parameters.AddWithValue("@id", doc.Id);
                                using (var reader = cmd.ExecuteReader())
                                    while (reader.Read())
                                        items.Add(new DocumentItem { ProductId = (int)reader["ProductId"], Quantity = (decimal)reader["Quantity"] });
                            }

                            // 2. РЕВЕРС ОСТАТКОВ
                            foreach (var item in items) {
                                // Если удаляем Приход (-), если Расход (+)
                                string op = doc.DocType == "Income" ? "-" : "+";
                                string sql = $"UPDATE Products SET Quantity = Quantity {op} @q WHERE Id = @pid";
                                using (var upCmd = new SqlCommand(sql, conn, trans)) {
                                    upCmd.Parameters.AddWithValue("@q", item.Quantity);
                                    upCmd.Parameters.AddWithValue("@pid", item.ProductId);
                                    upCmd.ExecuteNonQuery();
                                }
                            }

                            // 3. Удаляем сам документ
                            using (var delCmd = new SqlCommand("DELETE FROM Documents WHERE Id = @id", conn, trans)) {
                                delCmd.Parameters.AddWithValue("@id", doc.Id);
                                delCmd.ExecuteNonQuery();
                            }

                            trans.Commit();
                            MessageBox.Show("Документ удален, складские остатки пересчитаны.");
                            LoadDocuments();
                        }
                        catch (Exception ex) { trans.Rollback(); MessageBox.Show("Ошибка: " + ex.Message); }
                    }
                }
            }
        }
    }
}