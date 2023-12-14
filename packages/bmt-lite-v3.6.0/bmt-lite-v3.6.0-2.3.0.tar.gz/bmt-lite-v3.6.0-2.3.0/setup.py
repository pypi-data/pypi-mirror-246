"""Set up bmt-lite package."""
import json
import re
import sys
from pathlib import Path
import yaml

from setuptools import setup

stash = sys.path.pop(0)  # avoid trying to import the local bmt
from bmt import Toolkit
sys.path = [stash] + sys.path  # restore the path
import httpx

FILEPATH = Path(__file__).parent

DATAPATH = Path("bmt/_data")
DATAPATH.mkdir(exist_ok=True)  # create data dir
(DATAPATH / "__init__.py").touch(exist_ok=True)  # make data path a module

response = httpx.get("https://api.github.com/repos/biolink/biolink-model/releases")
releases = response.json()
versions = [
    release["tag_name"]
    for release in releases
]


def build_enum_hierarchy(biolink_version):
    url = f"https://raw.githubusercontent.com/biolink/biolink-model/{biolink_version}/biolink-model.yaml"
    source = httpx.get(url).text
    source = yaml.load(source, Loader=yaml.FullLoader)
    formatted = {}
    for enum_name, value in source.get('enums', {}).items():
        values_ancestry = {}
        values_descendants = {}
        all_values = []
        formatted[enum_name] = {
            "descendants": values_descendants,
            "ancestors": values_ancestry,
            "all_values": all_values
        }
        permissible_values = value.get('permissible_values', {})
        # organize hierarchy of values
        for k, v in permissible_values.items():
            if k not in all_values:
                all_values.append(k)
            if v:
                parent = v.get('is_a')
                values_descendants[parent] = values_descendants.get(parent, [])
                if parent and k not in values_descendants[parent]:
                    values_descendants[parent].append(k)
                values_ancestry[k] = parent
            else:
                values_ancestry[k] = None
    return formatted


