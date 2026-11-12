using System;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using Microsoft.Data.SqlClient;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class ProductsViewModel : ViewModelBase
    {
        // Поля для списка
        private ObservableCollection<Product> _products = new ObservableCollection<Product>();
        private string _searchText = "";
        
        // Поля для формы добавления
        private bool _isAdding;
        public string NewName { get; set; }
        public decimal NewPrice { get; set; }
        public string NewUnit { get; set; } = "шт.";
        public Category SelectedCategory { get; set; }
        public ObservableCollection<Category> Categories { get; set; } = new ObservableCollection<Category>();

        // Свойства
        public ObservableCollection<Product> Products { get => _products; set { _products = value; OnPropertyChanged(); } }
        
        public string SearchText 
        { 
            get => _searchText; 
            set { _searchText = value; OnPropertyChanged(); LoadProducts(); } 
        }

        public bool IsAdding 
        { 
            get => _isAdding; 
            set { _isAdding = value; OnPropertyChanged(); OnPropertyChanged(nameof(ListVisibility)); OnPropertyChanged(nameof(FormVisibility)); } 
        }

        // Управление видимостью
        public Visibility ListVisibility => IsAdding ? Visibility.Collapsed : Visibility.Visible;
        public Visibility FormVisibility => IsAdding ? Visibility.Visible : Visibility.Collapsed;
        public Visibility DeleteVisibility => Session.CurrentUser?.RoleId == 1 ? Visibility.Visible : Visibility.Collapsed;

        // Команды
        public RelayCommand SwitchToAddCommand { get; }
        public RelayCommand CancelAddCommand { get; }
        public RelayCommand SaveProductCommand { get; }
        public RelayCommand DeleteCommand { get; }

        public ProductsViewModel()
        {
            LoadProducts();
            LoadCategories();

            SwitchToAddCommand = new RelayCommand(o => { IsAdding = true; });
            CancelAddCommand = new RelayCommand(o => { IsAdding = false; });
            
            SaveProductCommand = new RelayCommand(o => ExecuteSave(), o => !string.IsNullOrEmpty(NewName) && SelectedCategory != null);
            DeleteCommand = new RelayCommand(o => ExecuteDelete(o));
        }

        public void LoadProducts()
        {
            try {
                Products.Clear();
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    string sql = "SELECT p.*, c.Name as CategoryName FROM Products p JOIN Categories c ON p.CategoryId = c.Id WHERE p.Name LIKE @s";
                    var cmd = new SqlCommand(sql, conn);
                    cmd.Parameters.AddWithValue("@s", $"%{SearchText}%");
                    using (var r = cmd.ExecuteReader())
                        while (r.Read()) Products.Add(new Product { 
                            Id = (int)r["Id"], Name = r["Name"].ToString(), CategoryName = r["CategoryName"].ToString(),
                            Quantity = (decimal)r["Quantity"], Price = (decimal)r["Price"], Unit = r["Unit"].ToString() 
                        });
                }
            } catch (Exception ex) { MessageBox.Show(ex.Message); }
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

        private void ExecuteSave()
        {
            try {
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    string sql = "INSERT INTO Products (Name, CategoryId, Price, Unit, Quantity) VALUES (@n, @c, @p, @u, 0)";
                    var cmd = new SqlCommand(sql, conn);
                    cmd.Parameters.AddWithValue("@n", NewName);
                    cmd.Parameters.AddWithValue("@c", SelectedCategory.Id);
                    cmd.Parameters.AddWithValue("@p", NewPrice);
                    cmd.Parameters.AddWithValue("@u", NewUnit);
                    cmd.ExecuteNonQuery();
                }
                IsAdding = false;
                LoadProducts();
                // Очистка полей
                NewName = ""; NewPrice = 0;
            } catch (Exception ex) { MessageBox.Show(ex.Message); }
        }

        private void ExecuteDelete(object obj)
        {
            if (obj is Product p)
            {
                var result = MessageBox.Show($"Вы уверены, что хотите удалить товар '{p.Name}'?", 
                    "Подтверждение удаления", MessageBoxButton.YesNo, MessageBoxImage.Warning);

                if (result == MessageBoxResult.Yes)
                {
                    try
                    {
                        using (var conn = DatabaseHelper.GetConnection())
                        {
                            conn.Open();
                            // Используем параметры, чтобы избежать ошибок и инъекций
                            var cmd = new SqlCommand("DELETE FROM Products WHERE Id = @id", conn);
                            cmd.Parameters.AddWithValue("@id", p.Id);
                            cmd.ExecuteNonQuery();
                        }
                        LoadProducts(); // Обновляем список
                    }
                    catch (SqlException ex) when (ex.Number == 547)
                    {
                        // Ошибка 547 - это нарушение внешнего ключа (Foreign Key Constraint)
                        MessageBox.Show("Невозможно удалить товар, так как он уже используется в документах (приход или расход).\n\n" +
                                        "Чтобы удалить этот товар, сначала нужно удалить все документы, в которых он участвует.", 
                            "Системное ограничение", MessageBoxButton.OK, MessageBoxImage.Stop);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Произошла непредвиденная ошибка: " + ex.Message, 
                            "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
        }
    }
}