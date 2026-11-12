/* =====================================================================
   WarehouseApp - создание базы данных WarehouseDB с нуля
   СУБД: Microsoft SQL Server (в том числе LocalDB: (localdb)\MSSQLLocalDB)

   ВНИМАНИЕ: если база WarehouseDB уже существует, скрипт её УДАЛИТ
   и создаст заново. Все данные в ней будут потеряны.

   Таблицы:
     Roles, Users              - роли и пользователи (пароль хранится как SHA-256)
     Categories, Products      - категории и товары (Products.Quantity - текущий остаток)
     Contractors               - контрагенты (поставщики и покупатели)
     Documents, DocumentItems  - документы прихода/расхода и их позиции
     SystemSettings            - настройки склада (одна строка с Id = 1)
     SupportTickets            - обращения в техподдержку

   Учётные записи для входа после создания базы:
     admin    / admin123     (Администратор)
     manager  / manager123   (Менеджер)
     sklad    / sklad123     (Сотрудник склада)
   ===================================================================== */

USE master;
GO

IF DB_ID(N'WarehouseDB') IS NOT NULL
BEGIN
    ALTER DATABASE WarehouseDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE WarehouseDB;
END
GO

CREATE DATABASE WarehouseDB COLLATE Cyrillic_General_CI_AS;
GO

USE WarehouseDB;
GO

SET NOCOUNT ON;
GO

/* ---------------------------- Таблицы ---------------------------- */

CREATE TABLE dbo.Roles
(
    Id   INT IDENTITY(1,1) NOT NULL,
    Name NVARCHAR(50)      NOT NULL,
    CONSTRAINT PK_Roles PRIMARY KEY (Id),
    CONSTRAINT UQ_Roles_Name UNIQUE (Name)
);
GO

CREATE TABLE dbo.Users
(
    Id       INT IDENTITY(1,1) NOT NULL,
    Login    NVARCHAR(50)      NOT NULL,
    Password NVARCHAR(64)      NOT NULL,   -- SHA-256 в виде 64 шестнадцатеричных символов
    FullName NVARCHAR(150)     NOT NULL,
    RoleId   INT               NOT NULL,
    CONSTRAINT PK_Users PRIMARY KEY (Id),
    CONSTRAINT UQ_Users_Login UNIQUE (Login),
    CONSTRAINT FK_Users_Roles FOREIGN KEY (RoleId) REFERENCES dbo.Roles (Id)
);
GO

CREATE TABLE dbo.Categories
(
    Id   INT IDENTITY(1,1) NOT NULL,
    Name NVARCHAR(100)     NOT NULL,
    CONSTRAINT PK_Categories PRIMARY KEY (Id),
    CONSTRAINT UQ_Categories_Name UNIQUE (Name)
);
GO

CREATE TABLE dbo.Products
(
    Id          INT IDENTITY(1,1) NOT NULL,
    Name        NVARCHAR(200)     NOT NULL,
    CategoryId  INT               NOT NULL,
    Description NVARCHAR(500)     NULL,
    Price       DECIMAL(18,2)     NOT NULL CONSTRAINT DF_Products_Price DEFAULT (0),
    Unit        NVARCHAR(20)      NOT NULL CONSTRAINT DF_Products_Unit DEFAULT (N'шт'),
    Quantity    DECIMAL(18,3)     NOT NULL CONSTRAINT DF_Products_Quantity DEFAULT (0),
    CONSTRAINT PK_Products PRIMARY KEY (Id),
    CONSTRAINT FK_Products_Categories FOREIGN KEY (CategoryId) REFERENCES dbo.Categories (Id),
    CONSTRAINT CK_Products_Price CHECK (Price >= 0),
    CONSTRAINT CK_Products_Quantity CHECK (Quantity >= 0)   -- остаток не может быть отрицательным
);
GO

CREATE TABLE dbo.Contractors
(
    Id      INT IDENTITY(1,1) NOT NULL,
    Name    NVARCHAR(200)     NOT NULL,
    Phone   NVARCHAR(30)      NULL,
    Address NVARCHAR(300)     NULL,
    CONSTRAINT PK_Contractors PRIMARY KEY (Id)
);
GO