def build(version: str):
    """Build BMT data."""
    version_formatted = None
    if version in versions:
        version_formatted = version
    elif "v" + version in versions:
        version_formatted = "v" + version
    elif version.removeprefix("v") in versions:
        version_formatted = version[1:]
    if not version_formatted:
        raise Exception(f"Version {version} not found.")
    print(f'Building version {version_formatted}')
    BMT = Toolkit(
        schema=f"https://raw.githubusercontent.com/biolink/biolink-model/{version_formatted}/biolink-model.yaml",
    )

    enums = build_enum_hierarchy(biolink_version=version_formatted)
    with open(DATAPATH / "all_enums.json", "w") as stream:
        json.dump(enums, stream)

    # get_all_classes()
    classes = BMT.get_all_classes()
    with open(DATAPATH / "all_classes.json", "w") as stream:
        json.dump(classes, stream)

    # get_all_slots()
    slots = BMT.get_all_slots()
    with open(DATAPATH / "all_slots.json", "w") as stream:
        json.dump(slots, stream)

    # get_all_types()
    types = BMT.get_all_types()
    with open(DATAPATH / "all_types.json", "w") as stream:
        json.dump(types, stream)

    # get_all_elements() , make sure they are supported by bmt
    elements = list(filter(lambda e: BMT.get_element(e), classes + slots  + types))
    with open(DATAPATH / "all_elements.json", "w") as stream:
        json.dump(elements, stream)

    # get_ancestors()
    basic_ancestors = {
        element: BMT.get_ancestors(
            element,
            reflexive=False,
            mixin=False,
        )
        for element in elements
    }
    alias_ancestors = {
        element: [
            alias
            for ancestor in basics
            if (el := BMT.get_element(ancestor)) is not None and (aliases := el.aliases) is not None
            for alias in aliases
        ]
        for element, basics in basic_ancestors.items()
    }
    mixin_ancestors = {
        element: [
            ancestor
            for ancestor in BMT.get_ancestors(
                element,
                reflexive=False,
                mixin=True,
            )
            if ancestor not in basic_ancestors[element]
        ]
        for element in elements
    }
    alias_mixin_ancestors = {
        element: [
            alias
            for ancestor in mixins
            if (el := BMT.get_element(ancestor)) is not None and (aliases := el.aliases) is not None
            for alias in aliases
        ]
        for element, mixins in mixin_ancestors.items()
    }
    with open(DATAPATH / "basic_ancestors.json", "w") as stream:
        json.dump(basic_ancestors, stream)
    with open(DATAPATH / "alias_ancestors.json", "w") as stream:
        json.dump(alias_ancestors, stream)
    with open(DATAPATH / "mixin_ancestors.json", "w") as stream:
        json.dump(mixin_ancestors, stream)
    with open(DATAPATH / "alias_mixin_ancestors.json", "w") as stream:
        json.dump(alias_mixin_ancestors, stream)

    # get_descendants()
    basic_descendants = {
        element: BMT.get_descendants(
            element,
            reflexive=False,
            mixin=False,
        )
        for element in elements
    }
    alias_descendants = {
        element: [
            alias
            for descendant in basics
            if (el := BMT.get_element(descendant)) is not None and (aliases := el.aliases) is not None
            for alias in aliases
        ]
        for element, basics in basic_descendants.items()
    }
    mixin_descendants = {
        element: [
            descendant
            for descendant in BMT.get_descendants(
                element,
                reflexive=False,
                mixin=True,
            )
            if descendant not in basic_descendants[element]
        ]
        for element in elements
    }
    alias_mixin_descendants = {
        element: [
            alias
            for descendant in mixins
            if (el := BMT.get_element(descendant)) is not None and (aliases := el.aliases) is not None
            for alias in aliases
        ]
        for element, mixins in mixin_descendants.items()
    }
    with open(DATAPATH / "basic_descendants.json", "w") as stream:
        json.dump(basic_descendants, stream)
    with open(DATAPATH / "alias_descendants.json", "w") as stream:
        json.dump(alias_descendants, stream)
    with open(DATAPATH / "mixin_descendants.json", "w") as stream:
        json.dump(mixin_descendants, stream)
    with open(DATAPATH / "alias_mixin_descendants.json", "w") as stream:
        json.dump(alias_mixin_descendants, stream)

    # get_children()
    basic_children = {
        element: BMT.get_children(
            element,
            mixin=False,
        )
        for element in elements
    }
    alias_children = {
        element: [
            alias
            for _child in basics
            if (el := BMT.get_element(_child)) is not None and (aliases := el.aliases) is not None
            for alias in aliases
        ]
        for element, basics in basic_children.items()
    }
    mixin_children = {
        element: [
            child
            for child in BMT.get_children(
                element,
                mixin=True,
            )
            if child not in basic_children[element]
        ]
        for element in elements
    }
    alias_mixin_children = {
        element: [
            alias
            for _child in mixins
            if (el := BMT.get_element(_child)) is not None and (aliases := el.aliases) is not None
            for alias in aliases
        ]
        for element, mixins in mixin_children.items()
    }
    with open(DATAPATH / "basic_children.json", "w") as stream:
        json.dump(basic_children, stream)
    with open(DATAPATH / "alias_children.json", "w") as stream:
        json.dump(alias_children, stream)
    with open(DATAPATH / "mixin_children.json", "w") as stream:
        json.dump(mixin_children, stream)
    with open(DATAPATH / "alias_mixin_children.json", "w") as stream:
        json.dump(alias_mixin_children, stream)

    # get_parent()
    parent = {
        element: BMT.get_parent(element)
        for element in elements
    }
    with open(DATAPATH / "parent.json", "w") as stream:
        json.dump(parent, stream)

    # get_element()
    element = dict(
        **{
            class_: {
                "id_prefixes": el.id_prefixes,
                "mixins": el.mixins,
            }
            for class_ in classes
            if (el := BMT.get_element(class_)) is not None
        },
        **{
            slot: {
                "symmetric": el.symmetric,
                "inverse": el.inverse,
                "annotations": {
                    tag: annotation.value is True
                    for tag, annotation in el.annotations.items()
                },
                "slot_uri": el.slot_uri,
                "range": el.range,
            }
            for slot in slots
            if (el := BMT.get_element(slot)) is not None
        }
    )
    with open(DATAPATH / "element.json", "w") as stream:
        json.dump(element, stream)


with open("README.md", "r") as stream:
    long_description = stream.read()

try:
    idx = next(
        idx for idx, arg in enumerate(sys.argv)
        if (match := re.fullmatch(r"--vv?\d+\.\d+\.\d+", arg)) is not None
    )
except StopIteration:
    print("ERROR: Specify a biolink-model version using the '--vX.Y.Z' argument")
    exit()
version = sys.argv.pop(idx)[3:]
build(version)

setup(
    name=f"bmt-lite-{version}",
    version="2.3.0",
    author="Patrick Wang",
    author_email="patrick@covar.com",
    url="https://github.com/TranslatorSRI/bmt-lite",
    description="A zero-dependency near-clone of common bmt capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["bmt", "bmt._data"],
    package_data={"bmt._data": ["*.json"]},
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
    license="MIT",
    python_requires=">=3.9",
)
