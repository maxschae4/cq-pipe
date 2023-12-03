# PEP 563 (<3.11) support for return type in classmethod
from __future__ import annotations

from pydantic import BaseModel, Field


class UnknownHostKindError(ValueError):
    pass


class Host(BaseModel):
    """
    Host is a pydantic model representing a combination of the source models.

    kind_id is ultimately the magic for deduplicating between host types.
    By leveraging underlying knowledge about each "kind" (e.g. AWS instance id, Apple Serial Number, etc),
    we can marshal a Host and partially upsert the result.
    The tradeoff here is that we need to know about all the possible "kinds" of host,
    and their shapes in the underlying APIs. That may or may not be an ultimately assumption.

    While we could leverage other identifiers (e.g. FQDN, MAC, hostname), none seem to provide
    sufficiently unique identity as all can be reused or spoofed.

    Our goal is to leverage the magic of mongo to upsert or partially update (patch) existing entries.
    While this most likely doesn't represent a realistic approach,
    it is something magical that mongo makes possible.
    """

    # appears to be a uuid, but assumptions can be dangerous
    crowdstrike_device_id: str = Field(unique=True, default=None)
    # appears to be an int
    qualys_device_id: int = Field(unique=True, default=None)
    # cloud provider, system type, etc
    kind: str
    # unique identifier for the kind, could be a union type (harder to reason about)
    kind_id: str = Field(primary_field=True)

    @classmethod
    def from_crowdstrike(cls, host: dict) -> Host:
        """
        A constructor for Host from a crowdstrike dictionary

        These constructors are naturally brittle given the lack of uniformity in the API.
        Unfortunately, this seems to be the most critical of the business requirements.
        Based on my experience, this is likely to be a major investment for the project.
        """
        # a simple match is likely insufficient in reality.
        match host["platform_id"]:
            # linux/AWS
            case "3":
                # this is a weak association and ripe for improvement
                kind = "AWS"
                kind_id = host["instance_id"]
            # apple
            case "1":
                kind = "Apple"
                kind_id = host["serial_number"]
            # explicitly raise an error if we find an unknown type
            # a better system might create "unknown" types
            # those could be deduped later without data loss
            case _:
                raise UnknownHostKindError(f"Unknown host kind: {host}")

        return cls(kind=kind, kind_id=kind_id, crowdstrike_device_id=host["device_id"])

    @classmethod
    def from_qualys(cls, host: dict) -> Host:
        """
        A constructor for Host from a qualys dictionary

        Like the crowdstrike host constructor, this is also fundamentally brittle and ripe for improvement.
        """
        # again, this match is pretty weak; without better knowledge about the APIs,
        # it seems premature (at best) to reason about this too hard.
        match host["cloudProvider"]:
            case "AWS":
                kind = "AWS"
                # the following is extremely brittle.
                # we could chain .get() to improve the sanity of the lookup,
                # but without an instance id, we still end up without success
                kind_id = host["sourceInfo"]["list"][0]["Ec2AssetSourceSimple"][
                    "instanceId"
                ]
            # explicitly raise an error if we find an unknown type
            # a better system might create "unknown" types
            # those could be deduped later without data loss
            case _:
                raise UnknownHostKindError(f"Unknown host kind: {host}")

        return cls(kind=kind, kind_id=kind_id, qualys_device_id=host["id"])
