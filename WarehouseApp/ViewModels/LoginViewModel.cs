using System;
using System.Windows;
using WarehouseApp.Infrastructure;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    public class LoginViewModel : ViewModelBase
    {
        private string _login;
        private string _errorMessage;
        private readonly AuthService _authService;

        public string Login
        {
            get => _login;
            set { _login = value; OnPropertyChanged(); }
        }

        public string Password { get; set; }

        public string ErrorMessage
        {
            get => _errorMessage;
            set { _errorMessage = value; OnPropertyChanged(); }
        }

        public RelayCommand LoginCommand { get; }

        public LoginViewModel()
        {
            _authService = new AuthService();
            LoginCommand = new RelayCommand(ExecuteLogin);
        }

        private void ExecuteLogin(object parameter)
        {
            if (string.IsNullOrEmpty(Login) || string.IsNullOrEmpty(Password))
            {
                ErrorMessage = "Введите логин и пароль";
                return;
            }

            try
            {
                var user = _authService.Login(Login, Password);
                if (user != null)
                {
                    Session.CurrentUser = user;
                    
                    // Создаем главное окно
                    var mainWindow = new MainWindow();
                    Application.Current.MainWindow = mainWindow;
                    
                    mainWindow.Show();

                    // Закрываем окно входа
                    if (parameter is Window loginWindow)
                    {
                        loginWindow.Close();
                    }
                }
                else
                {
                    ErrorMessage = "Неверный логин или пароль";
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка: {ex.Message}");
            }
        }
    }
}