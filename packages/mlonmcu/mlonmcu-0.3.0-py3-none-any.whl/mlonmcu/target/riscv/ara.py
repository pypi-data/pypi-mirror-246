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
"""MLonMCU ARA Target definitions"""

import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory
import time

from mlonmcu.logging import get_logger
from mlonmcu.config import str2bool
from mlonmcu.feature.features import SUPPORTED_TVM_BACKENDS
from mlonmcu.target.common import cli, execute
from mlonmcu.target.metrics import Metrics
from .riscv import RISCVTarget
from .util import update_extensions

logger = get_logger()


class AraTarget(RISCVTarget):
    """Target using a Pulpino-like VP running in the GVSOC simulator"""

    FEATURES = RISCVTarget.FEATURES + ["log_instrs", "vext"]

    DEFAULTS = {
        **RISCVTarget.DEFAULTS,
        "xlen": 64,
        "nr_lanes": 4,
        "vlen": 4096,  # default value for hardware compilation, will be overwritten by -c vext.vlen
        "enable_vext": False,
        "vext_spec": 1.0,
        "embedded_vext": False,
        "elen": 64,
    }

    REQUIRED = RISCVTarget.REQUIRED + [
        "ara.src_dir",  # for the bsp package
        "verilator.install_dir",  # for simulation
    ]

    def __init__(self, name="ara", features=None, config=None):
        super().__init__(name, features=features, config=config)
        assert self.config["xlen"] == str(64), 'ARA target must has xlen equal 64, try "-c ara.xlen=64"'

    @property
    def ara_apps_dir(self):
        return Path(self.config["ara.src_dir"]) / "apps"

    @property
    def ara_hardware_dir(self):
        return Path(self.config["ara.src_dir"]) / "hardware"

    @property
    def verilator_install_dir(self):
        return Path(self.config["verilator.install_dir"])

    @property
    def nr_lanes(self):
        value = self.config["nr_lanes"]
        return value

    @property
    def vlen(self):
        value = self.config["vlen"]
        return value

    @property
    def enable_vext(self):
        value = self.config["enable_vext"]
        return str2bool(value) if not isinstance(value, (bool, int)) else value

    @property
    def vext_spec(self):
        return float(self.config["vext_spec"])

    @property
    def embedded_vext(self):
        value = self.config["embedded_vext"]
        return str2bool(value) if not isinstance(value, (bool, int)) else value

    @property
    def elen(self):
        return int(self.config["elen"])

    @property
    def extensions(self):
        exts = super().extensions
        return update_extensions(
            exts,
            vext=self.enable_vext,
            elen=self.elen,
            embedded=self.embedded_vext,
            fpu=self.fpu,
            variant=self.gcc_variant,
        )

    def prepare_simulator(self, program, *args, cwd=os.getcwd(), **kwargs):
        # populate the ara verilator testbench directory
        self.tb_ara_verilator_build_dir = TemporaryDirectory()
        env = os.environ.copy()
        env["ROOT_DIR"] = str(self.ara_hardware_dir)
        env["veril_library"] = self.tb_ara_verilator_build_dir.name
        env["veril_path"] = str(self.verilator_install_dir / "bin")
        env["nr_lanes"] = str(self.nr_lanes)
        env["vlen"] = str(self.vlen)
        env["bender_defs"] = f"--define NR_LANES={self.nr_lanes} --define VLEN={self.vlen} --define RVV_ARIANE=1"
        compile_verilator_tb_ret = execute(
            "make",
            "verilate",
            "-i",  # the origin Makefile will check the path of QuestaSim in line 80. This error should be ignored
            env=env,
            cwd=self.ara_hardware_dir,
            *args,
            **kwargs,
        )
        return compile_verilator_tb_ret

    def exec(self, program, *args, cwd=os.getcwd(), **kwargs):
        """Use target to execute an executable with given arguments"""
        # run simulation
        # to add trace: https://github.com/pulp-platform/ara/blob/main/hardware/Makefile#L201
        ara_verilator_args = ["-l", f"ram,{program}"]
        if len(self.extra_args) > 0:
            if isinstance(self.extra_args, str):
                extra_args = self.extra_args.split(" ")
            else:
                extra_args = self.extra_args
            ara_verilator_args.extend(extra_args)

        assert (
            self.tb_ara_verilator_build_dir is not None
        ), "A folder containing Vara_tb_verilator should be generated by the function prepare_simulator"
        env = os.environ.copy()
        simulation_ret = execute(
            str(Path(self.tb_ara_verilator_build_dir.name) / "Vara_tb_verilator"),
            *ara_verilator_args,
            env=env,
            cwd=cwd,
            *args,
            **kwargs,
        )
        self.tb_ara_verilator_build_dir.cleanup()
        return simulation_ret

    def parse_stdout(self, out):
        cpu_cycles = re.search(r"Total Cycles: (.*)", out)
        if not cpu_cycles:
            logger.warning("unexpected script output (cycles)")
            cycles = None
        else:
            cycles = int(float(cpu_cycles.group(1)))

        cpu_instructions = re.search(r"Total Instructions: (.*)", out)
        if not cpu_instructions:
            logger.warning("unexpected script output (instructions)")
            cpu_instructions = None
        else:
            cpu_instructions = int(float(cpu_instructions.group(1)))
        return cycles, cpu_instructions

    def get_metrics(self, elf, directory, *args, handle_exit=None):
        out = ""
        if self.print_outputs:
            self.prepare_simulator(elf, *args, cwd=directory, live=True, handle_exit=handle_exit)
        else:
            self.prepare_simulator(
                elf, *args, cwd=directory, live=False, print_func=lambda *args, **kwargs: None, handle_exit=handle_exit
            )
        simulation_start = time.time()
        if self.print_outputs:
            out += self.exec(elf, *args, cwd=directory, live=True, handle_exit=handle_exit)
        else:
            out += self.exec(
                elf, *args, cwd=directory, live=False, print_func=lambda *args, **kwargs: None, handle_exit=handle_exit
            )
        simulation_end = time.time()
        cycles, instructions = self.parse_stdout(out)
        metrics = Metrics()
        metrics.add("Cycles", cycles)
        metrics.add("Instructions", instructions)
        metrics.add("CPI", cycles / instructions)
        metrics.add("finished_in_sec", simulation_end - simulation_start)
        return metrics, out, []

    def get_target_system(self):
        return self.name

    def get_platform_defs(self, platform):
        assert platform == "mlif"
        ret = super().get_platform_defs(platform)
        # ret["RISCV_ARCH"] = "rv32imcxpulpv3"
        ret["XLEN"] = self.xlen
        ret["RISCV_ABI"] = self.abi
        ret["ARA_APPS_DIR"] = self.ara_apps_dir
        ret["MLONMCU_ARA_NR_LANES"] = self.nr_lanes
        ret["MLONMCU_ARA_VLEN"] = self.vlen
        ret["CMAKE_VERBOSE_MAKEFILE"] = "BOOL=OFF"
        return ret

    def get_backend_config(self, backend):
        ret = super().get_backend_config(backend)
        if backend in SUPPORTED_TVM_BACKENDS:
            ret.update({"target_mabi": self.abi})
        return ret


if __name__ == "__main__":
    cli(target=AraTarget)
