# Copyright (C) 2022. Huawei Technologies Co., Ltd. All rights reserved. Redistribution and use in source and binary
# forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
from pathlib import Path

import torch

ROOT_PROJECT = str(Path(os.path.realpath(__file__)).parent.parent.parent)
sys.path[0] = ROOT_PROJECT

from mcbo.optimizers import RandomSearch

if __name__ == '__main__':
    from mcbo.task_factory import task_factory

    task_kwargs = dict(seq_len=10, ntk_name='adder', objective='size')
    dtype = torch.float64
    task, search_space = task_factory('mig_optimization', dtype=dtype, **task_kwargs)

    optimizer = RandomSearch(search_space, input_constraints=task.input_constraints, store_observations=True)
    print(f"{optimizer.name}_{task.name}")

    for i in range(10):
        x_next = optimizer.suggest(2)
        y_next = task(x_next)
        optimizer.observe(x_next, y_next)
        print(f'Iteration {i + 1:>4d} - Best f(x) {optimizer.best_y:.3f}')
