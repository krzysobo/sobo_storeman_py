import sys
import os

sys.path.append(os.path.join(os.getcwd(), ".."))
print(sys.path)
import tkinter as tk
from tkinter import ttk
import app.views.connections_manager_page as cp




class WindowDef:
    root = None
    notebook = None
    frame1 = None

    # def __init__(cls):
    #     pass

    @classmethod
    def init_window(cls, width=1024, height=768):
        cls.root = tk.Tk()
        cls.root.geometry(f"{width}x{height}")
        cls.root.title('Sobo Storage Manager (Storeman)')
        return cls.root

    @classmethod
    def init_notebook(cls, root):
        # create a notebook
        cls.notebook = ttk.Notebook(root)
        cls.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # create frames
        cls.frame1 = ttk.Frame(cls.notebook, width=400, height=280)

        cls.frame1.pack(fill='both', expand=True)

        # add frames to notebook
        cls.notebook.add(cls.frame1, text='Connections Manager')
        cp.S3ConnectionsManagerFrame(cls, cls.frame1, cls.notebook)

        # cp.S3ConnectionFrame.init_s3_connection_frame(cls.frame1)

        # frame2 = ttk.Frame(TopWidgets.notebook, width=400, height=280)
        # frame3 = ttk.Frame(TopWidgets.notebook, width=400, height=280)
        # frame2.pack(fill='both', expand=True)
        # frame3.pack(fill='both', expand=True)
        # TopWidgets.notebook.add(frame2, text='Buckets')
        # TopWidgets.notebook.add(frame3, text='Object (Files)')

        # print("\ninit_notebook() ------------- TABSSSSSSSSSSSSSSSSSSSSSSSSSSSSSs ", TopWidgets.notebook.tabs(), type(TopWidgets.notebook.tabs()[0]))
        # print("\ninit_notebook() ------------- TAB ", TopWidgets.notebook.tab(TopWidgets.notebook.tabs()[0]))
        # init_buckets_frame(frame2)
        # init_objects_frame(frame3)
        # btn_1 = ttk.Button(frame1, text="Connect")
        # btn_2 = ttk.Button(frame2, text="Browse")
        # btn_3 = ttk.Button(frame3, text="File operations")

    # @classmethod
    # def add_connection_frame(cls, name: str):
    #     print("\nadd_connection_frame.... -> NOTEBOOK IS: ", cls.notebook)
    #     tab_ids = cls.notebook.tabs()
    #     print("\nADD CONNECTION FFRAME - TABS ", tab_ids)
    #     for tab_id in tab_ids:
    #         print("\n=================== AAAAXXXX ", cls.notebook.tab(tab_id))
    #         # return True
    #         if cls.notebook.tab(tab_id)["text"] == name:
    #             print(f"\n TAB ID {tab_id} is alraedy added...\n")
    #             return False   # already added
    #
    #     fr = ttk.Frame(cls.notebook, width=400, height=280)
    #     fr.pack(fill='both', expand=True)
    #     cls.notebook.add(fr, text=name)
    #     return True
