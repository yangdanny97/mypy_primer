from __future__ import annotations

import difflib
import subprocess
import sys

from mypy_primer.model import Project

# projects to re-enable:
# - https://github.com/edgedb/edgedb
# - https://github.com/twisted/twisted (needs mypy-zope plugin)

# repos with plugins
# - https://github.com/dry-python/returns
# - https://github.com/strawberry-graphql/strawberry
# - https://github.com/r-spacex/submanager
# - https://github.com/NeilGirdhar/efax
# - https://github.com/google/duet
# - https://github.com/RobertCraigie/prisma-client-py


def update_projects(projects: list[Project], check: bool = False) -> None:
    # modifies `get_projects` in place.
    result = []
    with open(__file__) as f:
        keep = True
        for line in f:
            if line.endswith("\n"):
                line = line[:-1]
            if line == "    projects = [":
                result.append(f"    projects = {projects!r}")
                keep = False
            if keep:
                result.append(line)
            if line == "    ]":
                keep = True

    if check:
        code_proc = subprocess.run(
            ["black", "-"], input="\n".join(result), capture_output=True, text=True
        )
        code_proc.check_returncode()
        code = code_proc.stdout

        with open(__file__) as f:
            in_file = f.read()
            if in_file != code:
                diff = difflib.context_diff(
                    in_file.splitlines(keepends=True),
                    code.splitlines(keepends=True),
                    fromfile=__file__,
                    tofile=__file__,
                )
                print("".join(diff))
                sys.exit(1)
    else:
        with open(__file__, "w") as f:
            f.write("\n".join(result))


