import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
import webbrowser
import database
import about
import ttkcalendar, calendar
import locale
locale.setlocale(locale.LC_ALL, '')
from functools import partial

#Standart pack seçenekleri
STD_OPTS = {'anchor': 'nw', 'pady': 10, 'padx': 10, 
            'expand': 'yes', 'fill': 'both'}

class AppWin(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.db = database.DB()
        
        self.set_main_window(title)
        self.menu = self.create_menu()
        self.tv = self.create_treeview()
        self.tv.bind("<Button-3>", self.create_context_menu)
        self.tv.bind("<Button-1>", self.left_button_click)
        
    def set_main_window(self, title):
        self.title(title)
        self.protocol('WM_DELETE_WINDOW', self.quit)
        
    def create_menu(self):
        #menü çubuğu
        menubar = tk.Menu(tearoff=0)
        
        #dosya menüsü
        filemenu = tk.Menu(tearoff=0)

        menubar.add_cascade(label='Dosya', menu=filemenu)
        filemenu.add_command(label='Çıkış', command=self.quit)
        
        #işlemler menüsü
        self.actionsmenu = tk.Menu(tearoff=0)
        menubar.add_cascade(label='İşlemler', menu=self.actionsmenu)
        self.actionsmenu.add_command(label="Ekle", command=self.create_add_record_dialog)
        self.actionsmenu.add_command(label="Sil", state='disabled', command=self.delete_db_item)
        self.actionsmenu.add_command(label="Güncelle", state='disabled', command=self.create_update_record_dialog)
        
        #işlemler menüsü içindeki listele alt menüsü
        listsubmenu = tk.Menu(tearoff=0)
        self.actionsmenu.add_cascade(label='Listele', menu=listsubmenu)
        listsubmenu.add_command(label='Tüm Siparişler', command=lambda: self.report(0))
        listsubmenu.add_command(label='Bekleyen Siparişler', command=lambda: self.report(1))
        listsubmenu.add_command(label='Biten Siparişler', command=lambda: self.report(2))
        
        #yardım menüsü
        helpmenu = tk.Menu(tearoff=0)
        menubar.add_cascade(label='Yardım', menu=helpmenu)
        helpmenu.add_command(label='Forum', command=lambda:webbrowser.open('http://www.istihza.com/forum'))
        helpmenu.add_command(label='Hakkında', command=self.create_about_dialog)
        self.config(menu=menubar)
        
    def create_treeview(self):
        tv = ttk.Treeview(columns=self.db.columns, show="headings")
        for col in self.db.columns:
            tv.heading(col, text=col, command=partial(self.tv_sort, tv, col, False))
                    
        tv.pack(expand='yes', fill='both')     
        return tv
    
    def tr_sort(self, word):
        import string
        
        if not word[0]:
            word = ' '
        
        letters = 'aAbBcCçÇdDeEfFgGğĞhHıIiİjJkKlLmMnNoOöÖpPqQrRsSşŞtTuUüÜvVwWxXyYzZ'
        chars = string.digits + letters + string.punctuation + string.whitespace   
        trans = {c: chars.index(c) for c in chars}
        return ([trans.get(word[0][i], 0) for i in range(len(word))])
        
    def tv_sort(self, tv, col, reverse): 
        values = [(tv.set(k, col), k) for k in tv.get_children('')]
        sorted_values = sorted(values, reverse=reverse, key=self.tr_sort)
    
        for index, (val, k) in enumerate(sorted_values):
            tv.move(k, '', index)
    
        tv.heading(col, command=partial(self.tv_sort, tv, col, not reverse))
        
    def create_add_record_dialog(self):
        self.add_record_dialog = tk.Toplevel()
        self.add_record_dialog.resizable(width='false', height='false')
        self.add_record_dialog.wm_attributes('-topmost', 1)
        self.add_record_dialog.title('Sipariş Ekle')
        
        frame_left = tk.Frame(self.add_record_dialog)
        frame_left.grid(row=0, column=0, sticky='news')
        frame_right = tk.Frame(self.add_record_dialog)
        frame_right.grid(row=0, column=1, sticky='news')
        frame_bottom = tk.Frame(self.add_record_dialog)
        frame_bottom.grid(row=1, column=1)
        
        for label in self.db.columns:
            tk.Label(frame_left, text=label).pack(anchor='nw', pady=10, padx=10)
        
        self.cmp_ent = tk.Entry(frame_right)
        self.cmp_ent.pack(STD_OPTS)
        
        self.order_no_ent = tk.Entry(frame_right)
        self.order_no_ent.pack(STD_OPTS)
        
        #tarih düğmesi ve etiketini tutacak frame
        frame_horiz = tk.Frame(frame_right)
        frame_horiz.pack(expand='yes', fill='x')
        
        self.order_date_ent = tk.Entry(frame_horiz)
        self.order_date_ent.bind('<Button-1>', lambda x: self.popup_calendar(self.order_date_ent))
        self.order_no_ent.bind('<Tab>', lambda x: self.popup_calendar(self.order_date_ent))
        self.order_date_ent.pack(STD_OPTS, padx=(10, 5), side='left')
        
        self.order_date_btn = ttk.Button(frame_horiz, text='...', width=2,
                                         command=lambda: self.popup_calendar(self.order_date_ent))
        self.order_date_btn.pack(pady=10, padx=(0, 10))
                
        self.var = tk.StringVar()
        self.options=['Bitti', 'Bekliyor']
        self.order_status_opm = ttk.OptionMenu(frame_right, self.var, self.options[1], *self.options)
        self.order_status_opm.pack(anchor='nw', pady=10, padx=5)
        
        self.remarks_txt = scrolledtext.ScrolledText(frame_right, width=40, height=10)
        self.remarks_txt.pack(anchor='nw', pady=10, padx=10)  
     
        self.add_btn = ttk.Button(frame_bottom, text='Ekle', 
                             command=lambda: self.add_to_db(self.cmp_ent.get(),
                                                            self.order_no_ent.get(), 
                                                            self.order_date_ent.get(), 
                                                            self.var.get(),
                                                            self.remarks_txt.get('1.0', 'end').strip()))
        self.add_btn.grid(row=0, column=0, pady=10, padx=10)
               
        self.update_btn = ttk.Button(frame_bottom, text='Güncelle', state='disabled')
        self.update_btn.grid(row=0, column=2, pady=10, padx=10)
    
    def create_update_record_dialog(self):
        #`create_add_record_dialog` fonksiyonunu temel alarak bir 
        #sipariş güncelleme ekranı oluşturuyoruz.
        self.create_add_record_dialog()
        
        #treeview'de seçili olan öğenin değerlerini yerlerine koyuyoruz
        self.add_record_dialog.title('Sipariş Güncelle')
        self.update_btn['state'] = 'enabled'
        self.update_btn['command'] = self.update_db_item
        self.add_btn['state'] = 'disabled'
        
        self.cmp_ent.insert('end', self.selection_data[0])
        self.order_no_ent.insert('end', self.selection_data[1])
        self.order_date_ent.insert('end', self.selection_data[2])
        self.var.set(self.selection_data[3])
        self.remarks_txt.insert('end', self.selection_data[4])
        
    def popup_calendar(self, widget):
        toplevel = tk.Toplevel()
        toplevel.resizable(width='false', height='false')
        toplevel.wm_attributes('-topmost', 1)
        ttkcal = ttkcalendar.Calendar(toplevel, firstweekday=calendar.MONDAY)
        ttkcal.pack()
        
        def select_date(widget):
            date = ttkcal.selection
            if date:
                widget.delete(0, 'end')
                widget.insert('end', '{}.{}.{}'.format(str(date.day).zfill(2), 
                                                       str(date.month).zfill(2),
                                                       date.year))
            toplevel.destroy()
                
        ok_btn = ttk.Button(toplevel, text='seç', command=lambda: select_date(widget))
        ok_btn.pack()       
    
    def create_context_menu(self, event):
        context_menu = tk.Menu(tearoff=0)
        context_menu.add_command(label='Güncelle', command=self.create_update_record_dialog)
        context_menu.add_separator()
        context_menu.add_command(label='Sil', command=self.delete_db_item)
        
        row = self.tv.identify_row(event.y)
        if row:
            self.tv.selection_set(row)
            self.selection_data = self.tv.item(row)['values']
            self.actionsmenu.entryconfigure(2, state='normal')
            self.actionsmenu.entryconfigure(1, state='normal')
            context_menu.tk_popup(event.x_root, event.y_root)  
           
    def left_button_click(self, event):
        #farenin sol tuşuna basıldığında hem treeview öğesini,
        #hem de işlemler menüsündeki 'güncelle' ve 'sil' düğmelerini etkinleştiriyoruz
        row = self.tv.identify_row(event.y)
        if row:
            self.tv.selection_set(row)
            self.selection_data = self.tv.item(row)['values']
            self.actionsmenu.entryconfigure(1, state='normal')
            self.actionsmenu.entryconfigure(2, state='normal')
            
    def create_about_dialog(self):
        ad = about.AboutDialog()
             
    def add_to_db(self, *args):
        '''
        Bilgileri veritabanına ekliyoruz
        '''
        data = [i for i in args]
        self.db.insert_db(data)
        #başarı raporu gösteriyoruz
        showinfo('Rapor', 'Bilgiler veri tabanına eklendi!', parent=self.add_record_dialog)
        
    def report(self, mode):
        #Veritabanındaki bilgileri kullanıcıya treeview üzerinde gösteriyoruz
        for children in self.tv.get_children():
            self.tv.delete(children)
        data = self.db.list_db(mode)
        for datum in data:
            self.tv.insert("", "end", values=datum)
            
    def update_db_item(self):
        self.db.columns = [i.lower() for i in self.db.columns]

        updated_values = [self.cmp_ent.get(),
                          self.order_no_ent.get(),
                          self.order_date_ent.get(),
                          self.var.get(),
                          self.remarks_txt.get('1.0', 'end').strip()]
                          
        updated = dict(zip(self.db.columns, updated_values))
        self.db.update_db_item(self.selection_data[1], updated)  
        showinfo('Rapor', 'Bilgiler güncellendi!', parent=self.add_record_dialog)
           
    def delete_db_item(self):
        item_to_delete = self.selection_data[1]
        yes = askyesno('Onay', 'Siparişi silmek istediğinizden emin misiniz?', parent=self)
        if yes:
            self.db.delete_db_item(item_to_delete)
            self.tv.delete(self.tv.selection())
            self.actionsmenu.entryconfigure(2, state='disabled')
            self.actionsmenu.entryconfigure(1, state='disabled')
        else:
            pass
        
    def quit(self):
        #Programdan çıkarken veritabanını kapatıyoruz
        import sys
        self.db.close_db()
        sys.exit()
            
if __name__ == '__main__':
    app = AppWin('Ana Ekran')
    app.mainloop()