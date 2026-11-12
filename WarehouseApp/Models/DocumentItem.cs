namespace WarehouseApp.Models
{
    public class DocumentItem
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Quantity { get; set; }
        public decimal Price { get; set; }
        public decimal Total => Quantity * Price; // Вычисляемое поле для UI
    }
}