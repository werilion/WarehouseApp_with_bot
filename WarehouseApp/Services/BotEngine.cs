using System.Collections.ObjectModel;
using System.Text.RegularExpressions;
using WarehouseApp.Models;

namespace WarehouseApp.Services
{
    /// <summary>
    /// Логика диалога бота: идёт по дереву решений, понимает свободный текст по ключевым словам
    /// (с учётом опечаток) и учитывает роль пользователя. Без обращения к базе данных.
    /// </summary>
    public class BotEngine
    {
        public const string BotName = "Складской помощник";

        private readonly Dictionary<string, BotNode> _nodes = BotKnowledge.Nodes;
        private readonly Stack<(int Count, string? Current, (string Key, string Label)? Nav)> _history = new();
        private readonly Func<int> _roleProvider;

        /// <summary>Сообщения чата (привязаны к интерфейсу).</summary>
        public ObservableCollection<BotMessage> Messages { get; } = new();

        /// <summary>Текущий вопрос дерева; null, если ветка закончилась.</summary>
        public string? Current { get; private set; }

        /// <summary>Кнопка перехода в раздел программы, предложенная ботом.</summary>
        public (string Key, string Label)? Nav { get; private set; }

        public bool CanGoBack => _history.Count > 0;

        /// <param name="roleProvider">Возвращает Id роли текущего пользователя (1 - администратор, 2 - менеджер, 0 - неизвестно).</param>
        public BotEngine(Func<int>? roleProvider = null)
        {
            _roleProvider = roleProvider ?? (() => Session.CurrentUser?.RoleId ?? 0);
            Reset();
        }

        private bool IsAdmin => _roleProvider() == 1;
        private bool IsManager => _roleProvider() is 1 or 2;

        /// <summary>Вопросы, на которые бот отвечает сам по роли пользователя.</summary>
        private bool? AutoAnswer(string nodeId) => nodeId switch
        {
            "C18" => IsAdmin,
            "E11" => IsAdmin,
            "D13" => IsManager,
            "E19" => !IsManager,
            _ => null
        };

        public bool CanOpen(string key) => key switch
        {
            "reports" => IsManager,
            "users" or "settings" => IsAdmin,
            _ => true
        };

        public void Reset()
        {
            _history.Clear();
            Messages.Clear();
            Nav = null;
            var name = Session.CurrentUser?.FullName;
            Say(string.IsNullOrWhiteSpace(name)
                ? $"Здравствуйте! Я {BotName}. Напишите, что нужно сделать, или выберите тему кнопкой."
                : $"Здравствуйте, {name}! Я {BotName}. Напишите, что нужно сделать, или выберите тему кнопкой.");
            Current = "Q0";
            Advance();
        }

        public void Back()
        {
            if (_history.Count == 0) return;
            var (count, current, nav) = _history.Pop();
            while (Messages.Count > count) Messages.RemoveAt(Messages.Count - 1);
            Current = current;
            Nav = nav;
        }

        /// <summary>Ответ пользователя кнопкой (индекс варианта текущего вопроса).</summary>
        public void Choose(int index)
        {
            if (Current == null) return;
            var options = _nodes[Current].Options;
            if (index < 0 || index >= options.Count) return;
            Snapshot();
            AddUser(options[index].Label);
            Current = options[index].Target;
            Advance();
        }

        /// <summary>Сообщение пользователя, написанное в чат.</summary>
        public void Send(string text)
        {
            text = text.Trim();
            if (text.Length == 0) return;
            var t = Normalize(text);
            if (t == "назад") { Back(); return; }
            if (t is "заново" or "сначала" or "начать заново") { Reset(); return; }

            Snapshot();
            AddUser(text);

            if (t == "другой вопрос")
            {
                Current = "Q0";
                Advance();
                return;
            }

            // Ответ словом на текущий вопрос: "да", "нет", "приход" и т.п.
            if (Current != null)
            {
                foreach (var (label, target) in _nodes[Current].Options)
                {
                    var l = Normalize(label);
                    if (t == l || (l == "да" && Yes.Contains(t)) || (l == "нет" && No.Contains(t)))
                    {
                        Current = target;
                        Advance();
                        return;
                    }
                }
            }

            var tokens = t.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            BotFaq? bestFaq = null;
            BotIntent? bestIntent = null;
            int best = 0;
            foreach (var faq in BotKnowledge.Faqs)
            {
                int s = Score(faq.Keywords, t, tokens);
                if (s > best) { best = s; bestFaq = faq; bestIntent = null; }
            }
            foreach (var intent in BotKnowledge.Intents)
            {
                int s = Score(intent.Keywords, t, tokens);
                if (s > best) { best = s; bestIntent = intent; bestFaq = null; }
            }

            if (bestFaq != null)
            {
                Say(bestFaq.Answer);
                if (bestFaq.Navigate != null && CanOpen(bestFaq.Navigate))
                    Nav = (bestFaq.Navigate, NavLabel(bestFaq.Navigate));
                if (Current != null)
                    Say("Вернёмся к вопросу: " + _nodes[Current].Text);
            }
            else if (bestIntent != null)
            {
                Say(bestIntent.Intro);
                Current = bestIntent.Entry;
                Advance();
            }
            else
            {
                foreach (var (words, answer) in BotKnowledge.SmallTalk)
                {
                    if (words.Any(w => Hit(w, t, tokens))) { Say(answer); return; }
                }
                Say(BotKnowledge.Fallback);
                Current = "Q0";
                Advance();
            }
        }

