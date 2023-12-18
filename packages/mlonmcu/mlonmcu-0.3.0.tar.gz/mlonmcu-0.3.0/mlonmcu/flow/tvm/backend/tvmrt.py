#
# Copyright (c) 2022 TUM Department of Electrical and Computer Engineering.
#
# This file is part of MLonMCU.
# See https://github.com/tum-ei-eda/mlonmcu.git for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
import tempfile
from typing import Tuple

# import json
import tarfile
from pathlib import Path

from .backend import TVMBackend
from .wrapper import generate_tvmrt_wrapper, generate_wrapper_header
from mlonmcu.flow.backend import main
from mlonmcu.config import str2bool
from mlonmcu.artifact import Artifact, ArtifactFormat
from .tvmc_utils import get_tvmrt_tvmc_args
from .model_info import get_relay_model_info


class TVMRTBackend(TVMBackend):
    FEATURES = [
        *TVMBackend.FEATURES,
        "debug_arena",
    ]

    DEFAULTS = {
        **TVMBackend.DEFAULTS,
        "debug_arena": False,
        "arena_size": 2**20,  # Can not be detemined automatically (Very large)
        # TODO: arena size warning!
    }

    name = "tvmrt"

    def __init__(self, runtime="crt", fmt="mlf", features=None, config=None):
        super().__init__(executor="graph", runtime=runtime, fmt=fmt, features=features, config=config)

    @property
    def arena_size(self):
        size = self.config["arena_size"]
        return int(size) if size else None

    @property
    def debug_arena(self):
        value = self.config["debug_arena"]
        return str2bool(value) if not isinstance(value, (bool, int)) else value

    def get_tvmc_compile_args(self, out, dump=None):
        return super().get_tvmc_compile_args(out, dump=dump) + get_tvmrt_tvmc_args()

    def get_graph_and_params_from_mlf(self, path):
        graph = None
        with open(Path(path) / "executor-config" / "graph" / "default.graph", "r") as handle:
            graph = handle.read()
        params = None
        with open(Path(path) / "parameters" / "default.params", "rb") as handle:
            params = handle.read()

        return graph, params

    def generate(self) -> Tuple[dict, dict]:
        artifacts = []
        assert self.model is not None
        full = False  # Required due to bug in TVM
        dump = ["c", "relay"] if full else []
        generate_wrapper = True
        if generate_wrapper and not self.model_info and "relay" not in dump:
            dump.append("relay")
        with tempfile.TemporaryDirectory() as temp_dir:
            out_path = Path(temp_dir) / f"{self.prefix}.tar"
            out = self.invoke_tvmc_compile(out_path, dump=dump)
            mlf_path = Path(temp_dir) / "mlf"
            tarfile.open(out_path).extractall(mlf_path)
            # with open(mlf_path / "metadata.json") as handle:
            #     metadata = json.load(handle)
            # metadata_txt = json.dumps(metadata)
            with open(out_path, "rb") as handle:
                mlf_data = handle.read()
                artifacts.append(
                    Artifact(
                        f"{self.prefix}.tar",
                        raw=mlf_data,
                        fmt=ArtifactFormat.MLF,
                        archive=True,
                    )
                )
            if "c" in dump:
                with open(str(out_path) + ".c", "r") as handle:
                    mod_src = handle.read()
                    artifacts.append(
                        Artifact(
                            f"{self.prefix}.c",
                            content=mod_src,
                            fmt=ArtifactFormat.SOURCE,
                            optional=True,
                        )
                    )
            if "relay" in dump:
                with open(str(out_path) + ".relay", "r") as handle:
                    mod_txt = handle.read()
                    artifacts.append(
                        Artifact(
                            f"{self.prefix}.relay",
                            content=mod_txt,
                            fmt=ArtifactFormat.TEXT,
                            optional=True,
                        )
                    )
            if generate_wrapper:
                workspace_size = self.arena_size
                assert workspace_size >= 0
                graph, params = self.get_graph_and_params_from_mlf(mlf_path)
                if not self.model_info:
                    self.model_info = get_relay_model_info(mod_txt)
                wrapper_src = generate_tvmrt_wrapper(
                    graph, params, self.model_info, workspace_size, debug_arena=self.debug_arena
                )
                artifacts.append(Artifact("rt_wrapper.c", content=wrapper_src, fmt=ArtifactFormat.SOURCE))
                header_src = generate_wrapper_header()
                artifacts.append(Artifact("tvm_wrapper.h", content=header_src, fmt=ArtifactFormat.SOURCE))
            workspace_size_artifact = Artifact(
                "tvmrt_workspace_size.txt", content=f"{workspace_size}", fmt=ArtifactFormat.TEXT
            )
            artifacts.append(workspace_size_artifact)
            stdout_artifact = Artifact(
                "tvmc_compile_out.log", content=out, fmt=ArtifactFormat.TEXT
            )  # TODO: rename to tvmrt_out.log?
            artifacts.append(stdout_artifact)

        # prepare -> common?
        # invoke_tvmc -> common?
        # generate_wrapper()
        return {"default": artifacts}, {}


if __name__ == "__main__":
    sys.exit(
        main(
            TVMRTBackend,
            args=sys.argv[1:],
        )
    )  # pragma: no cover
