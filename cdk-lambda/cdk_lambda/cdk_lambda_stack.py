from aws_cdk import (
    core,
    aws_lambda,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    aws_s3_notifications,
    aws_events,
    aws_events_targets,
)

class CdkLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        _fn = aws_lambda.Function(self, "lambda_prueba",
                                    runtime=aws_lambda.Runtime.PYTHON_3_8,
                                    handler="lambda_function.lambda_handler",
                                    timeout=core.Duration.seconds(20),
                                    memory_size=256, description= 'Mi funcioncita',
                                    code=aws_lambda.Code.asset("./lambda/test"))

        bucket = s3.Bucket(self, "bucket_prueba",  versioned=False, removal_policy=core.RemovalPolicy.DESTROY)
         
        bucket.grant_read(_fn)

        notification = aws_s3_notifications.LambdaDestination(_fn)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)

        ddb_table = ddb.Table(
            self, "TABLA_PRUEBA",
            partition_key=ddb.Attribute(name="s3_bucket", type=ddb.AttributeType.STRING),
            sort_key=ddb.Attribute(name="s3_key", type=ddb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY)

        ddb_table.grant_read_write_data(_fn)
        _fn.add_environment("TABLE_NAME", ddb_table.table_name)