CREATE TABLE dbo.Documents
(
    Id           INT IDENTITY(1,1) NOT NULL,
    DocType      NVARCHAR(10)      NOT NULL,   -- Income (приход) или Outcome (расход)
    DocDate      DATETIME          NOT NULL CONSTRAINT DF_Documents_DocDate DEFAULT (GETDATE()),
    ContractorId INT               NOT NULL,
    UserId       INT               NOT NULL,
    TotalAmount  DECIMAL(18,2)     NOT NULL CONSTRAINT DF_Documents_Total DEFAULT (0),
    CONSTRAINT PK_Documents PRIMARY KEY (Id),
    CONSTRAINT CK_Documents_DocType CHECK (DocType IN (N'Income', N'Outcome')),
    CONSTRAINT FK_Documents_Contractors FOREIGN KEY (ContractorId) REFERENCES dbo.Contractors (Id),
    CONSTRAINT FK_Documents_Users FOREIGN KEY (UserId) REFERENCES dbo.Users (Id)
);
GO

CREATE TABLE dbo.DocumentItems
(
    Id         INT IDENTITY(1,1) NOT NULL,
    DocumentId INT               NOT NULL,
    ProductId  INT               NOT NULL,
    Quantity   DECIMAL(18,3)     NOT NULL,
    Price      DECIMAL(18,2)     NOT NULL,
    CONSTRAINT PK_DocumentItems PRIMARY KEY (Id),
    -- при удалении документа его позиции удаляются автоматически
    CONSTRAINT FK_DocumentItems_Documents FOREIGN KEY (DocumentId) REFERENCES dbo.Documents (Id) ON DELETE CASCADE,
    -- товар, который есть в документах, удалить нельзя (ошибка 547, её перехватывает программа)
    CONSTRAINT FK_DocumentItems_Products FOREIGN KEY (ProductId) REFERENCES dbo.Products (Id),
    CONSTRAINT CK_DocumentItems_Quantity CHECK (Quantity > 0),
    CONSTRAINT CK_DocumentItems_Price CHECK (Price >= 0)
);
GO

CREATE TABLE dbo.SystemSettings
(
    Id               INT           NOT NULL,
    WarehouseName    NVARCHAR(150) NOT NULL,
    WarehouseAddress NVARCHAR(300) NOT NULL,
    CONSTRAINT PK_SystemSettings PRIMARY KEY (Id),
    CONSTRAINT CK_SystemSettings_SingleRow CHECK (Id = 1)   -- настройки хранятся одной строкой
);
GO

CREATE TABLE dbo.SupportTickets
(
    Id          INT IDENTITY(1,1) NOT NULL,
    UserId      INT               NOT NULL,
    Subject     NVARCHAR(100)     NOT NULL,
    Description NVARCHAR(2000)    NOT NULL,
    Contact     NVARCHAR(150)     NULL,
    Status      NVARCHAR(20)      NOT NULL CONSTRAINT DF_SupportTickets_Status DEFAULT (N'Новое'),
    CreatedAt   DATETIME          NOT NULL CONSTRAINT DF_SupportTickets_CreatedAt DEFAULT (GETDATE()),
    CONSTRAINT PK_SupportTickets PRIMARY KEY (Id),
    CONSTRAINT CK_SupportTickets_Status CHECK (Status IN (N'Новое', N'В работе', N'Закрыто')),
    -- обращения удаляются вместе с пользователем
    CONSTRAINT FK_SupportTickets_Users FOREIGN KEY (UserId) REFERENCES dbo.Users (Id) ON DELETE CASCADE
);
GO

/* ---------------------------- Индексы ---------------------------- */

CREATE INDEX IX_Products_CategoryId      ON dbo.Products (CategoryId);
CREATE INDEX IX_Products_Name            ON dbo.Products (Name);
CREATE INDEX IX_Documents_DocDate        ON dbo.Documents (DocDate DESC);
CREATE INDEX IX_Documents_ContractorId   ON dbo.Documents (ContractorId);
CREATE INDEX IX_Documents_UserId         ON dbo.Documents (UserId);
CREATE INDEX IX_DocumentItems_DocumentId ON dbo.DocumentItems (DocumentId);
CREATE INDEX IX_DocumentItems_ProductId  ON dbo.DocumentItems (ProductId);
CREATE INDEX IX_SupportTickets_UserId    ON dbo.SupportTickets (UserId);
GO