def get_projects() -> list[Project]:
    # See https://github.com/hauntsaninja/mypy_primer/issues/112
    # Project(
    #     location="https://github.com/ZettaAI/zetta_utils",
    #     mypy_cmd="{mypy} .",
    #     pip_cmd="{pip} install types-Pillow types-cachetools types-requests attrs",
    #     expected_mypy_success=True,
    #     supported_platforms=["linux", "darwin"],
    # ),
    projects = [
        Project(
            location="https://github.com/python/mypy",
            mypy_cmd="{mypy} --config-file mypy_self_check.ini -p mypy -p mypyc",
            pyright_cmd="{pyright} mypy mypyc",
            deps=["pytest", "types-psutil", "types-setuptools", "filelock", "tomli"],
            expected_mypy_success=True,
            cost={"mypy": 15},
        ),
        Project(
            location="https://github.com/hauntsaninja/mypy_primer",
            mypy_cmd="{mypy} -p mypy_primer --strict",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/psf/black",
            mypy_cmd="{mypy} src",
            pyright_cmd="{pyright} src",
            deps=["aiohttp", "click", "pathspec", "tomli", "platformdirs"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/hauntsaninja/pyp",
            mypy_cmd="{mypy} --strict -m pyp",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pytest-dev/pytest",
            mypy_cmd="{mypy} src testing",
            pyright_cmd="{pyright}",
            deps=["attrs", "pluggy", "py", "types-setuptools"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pandas-dev/pandas",
            mypy_cmd="{mypy} pandas",
            pyright_cmd="{pyright} pandas",
            deps=[
                "numpy",
                "types-python-dateutil",
                "types-pytz",
                "types-PyMySQL",
                "types-setuptools",
                "pytest",
            ],
            expected_mypy_success=True,
            cost={"mypy": 60},
        ),
        Project(
            location="https://github.com/pycqa/pylint",
            mypy_cmd="{mypy} pylint/checkers --ignore-missing-imports",
            pyright_cmd="{pyright} pylint/checkers",
            deps=["types-toml"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/aio-libs/aiohttp",
            mypy_cmd="{mypy} aiohttp",
            pyright_cmd="{pyright} aiohttp",
            deps=["pytest"],
            pip_cmd="AIOHTTP_NO_EXTENSIONS=1 {pip} install -e .",
            expected_mypy_success=True,
            supported_platforms=["linux", "darwin"],
        ),
        Project(
            location="https://github.com/python-attrs/attrs",
            mypy_cmd=(
                "{mypy} src/attr/__init__.pyi src/attr/_version_info.pyi src/attr/converters.pyi"
                " src/attr/exceptions.pyi src/attr/filters.pyi src/attr/setters.pyi"
                " src/attr/validators.pyi tests/typing_example.py"
            ),
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/sphinx-doc/sphinx",
            mypy_cmd="{mypy} sphinx",
            pyright_cmd="{pyright} sphinx",
            deps=["babel", "docutils-stubs", "types-requests", "packaging", "jinja2"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/scikit-learn/scikit-learn",
            mypy_cmd="{mypy} sklearn",
            pyright_cmd="{pyright} sklearn",
            deps=["numpy"],
            expected_mypy_success=True,
            cost={"mypy": 15, "pyright": 240},
        ),
        Project(
            location="https://github.com/pypa/bandersnatch",
            mypy_cmd="{mypy} src",
            pyright_cmd="{pyright} src",
            deps=["types-filelock", "types-freezegun", "types-setuptools"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/hauntsaninja/boostedblob",
            mypy_cmd="{mypy} boostedblob",
            pyright_cmd="{pyright} boostedblob",
            deps=["aiohttp", "uvloop", "pycryptodome"],
            expected_mypy_success=True,
            supported_platforms=["linux", "darwin"],
        ),
        Project(
            location="https://github.com/quora/asynq",
            mypy_cmd="{mypy} asynq",
            pyright_cmd="{pyright} asynq",
            deps=["qcore"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/scrapy/scrapy",
            mypy_cmd="{mypy} scrapy tests",
            pyright_cmd="{pyright}",
            deps=["attrs", "types-pyOpenSSL", "types-setuptools"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pypa/twine",
            mypy_cmd="{mypy} twine",
            pyright_cmd="{pyright} twine",
            deps=["keyring", "types-requests", "rich"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/more-itertools/more-itertools",
            mypy_cmd="{mypy} more_itertools",
            pyright_cmd="{pyright} more_itertools",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pydata/xarray",
            mypy_cmd="{mypy} --exclude conftest.py",
            pyright_cmd="{pyright}",
            deps=["types-PyYAML", "types-python-dateutil", "types-pytz", "numpy"],
            expected_mypy_success=True,
            cost={"mypy": 15, "pyright": 170},
        ),
        Project(
            location="https://github.com/pallets/werkzeug",
            mypy_cmd="{mypy} src/werkzeug tests",
            pyright_cmd="{pyright}",
            deps=["types-setuptools", "pytest", "markupsafe"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pallets/jinja",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            deps=["markupsafe"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/mystor/git-revise",
            mypy_cmd="{mypy} gitrevise",
            pyright_cmd="{pyright} gitrevise",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/PyGithub/PyGithub",
            mypy_cmd="{mypy} github tests",
            pyright_cmd="{pyright}",
            deps=["types-requests", "pyjwt"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/we-like-parsers/pegen",
            mypy_cmd="{mypy} src/pegen",
            pyright_cmd="{pyright} src/pegen",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/zulip/zulip",
            mypy_cmd=(
                "{mypy} zerver zilencer zproject tools analytics corporate scripts --platform=linux"
            ),
            pyright_cmd="{pyright}",
            deps=[
                "types-PyYAML",
                "types-polib",
                "types-redis",
                "types-Markdown",
                "types-decorator",
                "types-pytz",
                "types-requests",
                "types-python-dateutil",
                "types-orjson",
                "cryptography",
                "django-stubs",
            ],
            # TODO: the plugin here is a little involved and might only work on linux
            # figure out what it would take to make it actually work
            # needs_mypy_plugins=True,
            expected_mypy_success=True,
            cost={"pyright": 60},
        ),
        Project(
            location="https://github.com/dropbox/stone",
            mypy_cmd="{mypy} stone test",
            pyright_cmd="{pyright}",
            deps=["types-six"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/yelp/paasta",
            mypy_cmd="{mypy} paasta_tools",
            pyright_cmd="{pyright} paasta_tools",
            deps=[
                "types-retry",
                "types-tzlocal",
                "types-ujson",
                "types-python-dateutil",
                "types-pytz",
                "types-PyYAML",
                "types-requests",
            ],
            expected_mypy_success=True,
            supported_platforms=["linux", "darwin"],
        ),
        Project(
            location="https://github.com/PrefectHQ/prefect",
            mypy_cmd="{mypy} src/prefect --exclude conftest.py",
            pyright_cmd="{pyright} src",
            deps=[
                "types-python-dateutil",
                "types-requests",
                "types-simplejson",
                "types-toml",
                "types-croniter",
                "types-PyYAML",
                "types-python-slugify",
                "types-pytz",
                "cryptography",
                "SQLAlchemy",
                "pydantic",
            ],
            needs_mypy_plugins=True,
            expected_mypy_success=True,
            cost={"pyright": 60},
        ),
        Project(
            location="https://github.com/pallets/itsdangerous",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            deps=["pytest"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/jab/bidict",
            mypy_cmd="{mypy} bidict",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/jaraco/zipp",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/aaugustin/websockets",
            mypy_cmd="{mypy} --strict src",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pycqa/isort",
            mypy_cmd="{mypy} --ignore-missing-imports isort",
            pyright_cmd="{pyright} isort",
            deps=["types-setuptools"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/aio-libs/aioredis",
            mypy_cmd="{mypy} aioredis --ignore-missing-imports",
            pyright_cmd="{pyright} aioredis",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/agronholm/anyio",
            mypy_cmd="{mypy} src",
            pyright_cmd="{pyright} src",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/aio-libs/yarl",
            mypy_cmd="{mypy} --show-error-codes yarl tests",
            pyright_cmd="{pyright}",
            deps=["multidict"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/freqtrade/freqtrade",
            mypy_cmd="{mypy} freqtrade scripts",
            pyright_cmd="{pyright}",
            deps=[
                "types-cachetools",
                "types-requests",
                "types-python-dateutil",
                "types-tabulate",
                "types-filelock",
                "pydantic",
                "sqlalchemy",
            ],
            needs_mypy_plugins=True,
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/google/jax",
            mypy_cmd="{mypy} jax",
            pyright_cmd="{pyright} jax",
            deps=["types-requests", "numpy"],
            expected_mypy_success=True,
            cost={"mypy": 20, "pyright": 90},
        ),
        Project(
            location="https://github.com/dulwich/dulwich",
            mypy_cmd="{mypy} dulwich",
            pyright_cmd="{pyright} dulwich",
            deps=["types-certifi", "types-paramiko"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/optuna/optuna",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["types-PyYAML", "types-redis", "types-setuptools", "SQLAlchemy", "numpy"],
            expected_mypy_success=True,
            cost={"pyright": 70},
        ),
        Project(
            location="https://github.com/trailofbits/manticore",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            deps=["types-protobuf", "types-PyYAML", "types-redis", "types-setuptools"],
            expected_mypy_success=True,
            cost={"pyright": 75},
        ),
        Project(
            location="https://github.com/aiortc/aiortc",
            mypy_cmd="{mypy} src",
            pyright_cmd="{pyright} src",
            deps=["cryptography"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/Textualize/rich",
            mypy_cmd="{mypy} -p rich --ignore-missing-imports --warn-unreachable",
            pyright_cmd="{pyright}",
            deps=["attrs"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/dedupeio/dedupe",
            mypy_cmd="{mypy} --ignore-missing-imports dedupe",
            pyright_cmd="{pyright}",
            deps=["numpy"],
            needs_mypy_plugins=True,
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/schemathesis/schemathesis",
            mypy_cmd="{mypy} src/schemathesis",
            pyright_cmd="{pyright} src/schemathesis",
            deps=["attrs", "types-requests", "types-PyYAML", "hypothesis"],
            expected_mypy_success=True,
            supported_platforms=["linux", "darwin"],
        ),
        Project(
            location="https://github.com/graphql-python/graphql-core",
            mypy_cmd="{mypy} src tests",
            pyright_cmd="{pyright} src tests",
            expected_mypy_success=True,
            cost={"mypy": 40},
        ),
        Project(
            location="https://github.com/Legrandin/pycryptodome",
            mypy_cmd="{mypy} lib",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/niklasf/python-chess",
            mypy_cmd="{mypy} --strict chess",
            pyright_cmd="{pyright} chess",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pytorch/ignite",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pypa/packaging",
            mypy_cmd="{mypy} packaging",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pydantic/pydantic",
            mypy_cmd="{mypy} pydantic",
            pyright_cmd="{pyright}",
            deps=["types-toml"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/encode/starlette",
            mypy_cmd="{mypy} starlette tests",
            pyright_cmd="{pyright}",
            deps=["types-requests", "types-PyYAML"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/aio-libs/janus",
            mypy_cmd="{mypy} janus --disallow-untyped-calls --disallow-incomplete-defs --strict",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/alerta/alerta",
            mypy_cmd="{mypy} alerta tests",
            pyright_cmd="{pyright}",
            deps=["types-PyYAML", "types-setuptools", "types-requests", "types-pytz"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/nolar/kopf",
            mypy_cmd="{mypy} kopf",
            pyright_cmd="{pyright}",
            deps=["types-setuptools", "types-PyYAML"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/davidhalter/parso",
            mypy_cmd="{mypy} parso",
            pyright_cmd=None,
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/konradhalas/dacite",
            mypy_cmd="{mypy} dacite",
            pyright_cmd="{pyright} dacite",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/ilevkivskyi/com2ann",
            mypy_cmd="{mypy} --python-version=3.8 src/com2ann.py src/test_com2ann.py",
            pyright_cmd="{pyright} com2ann",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/srittau/python-htmlgen",
            mypy_cmd="{mypy} htmlgen test_htmlgen",
            pyright_cmd="{pyright}",
            deps=["asserts"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/mitmproxy/mitmproxy",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/jpadilla/pyjwt",
            mypy_cmd="{mypy} jwt",
            pyright_cmd="{pyright} jwt",
            deps=["cryptography"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/apache/spark",
            mypy_cmd="{mypy} --config python/mypy.ini python/pyspark",
            pyright_cmd="{pyright} python/pyspark",
            deps=["numpy"],
            expected_mypy_success=True,
            cost={"mypy": 20, "pyright": 110},
        ),
        Project(
            location="https://github.com/laowantong/paroxython",
            mypy_cmd="{mypy} paroxython",
            pyright_cmd="{pyright} paroxython",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/Akuli/porcupine",
            mypy_cmd="{mypy} --config-file= porcupine",
            pyright_cmd="{pyright} porcupine",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/dropbox/mypy-protobuf",
            mypy_cmd="{mypy} mypy_protobuf/",
            pyright_cmd="{pyright}",
            deps=["types-protobuf"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/spack/spack",
            mypy_cmd="{mypy} -p spack -p llnl",
            pyright_cmd=None,
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/johtso/httpx-caching",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["types-freezegun", "types-mock", "httpx", "anyio", "pytest"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/python-poetry/poetry",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            deps=["types-requests"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/awslabs/sockeye",
            mypy_cmd=(
                "{mypy} --ignore-missing-imports --follow-imports=silent @typechecked-files"
                " --no-strict-optional"
            ),
            pyright_cmd=None,
            deps=["types-PyYAML"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/wntrblm/nox",
            mypy_cmd="{mypy} nox",
            pyright_cmd="{pyright} nox",
            deps=["jinja2", "packaging", "importlib_metadata"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pandera-dev/pandera",
            mypy_cmd="{mypy} pandera tests",
            pyright_cmd="{pyright}",
            deps=["types-click", "types-PyYAML", "types-setuptools", "types-requests"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://gitlab.com/cki-project/cki-lib",
            mypy_cmd="{mypy} --strict",
            pyright_cmd="{pyright}",
            deps=["types-PyYAML", "types-requests"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/python-jsonschema/check-jsonschema",
            mypy_cmd="{mypy} src",
            pyright_cmd="{pyright} src",
            deps=["types-jsonschema", "types-requests"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pybind/pybind11",
            mypy_cmd="{mypy} --exclude '^(tests|docs)/' .",
            pyright_cmd="{pyright}",
            deps=["nox", "rich"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/rpdelaney/downforeveryone",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["types-requests", "types-requests", "pytest"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/DataDog/dd-trace-py",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            deps=[
                "attrs",
                "types-six",
                "types-setuptools",
                "types-docutils",
                "types-PyYAML",
                "types-protobuf",
                "envier",
            ],
            needs_mypy_plugins=True,
            expected_mypy_success=True,
            cost={"pyright": 75},
        ),
        Project(
            location="https://github.com/systemd/mkosi",
            mypy_cmd="{mypy} mkosi",
            pyright_cmd="{pyright}",
            deps=["cryptography"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/sympy/sympy",
            mypy_cmd="{mypy} sympy",
            pyright_cmd="{pyright} sympy",
            expected_mypy_success=True,
            cost={"mypy": 35, "pyright": 240},
        ),
        Project(
            location="https://github.com/nion-software/nionutils",
            mypy_cmd="{mypy} --namespace-packages --strict -p nion.utils",
            pyright_cmd="{pyright}",
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/PyCQA/flake8-pyi",
            mypy_cmd="{mypy} pyi.py",
            pyright_cmd="{pyright} pyi.py",
            deps=["types-pyflakes"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/internetarchive/openlibrary",
            mypy_cmd="{mypy} openlibrary",
            pyright_cmd="{pyright} openlibrary",
            deps=[
                "types-PyYAML",
                "types-python-dateutil",
                "types-requests",
                "types-simplejson",
                "types-Deprecated",
            ],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/JohannesBuchner/imagehash",
            mypy_cmd="{mypy} imagehash",
            pyright_cmd="{pyright}",
            deps=["numpy", "types-Pillow"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/Kalmat/PyWinCtl",
            mypy_cmd="{mypy} src/pywinctl",
            pyright_cmd="{pyright}",
            deps=["types-setuptools", "types-pywin32", "types-python-xlib"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/mesonbuild/meson",
            mypy_cmd="./run_mypy.py --mypy {mypy}",
            pyright_cmd=None,
            deps=["types-PyYAML", "coverage", "types-chevron", "types-PyYAML", "types-tqdm"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/aio-libs/aiohttp-devtools",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            deps=["aiohttp", "watchfiles", "types-pygments"],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/sco1/pylox",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["attrs", "pytest"],
            expected_mypy_success=True,
            min_python_version=(3, 10),
        ),
        Project(
            location="https://github.com/ppb/ppb-vector",
            mypy_cmd="{mypy} ppb_vector tests",
            pyright_cmd="{pyright}",
            deps=["hypothesis"],
            expected_mypy_success=True,
            min_python_version=(3, 10),
        ),
        Project(
            location="https://github.com/mkdocs/mkdocs",
            mypy_cmd="{mypy} mkdocs",
            pyright_cmd="{pyright}",
            deps=[
                "babel",
                "types-Markdown",
                "types-pytz",
                "types-PyYAML",
                "types-setuptools",
                "jinja2",
                "click",
                "watchdog",
                "pathspec",
                "platformdirs",
                "packaging",
            ],
            expected_mypy_success=True,
        ),
        Project(
            location="https://github.com/pyppeteer/pyppeteer",
            mypy_cmd="{mypy} pyppeteer --config-file tox.ini",
            pyright_cmd="{pyright}",
            pip_cmd="{pip} install .",
        ),
        Project(
            location="https://github.com/pypa/pip",
            mypy_cmd="{mypy} src",
            pyright_cmd="{pyright}",
        ),
        Project(
            location="https://github.com/pytorch/vision",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            cost={"pyright": 50},
        ),
        Project(
            location="https://github.com/tornadoweb/tornado",
            mypy_cmd="{mypy} tornado",
            pyright_cmd="{pyright}",
            deps=["types-contextvars", "types-pycurl"],
        ),
        Project(
            location="https://github.com/scipy/scipy",
            mypy_cmd="{mypy} scipy",
            pyright_cmd=None,
            deps=["numpy", "pytest", "hypothesis", "types-psutil"],
            needs_mypy_plugins=True,
        ),
        Project(
            location="https://github.com/pycqa/flake8",
            mypy_cmd="{mypy} src tests",
            pyright_cmd="{pyright}",
            deps=["pytest"],
        ),
        Project(
            location="https://github.com/home-assistant/core",
            mypy_cmd=(
                "sed -i.bak '/^plugins = pydantic.mypy$/s/^/#/' mypy.ini; {mypy} homeassistant"
            ),
            pyright_cmd="{pyright} homeassistant",
            deps=[
                "attrs",
                "pydantic",
                "types-setuptools",
                "types-atomicwrites",
                "types-certifi",
                "types-croniter",
                "types-PyYAML",
                "types-requests",
                "types-python-slugify",
                "types-backports",
            ],
            cost={"mypy": 40, "pyright": 240},
            supported_platforms=["linux", "darwin"],  # hack for sed
        ),
        Project(
            location="https://github.com/kornia/kornia",
            mypy_cmd="{mypy} kornia",
            pyright_cmd="{pyright} kornia",
        ),
        Project(
            location="https://github.com/ibis-project/ibis",
            mypy_cmd="{mypy} --ignore-missing-imports ibis",
            pyright_cmd="{pyright} ibis",
            deps=[
                "types-setuptools",
                "types-requests",
                "types-python-dateutil",
                "types-pytz",
                "SQLAlchemy",
            ],
            cost={"pyright": 60},
        ),
        Project(
            location="https://github.com/streamlit/streamlit",
            mypy_cmd="{mypy} --config-file=lib/mypy.ini lib scripts",
            pyright_cmd="{pyright}",
            deps=[
                "attrs",
                "tornado",
                "packaging",
                "types-toml",
                "types-python-dateutil",
                "types-setuptools",
                "types-protobuf",
                "types-pytz",
                "types-requests",
                "types-cffi",
                "click",
                "pytest",
            ],
        ),
        Project(
            location="https://github.com/dragonchain/dragonchain",
            mypy_cmd="{mypy} dragonchain --error-summary",
            pyright_cmd="{pyright} dragonchain",
            deps=["types-redis", "types-requests"],
        ),
        Project(
            location="https://github.com/mikeshardmind/SinbadCogs",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["attrs", "types-pytz", "types-python-dateutil", "types-PyYAML"],
        ),
        Project(
            location="https://github.com/rotki/rotki",
            mypy_cmd="{mypy} rotkehlchen/ tools/data_faker",
            pyright_cmd="{pyright}",
            deps=["eth-typing", "types-requests", "types-setuptools"],
            cost={"pyright": 60},
        ),
        Project(
            location="https://github.com/arviz-devs/arviz",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["pytest", "types-setuptools", "types-ujson", "numpy", "xarray"],
        ),
        Project(
            location="https://github.com/urllib3/urllib3",
            mypy_cmd="{mypy} . --exclude setup.py",
            pyright_cmd="{pyright}",
            deps=[
                "idna>=2.0.0",
                "cryptography>=1.3.4",
                "tornado>=6.1",
                "pytest",
                "trustme==0.9.0",
                "types-backports",
                "types-requests",
            ],
        ),
        Project(
            location="https://github.com/common-workflow-language/schema_salad",
            mypy_cmd="MYPYPATH=$MYPYPATH:mypy-stubs {mypy} schema_salad",
            pyright_cmd=None,
            pip_cmd=(
                "{pip} install $(grep -v mypy mypy-requirements.txt) -r test-requirements.txt"
                " -rrequirements.txt"
            ),
            expected_mypy_success=True,
            supported_platforms=["linux", "darwin"],
        ),
        Project(
            location="https://github.com/common-workflow-language/cwltool",
            mypy_cmd="MYPYPATH=$MYPYPATH:mypy-stubs {mypy} cwltool tests/*.py setup.py",
            pyright_cmd=None,
            pip_cmd="{pip} install $(grep -v mypy mypy-requirements.txt) -r test-requirements.txt",
            expected_mypy_success=True,
            cost={"mypy": 15},
            supported_platforms=["linux", "darwin"],
        ),
        Project(
            location="https://github.com/AlexWaygood/typeshed-stats",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["attrs", "cattrs", "pytest", "aiohttp", "pathspec", "jinja2", "tomli"],
        ),
        Project(
            location="https://github.com/FasterSpeeding/Tanjun",
            mypy_cmd="{mypy} tanjun",
            pyright_cmd="{pyright}",
            deps=["hikari", "alluka"],
        ),
        Project(
            location="https://github.com/joerick/pyinstrument",
            mypy_cmd="{mypy} pyinstrument",
            pyright_cmd="{pyright}",
        ),
        Project(
            location="https://github.com/Gobot1234/steam.py",
            mypy_cmd="{mypy} steam",
            pyright_cmd="{pyright}",
            deps=["cryptography"],
        ),
        Project(
            location="https://github.com/cpitclaudel/alectryon",
            mypy_cmd="{mypy} alectryon.py",
            pyright_cmd="{pyright}",
        ),
        Project(
            location="https://github.com/yurijmikhalevich/rclip",
            mypy_cmd="{mypy} rclip",
            pyright_cmd="{pyright}",
        ),
        Project(
            location="https://github.com/psycopg/psycopg",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            deps=["pytest", "pproxy"],
        ),
        Project(
            location="https://gitlab.com/dkg/python-sop",
            mypy_cmd="{mypy} --strict sop",
            pyright_cmd="{pyright} sop",
        ),
        Project(
            location="https://github.com/Rapptz/discord.py",
            mypy_cmd="{mypy} discord",
            pyright_cmd="{pyright}",
            deps=["types-requests", "types-setuptools", "aiohttp"],
            cost={"mypy": 20},
        ),
        Project(
            location="https://github.com/canonical/cloud-init",
            mypy_cmd="{mypy} cloudinit/ tests/ tools/",
            pyright_cmd="{pyright}",
            deps=[
                "jinja2",
                "pytest",
                "types-jsonschema",
                "types-oauthlib",
                "types-pyyaml",
                "types-requests",
                "types-setuptools",
            ],
            cost={"mypy": 15},
        ),
        Project(
            location="https://github.com/mongodb/mongo-python-driver",
            mypy_cmd="{mypy} bson gridfs tools pymongo",
            pyright_cmd="{pyright}",
            deps=["types-requests", "types-pyOpenSSL", "cryptography", "certifi"],
        ),
        Project(
            location="https://github.com/artigraph/artigraph",
            mypy_cmd="{mypy}",
            pyright_cmd="{pyright}",
            deps=["pydantic", "numpy", "pytest"],
            needs_mypy_plugins=True,
        ),
        Project(
            location="https://github.com/MaterializeInc/materialize",
            mypy_cmd=(
                "MYPYPATH=$MYPYPATH:misc/python {mypy} --explicit-package-bases ci misc/python"
            ),
            pyright_cmd="{pyright}",
            pip_cmd="{pip} install -r ci/builder/requirements.txt",
        ),
        Project(
            location="https://github.com/canonical/operator",
            mypy_cmd="{mypy} ops",
            pyright_cmd="{pyright}",
            deps=["types-PyYAML"],
        ),
        Project(
            location="https://github.com/astropenguin/xarray-dataclasses",
            mypy_cmd="{mypy} xarray_dataclasses",
            pyright_cmd="{pyright}",
            deps=["numpy", "xarray"],
        ),
        Project(
            location="https://github.com/caronc/apprise",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=[
                "types-six",
                "types-mock",
                "cryptography",
                "types-requests",
                "types-Markdown",
                "pytest",
                "certifi",
                "babel",
            ],
        ),
        Project(
            location="https://github.com/Finistere/antidote",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["pytest"],
        ),
        Project(
            location="https://github.com/cognitedata/Expression",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["pytest"],
        ),
        Project(
            location="https://github.com/pyodide/pyodide",
            mypy_cmd="{mypy} src pyodide-build --exclude 'setup.py|^src/tests|conftest.py'",
            pyright_cmd="{pyright} src pyodide-build",
            deps=[
                "packaging",
                "types-docutils",
                "types-pyyaml",
                "types-setuptools",
                "numpy",
                "pydantic",
            ],
            needs_mypy_plugins=True,
        ),
        Project(
            location="https://github.com/bokeh/bokeh",
            mypy_cmd="{mypy} src release",
            pyright_cmd="{pyright}",
            deps=["types-boto", "tornado", "numpy", "jinja2", "selenium"],
            cost={"pyright": 60},
        ),
        Project(
            location="https://github.com/pandas-dev/pandas-stubs",
            mypy_cmd="{mypy} pandas-stubs tests",
            pyright_cmd="{pyright}",
            deps=[
                "numpy",
                "types-pytz",
                "matplotlib",
                "xarray",
                "pyarrow",
                "jinja2",
                "pytest",
                "SQLAlchemy",
            ],
            expected_pyright_success=True,
            cost={"mypy": 40, "pyright": 75},
        ),
        Project(
            location="https://github.com/enthought/comtypes",
            mypy_cmd="{mypy} comtypes --platform win32",
            pyright_cmd="{pyright}",
            deps=["numpy"],
        ),
        Project(
            location="https://github.com/mit-ll-responsible-ai/hydra-zen",
            mypy_cmd="{mypy} src tests/annotations/mypy_checks.py",
            pyright_cmd="{pyright} tests/annotations src",
            deps=["pydantic", "beartype", "hydra-core"],
        ),
        Project(
            location="https://github.com/Toufool/AutoSplit",
            mypy_cmd="{mypy} src",
            pyright_cmd="{pyright} src",
            deps=[
                "certifi",
                "ImageHash",
                "numpy",
                "packaging",
                "PyWinCtl",
                "PySide6-Essentials",
                "types-D3DShot",
                "types-keyboard",
                "types-Pillow",
                "types-psutil",
                "types-PyAutoGUI",
                "types-pyinstaller",
                "types-pywin32",
                "types-requests",
                "types-toml",
            ],
        ),
        Project(
            location="https://github.com/Avasam/speedrun.com_global_scoreboard_webapp",
            mypy_cmd="{mypy} backend",
            pyright_cmd="{pyright}",
            deps=[
                "Flask",
                "PyJWT",
                "requests-cache",
                "types-Flask-SQLAlchemy",
                "types-httplib2",
                "types-requests",
            ],
        ),
        Project(
            location="https://github.com/pwndbg/pwndbg",
            mypy_cmd="{mypy} pwndbg",
            pyright_cmd="{pyright}",
            deps=["types-gdb"],
            cost={"pyright": 75},
        ),
        Project(
            location="https://github.com/keithasaurus/koda-validate",
            mypy_cmd="{mypy} koda_validate --strict",
            pyright_cmd="{pyright}",
            deps=["koda"],
        ),
        Project(
            location="https://github.com/python/cpython",
            mypy_cmd="{mypy} --config-file Tools/clinic/mypy.ini",
            pyright_cmd=None,
            name_override="CPython (Argument Clinic)",
        ),
        Project(
            location="https://github.com/python/cpython",
            mypy_cmd="{mypy} --config-file Tools/cases_generator/mypy.ini",
            pyright_cmd=None,
            name_override="CPython (cases_generator)",
        ),
        Project(
            location="https://github.com/python/cpython",
            mypy_cmd="{mypy} --config-file Tools/peg_generator/mypy.ini",
            pyright_cmd=None,
            deps=["types-setuptools", "types-psutil"],
            name_override="CPython (peg_generator)",
        ),
        Project(
            location="https://github.com/python-trio/trio",
            mypy_cmd="{mypy} src/trio",
            pyright_cmd="{pyright} src/trio",
            deps=[
                "types-pyOpenSSL",
                "types-cffi",
                "attrs",
                "outcome",
                "exceptiongroup",
                "pytest",
                "sniffio",
            ],
        ),
        Project(
            location="https://github.com/pypa/setuptools",
            mypy_cmd="{mypy} setuptools pkg_resources",
            pyright_cmd="{pyright}",
            deps=[
                "pytest",
                "filelock",
                "ini2toml",
                "packaging",
                "tomli",
                "tomli-w",
            ],
        ),
        Project(
            location="https://github.com/detachhead/pytest-robotframework",
            mypy_cmd="{mypy} -p pytest_robotframework",
            pyright_cmd="{pyright}",
        ),
        Project(
            location="https://github.com/mhammond/pywin32",
            mypy_cmd="{mypy} .",
            pyright_cmd="{pyright}",
            deps=["types-pywin32", "types-regex", "types-setuptools"],
        ),
    ]
    assert len(projects) == len({p.name for p in projects})
    for p in projects:
        assert p.supported_platforms is None or all(
            p in ("linux", "darwin") for p in p.supported_platforms
        )
    return projects
