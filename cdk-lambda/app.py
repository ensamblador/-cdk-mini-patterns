#!/usr/bin/env python3

from aws_cdk import core

from cdk_lambda.cdk_lambda_stack import CdkLambdaStack

app = core.App()
CdkLambdaStack(app, "cdk-lambda")

app.synth()
