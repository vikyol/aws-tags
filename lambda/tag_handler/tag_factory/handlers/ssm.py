import boto3

from .base import Tagger


class SSMTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        client = boto3.client('ssm')

        resource_id = self.get_resource_id()

        if resource_id:
            self.logger.info('Tagging the SSM resource ' + resource_id)
            tags = self.fetch_tags()

            if len(tags) > 0:
                self.logger.info(f'Tagging {resource_id} with {tags}')
                response = client.add_tags_to_resource(
                    ResourceType=self.get_resource_type(),
                    ResourceId=resource_id,
                    Tags=tags
                )
            else:
                self.logger.debug("No tag found to apply")
        else:
            self.logger.warning("No SSM resource found in the event data")

    # Returns the resource type of the SSM resource
    def get_resource_type(self):
        resource_types = dict(
            CreateDocument="Document",
            CreateMaintenanceWindow="MaintenanceWindow",
            PutParameter="Parameter",
            CreatePatchBaseline="PatchBaseline",
            CreateOpsItem="OpsItem"
        )

        return resource_types[self.event["detail"]["eventName"]]