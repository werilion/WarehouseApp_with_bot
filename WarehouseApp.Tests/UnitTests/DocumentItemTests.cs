using Microsoft.VisualStudio.TestTools.UnitTesting;
using WarehouseApp.Models;

namespace WarehouseApp.Tests
{
    [TestClass] 
    public class DocumentItemTests
    {
        [TestMethod]
        public void Total_ShouldCalculateCorrectly()
        {
            // Arrange (Подготовка)
            var item = new DocumentItem
            {
                Quantity = 5.5m,
                Price = 1000m
            };

            // Act (Действие)
            decimal result = item.Total;

            // Assert (Проверка)
            Assert.AreEqual(5500m, result, "Сумма строки рассчитана неверно");
        }
    }
}