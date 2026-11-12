using System.Collections.ObjectModel;
using System.Windows;
using Microsoft.Data.SqlClient;
using WarehouseApp.Infrastructure;
using WarehouseApp.Models;
using WarehouseApp.Services;

namespace WarehouseApp.ViewModels
{
    /// <summary>
    /// Страница «Техподдержка»: форма обращения, контакты и список обращений.
    /// Обычный пользователь видит свои обращения, администратор - все и может менять статус.
    /// </summary>
    public class SupportViewModel : ViewModelBase
    {
        private string? _selectedSubject;
        private string _description = "";
        private string _contact = "";
        private string _statusMessage = "";

        public ObservableCollection<SupportTicket> Tickets { get; } = new();

        public ObservableCollection<string> Subjects { get; } = new()
        {
            "Ошибка при входе",
            "Ошибка при оформлении прихода или расхода",
            "Неверные остатки",
            "Проблема с отчётами",
            "Нужен доступ или новая роль",
            "Другое"
        };

        public string? SelectedSubject
        {
            get => _selectedSubject;
            set { _selectedSubject = value; OnPropertyChanged(); }
        }

        public string Description
        {
            get => _description;
            set { _description = value; OnPropertyChanged(); }
        }

        public string Contact
        {
            get => _contact;
            set { _contact = value; OnPropertyChanged(); }
        }

        public string StatusMessage
        {
            get => _statusMessage;
            set { _statusMessage = value; OnPropertyChanged(); }
        }

        public string Phone => SupportInfo.Phone;
        public string Email => SupportInfo.Email;
        public string WorkingHours => SupportInfo.WorkingHours;

        public bool IsAdmin => Session.CurrentUser?.RoleId == 1;
        public Visibility AdminVisibility => IsAdmin ? Visibility.Visible : Visibility.Collapsed;
        public string ListTitle => IsAdmin ? "ВСЕ ОБРАЩЕНИЯ" : "МОИ ОБРАЩЕНИЯ";

        public RelayCommand SendCommand { get; }
        public RelayCommand ChangeStatusCommand { get; }

        /// <param name="prefill">Текст, который бот передаёт в описание проблемы (например, последний вопрос пользователя).</param>
        public SupportViewModel(string? prefill = null)
        {
            if (!string.IsNullOrWhiteSpace(prefill))
            {
                Description = prefill;
                SelectedSubject = "Другое";
            }

            SendCommand = new RelayCommand(o => ExecuteSend(),
                o => !string.IsNullOrWhiteSpace(SelectedSubject) && !string.IsNullOrWhiteSpace(Description));
            ChangeStatusCommand = new RelayCommand(o => ExecuteChangeStatus(o));

            LoadTickets();
        }

        private void LoadTickets()
        {
            Tickets.Clear();
            try
            {
                using (var conn = DatabaseHelper.GetConnection())
                {
                    conn.Open();
                    string sql = @"SELECT t.Id, t.UserId, u.FullName, t.Subject, t.Description, t.Contact, t.Status, t.CreatedAt
                                   FROM SupportTickets t
                                   JOIN Users u ON t.UserId = u.Id "
                               + (IsAdmin ? "" : "WHERE t.UserId = @uid ")
                               + "ORDER BY t.CreatedAt DESC";
                    using (var cmd = new SqlCommand(sql, conn))
                    {
                        if (!IsAdmin) cmd.Parameters.AddWithValue("@uid", Session.CurrentUser!.Id);
                        using (var r = cmd.ExecuteReader())
                        {
                            while (r.Read())
                            {
                                Tickets.Add(new SupportTicket
                                {
                                    Id = (int)r["Id"],
                                    UserId = (int)r["UserId"],
                                    UserName = r["FullName"].ToString() ?? "",
                                    Subject = r["Subject"].ToString() ?? "",
                                    Description = r["Description"].ToString() ?? "",
                                    Contact = r["Contact"] == DBNull.Value ? "" : r["Contact"].ToString() ?? "",
                                    Status = r["Status"].ToString() ?? "Новое",
                                    CreatedAt = (DateTime)r["CreatedAt"]
                                });
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                StatusMessage = "Не удалось загрузить обращения: " + ex.Message;
            }
        }

        private void ExecuteSend()
        {
            try
            {
                int id;
                using (var conn = DatabaseHelper.GetConnection())
                {
                    conn.Open();
                    var cmd = new SqlCommand(
                        @"INSERT INTO SupportTickets (UserId, Subject, Description, Contact, Status, CreatedAt)
                          OUTPUT INSERTED.Id
                          VALUES (@u, @s, @d, @c, N'Новое', GETDATE())", conn);
                    cmd.Parameters.AddWithValue("@u", Session.CurrentUser!.Id);
                    cmd.Parameters.AddWithValue("@s", SelectedSubject!);
                    cmd.Parameters.AddWithValue("@d", Description.Trim());
                    cmd.Parameters.AddWithValue("@c", string.IsNullOrWhiteSpace(Contact) ? DBNull.Value : (object)Contact.Trim());
                    id = (int)cmd.ExecuteScalar();
                }
                StatusMessage = $"Обращение №{id} отправлено. Статус: «Новое».";
                Description = "";
                SelectedSubject = null;
                LoadTickets();
            }
            catch (Exception ex)
            {
                StatusMessage = "Не удалось отправить обращение: " + ex.Message;
            }
        }

        private void ExecuteChangeStatus(object? obj)
        {
            if (!IsAdmin || obj is not SupportTicket ticket) return;
            try
            {
                string next = SupportInfo.NextStatus(ticket.Status);
                using (var conn = DatabaseHelper.GetConnection())
                {
                    conn.Open();
                    var cmd = new SqlCommand("UPDATE SupportTickets SET Status = @s WHERE Id = @id", conn);
                    cmd.Parameters.AddWithValue("@s", next);
                    cmd.Parameters.AddWithValue("@id", ticket.Id);
                    cmd.ExecuteNonQuery();
                }
                StatusMessage = $"Обращение №{ticket.Id}: статус «{next}».";
                LoadTickets();
            }
            catch (Exception ex)
            {
                StatusMessage = "Не удалось изменить статус: " + ex.Message;
            }
        }
    }
}
