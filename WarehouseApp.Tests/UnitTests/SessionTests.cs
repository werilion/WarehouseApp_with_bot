using Microsoft.VisualStudio.TestTools.UnitTesting;
using WarehouseApp.Services;
using WarehouseApp.Models;

namespace WarehouseApp.Tests
{
    [TestClass]
    public class SessionTests
    {
        [TestMethod]
        public void Logout_ShouldClearCurrentUser()
        {
            // Arrange
            Session.CurrentUser = new User { Login = "admin" };

            // Act
            Session.Logout();

            // Assert
            Assert.IsNull(Session.CurrentUser, "После Logout пользователь остался в сессии");
        }
    }
}