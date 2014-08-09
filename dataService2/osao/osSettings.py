# coding=utf-8

true = True
null = None

identity_service = "192.168.0.50:35357"
volume_service = "192.168.0.51:8776"
compute_service = "192.168.0.51:8774"
image_service = "192.168.0.50:9292"

serviceCatalog = [
            {
                "endpoints": [
                    {
                        "adminURL": "http://192.168.0.51:8774/v2/86e5ae17b73749b3957886c5ad512ba0",
                        "id": "8eeb6834d2b147269f4d8e7d2721d65e",
                        "internalURL": "http://192.168.0.51:8774/v2/86e5ae17b73749b3957886c5ad512ba0",
                        "publicURL": "http://192.168.0.51:8774/v2/86e5ae17b73749b3957886c5ad512ba0",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "nova",
                "type": "compute"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://192.168.0.50:9292/v1",
                        "id": "eb31a521e3534ed2be1d04b1f4dfd5db",
                        "internalURL": "http://192.168.0.50:9292/v1",
                        "publicURL": "http://192.168.0.50:9292/v1",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "glance",
                "type": "image"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://192.168.0.51:8776/v1/86e5ae17b73749b3957886c5ad512ba0",
                        "id": "9e526642c2b4423998af42ed6100b2b4",
                        "internalURL": "http://192.168.0.51:8776/v1/86e5ae17b73749b3957886c5ad512ba0",
                        "publicURL": "http://192.168.0.51:8776/v1/86e5ae17b73749b3957886c5ad512ba0",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "volume",
                "type": "volume"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://192.168.0.51:8773/services/Admin",
                        "id": "253ad85777bd4cfd82e2aa759b177cd5",
                        "internalURL": "http://192.168.0.51:8773/services/Cloud",
                        "publicURL": "http://192.168.0.51:8773/services/Cloud",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "ec2",
                "type": "ec2"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://192.168.0.55:8888/v1",
                        "id": "5b011db85ad147949e9e47b2d213eec9",
                        "internalURL": "http://192.168.0.55:8888/v1/AUTH_86e5ae17b73749b3957886c5ad512ba0",
                        "publicURL": "http://192.168.0.55:8888/v1/AUTH_86e5ae17b73749b3957886c5ad512ba0",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "swift",
                "type": "object-store"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://192.168.0.50:35357/v2.0",
                        "id": "8a223da58e16418895f6caead9e458aa",
                        "internalURL": "http://192.168.0.50:5000/v2.0",
                        "publicURL": "http://192.168.0.50:5000/v2.0",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "keystone",
                "type": "identity"
            }
        ]
