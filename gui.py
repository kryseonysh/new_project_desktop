#gui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from models.users import verify_user, register_user, getUserRole, getUserEmail, get_all_users
from models.clients import add_client, get_all_clients, update_client_field, delete_client, get_client_by_email, get_full_name
from models.orders import add_order, get_all_orders, update_order_field, delete_order, update_order_status, get_client_orders
from models.hotels import add_hotel, get_all_hotels, update_hotel_field, delete_hotel
from models.analytics import add_analytics, get_all_analytics, update_analytics_field,  delete_analytics, sales_summary, transport_order_count
from models.transport import add_transport,  get_all_transport, update_transport_field, delete_transport
from models.discounts import add_discount,  get_all_discounts, update_discount_field, delete_discount, active_discounts
from models.routes import add_route, get_all_routes,  update_route_field, delete_route, get_routes_by_startpoint, route_order_count

class UserManagementGUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app 
        self.client_management_frame = tk.Frame(self.root)
        self.order_management_frame = tk.Frame(self.root)
        self.hotel_management_frame = tk.Frame(self.root)
        self.analytics_management_frame = tk.Frame(self.root)
        self.transport_management_frame = tk.Frame(self.root)
        self.discounts_management_frame = tk.Frame(self.root)
        self.routes_management_frame = tk.Frame(self.root)
        self.main_menu_frame = tk.Frame(self.root)
  
        self.root.title("Туристическое агенство")

        self.is_logged_in = False
        self.current_user_role = None

        # User Login Frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=10)

        tk.Label(self.login_frame, text="Логин пользователя").grid(row=0, columnspan=2)

        tk.Label(self.login_frame, text="Имя пользователя").grid(row=1, column=0)
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.grid(row=1, column=1)

        tk.Label(self.login_frame, text="Пароль").grid(row=2, column=0)
        self.login_password_entry = tk.Entry(self.login_frame, show='*')
        self.login_password_entry.grid(row=2, column=1)

        tk.Button(self.login_frame, text="Войти", command=self.login_user).grid(row=3, columnspan=2)
        tk.Button(self.login_frame, text="Перейти к регистрации", command=self.show_registration_frame).grid(row=4, columnspan=2)

        self.registration_frame = tk.Frame(self.root)

        tk.Label(self.registration_frame, text="Регистрация пользователя").grid(row=0, columnspan=2)

        tk.Label(self.registration_frame, text="Имя пользователя").grid(row=1, column=0)
        self.registration_username_entry = tk.Entry(self.registration_frame)
        self.registration_username_entry.grid(row=1, column=1)

        tk.Label(self.registration_frame, text="Email").grid(row=2, column=0)
        self.registration_email_entry = tk.Entry(self.registration_frame)
        self.registration_email_entry.grid(row=2, column=1)

        tk.Label(self.registration_frame, text="Пароль").grid(row=3, column=0)
        self.registration_password_entry = tk.Entry(self.registration_frame, show='*')
        self.registration_password_entry.grid(row=3, column=1)

        tk.Label(self.registration_frame, text="Тип пользователя").grid(row=4, column=0)
        self.registration_role_entry = tk.Entry(self.registration_frame)
        self.registration_role_entry.grid(row=4, column=1)

        tk.Button(self.registration_frame, text="Регистрация", command=self.register_user).grid(row=5, columnspan=2)
        tk.Button(self.registration_frame, text="Обратно к входу", command=self.show_login_frame).grid(row=6, columnspan=2)

    def create_main_menu(self):
        """Create the main menu based on user role."""
        tk.Label(self.main_menu_frame, text="Главное меню", font=("Arial", 16)).grid(row=0, columnspan=4)

        if self.current_user_role == "администратор":
            tk.Button(self.main_menu_frame, text="Клиенты", command=self.show_manage_clients).grid(row=1, columnspan=4)
            tk.Button(self.main_menu_frame, text="Заказы", command=self.show_manage_orders).grid(row=2, columnspan=4)
            tk.Button(self.main_menu_frame, text="Отели", command=self.show_manage_hotels).grid(row=3, columnspan=4)
            tk.Button(self.main_menu_frame, text="Аналитика", command=self.show_manage_analytics).grid(row=4, columnspan=4)
            tk.Button(self.main_menu_frame, text="Транспорт", command=self.show_manage_transport).grid(row=5, columnspan=4)
            tk.Button(self.main_menu_frame, text="Скидки", command=self.show_manage_discounts).grid(row=6, columnspan=4)
            tk.Button(self.main_menu_frame, text="Маршруты", command=self.show_manage_routes).grid(row=7, columnspan=4)
            tk.Button(self.main_menu_frame, text="Список пользователей", command=self.get_users).grid(row=8, columnspan=4)
            tk.Button(self.main_menu_frame, text="Выход", command=self.logout).grid(row=9, columnspan=4)

        elif self.current_user_role == "менеджер по продажам":
            tk.Button(self.main_menu_frame, text="Клиенты", command=self.show_manage_clients).grid(row=1, columnspan=4)
            tk.Button(self.main_menu_frame, text="Заказы", command=self.show_manage_orders).grid(row=2, columnspan=4)
            tk.Button(self.main_menu_frame, text="Отели", command=self.show_manage_hotels).grid(row=3, columnspan=4)
            tk.Button(self.main_menu_frame, text="Транспорт", command=self.show_manage_transport).grid(row=4, columnspan=4)
            tk.Button(self.main_menu_frame, text="Скидки", command=self.show_manage_discounts).grid(row=5, columnspan=4)
            tk.Button(self.main_menu_frame, text="Маршруты", command=self.show_manage_routes).grid(row=6, columnspan=4)
            tk.Button(self.main_menu_frame, text="Выход", command=self.logout).grid(row=7, columnspan=4)

        elif self.current_user_role == "клиент":
            tk.Button(self.main_menu_frame, text="Показать маршруты", command=self.get_all_routes).grid(row=1, columnspan=4)
            tk.Button(self.main_menu_frame, text="Найти маршруты по точке начала маршрута", command=self.get_routes_startpoint).grid(row=2, columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать действующие скидки", command=self.get_active_discounts).grid(row=3, columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать транспорт", command=self.get_all_transport).grid(row=4, columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать отели", command=self.get_all_hotels).grid(row=5, columnspan=4)
            tk.Button(self.main_menu_frame, text="Найти себя в списке клиентов", command=self.get_client).grid(row=6, columnspan=4)
            tk.Button(self.main_menu_frame, text="Зарегистрироваться как клиент", command=self.add_client).grid(row=7, columnspan=4)
            tk.Button(self.main_menu_frame, text="Сделать заказ", command=self.add_order).grid(row=8, columnspan=4)
            tk.Button(self.main_menu_frame, text="Выход", command=self.logout).grid(row=9, columnspan=4)

        elif self.current_user_role == "аналитик":
            tk.Button(self.main_menu_frame, text="Показать маршруты и количество заказов", command=self.get_route_order_count).grid(row=1, columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать скидки", command=self.get_all_discounts).grid(row=2, columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать действующие скидки", command=self.get_active_discounts).grid(row=3, columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать транспорт", command=self.get_all_transport).grid(row=4, columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать количество заказов транспорта", command=self.get_transport_order_count).grid(row=5,  columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать отели", command=self.get_all_hotels).grid(row=6, columnspan=4)
            tk.Button(self.main_menu_frame, text="Показать заказы", command=self.client_orders).grid(row=7, columnspan=4)
            tk.Button(self.main_menu_frame, text="Аналитика", command=self.show_manage_analytics).grid(row=8, columnspan=4)
            tk.Button(self.main_menu_frame, text="Выход", command=self.logout).grid(row=9, columnspan=4)
        self.main_menu_frame.pack(pady=10)
    
    def show_manage_clients(self):
        self.main_menu_frame.pack_forget()
        self.client_management_frame.pack_forget()
        self.order_management_frame.pack_forget()
        self.hotel_management_frame.pack_forget()
        self.analytics_management_frame.pack_forget()
        self.transport_management_frame.pack_forget()
        self.discounts_management_frame.pack_forget()
        self.routes_management_frame.pack_forget()

        self.client_management_frame.pack(pady=10)

        tk.Button(self.client_management_frame, text="Добавить клиента", command=self.add_client).grid(row=1, columnspan=4)
        tk.Button(self.client_management_frame, text="Показать полное имя клиента по ID", command=self.fullname_client).grid(row=2, columnspan=4)
        tk.Button(self.client_management_frame, text="Удалить клиента", command=self.delete_client).grid(row=3, columnspan=4)
        tk.Button(self.client_management_frame, text="Список клиентов", command=self.get_all_clients).grid(row=4, columnspan=4)
        tk.Button(self.client_management_frame, text="Изменить информацию о клиенте", command=self.update_client_field).grid(row=5, columnspan=4)
        tk.Button(self.client_management_frame, text="Назад к главному меню", command=self.show_main_menu).grid(row=6, columnspan=4)

    def show_manage_orders(self):
        self.main_menu_frame.pack_forget()
        self.client_management_frame.pack_forget()
        self.order_management_frame.pack_forget()
        self.hotel_management_frame.pack_forget()
        self.analytics_management_frame.pack_forget()
        self.transport_management_frame.pack_forget()
        self.discounts_management_frame.pack_forget()
        self.routes_management_frame.pack_forget()

        self.order_management_frame.pack(pady=10)

        tk.Button(self.order_management_frame, text="Добавить заказ", command=self.add_order).grid(row=1, columnspan=4)
        tk.Button(self.order_management_frame, text="Удалить заказ", command=self.delete_order).grid(row=2, columnspan=4)
        tk.Button(self.order_management_frame, text="Список заказов", command=self.get_all_orders).grid(row=3, columnspan=4)
        tk.Button(self.order_management_frame, text="Изменить информацию о заказе", command=self.update_order_field).grid(row=4, columnspan=4)
        tk.Button(self.order_management_frame, text="Изменить информацию о статусе заказа", command=self.update_order_status).grid(row=5, columnspan=4)
        tk.Button(self.order_management_frame, text="Назад к главному меню", command=self.show_main_menu).grid(row=6, columnspan=4)

    def show_manage_hotels(self):
        self.main_menu_frame.pack_forget()
        self.client_management_frame.pack_forget()
        self.order_management_frame.pack_forget()
        self.hotel_management_frame.pack_forget()
        self.analytics_management_frame.pack_forget()
        self.transport_management_frame.pack_forget()
        self.discounts_management_frame.pack_forget()
        self.routes_management_frame.pack_forget()

        self.hotel_management_frame.pack(pady=10)

        tk.Button(self.hotel_management_frame, text="Добавить отель", command=self.add_hotel).grid(row=1, columnspan=4)
        tk.Button(self.hotel_management_frame, text="Удалить отель", command=self.delete_hotel).grid(row=2, columnspan=4)
        tk.Button(self.hotel_management_frame, text="Список отелей", command=self.get_all_hotels).grid(row=3, columnspan=4)
        tk.Button(self.hotel_management_frame, text="Изменить информацию об отеле", command=self.update_hotel_field).grid(row=4, columnspan=4)
        tk.Button(self.hotel_management_frame, text="Назад к главному меню", command=self.show_main_menu).grid(row=5, columnspan=4)

    def show_manage_analytics(self):
        self.main_menu_frame.pack_forget()
        self.client_management_frame.pack_forget()
        self.order_management_frame.pack_forget()
        self.hotel_management_frame.pack_forget()
        self.analytics_management_frame.pack_forget()
        self.transport_management_frame.pack_forget()
        self.discounts_management_frame.pack_forget()
        self.routes_management_frame.pack_forget()

        self.analytics_management_frame.pack(pady=10)

        tk.Button(self.analytics_management_frame, text="Добавить аналитику", command=self.add_analytics).grid(row=1, columnspan=4)
        tk.Button(self.analytics_management_frame, text="Удалить аналитику", command=self.delete_analytics).grid(row=2, columnspan=4)
        tk.Button(self.analytics_management_frame, text="Список отчетов", command=self.get_all_analytics).grid(row=3, columnspan=4)
        tk.Button(self.analytics_management_frame, text="Изменить информацию об отчете", command=self.update_analytics_field).grid(row=4, columnspan=4)
        tk.Button(self.analytics_management_frame, text="Продажи за всё время", command=self.get_sales_summary).grid(row=5, columnspan=4)
        tk.Button(self.analytics_management_frame, text="Назад к главному меню", command=self.show_main_menu).grid(row=6, columnspan=4)

    def show_manage_transport(self):
        self.main_menu_frame.pack_forget()
        self.client_management_frame.pack_forget()
        self.order_management_frame.pack_forget()
        self.hotel_management_frame.pack_forget()
        self.analytics_management_frame.pack_forget()
        self.transport_management_frame.pack_forget()
        self.discounts_management_frame.pack_forget()
        self.routes_management_frame.pack_forget()

        self.transport_management_frame.pack(pady=10)

        tk.Button(self.transport_management_frame, text="Добавить транспорт", command=self.add_transport).grid(row=1, columnspan=4)
        tk.Button(self.transport_management_frame, text="Удалить транспорт", command=self.delete_transport).grid(row=2, columnspan=4)
        tk.Button(self.transport_management_frame, text="Список транспорта", command=self.get_all_transport).grid(row=3, columnspan=4)
        tk.Button(self.transport_management_frame, text="Изменить информацию о транспорте", command=self.update_transport_field).grid(row=4, columnspan=4)
        tk.Button(self.transport_management_frame, text="Назад к главному меню", command=self.show_main_menu).grid(row=5, columnspan=4)

    def show_manage_discounts(self):
        self.main_menu_frame.pack_forget()
        self.client_management_frame.pack_forget()
        self.order_management_frame.pack_forget()
        self.hotel_management_frame.pack_forget()
        self.analytics_management_frame.pack_forget()
        self.transport_management_frame.pack_forget()
        self.discounts_management_frame.pack_forget()
        self.routes_management_frame.pack_forget()

        self.discounts_management_frame.pack(pady=10)

        tk.Button(self.discounts_management_frame, text="Добавить скидку", command=self.add_discount).grid(row=1, columnspan=4)
        tk.Button(self.discounts_management_frame, text="Удалить скидку", command=self.delete_discount).grid(row=2, columnspan=4)
        tk.Button(self.discounts_management_frame, text="Список скидок", command=self.get_all_discounts).grid(row=3, columnspan=4)
        tk.Button(self.discounts_management_frame, text="Показать действующие скидки", command=self.get_active_discounts).grid(row=4, columnspan=4)
        tk.Button(self.discounts_management_frame, text="Изменить информацию о скидке", command=self.update_discount_field).grid(row=5, columnspan=4)
        tk.Button(self.discounts_management_frame, text="Назад к главному меню", command=self.show_main_menu).grid(row=6, columnspan=4)

    def show_manage_routes(self):
        self.main_menu_frame.pack_forget()
        self.client_management_frame.pack_forget()
        self.order_management_frame.pack_forget()
        self.hotel_management_frame.pack_forget()
        self.analytics_management_frame.pack_forget()
        self.transport_management_frame.pack_forget()
        self.discounts_management_frame.pack_forget()
        self.routes_management_frame.pack_forget()

        self.routes_management_frame.pack(pady=10)

        tk.Button(self.routes_management_frame, text="Добавить маршрут", command=self.add_route).grid(row=1, columnspan=4)
        tk.Button(self.routes_management_frame, text="Удалить маршрут", command=self.delete_route).grid(row=2, columnspan=4)
        tk.Button(self.routes_management_frame, text="Список маршрутов", command=self.get_all_routes).grid(row=3, columnspan=4)
        tk.Button(self.routes_management_frame, text="Изменить информацию о маршруте", command=self.update_route_field).grid(row=4, columnspan=4)
        tk.Button(self.routes_management_frame, text = "Найти маршруты по точке начала маршрута", command=self.get_routes_startpoint).grid(row=5, columnspan=4)
        tk.Button(self.routes_management_frame, text="Назад к главному меню", command=self.show_main_menu).grid(row=6, columnspan=4)

    def logout(self):
        self.is_logged_in = False
        self.current_user_role = None
        for widget in self.main_menu_frame.winfo_children():
            widget.destroy()
        self.login_frame.pack(pady=10)
        self.login_username_entry.delete(0, tk.END)
        self.login_password_entry.delete(0, tk.END)
        tk.Label(self.login_frame, text="Вы вышли из системы.", fg="red").grid(row=5, columnspan=2)

    def get_users(self):
        users = get_all_users()
        if not users: 
            messagebox.showinfo("Пользователи", "Нет пользователей для отображения.")
            return
        user_list = ""
        for user in users:
            user_list += f"ID: {user[0]}, username: {user[1]}, email: {user[2]}, role: {user[4]}, создан: {user[5]}\n"
        messagebox.showinfo("Пользователи", user_list)

    def add_client(self):
        name = simpledialog.askstring("Ввод", "Введите имя клиента:")
        surname = simpledialog.askstring("Ввод", "Введите фамилию клиента:")
        fathersname = simpledialog.askstring("Ввод", "Введите отчество клиента:")
        passport = simpledialog.askstring("Ввод", "Введите паспортные данные клиента:")
        number = simpledialog.askstring("Ввод", "Введите номер телефона клиента:")
        email = simpledialog.askstring("Ввод", "Введите e-mail клиента:")
        address = simpledialog.askstring("Ввод", "Введите адрес клиента:")
        status =  simpledialog.askstring("Ввод", "Введите статус клиента(True/False):")

        if add_client(name, surname, fathersname, passport, number, email, address, status):
            messagebox.showinfo("Клиент добавлен", "Клиент успешно добавлен!")
        else:
            messagebox.showerror("Клиент не добавлен", "Ошибка добавления клиента.")

    def delete_client(self):
        client_id = simpledialog.askinteger("Ввод", "Введите ID клиента для удаления:")
        if delete_client(client_id):
            messagebox.showinfo("Клиент удален", "Клиент успешно удален!")
        else:
            messagebox.showerror("Клиент не удален", "Ошибка удаления клиента.")

    def get_all_clients(self):
        clients = get_all_clients()
        client_list = ""
        for client in clients:
            client_list += f"ID: {client[0]}, Имя: {client[1]}, Фамилия: {client[2]}, Отчество: {client[3]}, Паспорт: {client[4]}, Телефон: {client[5]}, Email: {client[6]}, Адрес: {client[7]}, Дата регистрации: {client[8]}, Статус: {client[9]}\n"
        messagebox.showinfo("Клиенты", client_list)

    def update_client_field(self):
        client_id = simpledialog.askinteger("Ввод", "Введите ID клиента для изменения:")
        field_name = simpledialog.askstring("Ввод", "Введите поле для изменения (name, surname, fathersname, passport, number, email, address, status):")
        new_value = simpledialog.askstring("Ввод", "Введите новое значение поля:")
        if update_client_field(client_id, field_name, new_value):
            messagebox.showinfo("Изменения внесены", "Изменения успешно внесены!")
        else:
            messagebox.showerror("Изменения не внесены", "Ошибка внесения изменений.")
    
    def fullname_client(self):
        client_id = simpledialog.askinteger("Ввод", "Введите ID клиента для получения его полного имени:")
        if get_full_name(client_id) != None:
            messagebox.showinfo("Полное имя клиента", get_full_name(client_id))
        else:
            messagebox.showerror("Полное имя клиента", "Клиент не найден.")
    
    def add_order(self):
        client_id = simpledialog.askinteger("Ввод", "Введите ID клиента:")
        route_id = simpledialog.askinteger("Ввод", "Введите ID маршрута:")
        order_status = simpledialog.askstring("Ввод", "Введите статус заказа:")
        payment_method = simpledialog.askstring("Ввод", "Введите способ оплаты:")
        discount_id = simpledialog.askinteger("Ввод", "Введите ID скидки:")
        cost = simpledialog.askfloat("Ввод", "Введите стоимость заказа:")
        transport_id = simpledialog.askinteger("Ввод", "Введите ID транспорта:")
        hotel_id = simpledialog.askinteger("Ввод", "Введите ID отеля:")

        if add_order(client_id, route_id, order_status, payment_method, discount_id, cost, transport_id, hotel_id):
            messagebox.showinfo("Заказ добавлен", "Заказ успешно добавлен!")
        else:
            messagebox.showerror("Заказ не добавлен", "Ошибка создания заказа.")

    def delete_order(self):
        order_id = simpledialog.askinteger("Ввод", "Введите ID заказа для удаления:")
        if delete_order(order_id):
            messagebox.showinfo("Заказ удален", "Заказ успешно удален!")
        else:
            messagebox.showerror("Заказ не удален", "Ошибка удаления заказа.")

    def get_all_orders(self):
        orders = get_all_orders()
        order_list = ""
        for order in orders:
            order_list += f"ID: {order[0]}, ID Клиента: {order[1]}, ID Маршрута: {order[2]}, Время создания: {order[3]}, Статус заказа: {order[4]}, Метод оплаты: {order[5]}, ID Скидки: {order[6]}, Стоимость: {order[7]}, ID Транспорта: {order[8]}, ID Отеля: {order[9]}\n"
        messagebox.showinfo("Заказы", order_list)

    def update_order_field(self):
        order_id = simpledialog.askinteger("Ввод", "Введите ID заказа для изменения:")
        field_name = simpledialog.askstring("Ввод", "Введите название поля для изменения (client_Id, route_Id, payment_method, discount_Id, cost, transport_Id, hotel_Id):")
        new_value = simpledialog.askstring("Ввод", "Введите новое значение поля:")
        if update_order_field(order_id, field_name, new_value):
            messagebox.showinfo("Заказ изменен", "Заказ успешно изменен!")
        else:
            messagebox.showerror("Заказ не изменен", "Ошибка изменения заказа.")

    def update_order_status(self):
        order_id = simpledialog.askinteger("Ввод", "Введите ID заказа для изменения статуса")
        new_status = simpledialog.askstring("Ввод", "Введите новый статус заказа")
        if update_order_status(order_id, new_status):
            messagebox.showinfo("Заказ изменен", "Статус заказа успешно изменен!")
        else:
            messagebox.showerror("Заказ не изменен", "Ошибка изменения статуса заказа.")

    def client_orders(self):
        orders =  get_client_orders()
        if not orders:
            messagebox.showinfo("Заказы клиента", "Нет доступных заказов.")
            return
        order_list = ""
        for order in orders:
            order_list += f"Имя: {order[0]}, Фамилия: {order[1]},  Название маршрута: {order[2]}, Время создания заказа: {order[3]}, Стоимость:  {order[4]}\n"
        messagebox.showinfo("Заказы клиента", order_list)

    def add_hotel(self):
        star = simpledialog.askinteger("Ввод", "Введите количество звезд отеля:")
        room_class = simpledialog.askstring("Ввод", "Введите класс номера:")
        bedding = simpledialog.askstring("Ввод", "Введите тип постели:")

        if add_hotel(star, room_class, bedding):
            messagebox.showinfo("Отель добавлен", "Отель успешно добавлен!")
        else:
            messagebox.showerror("Отель не добавлен", "Ошибка добавления отеля.")

    def delete_hotel(self):
        hotel_id = simpledialog.askinteger("Ввод", "Введите ID отеля для удаления:")
        if delete_hotel(hotel_id):
            messagebox.showinfo("Отель удален", "Отель успешно удален!")
        else:
            messagebox.showerror("Отель не удален", "Ошибка удаления отеля.")

    def get_all_hotels(self):
        hotels = get_all_hotels()
        hotel_list = ""
        for hotel in hotels:
            hotel_list += f"ID: {hotel[0]}, Количество звезд: {hotel[1]}, Класс номера: {hotel[2]}, Тип постели: {hotel[3]}\n"
        messagebox.showinfo("Отели", hotel_list)

    def update_hotel_field(self):
        hotel_id = simpledialog.askinteger("Ввод", "Введите ID отеля для изменения:")
        field_name = simpledialog.askstring("Ввод", "Введите название поля для изменения (star, room_class, bedding):")
        new_value = simpledialog.askstring("Ввод", "Введите новое значение поля:")
        if update_hotel_field(hotel_id, field_name, new_value):
            messagebox.showinfo("Информация изменена", "Информация успешно изменена!")
        else:
            messagebox.showerror("Информация не изменена", "Ошибка изменения информации.")
    
    def add_analytics(self):
        report_start = simpledialog.askstring("Ввод", "Введите начало отчета:")
        report_finish = simpledialog.askstring("Ввод", "Введите окончание отчета:")

        if add_analytics(report_start, report_finish):
            messagebox.showinfo("Отчет добавлен", "Отчет успешно добавлен!")
        else:
            messagebox.showerror("Отчет не добавлен", "Ошибка добавления отчета.")

    def delete_analytics(self):
        report_id = simpledialog.askinteger("Ввод", "Введите ID отчета для удаления:")
        if delete_analytics(report_id):
            messagebox.showinfo("Отчет удален", "Отчет успешно удален!")
        else:
            messagebox.showerror("Отчет не удален", "Ошибка удаления отчета.")

    def get_all_analytics(self):
        reports = get_all_analytics()
        report_list = ""
        for report in reports:
            report_list += f"ID: {report[0]}, Начало отчета: {report[1]}, Конец отчета: {report[2]}, Продажи: {report[3]}, Количество новых клиентов: {report[4]}, Популярные маршруты: {report[5]}\n"
        messagebox.showinfo("Отчеты", report_list)

    def update_analytics_field(self):
        report_id = simpledialog.askinteger("Ввод", "Введите ID отчета для изменения:")
        field_name = simpledialog.askstring("Ввод", "Введите название поля для изменения (report_start, report_finish):")
        new_value = simpledialog.askstring("Ввод", "Введите новое значение поля:")
        if update_analytics_field(report_id, field_name, new_value):
            messagebox.showinfo("Отчет изменен", "Отчет успешно изменен!")
        else:
            messagebox.showerror("Отчет не изменен", "Ошибка изменения отчета.")
    
    def get_sales_summary(self):
        sales = sales_summary()
        sales_list = ""
        for sale in sales:
            sales_list += f"Начало отчета: {sale[0]}, Конец отчета: {sale[1]}, Продажи: {sale[2]}, Количество новых клиентов: {sale[3]}\n"
        messagebox.showinfo("Обзор продаж", sales_list)

    def add_transport(self):
        transport = simpledialog.askstring("Ввод", "Введите вид транспорта:")
        tclass = simpledialog.askstring("Ввод", "Введите класс транпорта:")
        
        if add_transport(transport, tclass):
            messagebox.showinfo("Транспорт добавлен", "Транспорт успешно добавлен!")
        else:
            messagebox.showerror("Транспорт не добавлен", "Ошибка добавления транспорта.")

    def delete_transport(self):
        transport_id = simpledialog.askinteger("Ввод", "Введите ID транспорта для удаления:")
        if delete_transport(transport_id):
            messagebox.showinfo("Транспорт удален", "Транспорт успешно удален!")
        else:
            messagebox.showerror("Транспорт не удален", "Ошибка удаления транспорта.")

    def get_all_transport(self):
        transports = get_all_transport()
        transport_list = ""
        for transport in transports:
            transport_list += f"ID: {transport[0]}, Вид транспорта: {transport[1]}, Класс: {transport[2]}\n"
        messagebox.showinfo("Транспорт", transport_list)

    def update_transport_field(self):
        transport_id = simpledialog.askinteger("Ввод", "Введите ID транспорта для изменения:")
        field_name = simpledialog.askstring("Ввод", "Введите название поля для изменения (transport, class):")
        new_value = simpledialog.askstring("Ввод", "Введите новое значение поля:")
        if update_transport_field(transport_id, field_name, new_value):
            messagebox.showinfo("Информация изменена", "Информация успешно изменена!")
        else:
            messagebox.showerror("Информация не изменена", "Ошибка изменения информации.")
    
    def get_transport_order_count(self):
        transports = transport_order_count()
        transport_list = ""
        for transport in transports:
            transport_list += f"ID: {transport[0]}, Название транспорта: {transport[1]}, Количество заказов: {transport[2]}\n"
        messagebox.showinfo("Заказы транспорта", transport_list)

    def add_discount(self):
        discount_description = simpledialog.askstring("Ввод", "Введите описание скидки:")
        rate = simpledialog.askfloat("Ввод", "Введите ставку скидки:")
        startdate = simpledialog.askstring("Ввод", "Введите начало действия скидки:")
        finishdate = simpledialog.askstring("Ввод", "Введите окончание действия скидки:")

        if add_discount(discount_description, rate, startdate, finishdate):
            messagebox.showinfo("Скидка добавлена", "Скидка успешно добавлена!")
        else:
            messagebox.showerror("Скидка не добавлена", "Ошибка добавления скидки.")

    def delete_discount(self):
        discount_id = simpledialog.askinteger("Ввод", "Введите ID скидки для удаления:")
        if delete_discount(discount_id):
            messagebox.showinfo("Скидка удалена", "Скидка успешно удалена!")
        else:
            messagebox.showerror("Скидка не удалена", "Ошибка удаления скидки.")

    def get_all_discounts(self):
        discounts = get_all_discounts()
        discounts_list = ""
        for discount in discounts:
            discounts_list += f"ID: {discount[0]}, Описание скидки: {discount[1]}, Процент скидки: {discount[2]}, Начало действия: {discount[3]}, Окончание действия: {discount[4]}\n"
        messagebox.showinfo("Скидки", discounts_list)

    def update_discount_field(self):
        discount_id = simpledialog.askinteger("Ввод", "Введите ID скидки для изменения:")
        field_name = simpledialog.askstring("Ввод", "Введите название поля для изменения (discount_description, rate, startdate, finishdate):")
        new_value = simpledialog.askstring("Ввод", "Введите новое значение поля:")
        if update_discount_field(discount_id, field_name, new_value):
            messagebox.showinfo("Скидка изменена", "Скидка успешно изменена!")
        else:
            messagebox.showerror("Скидка не изменена", "Ошибка изменения скидки.")
    
    def get_active_discounts(self):
        discounts = active_discounts()
        discounts_list = ""
        for discount in discounts:
            discounts_list += f"ID: {discount[0]}, Описание скидки: {discount[1]},  Процент скидки: {discount[2]}, Начало действия: {discount[3]},  Окончание действия: {discount[4]}\n"
        messagebox.showinfo("Активные скидки", discounts_list)
    
    def add_route(self):
        route_name = simpledialog.askstring("Ввод", "Введите название маршрута:")
        startpoint = simpledialog.askstring("Ввод", "Введите начало маршрута:")
        endpoint = simpledialog.askstring("Ввод", "Введите окончание маршрута:")
        time_departure = simpledialog.askstring("Ввод", "Введите время отправления:")
        time_arrival = simpledialog.askstring("Ввод", "Введите время прибытия:")
        
        if add_route(route_name, startpoint, endpoint, time_departure, time_arrival):
            messagebox.showinfo("Маршрут добавлен", "Маршрут успешно добавлен!")
        else:
            messagebox.showerror("Маршрут не добавлен", "Ошибка добавления маршрута.")

    def delete_route(self):
        route_id = simpledialog.askinteger("Ввод", "Введите ID маршрута для удаления:")
        if delete_route(route_id):
            messagebox.showinfo("Маршрут удален", "Маршрут успешно удален!")
        else:
            messagebox.showerror("Маршрут не удален", "Ошибка удаления маршрута.")

    def get_all_routes(self):
        routes = get_all_routes()
        route_list = ""
        for route in routes:
            route_list += f"ID: {route[0]}, Название: {route[1]}, Точка начала: {route[2]}, Точка окончания: {route[3]}, Время отправления: {route[4]}, Время прибытия: {route[5]}\n"
        messagebox.showinfo("Маршруты", route_list)

    def update_route_field(self):
        route_id = simpledialog.askinteger("Ввод", "Введите ID маршрута для изменения:")
        field_name = simpledialog.askstring("Ввод", "Введите поле для изменения (route_name, startpoint, endpoint, time_departure, time_arrival):")
        new_value = simpledialog.askstring("Ввод", "Введите новое значение поля:")
        if update_route_field(route_id, field_name, new_value):
            messagebox.showinfo("Изменения внесены", "Изменения успешно внесены!")
        else:
            messagebox.showerror("Изменения не внесены", "Ошибка внесения изменений.")

    def get_routes_startpoint(self):
        startpoint = simpledialog.askstring("Ввод", "Введите точку начала маршрута:")
        routes = get_routes_by_startpoint(startpoint)
        if not routes:
            messagebox.showinfo("Маршруты", "Маршруты не найдены.")
            return
        route_list = ""
        for route in routes:
            route_list += f"ID: {route[0]}, Название: {route[1]}, Точка окончания: {route[2]}, Время отправления: {route[3]}, Время прибытия: {route[4]}\n"
        messagebox.showinfo("Маршруты", route_list)

    def get_route_order_count(self):
        routes = route_order_count()
        routes_list = ""
        for route in routes:
            routes_list += f"ID: {route[0]}, Название: {route[1]}, Количество заказов: {route[2]}\n"
        messagebox.showinfo("Заказы", routes_list)

    def login_user(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if verify_user(username, password):
            self.is_logged_in = True
            role = self.get_user_role(username)
            if role is not None:
                self.current_user_role = role
                messagebox.showinfo("Успешный вход", f"Добро пожаловать {username}!")
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Невозможно получить тип пользователя.")
        else:
            messagebox.showerror("Ошибка входа", "Неверное имя пользователя или пароль.")

    def register_user(self):
        username = self.registration_username_entry.get()
        email = self.registration_email_entry.get()
        password = self.registration_password_entry.get()
        role = self.registration_role_entry.get()

        if username and email and password and role:
            if register_user(username, email, password, role):
                messagebox.showinfo("Успешная регистрация", "Пользователь успешно зарегистрирован!")
                self.show_login_frame()
            else:
                messagebox.showerror("Ошибка регистрации", "Ошибка регистрации пользователя. Пожалуйста, попробуйте снова.")
        else:
            messagebox.showwarning("Ошибка ввода", "Все поля должны быть заполнены.")

    def show_login_frame(self):
        self.registration_frame.pack_forget()
        self.login_frame.pack(pady=10)

    def show_registration_frame(self):
        self.login_frame.pack_forget()
        self.registration_frame.pack(pady=10)

    def show_main_menu(self):
        self.client_management_frame.pack_forget()
        self.order_management_frame.pack_forget()
        self.hotel_management_frame.pack_forget()
        self.analytics_management_frame.pack_forget()
        self.transport_management_frame.pack_forget()
        self.discounts_management_frame.pack_forget()
        self.routes_management_frame.pack_forget()
        self.main_menu_frame.pack_forget()
    
        self.login_frame.pack_forget()
        self.registration_frame.pack_forget()
    
        self.create_main_menu()
        
    def get_user_role(self, username):
        user_role_result = getUserRole(username)
        if user_role_result and len(user_role_result) > 0:
            role = user_role_result[0][0]
            messagebox.showinfo("Вход", "Вход выполнен как " + role)
            return role
        else:
            messagebox.showerror("Ошибка", "Невозмно получить тип пользователя.")
            return None
    
    def get_client(self):
        """Get a client based on their username."""
        username = self.login_username_entry.get()
        email_result = getUserEmail(username)
        if email_result and len(email_result) > 0:
            email = email_result[0][0]
            client = get_client_by_email(email)
            client_data = ""
            client_data += f"ID: {client[0]}, Имя: {client[1]}, Фамилия: {client[2]}, Отчество: {client[3]}, Паспорт: {client[4]}, Телефон: {client[5]}, Email: {client[6]}, Адрес: {client[7]}, Дата регистрации: {client[8]}, Статус: {client[9]}\n"
            messagebox.showinfo("Клиент", client_data)
        else:
            messagebox.showerror("Ошибка", "Клиент с вашими данными не найден, пожалуйста пройдите регистрацию как клиент, чтобы оформлять заказы.")
            return None