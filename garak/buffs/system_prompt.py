# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Buff that prepends a system prompt to queries."""

from collections.abc import Iterable
import logging

import garak.attempt
from garak.buffs.base import Buff
from garak import _config


class SystemPromptBuff(Buff):
    """Buff that prepends a system prompt to user queries.

    This buff takes a system prompt and adds it to the beginning of a query
    by modifying the message structure to include a system message.

    Parameters:
        system_prompt (str): The system prompt to prepend to queries.
                            Can be set in config as system_prompt.system_prompt
    """

    DEFAULT_PARAMS = {
        "system_prompt": "{user_input}",
    }

    def __init__(self, config_root=_config) -> None:
        super().__init__(config_root)
        # After _load_config in the parent class, the system_prompt attribute should be set
        # or we use the default value
        # print("CONFIG ROOT", config_root)
        self.system_prompt = config_root.plugins.system_prompt
        print("SYSTEM PROMPT", self.system_prompt)
        if not hasattr(self, "system_prompt"):
            self.system_prompt = self.DEFAULT_PARAMS["system_prompt"]
        logging.info(
            f"SystemPromptBuff initialized with system prompt: {self.system_prompt}"
        )

    def transform(
        self, attempt: garak.attempt.Attempt
    ) -> Iterable[garak.attempt.Attempt]:
        """Transform the attempt by adding a system prompt to the messages."""
        user_input = attempt.prompt
        attempt.prompt = self.system_prompt.format(user_input=user_input)
        # print("TRANSFORMED PROMPT", attempt.prompt)
        yield attempt
