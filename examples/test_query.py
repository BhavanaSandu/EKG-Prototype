from graph.query import QueryEngine

if __name__ == "__main__":
    qe = QueryEngine()

    # Test get_owner
    owners = qe.get_owner("service-id-1")
    print("Owners:", owners)

    # Test blast_radius
    radius = qe.blast_radius("service-id-1")
    print("Blast Radius:", radius)

    # Test find_path
    path = qe.find_path("service-id-1", "service-id-2")
    print("Path:", path)

    qe.close()