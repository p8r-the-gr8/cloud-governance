import boto3
from moto import mock_s3, mock_ec2

from cloud_governance.common.clouds.aws.s3.s3_operations import S3Operations
from cloud_governance.policy.aws.zombie_cluster_resource import ZombieClusterResources


@mock_ec2
@mock_s3
def test_not_zombie_s3_bucket_deletion():
    """
    This method tests force the s3 bucket deletion
    :return:
    """
    s3_resource = boto3.resource('s3', region_name='us-east-1')
    s3_resource.create_bucket(Bucket='unitest-test-ocp-image-registry-us-east-1')
    bucket_tagging = s3_resource.BucketTagging('unitest-test-ocp-image-registry-us-east-1')
    tags = [{'Key': 'kubernetes.io/cluster/unittest-test-cluster',
             'Value': 'Owned'
             }, {
                'Key': 'Owner',
                'Value': 'unitest'
            }]
    bucket_tagging.put(Tagging={
        'TagSet': tags
    })
    zombie_cluster_resources = ZombieClusterResources(cluster_prefix=["kubernetes.io/cluster", "sigs.k8s.io/cluster-api-provider-aws/cluster"], delete=True,
                                                      cluster_tag='kubernetes.io/cluster/unittest-test-cluster',
                                                      resource_name='zombie_cluster_s3_bucket')
    zombie_cluster_resources.zombie_cluster_s3_bucket()
    s3_operations = S3Operations(region_name='us-east-1')
    assert s3_operations.find_bucket(bucket_name='unitest-test-ocp-image-registry-us-east-1')


@mock_ec2
@mock_s3
def test_force_zombie_s3_bucket_deletion():
    """
    This method tests force the s3 bucket deletion
    :return:
    """
    s3_resource = boto3.resource('s3', region_name='us-east-1')
    s3_resource.create_bucket(Bucket='unitest-test-ocp-image-registry-us-east-1')
    bucket_tagging = s3_resource.BucketTagging('unitest-test-ocp-image-registry-us-east-1')
    tags = [{'Key': 'kubernetes.io/cluster/unittest-test-cluster',
             'Value': 'Owned'
             }, {
                'Key': 'Owner',
                'Value': 'unitest'
            }]
    bucket_tagging.put(Tagging={
        'TagSet': tags
    })
    zombie_cluster_resources = ZombieClusterResources(cluster_prefix=["kubernetes.io/cluster", "sigs.k8s.io/cluster-api-provider-aws/cluster"], delete=True,
                                                      cluster_tag='kubernetes.io/cluster/unittest-test-cluster',
                                                      resource_name='zombie_cluster_s3_bucket', force_delete=True)
    zombie_cluster_resources.zombie_cluster_s3_bucket()
    s3_operations = S3Operations(region_name='us-east-1')
    assert not s3_operations.find_bucket(bucket_name='unitest-test-ocp-image-registry-us-east-1')
