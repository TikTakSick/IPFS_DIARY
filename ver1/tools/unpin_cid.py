from pinata_python.pinning import Pinning
import tools.settings as settings


def unpin_(cid):
    pinata = Pinning(AUTH="jwt", PINATA_JWT_TOKEN=settings.PINATA_JWT)
    response = pinata.unpin(cid)
    print(response)
    return response