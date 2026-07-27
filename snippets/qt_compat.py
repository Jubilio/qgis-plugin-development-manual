def compat_enum(container, scoped_container_name, member_name, legacy_name):
    scoped_container = getattr(container, scoped_container_name, None)
    if scoped_container is not None:
        return getattr(scoped_container, member_name)
    return getattr(container, legacy_name)
