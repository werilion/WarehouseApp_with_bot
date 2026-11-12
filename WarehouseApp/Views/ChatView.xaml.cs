using System.Collections.Specialized;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;
using WarehouseApp.ViewModels;

namespace WarehouseApp.Views
{
    public partial class ChatView : UserControl
    {
        public ChatView()
        {
            InitializeComponent();
            // Когда приходит ViewModel, подписываемся на новые сообщения, чтобы прокручивать чат вниз
            DataContextChanged += OnDataContextChanged;
        }

        private void OnDataContextChanged(object sender, DependencyPropertyChangedEventArgs e)
        {
            if (e.NewValue is ChatViewModel vm)
            {
                vm.Messages.CollectionChanged += OnMessagesChanged;
                ScrollToEnd();
            }
        }

        private void OnMessagesChanged(object? sender, NotifyCollectionChangedEventArgs e) => ScrollToEnd();

        private void ScrollToEnd()
        {
            // Прокрутка после того, как интерфейс отрисовал новые сообщения
            Dispatcher.BeginInvoke(new Action(() => MessagesScroll.ScrollToEnd()), DispatcherPriority.Background);
        }
    }
}
