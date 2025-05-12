INSERT INTO environment_entity (id, name, namespace, definition)
VALUES (
    1,
    'openstack-instance',
    'testbed',
    '{
      "apiVersion": "compute.openstack.crossplane.io/v1alpha1",
      "kind": "InstanceV2",
      "metadata": {
        "name": "crossplane-playground-openstack-instance-mr"
      },
      "spec": {
        "forProvider": {
          "flavorId": "f2559863-ef7d-416c-907e-4ea4043d4831",
          "imageId": "5e7f4d9d-0ce0-4ef9-96c8-67ee5693cfa0",
          "keyPairSelector": {
            "matchLabels": {
              "name": "crossplane-playground-openstack-keypair-mr"
            }
          },
          "name": "crossplane-playground-openstack-instance-er",
          "network": [
            {
              "name": "ii-executor-network"
            }
          ]
        },
        "providerConfigRef": {
          "name": "provider-config-openstack"
        }
      }
    }'
);

INSERT INTO environment_entity_label (id, environment_entity_id, name, value)
VALUES (
    1,
    1,
    'role',
    'dummy'
);

INSERT INTO environment_entity_label (id, environment_entity_id, name, value)
VALUES (
    2,
    1,
    'owner',
    'raccoon'
);