        // --- внутренняя логика ---

        /// <summary>Идёт по дереву: выводит действия, пока не дойдёт до вопроса или конца ветки.</summary>
        private void Advance()
        {
            int guard = 0;
            while (Current != null && guard++ < 200)
            {
                var node = _nodes[Current];
                if (BotKnowledge.NavTargets.TryGetValue(node.Id, out var nav) && CanOpen(nav.Key))
                    Nav = nav;
                Say(node.Text);

                if (node.IsQuestion)
                {
                    var auto = AutoAnswer(node.Id);
                    if (auto == null) return;

                    // Бот отвечает на вопрос сам, исходя из роли пользователя
                    var role = Session.CurrentUser?.Role?.Name;
                    var answer = auto.Value ? "Да" : "Нет";
                    Say(string.IsNullOrEmpty(role)
                        ? $"По вашей роли отвечаю: {answer}."
                        : $"Вы вошли как «{role}», поэтому отвечаю: {answer}.");
                    Current = node.Options.First(o => o.Label == answer).Target;
                    continue;
                }

                if (node.Options.Count == 0)
                {
                    Say("Надеюсь, это помогло. Если есть другой вопрос, просто напишите его.");
                    Current = null;
                    return;
                }
                Current = node.Options[0].Target;
            }
        }

        private static string NavLabel(string key) => key switch
        {
            "reports" => "Открыть «Отчёты»",
            "history" => "Открыть «Историю операций»",
            "support" => "Открыть «Техподдержку»",
            _ => "Открыть раздел"
        };

        private void Snapshot() => _history.Push((Messages.Count, Current, Nav));
        private void Say(string text) => Messages.Add(new BotMessage { Text = text, IsUser = false });
        private void AddUser(string text) => Messages.Add(new BotMessage { Text = text, IsUser = true });

        private static readonly HashSet<string> Yes = new() { "да", "ага", "угу", "конечно", "верно", "есть" };
        private static readonly HashSet<string> No = new() { "нет", "неа", "нету", "не" };

        /// <summary>Нижний регистр, ё заменяется на е, знаки препинания убираются.</summary>
        public static string Normalize(string text)
        {
            text = text.ToLowerInvariant().Replace('ё', 'е');
            text = Regex.Replace(text, @"[^\p{L}\p{N}\s]", " ");
            return Regex.Replace(text, @"\s+", " ").Trim();
        }

        private static int Score((string Word, int Weight)[] keywords, string text, string[] tokens)
        {
            int sum = 0;
            foreach (var (word, weight) in keywords)
                if (Hit(word, text, tokens)) sum += weight;
            return sum;
        }

        /// <summary>Слово из одной части ищется как начало слова (допускаются опечатки), из нескольких - как фраза.</summary>
        public static bool Hit(string keyword, string text, string[] tokens)
        {
            if (keyword.Contains(' ')) return text.Contains(keyword);
            int limit = keyword.Length <= 3 ? 2 : 5;
            foreach (var token in tokens)
            {
                if (token.Length > keyword.Length + limit) continue;
                if (token.StartsWith(keyword, StringComparison.Ordinal)) return true;
                if (keyword.Length >= 5 && token.Length >= keyword.Length - 1)
                {
                    var head = token.Length >= keyword.Length ? token.Substring(0, keyword.Length) : token;
                    if (Distance(head, keyword) <= 1) return true;
                }
            }
            return false;
        }

        /// <summary>Расстояние Левенштейна: сколько правок отделяет одну строку от другой.</summary>
        private static int Distance(string a, string b)
        {
            var d = new int[a.Length + 1, b.Length + 1];
            for (int i = 0; i <= a.Length; i++) d[i, 0] = i;
            for (int j = 0; j <= b.Length; j++) d[0, j] = j;
            for (int i = 1; i <= a.Length; i++)
                for (int j = 1; j <= b.Length; j++)
                    d[i, j] = Math.Min(Math.Min(d[i - 1, j] + 1, d[i, j - 1] + 1),
                                       d[i - 1, j - 1] + (a[i - 1] == b[j - 1] ? 0 : 1));
            return d[a.Length, b.Length];
        }
    }
}
