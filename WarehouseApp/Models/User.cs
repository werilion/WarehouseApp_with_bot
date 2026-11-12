namespace WarehouseApp.Models
{
    public class User
    {
        public int Id { get; set; }
        public string Login { get; set; }
        public string Password { get; set; }
        public string FullName { get; set; }
        public int RoleId { get; set; }
        
        // Навигационное свойство для отображения названия роли
        public Role Role { get; set; }
    }
}