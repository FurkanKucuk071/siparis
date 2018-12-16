import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
import webbrowser
import version

class AboutDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.version = version.ver
        self.title('SiparişTakip {} Hakkında'.format(self.version))
        self.resizable(False, False)
        self.show_title()
        self.show_description()
        
    def show_title(self):
        title = 'SiparişTakip {}'.format(self.version)
        title_label = tk.Label(self, text=title, font=('Cursive', 20))
        title_label.pack(pady=(40, 0))
        
    def show_description(self):
        text = '''Basit bir sipariş takip programı'''
        desc = tk.Label(self, text=text, font=14)
        desc.pack(padx=40, pady=(40, 0))
        self.show_author()
        self.show_hyperlink()
        
    def show_author(self):
       text = 'Yazan: Fırat Özgül'
       author = tk.Label(self, text=text, font=14)
       author.pack()
        
    def show_hyperlink(self):
        url = 'www.istihza.com'
        label = tk.Label(self, text=url, font=14, fg='royalblue')
        label.bind('<Enter>', lambda x:self.hover(label))
        label.bind('<Button-1>', self.click_url)
        
        f = tkfont.Font(label, label.cget("font"))
        f.configure(underline = True)
        label.configure(font=f)
        
        label.pack(pady=(0, 50))
 
    def hover(self, widget):
        widget['cursor'] = 'hand2'
        
    def click_url(self, event):
        webbrowser.open('http://www.istihza.com')
