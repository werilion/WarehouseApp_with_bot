using Microsoft.VisualStudio.TestTools.UnitTesting;
using WarehouseApp.Infrastructure;
using System;

namespace WarehouseApp.Tests
{
    [TestClass]
    public class RelayCommandTests
    {
        [TestMethod]
        public void Command_ShouldExecuteAction()
        {
            // Arrange
            bool invoked = false;
            var command = new RelayCommand(obj => invoked = true);

            // Act
            command.Execute(null);

            // Assert
            Assert.IsTrue(invoked, "Команда не выполнила действие");
        }

        [TestMethod]
        public void Command_CanExecute_ShouldReturnFalse_WhenConditionIsMet()
        {
            // Arrange
            // Команда не должна работать, если условие false
            var command = new RelayCommand(obj => { }, obj => false);

            // Act
            bool canExec = command.CanExecute(null);

            // Assert
            Assert.IsFalse(canExec, "Команда доступна, хотя предикат вернул false");
        }
    }
}