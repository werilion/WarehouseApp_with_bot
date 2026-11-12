using System;

namespace WarehouseApp.Models
{
    public class Document
    {
        public int Id { get; set; }
        public string DocType { get; set; } // Income / Outcome
        public DateTime DocDate { get; set; }
        public int ContractorId { get; set; }
        public string ContractorName { get; set; }
        public decimal TotalAmount { get; set; }
        public string UserName { get; set; }
    }
}