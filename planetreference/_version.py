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
"""Project metadata."""
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

__name_soft__ = "planetreference"
try:
    __version__ = get_distribution(__name_soft__).version
except DistributionNotFound:
    __version__ = "0.0.0"
__title__ = "planetreference"
__description__ = "Spatial references for solar system bodies"
__url__ = "https://github.com/J-Christophe/planetreference"
__author__ = "Jean-Christophe Malapert"
__author_email__ = "jean-christophe.malapert@cnes.fr"
__license__ = "GNU General Public License v3"
__copyright__ = "2021, CNES (Jean-Christophe Malapert for Centre National d'Etudes Spatiales)"
