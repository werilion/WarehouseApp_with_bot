using Microsoft.Data.SqlClient;

namespace WarehouseApp.Services
{
    public static class DatabaseHelper
    {
        private static string _connectionString = @"Server=(localdb)\MSSQLLocalDB;Database=WarehouseDB;Trusted_Connection=True;";

        public static SqlConnection GetConnection()
        {
            return new SqlConnection(_connectionString);
        }
    }
}