# planetreference - Spatial references for solar system bodies
# Copyright (C) 2021 - CNES (Jean-Christophe Malapert for Centre National d'Etudes Spatiales)
#
# This file is part of planetreference.
#
# planetreference is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# planetreference is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with planetreference.  If not, see <https://www.gnu.org/licenses/>.
"""Main program."""
import logging

import uvicorn

from planetreference import __name_soft__

from .server import app


def run():
    logger = logging.getLogger(__name__)
    logger.info(f"Main program of {__name_soft__}")
    uvicorn.run(app, host="0.0.0.0", port=8080)
