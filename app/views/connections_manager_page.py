import tkinter as tk
from tkinter import ttk
import app.viewmodels as vms
import app.views.theme as th
import app.views.window as win



class S3ConnectionsManagerFrame:
    ROW_ACCESS_KEY_ID = 0
    ROW_ACCESS_KEY_ID_ERROR_LABEL = ROW_ACCESS_KEY_ID + 1

    ROW_SECRET_ACCESS_KEY = ROW_ACCESS_KEY_ID + 2
    ROW_SECRET_ACCESS_KEY_ERROR_LABEL = ROW_SECRET_ACCESS_KEY + 1

    ROW_USE_LONG_TERM_CREDS = ROW_SECRET_ACCESS_KEY + 2
    ROW_AWS_SESSION_TOKEN = ROW_USE_LONG_TERM_CREDS + 1
    ROW_AWS_SESSION_TOKEN_ERROR_LABEL = ROW_AWS_SESSION_TOKEN + 1

    ROW_API_ERROR_LABEL = ROW_AWS_SESSION_TOKEN_ERROR_LABEL + 1
    ROW_CONNECT_BUTTON = ROW_API_ERROR_LABEL + 1


    # ============================ callbacks =================================
    def show_access_key_id_error_label(self, msg):
        self.access_key_id_error_label['text'] = msg
        self.access_key_id_error_label.grid(
            row=self.ROW_ACCESS_KEY_ID_ERROR_LABEL, column=0, columnspan=2,
            sticky=th.Theme.sticky_error_label)

    def hide_access_key_id_error_label(self):
        self.access_key_id_error_label.grid_remove()

    def show_secret_access_key_error_label(self, msg):
        self.secret_access_key_error_label['text'] = msg
        self.secret_access_key_error_label.grid(
            row=self.ROW_SECRET_ACCESS_KEY_ERROR_LABEL, column=0, columnspan=2,
            sticky=th.Theme.sticky_error_label)

    def hide_secret_access_key_error_label(self):
        self.secret_access_key_error_label.grid_remove()

    def show_session_token_error_label(self, msg):
        self.session_token_error_label['text'] = msg
        self.session_token_error_label.grid(
            row=self.ROW_AWS_SESSION_TOKEN_ERROR_LABEL,
            column=0, columnspan=2, sticky=th.Theme.sticky_error_label)

    def hide_session_token_error_label(self):
        self.session_token_error_label.grid_remove()

    def show_api_error_label(self, msg):
        self.api_error_label['text'] = msg
        self.api_error_label.grid(row=self.ROW_API_ERROR_LABEL, column=0, columnspan=2, sticky=th.Theme.sticky_error_label)

    def hide_api_error_label(self):
        self.api_error_label.grid_remove()

    def show_hide_credentials_fields(self):
        if self.vm.using_long_term_credentials.get():
            self.session_token_lbl.grid_remove()
            self.session_token_entry.grid_remove()
            self.session_token_error_label.grid_remove()
        else:
            self.session_token_lbl.grid(row=self.ROW_AWS_SESSION_TOKEN, column=0,
                                        sticky=th.Theme.sticky_label)
            self.session_token_entry.grid(row=self.ROW_AWS_SESSION_TOKEN, column=1)
            pass

    def update_connection_listbox(self, connection_names_list):
        self.current_connections_list.delete(0, tk.END)
        for index, conn in enumerate(connection_names_list):
            self.current_connections_list.insert(index, conn)

    def add_connection_frame(self, conn: str):
        print("\nadd_connection_frame.... -> NOTEBOOK IS: ", self.notebook)
        tab_ids = self.notebook.tabs()
        print("\nADD CONNECTION FFRAME - TABS ", tab_ids)
        for tab_id in tab_ids:
            print("\n=================== AAAAXXXX ", self.notebook.tab(tab_id))
            # return True
            if self.notebook.tab(tab_id)["text"] == conn:
                print(f"\n TAB ID {tab_id} is alraedy added...\n")
                return False   # already added

        fr = ttk.Frame(self.notebook, width=400, height=280)
        fr.pack(fill='both', expand=True)
        self.notebook.add(fr, text=conn)
        return True


    # ============================ /callbacks =================================


    def __init__(self, windowDef, parent_frame, notebook_obj):
        self.frame = parent_frame
        self.notebook = notebook_obj
        self.vm = vms.ConnectionS3VM()
        self.windowDef = windowDef
        # ====== Connections tab contents =====
        self.connections_frame = tk.Frame(self.frame, width=900, height=600)
        self.connections_frame.pack(side=tk.constants.TOP, anchor=tk.constants.NW,  # noqa
                                    expand=True, fill="both")  # noqa

        # ====== List of open connections =====
        self.current_connections_frame = tk.LabelFrame(self.connections_frame, text="Currently open connections", padx=15, pady=15)
        self.current_connections_frame.pack(side=tk.constants.TOP, anchor=tk.constants.N, expand=True, fill="x")  # noqa

        self.cur_conn_lbl = tk.Label(self.current_connections_frame, text="All currently open connections",
                                font=th.Theme.font_label)
        self.cur_conn_lbl.grid(row=0, column=0, padx=th.Theme.padding_label_x, pady=th.Theme.padding_label_y,
                          sticky=th.Theme.sticky_label)

        self.current_connections_frame.update()
        self.listbox_width = self.current_connections_frame.winfo_reqwidth() - 200
        print(f"\n\nLISTBOX WIDTH: {self.listbox_width}\n\n")
        self.current_connections_list = tk.Listbox(self.current_connections_frame, selectmode=tk.SINGLE,
                                              width=self.listbox_width)
        self.current_connections_list.grid(row=1, column=0, padx=th.Theme.padding_label_x, pady=th.Theme.padding_label_y,
                                      sticky=th.Theme.sticky_label)

        # current_connections_list.insert(tk.END, "Element 1")
        # current_connections_list.insert(tk.END, "Element 2")
        # current_connections_list.insert(tk.END, "Element 3")

        # ====== New connection =====
        self.new_connection_frame = tk.LabelFrame(
            self.connections_frame, padx=15, pady=15, relief="solid", border="1",
            text="New Connection")
        self.new_connection_frame.pack(side=tk.constants.TOP, anchor=tk.constants.N, expand=True, fill="x")  # noqa

        self.access_key_id_error_label = tk.Label(self.new_connection_frame, text="",
                                             foreground=th.Theme.fg_error,
                                             font=th.Theme.font_error)
        self.secret_access_key_error_label = tk.Label(self.new_connection_frame, text="",
                                                 foreground=th.Theme.fg_error,
                                                 font=th.Theme.font_error)
        self.session_token_error_label = tk.Label(self.new_connection_frame, text="",
                                             foreground=th.Theme.fg_error,
                                             font=th.Theme.font_error)
        self.api_error_label = tk.Label(self.new_connection_frame, text="",
                                   foreground=th.Theme.fg_error, font=th.Theme.font_error)


        self.vm.set_error_label_handlers(self.show_access_key_id_error_label,
                                         self.hide_access_key_id_error_label,
                                    self.show_secret_access_key_error_label,
                                         self.hide_secret_access_key_error_label,
                                    self.show_session_token_error_label,
                                         self.hide_session_token_error_label,
                                    self.show_api_error_label, self.hide_api_error_label)

        self.vm.set_other_handlers(update_connection_listbox_lmb=self.update_connection_listbox,
                              add_connection_frame_lmb=self.add_connection_frame)

        self.access_key_id_lbl = tk.Label(self.new_connection_frame, text="AWS Access Key ID",
                                     font=th.Theme.font_label)
        self.access_key_id_lbl.grid(row=self.ROW_ACCESS_KEY_ID, column=0, sticky=th.Theme.sticky_label,
                               padx=th.Theme.padding_label_x, pady=th.Theme.padding_label_y)

        self.access_key_id_entry = tk.Entry(self.new_connection_frame, textvariable=self.vm.access_key_id,
                                       font=th.Theme.font_entry)
        self.access_key_id_entry.grid(row=self.ROW_ACCESS_KEY_ID, column=1)

        self.secret_access_key_lbl = tk.Label(self.new_connection_frame, text="AWS Secret Access Key",
                                         font=th.Theme.font_label)
        self.secret_access_key_lbl.grid(row=self.ROW_SECRET_ACCESS_KEY, column=0,
                                   sticky=th.Theme.sticky_label,
                                   padx=th.Theme.padding_label_x, pady=th.Theme.padding_label_y)

        self.secret_access_key_entry = tk.Entry(self.new_connection_frame,
                                                textvariable=self.vm.secret_access_key,
                                           font=th.Theme.font_entry)
        self.secret_access_key_entry.grid(row=self.ROW_SECRET_ACCESS_KEY, column=1)

        self.use_long_term_creds = tk.Checkbutton(self.new_connection_frame, text='Long-term credentials',
                                             variable=self.vm.using_long_term_credentials,
                                             onvalue=True, offvalue=False,
                                             command=self.show_hide_credentials_fields,
                                             font=th.Theme.font_label)
        self.use_long_term_creds.grid(row=self.ROW_USE_LONG_TERM_CREDS, column=0, columnspan=2,
                                 sticky=th.Theme.sticky_label,
                                 padx=th.Theme.padding_label_x, pady=th.Theme.padding_label_y)

        self.session_token_lbl = tk.Label(self.new_connection_frame, text="AWS Session Token",
                                     font=th.Theme.font_label)
        self.session_token_lbl.grid(row=self.ROW_AWS_SESSION_TOKEN, column=0, sticky=th.Theme.sticky_label,
                               padx=th.Theme.padding_label_x, pady=th.Theme.padding_label_y)

        self.session_token_entry = tk.Entry(self.new_connection_frame, textvariable=self.vm.session_token,
                                       font=th.Theme.font_entry)
        self.connect_btn = tk.Button(self.new_connection_frame, text="Connect!", command=self.vm.connect)

        self.session_token_entry.grid(row=self.ROW_AWS_SESSION_TOKEN, column=1)

        self.connect_btn = tk.Button(self.new_connection_frame, text="Connect!", command=self.vm.connect,
                                font=th.Theme.font_button)
        self.connect_btn.grid(row=self.ROW_CONNECT_BUTTON, column=0, columnspan=2, pady=5)


        """
        aws_access_key_id
    aws_secret_access_key
    aws_session_token
        """




