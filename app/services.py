import boto3
import botocore
import logging
import os
import validators as vals


class AwsUnauthorizedException(Exception):
    pass


class AwsUnauthenticatedException(Exception):
    pass


class S3BucketService:

    def __init__(self):

        # defaults
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.aws_session_token = None
        self.use_long_time_creds = False
        self.authenticated_iam_client = None
        self.authenticated_s3_client = None

    def set_credentials_from_params(self,
                                    aws_access_key_id=None,
                                    aws_secret_access_key=None,
                                    aws_session_token=None, use_long_time_creds=False):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = None if use_long_time_creds else aws_session_token
        self.use_long_time_creds = use_long_time_creds

    def get_credentials_for_auth(self):
        # TODO - later we will also handle IAM roles etc, for now we only use direct credentials
        if (not self.use_long_time_creds) and vals.Validators.is_not_empty(self.aws_access_key_id) and \
                vals.Validators.is_not_empty(self.aws_secret_access_key) and \
                vals.Validators.is_not_empty(self.aws_session_token):
            creds = {
                "aws_access_key_id": self.aws_access_key_id,
                "aws_secret_access_key": self.aws_secret_access_key,
                "aws_session_token": self.aws_session_token,
            }
            return creds
        elif self.use_long_time_creds and vals.Validators.is_not_empty(self.aws_access_key_id) and \
                vals.Validators.is_not_empty(self.aws_secret_access_key):
            creds = {
                "aws_access_key_id": self.aws_access_key_id,
                "aws_secret_access_key": self.aws_secret_access_key
            }
            return creds
        else:
            raise AwsUnauthenticatedException("AWS credentials were not provided.")

    def get_iam_client(self):
        if self.authenticated_iam_client is None or not self.test_connection():
            self.authenticated_iam_client = boto3.client('iam', **self.get_credentials_for_auth())

        return self.authenticated_iam_client

    def get_s3_client(self, **kwargs):
        if self.authenticated_s3_client is None or not self.test_connection():
            self.authenticated_iam_client = boto3.client('iam', **self.get_credentials_for_auth())
            self.authenticated_s3_client = boto3.client('s3', **self.get_credentials_for_auth())

        return self.authenticated_s3_client

    def test_connection(self):
        iam_client = self.get_iam_client()

        print("\n\n IAM CLIENT IS: ", dir(iam_client))
        try:  # getting exception means bad authentication/authorization
            acc_summary = iam_client.get_account_summary()
            return True
        except botocore.exceptions.ClientError as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)

        return False

    # ===== BUCKETS =====
    def get_buckets(self,
                    bucket_region=None,
                    max_buckets=0,
                    continuation_token=None,
                    prefix=None
                    ):
        try:
            s3 = self.get_s3_client()
            kwargs = {}
            if bucket_region is not None and bucket_region != "":
                kwargs["BucketRegion"] = bucket_region
            if prefix is not None and prefix != "":
                kwargs["Prefix"] = prefix
            if max_buckets > 0:
                kwargs["MaxBuckets"] = max_buckets
            if continuation_token is not None and continuation_token != "":
                kwargs["ContinuationToken"] = continuation_token

            response = s3.list_buckets(**kwargs)
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            return []
        except Exception as e:
            logging.error(e)
            return []

        buckets_out = []
        for bucket in response['Buckets']:
            buckets_out.append(bucket)

        return buckets_out

    def add_bucket(self, bucket_name, bucket_region=None, acl=None, **kwargs) -> bool:
        try:
            client_kwargs = {}
            create_kwargs = {"Bucket": bucket_name}

            if bucket_region is not None and bucket_region != "":
                client_kwargs["region_name"] = bucket_region
                location = {'LocationConstraint': bucket_region}
                create_kwargs["CreateBucketConfiguration"] = location

            if vals.S3BucketServiceValidators.is_acl_valid(acl):
                create_kwargs["ACL"] = acl

            # vals.Validators.add_param_if_set_not_empty(create_kwargs, kwargs, "CacheControl")
            if "grantee_full_control" in kwargs and kwargs["grantee_full_control"] != "":
                create_kwargs["GrantFullControl"] = kwargs["grantee_full_control"]

            if "grantee_read" in kwargs and kwargs["grantee_read"] != "":
                create_kwargs["GrantRead"] = kwargs["grantee_read"]

            if "grantee_read_acp" in kwargs and kwargs["grantee_read_acp"] != "":
                create_kwargs["GrantReadACP"] = kwargs["grantee_read"]

            if "grantee_write" in kwargs and kwargs["grantee_write"] != "":
                create_kwargs["GrantWrite"] = kwargs["grantee_write"]

            if "grantee_write_acp" in kwargs and kwargs["grantee_write_acp"] != "":
                create_kwargs["GrantWriteACP"] = kwargs["grantee_write_acp"]

            if "grantee_read_acp" in kwargs and kwargs["grantee_read_acp"] != "":
                create_kwargs["GrantReadACP"] = kwargs["grantee_read"]

            if "object_lock_enabled_for_bucket" in kwargs and kwargs["object_lock_enabled_for_bucket"] in [True, False]:
                create_kwargs["ObjectLockEnabledForBucket"] = kwargs["object_lock_enabled_for_bucket"]

            # GRANTS - grantee is a person/role allowed to do sth
            if "object_ownership" in kwargs and vals.S3BucketServiceValidators.is_object_ownership_valid(
                    ["object_ownership"]):
                create_kwargs["ObjectOwnership"] = kwargs["object_ownership"]

            s3_client = self.get_s3_client(**client_kwargs)
            s3_client.create_bucket(**create_kwargs)

            """
                ACL='private'|'public-read'|'public-read-write'|'authenticated-read',
                Bucket='string',
                CreateBucketConfiguration={
                    'LocationConstraint': 'af-south-1'|'ap-east-1'|'ap-northeast-1'|'ap-northeast-2'|'ap-northeast-3'|'ap-south-1'|'ap-south-2'|'ap-southeast-1'|'ap-southeast-2'|'ap-southeast-3'|'ap-southeast-4'|'ap-southeast-5'|'ca-central-1'|'cn-north-1'|'cn-northwest-1'|'EU'|'eu-central-1'|'eu-central-2'|'eu-north-1'|'eu-south-1'|'eu-south-2'|'eu-west-1'|'eu-west-2'|'eu-west-3'|'il-central-1'|'me-central-1'|'me-south-1'|'sa-east-1'|'us-east-2'|'us-gov-east-1'|'us-gov-west-1'|'us-west-1'|'us-west-2',
                    'Location': {
                        'Type': 'AvailabilityZone'|'LocalZone',
                        'Name': 'string'
                    },
                    'Bucket': {
                        'DataRedundancy': 'SingleAvailabilityZone'|'SingleLocalZone',
                        'Type': 'Directory'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                },
                GrantFullControl='string',
                GrantRead='string',
                GrantReadACP='string',
                GrantWrite='string',
                GrantWriteACP='string',
                ObjectLockEnabledForBucket=True|False,
                ObjectOwnership='BucketOwnerPreferred'|'ObjectWriter'|'BucketOwnerEnforced'
            """

            return True
        except botocore.exceptions.ClientError as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)
        return False

    def delete_bucket_simple(self, bucket_name):
        try:
            s3_client = self.get_s3_client()
            response = s3_client.delete_bucket(Bucket=bucket_name)

            return True
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False

    def delete_bucket(self, bucket_name):
        try:
            s3_client = self.get_s3_client()
            bucket_obj = s3_client.Bucket(bucket_name)
            bucket_versioning = s3_client.BucketVersioning(bucket_name)
            if bucket_versioning.status == 'Enabled':
                bucket_obj.object_versions.delete()
            else:
                bucket_obj.objects.all().delete()

            response = bucket_obj.delete()
            return True
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False

    # ===== /BUCKETS =====

    # ===== FILES (OBJECTS) =====
    def list_objects(self, bucket_name, **kwargs):
        req_params = {
            "Bucket": bucket_name
        }

        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Delimiter")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "EncodingType")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "MaxKeys")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Prefix")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ContinuationToken")

        if (vals.Validators.is_kwarg_set_and_not_empty(kwargs, "FetchOwner") and
                vals.S3BucketServiceValidators.is_fetch_owner_option_valid(kwargs["FetchOwner"])):
            vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "FetchOwner")

        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "StartAfter")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "RequestPayer")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ExpectedBucketOwner")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "OptionalObjectAttributes")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html

        try:
            s3_client = self.get_s3_client()
            response = s3_client.list_objects_v2(**req_params)
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            return {}
        except Exception as e:
            logging.error(e)
            return {}

        return response

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_object.html
    def get_object(self, key):
        s3_client = self.get_s3_client()

    def download_file(self, src_object_name, target_file_name, bucket_name, **kwargs) -> bool:
        req_params = {
            "Bucket": bucket_name,
            "Key": src_object_name,
            "Filename": target_file_name,
        }
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ExtraArgs")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Callback")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Config")

        try:
            s3_client = self.get_s3_client()
            s3_client.download_file(**req_params)
            return True
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False

    def download_file_with_fileobj(self, src_object_name, target_file_name, bucket_name, **kwargs) -> bool:
        req_params = {
            "Bucket": bucket_name,
            "Key": src_object_name,
        }
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ExtraArgs")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Callback")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Config")

        try:
            s3_client = self.get_s3_client()
            with open(target_file_name, 'wb') as f:
                req_params["Fileobj"] = f
                # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/download_fileobj.html
                s3_client.download_fileobj(**kwargs)
            return True
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False

    def upload_file_by_name(self, src_file_name, object_name, bucket_name, **kwargs):
        target_object_name = object_name if vals.Validators.is_not_empty(object_name) \
            else os.path.basename(src_file_name)

        req_params = {
            "Bucket": bucket_name,
            "Key": target_object_name,
            "Filename": src_file_name,
        }
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ExtraArgs")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Callback")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Config")

        try:
            s3_client = self.get_s3_client()
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_file.html
            s3_client.upload_file(src_file_name, bucket_name, target_object_name)
            return True
        except botocore.exceptions.ClientError as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)

        return False

    def upload_file_with_fileobj(self, src_file_name, object_name, bucket_name, **kwargs):
        target_object_name = object_name if vals.Validators.is_not_empty(object_name) \
            else os.path.basename(src_file_name)

        req_params = {
            "Bucket": bucket_name,
            "Key": target_object_name,
        }
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ExtraArgs")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Callback")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Config")

        try:
            s3_client = self.get_s3_client()
            with open(src_file_name, "rb") as f:
                req_params["Fileobj"] = f
                s3_client.upload_fileobj(**kwargs)
        except botocore.exceptions.ClientError as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)

    def put_object(self, target_object_name, object_body, bucket_name, server_side_enc='AES256', **kwargs):
        req_params = {
            "Body": object_body,  # Body=b'bytes' | file,
            "Bucket": bucket_name,
            "Key": target_object_name,
        }

        if vals.S3BucketServiceValidators.is_enc_type_valid(server_side_enc):
            req_params["ServerSideEncryption"] = server_side_enc

        if "acl" in kwargs and vals.S3BucketServiceValidators.is_acl_valid(kwargs["acl"]):
            req_params["acl"] = kwargs["acl"]

        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "CacheControl")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ContentDisposition")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ContentEncoding")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ContentLanguage")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ContentLength")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ContentMD5")

        if vals.Validators.is_kwarg_set_and_not_empty(kwargs, "ChecksumAlgorithm") and \
                vals.S3BucketServiceValidators.is_checksum_algorithm_valid(kwargs["ChecksumAlgorithm"]):
            vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ChecksumAlgorithm")

        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ChecksumCRC32")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ChecksumCRC32C")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ChecksumCRC64NVME")

        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ChecksumSHA1")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ChecksumSHA256")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Expires")  # TODO
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "IfMatch")

        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "IfNoneMatch")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "GrantFullControl")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "GrantRead")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "GrantReadACP")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "GrantWriteACP")

        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "WebsiteRedirectLocation")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "SSECustomerAlgorithm")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "SSECustomerKey")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "SSEKMSKeyId")

        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "SSEKMSEncryptionContext")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "BucketKeyEnabled")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "RequestPayer")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Tagging")
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ExpectedBucketOwner")

        # Metadata={
        #     'string': 'string'
        # },
        vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "Metadata")

        if vals.Validators.is_kwarg_set_and_not_empty(kwargs, "StorageClass") and \
                vals.S3BucketServiceValidators.is_storage_class_valid(kwargs["StorageClass"]):
            vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "StorageClass")

        if vals.Validators.is_kwarg_set_and_not_empty(kwargs, "ObjectLockMode") and \
                vals.S3BucketServiceValidators.is_object_lock_mode_valid(kwargs["ObjectLockMode"]):
            vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ObjectLockMode")

        if vals.Validators.is_kwarg_set_and_not_empty(kwargs, "ObjectLockLegalHoldStatus") and \
                vals.S3BucketServiceValidators.is_object_lock_legal_hold_status_valid(
                    kwargs["ObjectLockLegalHoldStatus"]):
            vals.Validators.add_param_if_set_not_empty(req_params, kwargs, "ObjectLockLegalHoldStatus")

        s3_client = self.get_s3_client()
        response = s3_client.put_object(**req_params)
        return response

    def delete_object(self):
        pass

    # TODO:
    # - copy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/copy_object.html
    # - upload_part: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_part.html
    # ===== /FILES (OBJECTS) =====
