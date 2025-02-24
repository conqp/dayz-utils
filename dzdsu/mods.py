"""Modifications from the Steam workshop."""

from __future__ import annotations

from hashlib import sha1
from logging import getLogger
from pathlib import Path
from shutil import rmtree
from typing import Iterable, Iterator, NamedTuple, Optional

from dzdsu.constants import LINK
from dzdsu.constants import MODS_DIR
from dzdsu.constants import STRIKETHROUGH
from dzdsu.constants import WORKSHOP_URL

__all__ = ["Mod", "InstalledMod", "mods_str", "print_mods"]


class Mod(NamedTuple):
    """A server mod."""

    id: int
    name: Optional[str] = None
    enabled: bool = True
    update: bool = True

    def __str__(self) -> str:
        if self.enabled:
            return self.url_string

        return STRIKETHROUGH.format(self.url_string)

    @classmethod
    def from_id(
        cls, ident: int, *, name: Optional[str] = None, update: bool = True
    ) -> Mod:
        """Creates a mod from an ID."""
        if ident == 0:
            raise ValueError(f"Invalid mod ID: {ident}")

        if ident < 0:
            return cls(abs(ident), name, enabled=False, update=update)

        return cls(ident, name, update=update)

    @classmethod
    def from_json(cls, json: dict[str, int | str | bool]) -> Mod:
        """Creates a mod from a JSON-ish dict."""
        return cls.from_id(
            json["id"], name=json.get("name"), update=json.get("update", True)
        )

    @classmethod
    def from_value(cls, value: int | dict[str, int | str]) -> Mod:
        """Creates a mod from an int or JSON value."""
        if isinstance(value, int):
            return cls.from_id(value)

        if isinstance(value, dict):
            return cls.from_json(value)

        raise TypeError(f"Cannot create mod from: {value} ({type(value)})")

    @property
    def path(self) -> Path:
        """Returns the relative path to the local mod directory."""
        return MODS_DIR / str(self.id)

    @property
    def text(self) -> str:
        """Returns the URL text."""
        return self.name or str(self.id)

    @property
    def url(self) -> str:
        """Returns the Steam Workshop URL."""
        return WORKSHOP_URL.format(self.id)

    @property
    def url_string(self) -> str:
        """Returns the URL string."""
        return LINK.format(url=self.url, text=self.text)


class InstalledMod(NamedTuple):
    """Represents an installed mod."""

    mod: Mod
    base_dir: Path

    @property
    def path(self) -> Path:
        """Returns the relative path to the local mod directory."""
        return self.base_dir / self.mod.path

    @property
    def addons(self) -> Path:
        """Returns the path to the addons directory."""
        return self.path / "addons"

    @property
    def keys(self) -> Path:
        """Returns the path to the keys directory."""
        return self.path / "keys"

    @property
    def metadata(self) -> Path:
        """Returns the path to the metadata file."""
        return self.path / "meta.cpp"

    @property
    def sha1sum(self) -> str:
        """Returns the SHA-1 checksum."""
        with self.metadata.open("rb") as file:
            return sha1(file.read()).hexdigest()

    @property
    def pbos(self) -> Iterator[Path]:
        """Yields paths to the .pbo files."""
        return self.addons.glob("*.pbo")

    @property
    def bikeys(self) -> Iterator[Path]:
        """Yields paths to the *.bikey files."""
        return self.keys.glob("*.bikey")

    def fix_paths(self) -> None:
        """Links paths to lower-case."""
        if (addons := self.path / "Addons").is_dir():
            link_to_lowercase(addons)

        if (keys := self.path / "Keys").is_dir():
            link_to_lowercase(keys)

        if not self.keys.exists() and (key := self.path / "key").is_dir():
            self.keys.symlink_to(key)

        for pbo in self.pbos:
            link_to_lowercase(pbo)

    def remove(self) -> None:
        """Removes this mod."""
        rmtree(self.path)


def link_to_lowercase(path: Path) -> None:
    """Creates a symlink with the path names in lower case."""

    if (filename := path.name) == (lower := filename.lower()):
        return

    if (symlink := path.parent / lower).exists():
        return

    getLogger(__file__).debug('Linking "%s" to "%s".', filename, symlink)
    symlink.symlink_to(filename)


def mods_str(mods: Iterable[Mod], sep: str = ";") -> str:
    """Returns a string representation of the given mods."""

    return sep.join(str(mod.path) for mod in mods)


def print_mods(mods: Iterable[Mod]) -> None:
    """Lists the respective mods."""

    for mod in mods:
        print(mod)
