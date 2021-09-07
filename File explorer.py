import os
import tkinter as tk
from tkinter import ttk, filedialog,messagebox

text_content = dict()

def create_file(content = "", title = 'untitiled'):
    text_area = tk.Text(notebook)
    text_area.insert('end', content)
    text_area.pack(side='left', expand=True)

    notebook.add(text_area, text=title)
    notebook.select(text_area)

    text_content[str(text_area)] = hash(content)



def quit_tab():
    unsaved = False
    for tab in notebook.tabs():
        text_widget = root.nametowidget(tab)
        content = text_widget.get('1.0', 'end-1c')
        if hash(content) != text_content[str(text_widget)]:
            unsaved = True
            break

    if unsaved:
        confirm = messagebox.askyesno(message = 'Are you sure you want to quit. If "yes" press Yes if "No" press No.',
                                      icon = 'question',title = 'confirm quit')
        if not confirm:
            return
    root.destroy()


def close_current_tab():
    current = save_changes_done()
    if unsaved_tab() and not confirm_done():
        return

    if len(notebook.tabs()) == 1:
        create_file()
    notebook.forget(current)


def unsaved_tab():
    current = save_changes_done()
    content = current.get('1.0','end-1c')
    return hash(content) != text_content[str(current)]


def confirm_done():
    confirm = messagebox.askyesno(message = 'Are you sure you want to close. If "yes" press Yes if "No" press No.',
                                      icon = 'question',title = 'confirm close')

    return confirm



def get_changes():
    current = save_changes_done()
    content = current.get('1.0','end-1c')
    name = notebook.tab('current')['text']

    if hash(content) != text_content[str(current)]:
        if name[-1] !='*':
            notebook.tab('current',text = name+'*')
    elif name[-1] == '*':
        notebook.tab('current',text = name[:-1])



def save_changes_done():
    text_widget = root.nametowidget(notebook.select())
    return text_widget



def save():
    file_path = filedialog.asksaveasfilename()
    try:
        filename = os.path.basename(file_path)
        text_widget = save_changes_done()
        content = text_widget.get('1.0', 'end-1c')

        with open(file_path, 'w') as file:
            file.write(content)

    except (AttributeError, FileNotFoundError):
        print('File not found.')
        return

    notebook.tab('current',text = filename)
    text_content[str(text_widget)] = hash(content)



def open_file():
    file_path = filedialog.askopenfilename()
    try:
        filename = os.path.basename(file_path)

        with open(file_path,"r") as file:
            content = file.read()

    except (AttributeError, FileNotFoundError):
        print('file not found!')
        return

    create_file(content, filename)



def show_file():
    messagebox.showinfo('tkinter is a GuI library in python. Tkinter is the interface that interacts with Tkinter GUI toolkit.')

root = tk.Tk()
root.title('file_explorer')
root.option_add('*tearOff',False)

main = tk.Frame(root)
main.pack(side= 'left', padx = (1,1), pady = (4,4), expand = True)

menubar = tk.Menu()
root.config(menu = menubar)

file_menu = tk.Menu(menubar)
menubar.add_cascade(menu = file_menu, label = 'File')
file_menu.add_command(label = 'New', command = create_file, accelerator = 'Ctrl+N')
file_menu.add_command(label = 'Save',command = save, accelerator = 'Ctrl+S')
file_menu.add_command(label ='Open',command = open_file, accelerator = 'Ctrl+O')
file_menu.add_command(label = 'Exit',command = quit_tab)
file_menu.add_command(label = 'Quit',command = close_current_tab, accelerator = 'Ctrl+q')


help_menu = tk.Menu(menubar)
menubar.add_cascade(menu = help_menu, label = 'Help')
help_menu.add_command(label = 'About', command = show_file)


notebook = ttk.Notebook(main)
notebook.pack(side = 'left', expand = True)

create_file()



root.bind('<KeyPress>',lambda event:get_changes())
root.bind('<Control-n>', lambda event: create_file())
root.bind('<Control-s>', lambda event: save())
root.bind('<Control-o>',lambda event:open_file())
root.bind('<Control-q>',lambda event:close_current_tab())

root.mainloop()