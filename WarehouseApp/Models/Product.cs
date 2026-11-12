using WarehouseApp.Infrastructure;

namespace WarehouseApp.Models
{
    public class Product : ViewModelBase
    {
        private decimal _quantity;
        private string _name;

        public int Id { get; set; }
        public int CategoryId { get; set; }
        public string CategoryName { get; set; }
        public string Description { get; set; }
        public decimal Price { get; set; }
        public string Unit { get; set; }

        public string Name 
        { 
            get => _name; 
            set { _name = value; OnPropertyChanged(); } 
        }
        
        public decimal Quantity
        {
            get => _quantity;
            set { _quantity = value; OnPropertyChanged(); }
        }
    }
}