def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)
