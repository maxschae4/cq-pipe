from cq_pipe.tasks import extract_crowdstrike_hosts, extract_qualys_hosts

extract_crowdstrike_hosts.delay()
extract_qualys_hosts.delay()
