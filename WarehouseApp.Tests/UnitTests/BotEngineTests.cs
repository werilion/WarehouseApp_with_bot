using Microsoft.VisualStudio.TestTools.UnitTesting;
using WarehouseApp.Services;

namespace WarehouseApp.Tests
{
    [TestClass]
    public class BotEngineTests
    {
        [TestMethod]
        public void Tree_AllTransitionsPointToExistingNodes()
        {
            foreach (var node in BotKnowledge.Nodes.Values)
            {
                if (node.IsQuestion)
                    Assert.IsTrue(node.Options.Count >= 2, $"У вопроса {node.Id} меньше двух вариантов ответа");
                foreach (var (_, target) in node.Options)
                    Assert.IsTrue(BotKnowledge.Nodes.ContainsKey(target), $"Узел {node.Id} ведёт в несуществующий узел {target}");
            }
        }

        [TestMethod]
        public void Send_IncomeText_OpensIncomeBranch()
        {
            var bot = new BotEngine(() => 3);
            bot.Send("хочу оформить приход");
            Assert.AreEqual("A2", bot.Current);   // «Товар есть в каталоге?»
            Assert.IsTrue(bot.Messages.Any(m => m.Text.Contains("Открыть раздел «Приход»")));
        }

        [TestMethod]
        public void Send_TextWithTypo_StillFindsOutcomeBranch()
        {
            var bot = new BotEngine(() => 3);
            bot.Send("надо оформить расхот");
            Assert.AreEqual("B3", bot.Current);   // «Контрагент выбран?»
        }

        [TestMethod]
        public void Choose_DeleteProduct_BotAnswersRoleQuestionItself()
        {
            var admin = new BotEngine(() => 1);
            admin.Send("удалить товар");
            admin.Choose(0);                      // «Да», нужно удалить товар
            Assert.AreEqual("C22", admin.Current); // администратор: идём к подтверждению удаления

            var storekeeper = new BotEngine(() => 3);
            storekeeper.Send("удалить товар");
            storekeeper.Choose(0);
            Assert.IsNull(storekeeper.Current);   // сотруднику склада: «Обратиться к администратору»
        }

        [TestMethod]
        public void Send_UnknownText_ShowsFallbackAndTopics()
        {
            var bot = new BotEngine(() => 3);
            bot.Send("абракадабра");
            Assert.IsTrue(bot.Messages.Any(m => m.Text == BotKnowledge.Fallback));
            Assert.AreEqual("Q0", bot.Current);
        }

        [TestMethod]
        public void Back_RestoresPreviousState()
        {
            var bot = new BotEngine(() => 3);
            int before = bot.Messages.Count;
            bot.Send("приход");
            bot.Back();
            Assert.AreEqual(before, bot.Messages.Count);
            Assert.AreEqual("Q0", bot.Current);
        }
    }
}
