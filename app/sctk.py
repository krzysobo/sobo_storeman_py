import views.window as win

if __name__ == "__main__":
    root = win.WindowDef.init_window()
    win.WindowDef.init_notebook(root)
    root.mainloop()