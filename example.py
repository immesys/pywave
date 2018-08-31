
import grpc
import wave as wv

channel = grpc.insecure_channel("localhost:410")
agent = wv.WAVEStub(channel)

# rv = stub.ListLocations(eapi_pb2.ListLocationsParams())
# print(rv)

ent = agent.CreateEntity(wv.CreateEntityParams())
agent.PublishEntity(wv.PublishEntityParams(DER=ent.PublicDER))
ent2 = agent.CreateEntity(wv.CreateEntityParams())
agent.PublishEntity(wv.PublishEntityParams(DER=ent2.PublicDER))

perspective = wv.Perspective(
    entitySecret=wv.EntitySecret(DER=ent.SecretDER)
)
att = agent.CreateAttestation(wv.CreateAttestationParams(
    perspective=perspective,
    subjectHash=ent2.hash,
    publish=True,
    policy=wv.Policy(rTreePolicy=wv.RTreePolicy(
        namespace=ent.hash,
        indirections=5,
        statements=[wv.RTreePolicyStatement(
            permissionSet=ent.hash,
            permissions=["foo"],
            resource="foo/bar",
        )]
    ))
))
ent2perspective = wv.Perspective(
    entitySecret=wv.EntitySecret(DER=ent2.SecretDER)
)

agent.ResyncPerspectiveGraph(wv.ResyncPerspectiveGraphParams(
    perspective=ent2perspective,
))
for status in agent.WaitForSyncComplete(wv.SyncParams(perspective=ent2perspective)):
    print (status)

proof = agent.BuildRTreeProof(wv.BuildRTreeProofParams(
    perspective=ent2perspective,
    namespace=ent.hash,
    statements=[
        wv.RTreePolicyStatement(
            permissionSet=ent.hash,
            permissions=["foo"],
            resource="foo/bar",
        )
    ]
))

vrfy = agent.VerifyProof(wv.VerifyProofParams(proofDER=proof.proofDER))