/* ------------------- Начальные данные (справочники) ------------------- */

INSERT INTO dbo.Roles (Name) VALUES (N'Администратор'), (N'Менеджер'), (N'Сотрудник склада');
-- Id ролей: 1 - администратор, 2 - менеджер, 3 - сотрудник склада (на это опирается программа)
GO

INSERT INTO dbo.Users (Login, Password, FullName, RoleId) VALUES
    (N'admin',   N'240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',   N'Администратор системы', 1),
    (N'manager', N'866485796cfa8d7c0cf7111640205b83076433547577511d81f8030ae99ecea5', N'Петрова Анна Сергеевна', 2),
    (N'sklad',   N'9e0cb207aec9bde8d197586a81d782a4d594621557343201be7ffed709e1ac62',   N'Иванов Иван Иванович',   3);
GO

INSERT INTO dbo.SystemSettings (Id, WarehouseName, WarehouseAddress)
VALUES (1, N'Центральный склад', N'г. Москва, ул. Складская, д. 1');
GO

INSERT INTO dbo.Categories (Name) VALUES
    (N'Электроника'), (N'Канцелярия'), (N'Продукты питания'), (N'Хозтовары'), (N'Инструменты');
GO

INSERT INTO dbo.Contractors (Name, Phone, Address) VALUES
    (N'ООО «ТехноСнаб»',  N'+7 (495) 111-22-33', N'г. Москва, ул. Промышленная, д. 5'),
    (N'ИП Соколов А. В.', N'+7 (916) 222-33-44', N'г. Москва, ул. Торговая, д. 12'),
    (N'ООО «ОфисПлюс»',   N'+7 (495) 333-44-55', N'г. Химки, Ленинградское ш., д. 8');
GO

/* ---------------- Тестовые товары (остаток 0, он появится после прихода) ---------------- */

INSERT INTO dbo.Products (Name, CategoryId, Description, Price, Unit, Quantity)
SELECT v.Name, c.Id, v.Description, v.Price, v.Unit, 0
FROM (VALUES
    (N'Ноутбук Lenovo IdeaPad',      N'Электроника',     N'15.6", 8 ГБ ОЗУ, SSD 256 ГБ', 52990.00, N'шт'),
    (N'Мышь беспроводная',           N'Электроника',     N'USB-приёмник',                  790.00, N'шт'),
    (N'Бумага А4 (500 листов)',      N'Канцелярия',      N'80 г/м2',                       420.00, N'пач'),
    (N'Ручка шариковая синяя',       N'Канцелярия',      NULL,                              18.00, N'шт'),
    (N'Чай чёрный (100 пакетиков)',  N'Продукты питания',NULL,                             250.00, N'уп'),
    (N'Кофе растворимый 190 г',      N'Продукты питания',NULL,                             640.00, N'шт'),
    (N'Моющее средство 5 л',         N'Хозтовары',       NULL,                             380.00, N'шт'),
    (N'Перчатки рабочие',            N'Хозтовары',       N'Хлопок с ПВХ',                   65.00, N'пара'),
    (N'Дрель аккумуляторная',        N'Инструменты',     N'18 В, два аккумулятора',       6490.00, N'шт')
) AS v(Name, CategoryName, Description, Price, Unit)
JOIN dbo.Categories c ON c.Name = v.CategoryName;
GO

/* ------------- Тестовые документы: приход и расход (остатки пересчитываются) ------------- */

DECLARE @income INT, @outcome INT;
DECLARE @supplier INT = (SELECT Id FROM dbo.Contractors WHERE Name = N'ООО «ТехноСнаб»');
DECLARE @buyer    INT = (SELECT Id FROM dbo.Contractors WHERE Name = N'ИП Соколов А. В.');

