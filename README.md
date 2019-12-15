
# Automatically Tag EC2 Resources

This solution tags  EC2 instances, EBS volumes, AMIs and EC2 snapshots with Owner and Principal tags automatically. 

1. A CloudWatch Event Rule is setup to monitor EC2:create* API calls via CloudTrail.

2. This rule triggers the lambda function, lambda/auto_tag.py, whenever a matching event found.

3. The lambda function fetches the resource identifier and principal information from the event and tags the resources accordingly.

This solution helps identify resource owners easily as the owner tag shows the principal who created the resource. 

It can also be used for automation purposes if the owner tag contains email addresses, e.g. notify the owner, 
if a resource is not tagged properly.


## Deploying a CDK Python project!

```
python3 -m venv .env`
```

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

If the previous step is successful, you can deploy this stack to your default AWS account/region.

```
$ cdk deploy
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
