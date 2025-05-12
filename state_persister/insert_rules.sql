INSERT INTO rule (id, _condition, _action)
VALUES (
    1,
    'clusterMemoryUsage : Metric(
            queryTag == "cluster-memory-usage",
            clusterMemoryUsageValue : value
        )
        clusterCpuUsage : Metric(
            queryTag == "cluster-cpu-usage",
            clusterCpuUsageValue : value
        )
        clusterFilesystemUsage : Metric(
            queryTag == "cluster-filesystem-usage",
            clusterFilesystemUsageValue : value
        )
        eval((clusterMemoryUsageValue > 70 ||
            clusterCpuUsageValue > 70 ||
            clusterFilesystemUsageValue > 70) &&
            cronChecker.checkPatternForSession("0 0/2 * ? * * *"))',
    'AddInstanceAction.builder()
            .region("RegionOne")
            .name("kube-worker-auto-scaled")
            .imageId("70a1dc73-f794-439f-8dd2-9e5cf8a73d5a")
            .flavorId("414a6a89-57c3-4331-9a05-0a53fc9a7d02")
            .keypairName("default")
            .securityGroup(null)
            .userData("#!/bin/bash\nsudo apt -y install nmap\nsudo cp /home/ubuntu/kubernetes-lab-setup/configs/" +
                "join_cluster.service /etc/systemd/system/join_cluster.service\nchmod +x /home/ubuntu/kubernetes-lab-" +
                "setup/scripts/kube_setup/join_cluster.sh\nsudo systemctl enable join_cluster.service\nsudo systemctl" +
                " start join_cluster.service")
            .count(1)
            .waitActiveSec(1)
            .openstackService(usableServices.getOpenstackService())
            .build()
            .execute();'
);
