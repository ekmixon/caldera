import asyncio
import json
import os
import aioftp
import pytest

from app.contacts import contact_ftp
from app.utility.base_world import BaseWorld


beacon_profile = {'architecture': 'amd64',
                  'contact': 'ftp',
                  'paw': '8924',
                  'exe_name': 'sandcat.exe',
                  'executors': ['cmd', 'psh'],
                  'group': 'red',
                  'host': 'testhost',
                  'location': 'C:\\sandcat.exe',
                  'pid': 1234,
                  'platform': 'windows',
                  'ppid': 123,
                  'privilege': 'User',
                  'username': 'testuser'
                  }


@pytest.fixture()
def base_world():
    BaseWorld.clear_config()
    BaseWorld.apply_config(name='main', config={'app.contact.ftp.host': '127.0.0.1',
                                                'app.contact.ftp.user.dir': '/tmp/caldera',
                                                'app.contact.ftp.server.dir': '/tmp/caldera',
                                                'app.contact.ftp.port': '2222',
                                                'app.contact.ftp.user': 'caldera_user',
                                                'app.contact.ftp.pword': 'caldera',
                                                'app.knowledge_svc.module': 'app.utility.base_knowledge_svc',
                                                'crypt_salt': 'REPLACE_WITH_RANDOM_VALUE',
                                                'encryption_key': 'ADMIN123',
                                                'exfil_dir': '/tmp/caldera',
                                                'host': '0.0.0.0',
                                                'plugins': ['sandcat', 'stockpile'],
                                                'api_key': 'ADMIN123'
                                                })
    yield BaseWorld
    BaseWorld.clear_config()


@pytest.fixture()
def ftp_c2(loop, app_svc, contact_svc, data_svc, file_svc, obfuscator, base_world):
    services = app_svc(loop).get_services()
    ftp_c2 = contact_ftp.Contact(services)
    return ftp_c2


class TestFtpServer:
    def test_server_setup(self, ftp_c2):
        assert ftp_c2.name == 'ftp'
        assert ftp_c2.description == 'Accept agent beacons through ftp'
        assert ftp_c2.host == '127.0.0.1'
        assert ftp_c2.port == '2222'
        assert ftp_c2.directory == '/tmp/caldera'
        assert ftp_c2.home == os.getcwd()
        assert ftp_c2.user == 'caldera_user'
        assert ftp_c2.pword == 'caldera'

    def test_create_response(self):
        assert None is None

    def test_write_response_file(self):
        assert None is None

    """@pytest.mark.asyncio
    async def test_payload(self):
        paw = beacon_profile.get('paw')
        directory = 'tmp/caldera/' + str(paw) + '/'

        beacon_file_path = os.path.join(directory, "Payload.txt")
        async with aioftp.Client.context(host='127.0.0.1', port=2222, user='red', password='admin') as client:
            if not await client.exists(directory):
                await client.make_directory(directory)

            path = os.getcwd() + "/"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Files that an agent would send
            with open(beacon_file_path, "w+") as outfile:
                outfile.write("fa6e8607-e0b1-425d-8924-9b894da5a002")

            if os.path.exists(str(path) + beacon_file_path):
                # print("Does Alive.txt file exist? " + str(os.path.isfile(str(path) + beacon_file_path)))
                await client.upload(str(path) + beacon_file_path, directory + "Payload.txt", write_into=True)"""
