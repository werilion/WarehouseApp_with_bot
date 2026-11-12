using System.Collections.ObjectModel;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    /// <summary>
    /// Страница «Помощник»: чат с ботом. Бот ведёт по дереву решений, понимает свободный текст,
    /// открывает разделы программы и передаёт вопрос в техподдержку.
    /// </summary>
    public class ChatViewModel : ViewModelBase
    {
        private readonly BotEngine _bot = new();
        private readonly Action<string, string?> _navigate;
        private string _inputText = "";

        public ObservableCollection<BotMessage> Messages => _bot.Messages;

        /// <summary>Кнопки быстрых ответов под сообщениями.</summary>
        public ObservableCollection<string> Options { get; } = new();

        public string InputText
        {
            get => _inputText;
            set { _inputText = value; OnPropertyChanged(); }
        }

        public bool HasNav => _bot.Nav != null;
        public string NavLabel => _bot.Nav?.Label ?? "";

        public RelayCommand SendCommand { get; }
        public RelayCommand ChooseCommand { get; }
        public RelayCommand BackCommand { get; }
        public RelayCommand ResetCommand { get; }
        public RelayCommand NavigateCommand { get; }
        public RelayCommand SupportCommand { get; }

        /// <param name="navigate">Открывает раздел программы: ключ раздела и необязательный текст для обращения.</param>
        public ChatViewModel(Action<string, string?> navigate)
        {
            _navigate = navigate;

            SendCommand = new RelayCommand(o =>
            {
                _bot.Send(InputText);
                InputText = "";
                Refresh();
            }, o => !string.IsNullOrWhiteSpace(InputText));

            ChooseCommand = new RelayCommand(o =>
            {
                var label = o as string ?? "";
                if (_bot.Current == null) _bot.Send(label);          // конец ветки: «Это помогло / Не помогло / Другой вопрос»
                else _bot.Choose(Options.IndexOf(label));
                Refresh();
            });

            BackCommand = new RelayCommand(o => { _bot.Back(); Refresh(); }, o => _bot.CanGoBack);
            ResetCommand = new RelayCommand(o => { _bot.Reset(); Refresh(); });

            NavigateCommand = new RelayCommand(o =>
            {
                if (_bot.Nav is { } nav) _navigate(nav.Key, nav.Key == "support" ? LastUserText() : null);
            });

            SupportCommand = new RelayCommand(o => _navigate("support", LastUserText()));

            Refresh();
        }

        private string? LastUserText() => Messages.LastOrDefault(m => m.IsUser)?.Text;

        private void Refresh()
        {
            Options.Clear();
            if (_bot.Current == null)
            {
                Options.Add("Это помогло");
                Options.Add("Не помогло");
                Options.Add("Другой вопрос");
            }
            else
            {
                foreach (var (label, _) in BotKnowledge.Nodes[_bot.Current].Options)
                    Options.Add(label);
            }
            OnPropertyChanged(nameof(HasNav));
            OnPropertyChanged(nameof(NavLabel));
        }
    }
}
