class Validators():
    @staticmethod
    def is_empty(item):
        return (item is None) or (str(item) == "")

    @staticmethod
    def is_not_empty(item):
        return item is not None and str(item) != ""

    @staticmethod
    def is_kwarg_set_and_not_empty(kwargs, item):
        return item in kwargs and Validators.is_not_empty(kwargs[item])

    @staticmethod
    def add_param_if_set_not_empty(output_params, kwargs, item):
        if Validators.is_kwarg_set_and_not_empty(kwargs, item):
            output_params[item] = kwargs[item]


class S3BucketServiceValidators:
    enc_types = [
        "AES256",
        "aws:fsx",
        "aws:kms",
        "aws:kms:dsse"
    ]

    acl_types = [
        "private",
        "public-read",
        "public-read-write",
        "authenticated-read",
        "aws-exec-read",
        "bucket-owner-read",
        "bucket-owner-full-control",
    ]

    object_ownership_types = [
        "BucketOwnerPreferred",
        "ObjectWriter",
        "BucketOwnerEnforced",
    ]

    checksum_algorithm_types = [
        "CRC32",
        "CRC32C",
        "SHA1",
        "SHA256",
        "CRC64NVME",
    ]

    storage_class_types = [
        "STANDARD",
        "REDUCED_REDUNDANCY",
        "STANDARD_IA",
        "ONEZONE_IA",
        "INTELLIGENT_TIERING",
        "GLACIER",
        "DEEP_ARCHIVE",
        "OUTPOSTS",
        "GLACIER_IR",
        "SNOW",
        "EXPRESS_ONEZONE",
        "FSX_OPENZFS",
    ]

    object_lock_modes = [
        "GOVERNANCE",
        "COMPLIANCE",
    ]

    object_lock_legal_hold_statuses = [
        "ON",
        "OFF",
    ]

    fetch_owner_options = [
        True,
        False,
    ]

    @classmethod
    def is_acl_valid(cls, acl):
        return acl is not None and acl != "" and acl in cls.acl_types

    @classmethod
    def is_checksum_algorithm_valid(cls, ca):
        return ca is not None and ca != "" and ca in cls.checksum_algorithm_types

    @classmethod
    def is_enc_type_valid(cls, enc_type):
        return enc_type is not None and enc_type != "" and enc_type in cls.enc_types

    @classmethod
    def is_object_ownership_valid(cls, object_ownership):
        return (object_ownership is not None and
                object_ownership != "" and
                object_ownership in cls.object_ownership_types)

    @classmethod
    def is_storage_class_valid(cls, storage_class):
        return storage_class is not None and storage_class != "" and storage_class in cls.storage_class_types

    @classmethod
    def is_object_lock_mode_valid(cls, lock_mode):
        return lock_mode is not None and lock_mode != "" and lock_mode in cls.object_lock_modes

    @classmethod
    def is_object_lock_legal_hold_status_valid(cls, status):
        return status is not None and status != "" and status in cls.object_lock_legal_hold_statuses

    @classmethod
    def is_fetch_owner_option_valid(cls, option):
        return option is not None and option in cls.fetch_owner_options
