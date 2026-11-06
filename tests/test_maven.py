from pullmc.core.maven import MavenCoord, installer_path_candidates


def test_parse_gav_and_path():
    coord = MavenCoord.parse("net.minecraftforge:forge:1.20.1-47.4.27")
    assert coord.group == "net.minecraftforge"
    assert coord.artifact == "forge"
    assert coord.version == "1.20.1-47.4.27"
    assert coord.path == "net/minecraftforge/forge/1.20.1-47.4.27/forge-1.20.1-47.4.27.jar"


def test_parse_classifier_and_extension():
    coord = MavenCoord.parse("net.minecraft:client:1.20.1:extra@zip")
    assert coord.classifier == "extra"
    assert coord.extension == "zip"
    assert coord.path.endswith("client-1.20.1-extra.zip")


def test_installer_old_forge_has_suffixed_fallback():
    paths = installer_path_candidates("1.7.10", "10.13.4.1614")
    assert "net/minecraftforge/forge/1.7.10-10.13.4.1614/forge-1.7.10-10.13.4.1614-installer.jar" in paths
    assert (
        "net/minecraftforge/forge/1.7.10-10.13.4.1614-1.7.10/"
        "forge-1.7.10-10.13.4.1614-1.7.10-installer.jar"
    ) in paths
