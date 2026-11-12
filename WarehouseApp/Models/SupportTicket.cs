using System;

namespace WarehouseApp.Models
{
    /// <summary>Обращение пользователя в техподдержку.</summary>
    public class SupportTicket
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string UserName { get; set; } = "";
        public string Subject { get; set; } = "";
        public string Description { get; set; } = "";
        public string Contact { get; set; } = "";
        /// <summary>Новое / В работе / Закрыто</summary>
        public string Status { get; set; } = "Новое";
        public DateTime CreatedAt { get; set; }
    }
}
