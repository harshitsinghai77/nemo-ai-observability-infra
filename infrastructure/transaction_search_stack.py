from aws_cdk import (
    Stack,
    aws_logs as logs,
    aws_xray as xray,
    aws_iam as iam,
    aws_logs as logs,
    CfnResource,
)
from constructs import Construct

class NemoAITransactionSearchStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

        # 1. Logs Resource Policy to allow X-Ray service (xray.amazonaws.com) to write to the spans log groups
        #    Similar to AWS::Logs::ResourcePolicy in CloudFormation examples. :contentReference[oaicite:1]{index=1}
        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "TransactionSearchXRayAccess",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "xray.amazonaws.com"
                    },
                    "Action": "logs:PutLogEvents",
                    "Resource": [
                        f"arn:aws:logs:{region}:{account}:log-group:aws/spans:*",
                        f"arn:aws:logs:{region}:{account}:log-group:/aws/application-signals/data:*"
                    ],
                    "Condition": {
                        "ArnLike": {
                            "aws:SourceArn": f"arn:aws:xray:{region}:{account}:*"
                        },
                        "StringEquals": {
                            "aws:SourceAccount": account
                        }
                    }
                }
            ]
        }

        logs.CfnResourcePolicy(
            self,
            "TransactionSearchXRayLogsResourcePolicy",
            policy_name="TransactionSearchAccess",
            policy_document=policy_doc
        )

        indexing_pct = 1
        tx_search = xray.CfnTransactionSearchConfig(
            self,
            "XRayTransactionSearchConfig",
            indexing_percentage=indexing_pct
        )

        # Ensure the ResourcePolicy is created before the TransactionSearchConfig
        tx_search.node.add_dependency(self.node.try_find_child("TransactionSearchXRayLogsResourcePolicy"))
