namespace WarehouseApp.Models
{
    public class ReportItem
    {
        public string ProductName { get; set; }
        public string CategoryName { get; set; }
        public decimal Quantity { get; set; }
        public decimal Price { get; set; }
        public decimal TotalSum { get; set; }
        public string DocType { get; set; } // Для отчета по движениям
        public System.DateTime Date { get; set; }
    }
}