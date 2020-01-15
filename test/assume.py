import configparser
import os
import boto3
import sys
import getopt


def assume_role(aws_account_number, role_name, session_name, session_tags, transitive_keys):
    """
    Assumes the provided role in the account and returns an STS session
    :param aws_account_number: AWS Account Number
    :param role_name: Role to assume in target account
    :param session_name session identifier
    :param session_tags tags to pass to the session
    :return:  client in the specified AWS Account and Region
    """

    # Beginning the assume role process for account
    sts_client = boto3.client('sts')

    # Get the current partition
    partition = sts_client.get_caller_identity()['Arn'].split(":")[1]

    response = sts_client.assume_role(
        RoleArn='arn:{}:iam::{}:role/{}'.format(
            partition,
            aws_account_number,
            role_name
        ),
        RoleSessionName=session_name,
        Tags=session_tags,
        TransitiveTagKeys=transitive_keys
    )
    print(response['Credentials'])
    return response['Credentials']


def update_credentials_file(*, profile_name, credentials):
    aws_dir = os.path.join(os.environ["HOME"], ".aws")

    credentials_path = os.path.join(aws_dir, "credentials")
    config = configparser.ConfigParser()
    config.read(credentials_path)

    if profile_name not in config.sections():
        config.add_section(profile_name)

    assert profile_name in config.sections()
    print("Updating profile with the temporary credentials")
    config[profile_name]["aws_access_key_id"] = credentials["AccessKeyId"]
    config[profile_name]["aws_secret_access_key"] = credentials["SecretAccessKey"]
    config[profile_name]["aws_session_token"] = credentials["SessionToken"]

    config.write(open(credentials_path, "w"), space_around_delimiters=False)


if __name__ == '__main__':
    account = None
    role = None
    profile = "temp"
    tag_args = None
    transitive = []
    tags = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:r:p:t:s:", ["acccount=", "role=", "profile=", "tags=", "transitive="])
    except getopt.GetoptError:
        print('assume.py -a <aws-account-id> -r <rolename> [-p profile_name]')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-a", "--account"):
            account = arg
        elif opt in ("-r", "--role"):
            role = arg
        elif opt in ("-p", "--profile"):
            profile  = arg
        elif opt in ("-t", "--tags"):
            tag_args = arg
        elif opt in ("--transitive"):
            transitive = [key for key in arg.split(',')]

    if account is None or role is None:
        print("assume.py -a <aws-account-id> -r <rolename>  [-p profile_name]")
        sys.exit(3)

    if tag_args:
        for tag_pair in tag_args.split(','):
            k, v = tag_pair.split('=')
            tags.append({"Key": k, "Value": v})
            print(tags)

    creds = assume_role(account, role, 'aws-tags', tags, transitive)
    update_credentials_file(profile_name=profile, credentials=creds)
