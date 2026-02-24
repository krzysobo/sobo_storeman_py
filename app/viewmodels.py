# import tkinter as tk
from tkinter import ttk, StringVar, BooleanVar
import validators as vals
import services as srv
import app.models as mdl


class ConnectionS3VM:
    def __init__(self):
        self.connection_is_fake = False
        self.access_key_id = StringVar()
        self.secret_access_key = StringVar()
        self.session_token = StringVar()

        self.using_long_term_credentials = BooleanVar()

        self.is_error_access_key_id = BooleanVar()
        self.is_error_secret_access_key = BooleanVar()
        self.is_error_session_token = BooleanVar()

        self.show_access_key_id_error_label_lmb = None
        self.hide_access_key_id_error_label_lmb = None
        self.show_secret_access_key_error_label_lmb = None
        self.hide_secret_access_key_error_label_lmb = None
        self.show_session_token_error_label_lmb = None
        self.hide_session_token_error_label_lmb = None
        self.add_connection_frame_lmb = None

        self.update_connection_listbox_lmb = None

        self.show_api_error_label = None
        self.hide_api_error_lbl = None

    def set_other_handlers(self, update_connection_listbox_lmb,
                           add_connection_frame_lmb):
        self.update_connection_listbox_lmb = update_connection_listbox_lmb
        self.add_connection_frame_lmb = add_connection_frame_lmb

    def set_error_label_handlers(self,
                                 show_access_key_id_error_label_lmb,
                                 hide_access_key_id_error_label_lmb,
                                 show_secret_access_key_error_label_lmb,
                                 hide_secret_access_key_error_label_lmb,
                                 show_session_token_error_label_lmb,
                                 hide_session_token_error_label_lmb,
                                 show_api_error_label,
                                 hide_api_error_lbl
                                 ):
        self.show_access_key_id_error_label_lmb = show_access_key_id_error_label_lmb
        self.hide_access_key_id_error_label_lmb = hide_access_key_id_error_label_lmb
        self.show_secret_access_key_error_label_lmb = show_secret_access_key_error_label_lmb
        self.hide_secret_access_key_error_label_lmb = hide_secret_access_key_error_label_lmb
        self.show_session_token_error_label_lmb = show_session_token_error_label_lmb
        self.hide_session_token_error_label_lmb = hide_session_token_error_label_lmb

        self.show_api_error_label = show_api_error_label
        self.hide_api_error_lbl = hide_api_error_lbl

    def clear_vals(self):
        self.access_key_id.set("")
        self.secret_access_key.set("")
        self.session_token.set("")
        self.using_long_term_credentials.set(False)

    def clear_errors(self):
        self.is_error_access_key_id.set(False)
        self.is_error_secret_access_key.set(False)
        self.is_error_session_token.set(False)

        self.hide_access_key_id_error_label_lmb()
        self.hide_secret_access_key_error_label_lmb()
        self.hide_session_token_error_label_lmb()
        self.hide_api_error_lbl()

    def validate(self):
        self.clear_errors()
        if vals.Validators.is_empty(self.access_key_id.get()):
            self.is_error_access_key_id.set(True)
            # self.error_msg_access_key_id.set("Access key ID is required")
            self.show_access_key_id_error_label_lmb("Access key ID is required")

        if vals.Validators.is_empty(self.secret_access_key.get()):
            self.is_error_secret_access_key.set(True)
            self.show_secret_access_key_error_label_lmb("Secret access key is required")

        if (not self.using_long_term_credentials.get()) and (vals.Validators.is_empty(self.session_token.get())):
            self.is_error_session_token.set(True)
            self.show_session_token_error_label_lmb("Session token is required")

        print(
            f"\nWTF::: {(self.is_error_access_key_id.get() or self.is_error_secret_access_key.get() or self.is_error_session_token.get())}")

        if self.using_long_term_credentials.get():
            return not (self.is_error_access_key_id.get() or
                        self.is_error_secret_access_key.get())
        else:
            return not (self.is_error_access_key_id.get() or
                        self.is_error_secret_access_key.get() or
                        self.is_error_session_token.get())

    def connect(self, *args, **kwargs):
        print("\n======> ConnectionVM -> connect -> trying to connect....")
        print("\n======> ConnectionVm -> connect -> args: ", args, "kwargs", kwargs, "\n\n")
        print(f"\n===> access_key_id: {self.access_key_id.get()}"
              f"\n====> secret_access_key: {self.secret_access_key.get()}"
              f"\n====> session_token: {self.session_token.get()}\n\n")

        if self.validate():
            print("========> VALIDATED OK! Connecting...")

            if self.connection_is_fake:
                api_service = srv.S3BucketService()
                api_service.set_credentials_from_params(
                    aws_access_key_id=self.access_key_id.get(),
                    aws_secret_access_key=self.secret_access_key.get(),
                    use_long_time_creds=True)
                conn_res = True
            else:
                api_service = srv.S3BucketService()
                if self.using_long_term_credentials.get():
                    api_service.set_credentials_from_params(
                        aws_access_key_id=self.access_key_id.get(),
                        aws_secret_access_key=self.secret_access_key.get(),
                        use_long_time_creds=True)
                else:
                    api_service.set_credentials_from_params(
                        aws_access_key_id=self.access_key_id.get(),
                        aws_secret_access_key=self.secret_access_key.get(),
                        aws_session_token=self.session_token.get(),
                        use_long_time_creds=False)

                conn_res = api_service.test_connection()

            if conn_res:
                print("\n\nConnection has been established and is OK\n\n")
                conn_name = mdl.S3ConnectionManager.add_connection_for_service(api_service)
                self.add_connection_frame_lmb(conn_name)
                self.update_connection_listbox_lmb(mdl.S3ConnectionManager.list_connection_names())

                # self.connection_list.set(S3ConnectionManager.list_connections())
                print("\nCONNECTIONS LIST ", [str(c) for c in mdl.S3ConnectionManager.list_connections()])
            else:
                self.show_api_error_label("Request has failed - check your internet connection.")
        else:
            print("========> VALIDATION FAILED!")
