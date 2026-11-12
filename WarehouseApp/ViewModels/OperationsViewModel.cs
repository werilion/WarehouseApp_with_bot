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
    public class OperationsViewModel : ViewModelBase
    {
        private string _docType;
        private Contractor _selectedContractor;
        private Product _selectedProduct;
        private decimal _inputQuantity = 1;
        private decimal _inputPrice = 0;

        // Заголовок страницы зависит от типа операции
        public string Title => _docType == "Income" ? "Приход товара на склад" : "Расход товара со склада";
        
        // Коллекции данных
        public ObservableCollection<Contractor> Contractors { get; set; } = new ObservableCollection<Contractor>();
        public ObservableCollection<Product> Products { get; set; } = new ObservableCollection<Product>();
        public ObservableCollection<DocumentItem> CurrentItems { get; set; } = new ObservableCollection<DocumentItem>();

        public Contractor SelectedContractor
        {
            get => _selectedContractor;
            set { _selectedContractor = value; OnPropertyChanged(); }
        }

        public Product SelectedProduct
        {
            get => _selectedProduct;
            set 
            { 
                _selectedProduct = value; 
                OnPropertyChanged();
                // При выборе товара автоматически подставляем его цену из справочника
                if (_selectedProduct != null) InputPrice = _selectedProduct.Price;
            }
        }

        public decimal InputQuantity { get => _inputQuantity; set { _inputQuantity = value; OnPropertyChanged(); } }
        public decimal InputPrice { get => _inputPrice; set { _inputPrice = value; OnPropertyChanged(); } }
        
        // Итоговая сумма по всему документу
        public decimal TotalDocumentAmount => CurrentItems.Sum(x => x.Total);

        // Команды
        public RelayCommand AddToCartCommand { get; }
        public RelayCommand RemoveFromCartCommand { get; }
        public RelayCommand SaveDocumentCommand { get; }

        public OperationsViewModel(string type)
        {
            _docType = type;
            LoadData();

            // Добавление товара в таблицу документа (в "корзину")
            AddToCartCommand = new RelayCommand(o => {
                if (SelectedProduct == null || InputQuantity <= 0) {
                    MessageBox.Show("Выберите товар и укажите корректное количество!", "Предупреждение");
                    return;
                }
                
                CurrentItems.Add(new DocumentItem {
                    ProductId = SelectedProduct.Id,
                    ProductName = SelectedProduct.Name,
                    Quantity = InputQuantity,
                    Price = InputPrice
                });
                OnPropertyChanged(nameof(TotalDocumentAmount));
            });

            // Удаление товара из таблицы документа
            RemoveFromCartCommand = new RelayCommand(o => {
                if (o is DocumentItem item) {
                    CurrentItems.Remove(item);
                    OnPropertyChanged(nameof(TotalDocumentAmount));
                }
            });

            // Сохранение всего документа в БД
            SaveDocumentCommand = new RelayCommand(o => ExecuteSave(), o => CurrentItems.Count > 0 && SelectedContractor != null);
        }

        /// <summary>
        /// Загрузка контрагентов и товаров для выбора в выпадающих списках
        /// </summary>
        private void LoadData()
        {
            try {
                Contractors.Clear();
                Products.Clear();
                using (var conn = DatabaseHelper.GetConnection()) {
                    conn.Open();
                    
                    // Загрузка контрагентов
                    var cmdC = new SqlCommand("SELECT Id, Name FROM Contractors", conn);
                    using (var r = cmdC.ExecuteReader())
                        while (r.Read()) Contractors.Add(new Contractor { Id = (int)r["Id"], Name = r["Name"].ToString() });

                    // Загрузка товаров (включая текущий остаток для проверки при расходе)
                    var cmdP = new SqlCommand("SELECT Id, Name, Price, Quantity FROM Products", conn);
                    using (var r = cmdP.ExecuteReader())
                        while (r.Read()) Products.Add(new Product { 
                            Id = (int)r["Id"], 
                            Name = r["Name"].ToString(), 
                            Price = (decimal)r["Price"],
                            Quantity = (decimal)r["Quantity"]
                        });
                }
            } catch (Exception ex) { MessageBox.Show("Ошибка загрузки справочников: " + ex.Message); }
        }

        /// <summary>
        /// Основная логика сохранения документа с использованием транзакции
        /// </summary>
        private void ExecuteSave()
        {
            // ПРОВЕРКА ОСТАТКОВ ПЕРЕД РАСХОДОМ
            if (_docType == "Outcome")
            {
                foreach (var item in CurrentItems)
                {
                    var productInDb = Products.FirstOrDefault(p => p.Id == item.ProductId);
                    if (productInDb != null && productInDb.Quantity < item.Quantity)
                    {
                        MessageBox.Show($"Недостаточно товара '{item.ProductName}' на складе!\n" +
                                        $"Доступно: {productInDb.Quantity}, требуется: {item.Quantity}", 
                                        "Ошибка остатка", MessageBoxButton.OK, MessageBoxImage.Warning);
                        return; // Прерываем выполнение метода
                    }
                }
            }

            using (var conn = DatabaseHelper.GetConnection())
            {
                conn.Open();
                var trans = conn.BeginTransaction();
                try {
                    // 1. Создаем заголовок документа
                    var cmdDoc = new SqlCommand(@"INSERT INTO Documents (DocType, ContractorId, UserId, TotalAmount, DocDate) 
                        OUTPUT INSERTED.Id VALUES (@t, @c, @u, @am, GETDATE())", conn, trans);
                    cmdDoc.Parameters.AddWithValue("@t", _docType);
                    cmdDoc.Parameters.AddWithValue("@c", SelectedContractor.Id);
                    cmdDoc.Parameters.AddWithValue("@u", Session.CurrentUser.Id);
                    cmdDoc.Parameters.AddWithValue("@am", TotalDocumentAmount);
                    int docId = (int)cmdDoc.ExecuteScalar();

                    // 2. Записываем каждую позицию и обновляем остатки на складе
                    foreach (var item in CurrentItems) {
                        // Запись строки в таблицу DocumentItems
                        var cmdItem = new SqlCommand("INSERT INTO DocumentItems (DocumentId, ProductId, Quantity, Price) VALUES (@d, @p, @q, @pr)", conn, trans);
                        cmdItem.Parameters.AddWithValue("@d", docId);
                        cmdItem.Parameters.AddWithValue("@p", item.ProductId);
                        cmdItem.Parameters.AddWithValue("@q", item.Quantity);
                        cmdItem.Parameters.AddWithValue("@pr", item.Price);
                        cmdItem.ExecuteNonQuery();

                        // Обновление остатка в таблице Products (+ при приходе, - при расходе)
                        string op = _docType == "Income" ? "+" : "-";
                        var cmdStock = new SqlCommand($"UPDATE Products SET Quantity = Quantity {op} @q WHERE Id = @p", conn, trans);
                        cmdStock.Parameters.AddWithValue("@q", item.Quantity);
                        cmdStock.Parameters.AddWithValue("@p", item.ProductId);
                        cmdStock.ExecuteNonQuery();
                    }

                    trans.Commit(); // Фиксируем изменения в БД
                    MessageBox.Show("Документ успешно проведен и остатки обновлены!", "Успех", MessageBoxButton.OK, MessageBoxImage.Information);
                    
                    CurrentItems.Clear(); // Очищаем форму
                    OnPropertyChanged(nameof(TotalDocumentAmount));
                    LoadData(); // Перезагружаем данные (обновленные остатки)
                } 
                catch (Exception ex) 
                { 
                    trans.Rollback(); // Откатываем всё назад в случае любой ошибки
                    MessageBox.Show("Критическая ошибка при сохранении: " + ex.Message); 
                }
            }
        }
    }
}