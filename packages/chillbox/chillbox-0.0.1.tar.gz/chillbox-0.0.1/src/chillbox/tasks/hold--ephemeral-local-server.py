## Holding this in case it needs to be used or referenced again.

# [[ephemeral-local-server]]
# # defaults
# # base_image_url = "https://github.com/jkenlooper/alpine-droplet/releases/download/alpine-virt-image-2023-01-21-2310/alpine-virt-image-2023-01-21-2310.qcow2.bz2"
# # user_data_path = "/root/user-data"
# # public_ssh_keys_path = "/root/.ssh/authorized_keys"
#
# owner = "bob"
# name = "example-local-server"
# login-users = [ "jake:dev", "bob:dev" ]
# no-home-users = [ "dev" ]
# secrets = [ "example_secret" ]
# [ephemeral-local-server.user-data]
# template = "chillbox:user-data.sh.jinja"
# file-size-limit = 16384
# [ephemeral-local-server.user-data.context]
# something = "example"

# [bunzip2]
# required = false
# full-name = "bzip2"
# website = "https://sourceware.org/bzip2/"
# download = "https://sourceware.org/bzip2/downloads.html"
# description = "High-quality block-sorting file compressor."
# use-case = """
# To uncompress (unzip) the downloaded disk image when running local virtual machine with QEMU.
# """
#
# [qemu-system-x86_64]
# required = false
# full-name = "QEMU"
# website = "https://www.qemu.org/"
# download = "https://www.qemu.org/download/"
# description = "A generic and open source machine emulator and virtualizer"
# use-case = """
# Create a local virtual machine to test out deployment of chillbox.
# """
#
# [virt-customize]
# required = false
# full-name = "libguestfs"
# website = "https://www.libguestfs.org/"
# download = "https://libguestfs.org/guestfs-faq.1.html#binaries"
# description = "Tools for accessing and modifying virtual machine disk images."
# use-case = """
# Modify the local virtual machine disk image used by QEMU to add the initial user-data file and public ssh keys.
# """


def get_hash_of_url(url):
    try:
        r = httpx.head(
            url,
            follow_redirects=True,
        )
        r.raise_for_status()
    except httpx.HTTPError as err:
        raise ChillboxHTTPError(f"ERROR: Request failed. {err}")
    logger.info(f"Successful HEAD response from {url}")
    return r.headers.get(
        "etag", hashlib.sha512(bytes(url, encoding="utf-8")).hexdigest()
    )


def fetch_url_to_tempfile(url):
    try:
        r = httpx.get(
            url,
            follow_redirects=True,
        )
        r.raise_for_status()
    except httpx.HTTPError as err:
        raise ChillboxHTTPError(f"ERROR: Request failed. {err}")
    logger.info(f"Successful GET response from {url}")

    t_file = mkstemp()[1]
    with open(t_file, "wb") as f:
        f.write(r.content)
    return t_file


@task(pre=[server_init])
def provision_local_server(c):
    "Provision ephemeral local servers with QEMU virtualization software."

    archive_directory = Path(c.chillbox_config["archive-directory"])
    base_images = c.state.get("base_images", {})
    server_images = c.state.get("server_images", {})

    # Setting up and using QEMU require _most_ of the optional commands.
    try:
        check_optional_commands()
    except ChillboxDependencyError as err:
        logger.warning(err)
        logger.warning(
            f"Executing some scripts may fail because there are some optional commands missing."
        )

    ephemeral_local_server_list = c.chillbox_config.get("ephemeral-local-server", [])
    if ephemeral_local_server_list:
        result = c.run(
            "sudo ip addr del 169.254.169.254/32 dev lo", hide=True, warn=True
        )
        result = c.run("sudo ip addr add 169.254.169.254/32 dev lo", hide=True)

    for ephemeral_local_server in ephemeral_local_server_list:
        s = ephemeral_local_server_defaults.copy()
        s.update(ephemeral_local_server)
        server_name = s["name"]

        base_image_url = s["base_image_url"]
        hash_url = get_hash_of_url(base_image_url)
        base_image = base_images.get(base_image_url, {})
        base_image_temp_file = base_image.get("temp_file")
        if (
            not base_image
            or hash_url != base_image.get("hash_url")
            or not base_image_temp_file
            or not Path(base_image_temp_file).exists()
        ):
            base_image_temp_file = fetch_url_to_tempfile(base_image_url)
            base_images[base_image_url] = {
                "hash_url": hash_url,
                "temp_file": base_image_temp_file,
            }

        server_image_temp_file = server_images.get(server_name)
        if not server_image_temp_file or not Path(server_image_temp_file).exists():
            tmp_server_dir = Path(mkdtemp())

            hostname_file = tmp_server_dir.joinpath("metadata", "v1", "hostname")
            hostname_file.parent.mkdir(parents=True, exist_ok=True)
            hostname_file.write_text(server_name)

            public_keys_file = tmp_server_dir.joinpath("metadata", "v1", "public-keys")
            public_keys_file.parent.mkdir(parents=True, exist_ok=True)
            public_keys_file.write_text(
                "\n".join(c.state["current_user_data"]["public_ssh_key"])
            )

            user_data = archive_directory.joinpath(
                "server", server_name, "user-data"
            ).read_text()
            user_data_file = tmp_server_dir.joinpath("metadata", "v1", "user-data")
            user_data_file.parent.mkdir(parents=True, exist_ok=True)
            user_data_file.write_text(user_data)

            # Not used, but need a file here anyways.
            ipv4_address_file = tmp_server_dir.joinpath(
                "metadata", "v1", "interfaces", "public", "0", "ipv4", "address"
            )
            ipv4_address_file.parent.mkdir(parents=True, exist_ok=True)
            ipv4_address_file.write_text("")

            print(
                f"sudo python -m http.server --directory '{tmp_server_dir}' --bind 169.254.169.254 80"
            )
            print(f"rm -rf '{tmp_server_dir}'")
            confirm = input("continue?")

            server_image_temp_file = mkstemp()[1]
            with bz2.open(base_image_temp_file, "rb") as fin:
                with open(server_image_temp_file, "wb") as fout:
                    copyfileobj(fin, fout)

            server_images[server_name] = server_image_temp_file

            # virt-customize -a "$image_dir/$image_file" --upload path-to/server/user-data:/root/user-data
            # /etc/hostname
            # /root/.ssh/authorized_keys
            # /root/user-data

        # store the port in statefile and configure ssh config to connect

        # start virt machine? Or should only start if --local was passed to remote task?
        c.run(
            f"""
qemu-system-x86_64 \
-machine type=q35,accel=tcg \
-smp 4 \
-hda '{server_image_temp_file}' \
-m 8G \
-vga virtio \
-usb \
-device usb-tablet \
-daemonize \
-net user,hostfwd=tcp::10022-:22 \
-net nic
            """,
            warn=False,
            hide=True,
            disown=True,
        )

    c.state["base_images"] = base_images
    c.state["server_images"] = server_images
