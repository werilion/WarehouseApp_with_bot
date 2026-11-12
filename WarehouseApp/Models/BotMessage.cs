namespace WarehouseApp.Models
{
    /// <summary>Сообщение в чате с ботом.</summary>
    public class BotMessage
    {
        public string Text { get; set; } = "";
        public bool IsUser { get; set; }
    }
}
