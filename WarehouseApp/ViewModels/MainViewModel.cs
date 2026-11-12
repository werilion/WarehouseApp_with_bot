using System.Windows;
using WarehouseApp.Infrastructure;
using WarehouseApp.Services;
using WarehouseApp.Views;

namespace WarehouseApp.ViewModels
{
    public class MainViewModel : ViewModelBase
    {
        private object _currentView;
        private string _globalSearchText;

        // Текущая отображаемая страница
        public object CurrentView
        {
            get => _currentView;
            set 
            { 
                _currentView = value; 
                OnPropertyChanged();
                // При смене страницы применяем текущий поиск к новому контексту
                UpdateSearchContext();
            }
        }

        // Глобальный поиск в хедере
        public string GlobalSearchText
        {
            get => _globalSearchText;
            set
            {
                _globalSearchText = value;
                OnPropertyChanged();
                UpdateSearchContext();
            }
        }

        // Метод перенаправления поиска в активную ViewModel (Контекстный поиск)
        private void UpdateSearchContext()
        {
            if (CurrentView is ProductsViewModel pvm) pvm.SearchText = _globalSearchText;
            else if (CurrentView is UsersViewModel uvm) uvm.SearchText = _globalSearchText;
            else if (CurrentView is InventoryViewModel ivm) ivm.SearchText = _globalSearchText;
            
            // Если пользователь на главной начал вводить текст — перекидываем в каталог товаров
            else if (!string.IsNullOrEmpty(_globalSearchText) && CurrentView is DashboardViewModel)
            {
                var newPvm = new ProductsViewModel();
                CurrentView = newPvm;
                newPvm.SearchText = _globalSearchText;
            }
        }

        public string UserFullName => Session.CurrentUser?.FullName;
        public string UserRole => Session.CurrentUser?.Role?.Name;

        // Права доступа (RBAC)
        public Visibility AdminVisibility => Session.CurrentUser?.RoleId == 1 ? Visibility.Visible : Visibility.Collapsed;
        public Visibility ManagerVisibility => (Session.CurrentUser?.RoleId == 1 || Session.CurrentUser?.RoleId == 2) ? Visibility.Visible : Visibility.Collapsed;

        // Команды навигации
        public RelayCommand ShowDashboardCommand { get; }
        public RelayCommand ShowProductsCommand { get; }
        public RelayCommand ShowIncomeCommand { get; }
        public RelayCommand ShowOutcomeCommand { get; }
        public RelayCommand ShowInventoryCommand { get; }
        public RelayCommand ShowHistoryCommand { get; }
        public RelayCommand ShowReportsCommand { get; }
        public RelayCommand ShowUsersCommand { get; }
        public RelayCommand ShowSettingsCommand { get; }
        public RelayCommand ShowChatCommand { get; }
        public RelayCommand ShowSupportCommand { get; }
        public RelayCommand LogoutCommand { get; }

        public MainViewModel()
        {
            CurrentView = new DashboardViewModel();
            
            ShowDashboardCommand = new RelayCommand(o => { GlobalSearchText = ""; CurrentView = new DashboardViewModel(); });
            ShowProductsCommand = new RelayCommand(o => { GlobalSearchText = ""; CurrentView = new ProductsViewModel(); });
            
            ShowIncomeCommand = new RelayCommand(o => CurrentView = new OperationsViewModel("Income"));
            ShowOutcomeCommand = new RelayCommand(o => CurrentView = new OperationsViewModel("Outcome"));
            
            ShowInventoryCommand = new RelayCommand(o => { GlobalSearchText = ""; CurrentView = new InventoryViewModel(); });
            ShowHistoryCommand = new RelayCommand(o => { GlobalSearchText = ""; CurrentView = new HistoryViewModel(); });
            
            ShowReportsCommand = new RelayCommand(o => CurrentView = new ReportsViewModel());
            ShowUsersCommand = new RelayCommand(o => { GlobalSearchText = ""; CurrentView = new UsersViewModel(); });
            
            ShowSettingsCommand = new RelayCommand(o => { GlobalSearchText = ""; CurrentView = new SettingsViewModel(); });

            ShowChatCommand = new RelayCommand(o => { GlobalSearchText = ""; CurrentView = new ChatViewModel(Navigate); });
            ShowSupportCommand = new RelayCommand(o => { GlobalSearchText = ""; CurrentView = new SupportViewModel(); });
            LogoutCommand = new RelayCommand(o => ExecuteLogout(o));
        }

        // Переход в раздел по ключу: этим пользуется бот («Открыть раздел...» и «Написать в техподдержку»)
        private void Navigate(string key, string? prefill)
        {
            GlobalSearchText = "";
            object? view = key switch
            {
                "income" => (object)new OperationsViewModel("Income"),
                "outcome" => new OperationsViewModel("Outcome"),
                "products" => new ProductsViewModel(),
                "inventory" => new InventoryViewModel(),
                "history" => new HistoryViewModel(),
                "reports" => new ReportsViewModel(),
                "users" => new UsersViewModel(),
                "settings" => new SettingsViewModel(),
                "support" => new SupportViewModel(prefill),
                _ => null
            };
            if (view != null) CurrentView = view;
        }

        private void ExecuteLogout(object window)
        {
            if (MessageBox.Show("Вы действительно хотите выйти из системы?", "Выход", 
                MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.Yes)
            {
                Session.Logout();
                var loginWin = new LoginWindow();
                loginWin.Show();
                if (window is Window currentWindow) currentWindow.Close();
            }
        }
    }
}