-- Приход: товар поступил на склад
INSERT INTO dbo.Documents (DocType, DocDate, ContractorId, UserId, TotalAmount)
VALUES (N'Income', DATEADD(DAY, -7, GETDATE()), @supplier, 3, 0);
SET @income = SCOPE_IDENTITY();

INSERT INTO dbo.DocumentItems (DocumentId, ProductId, Quantity, Price)
SELECT @income, p.Id, v.Qty, p.Price
FROM (VALUES
    (N'Ноутбук Lenovo IdeaPad', 15), (N'Мышь беспроводная', 80), (N'Бумага А4 (500 листов)', 200),
    (N'Ручка шариковая синяя', 500), (N'Чай чёрный (100 пакетиков)', 120), (N'Кофе растворимый 190 г', 60),
    (N'Моющее средство 5 л', 40), (N'Перчатки рабочие', 300), (N'Дрель аккумуляторная', 12)
) AS v(Name, Qty)
JOIN dbo.Products p ON p.Name = v.Name;

UPDATE p SET p.Quantity = p.Quantity + di.Quantity
FROM dbo.Products p JOIN dbo.DocumentItems di ON di.ProductId = p.Id
WHERE di.DocumentId = @income;

UPDATE dbo.Documents
SET TotalAmount = (SELECT SUM(Quantity * Price) FROM dbo.DocumentItems WHERE DocumentId = @income)
WHERE Id = @income;

-- Расход: часть товара отгружена покупателю
INSERT INTO dbo.Documents (DocType, DocDate, ContractorId, UserId, TotalAmount)
VALUES (N'Outcome', DATEADD(DAY, -2, GETDATE()), @buyer, 3, 0);
SET @outcome = SCOPE_IDENTITY();

INSERT INTO dbo.DocumentItems (DocumentId, ProductId, Quantity, Price)
SELECT @outcome, p.Id, v.Qty, p.Price
FROM (VALUES
    (N'Ноутбук Lenovo IdeaPad', 3), (N'Мышь беспроводная', 10), (N'Бумага А4 (500 листов)', 40),
    (N'Ручка шариковая синяя', 100), (N'Чай чёрный (100 пакетиков)', 20)
) AS v(Name, Qty)
JOIN dbo.Products p ON p.Name = v.Name;

UPDATE p SET p.Quantity = p.Quantity - di.Quantity
FROM dbo.Products p JOIN dbo.DocumentItems di ON di.ProductId = p.Id
WHERE di.DocumentId = @outcome;

UPDATE dbo.Documents
SET TotalAmount = (SELECT SUM(Quantity * Price) FROM dbo.DocumentItems WHERE DocumentId = @outcome)
WHERE Id = @outcome;
GO

/* ------------------------ Тестовое обращение в техподдержку ------------------------ */

INSERT INTO dbo.SupportTickets (UserId, Subject, Description, Contact, Status)
VALUES (3, N'Другое', N'Не получается найти раздел «Отчёты» в меню.', N'+7 (900) 000-00-00', N'Новое');
GO

/* ------------------------------- Проверка ------------------------------- */

SELECT N'Роли' AS [Таблица], COUNT(*) AS [Строк] FROM dbo.Roles
UNION ALL SELECT N'Пользователи', COUNT(*) FROM dbo.Users
UNION ALL SELECT N'Категории', COUNT(*) FROM dbo.Categories
UNION ALL SELECT N'Товары', COUNT(*) FROM dbo.Products
UNION ALL SELECT N'Контрагенты', COUNT(*) FROM dbo.Contractors
UNION ALL SELECT N'Документы', COUNT(*) FROM dbo.Documents
UNION ALL SELECT N'Позиции документов', COUNT(*) FROM dbo.DocumentItems
UNION ALL SELECT N'Обращения в техподдержку', COUNT(*) FROM dbo.SupportTickets;
GO

SELECT p.Name AS [Товар], c.Name AS [Категория], p.Quantity AS [Остаток], p.Unit AS [Ед.]
FROM dbo.Products p JOIN dbo.Categories c ON c.Id = p.CategoryId
ORDER BY c.Name, p.Name;
GO
