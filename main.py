#!/usr/bin/env python3
"""
GitHub README Seasons Generator

Generates an animated SVG that changes with the seasons.
"""

import argparse
import random
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import NamedTuple


class SeasonTheme(NamedTuple):
    """Color theme for each season."""

    name: str
    grass_colors: list[str]
    flower_colors: list[str]


# Season definitions
SEASONS = {
    "spring": SeasonTheme(
        name="spring",
        grass_colors=[
            "#81c784",
            "#a5d6a7",
            "#8bc34a",
            "#7cb342",
        ],  # Young but not too pale
        flower_colors=["#f48fb1", "#fff176", "#ce93d8", "#ffffff"],
    ),
    "summer": SeasonTheme(
        name="summer",
        grass_colors=["#388e3c", "#43a047", "#4caf50", "#66bb6a"],
        flower_colors=["#ff7043", "#ffca28", "#26a69a"],
    ),
    "autumn": SeasonTheme(
        name="autumn",
        grass_colors=["#f57c00", "#ff9800", "#ffa726", "#8d6e63"],
        flower_colors=["#d84315", "#bf360c", "#ffab00"],
    ),
    "winter": SeasonTheme(
        name="winter",
        grass_colors=["#78909c", "#90a4ae", "#b0bec5", "#8d6e63"],
        flower_colors=[],
    ),
}


def get_current_season(date: datetime | None = None) -> str:
    """Determine the current season based on the date."""
    if date is None:
        date = datetime.now()

    month = date.month

    # Northern hemisphere seasons
    if month in (3, 4, 5):
        return "spring"
    elif month in (6, 7, 8):
        return "summer"
    elif month in (9, 10, 11):
        return "autumn"
    else:  # 12, 1, 2
        return "winter"


def generate_grass_blade(
    x: float,
    height: float,
    color: str,
    animation_delay: float,
    blade_id: int,
) -> str:
    """Generate a single grass blade with animation."""
    # Grass blade is a curved path
    control_offset = height * 0.3
    tip_curve = height * 0.1

    # Base width tapers to tip
    base_width = random.uniform(2, 4)

    # Create path for grass blade (quadratic bezier curve)
    path = f"""
    <path
        id="blade-{blade_id}"
        d="M {x} 0 
           Q {x - control_offset} {-height * 0.6} {x + tip_curve} {-height}
           L {x + base_width + tip_curve} {-height}
           Q {x + base_width - control_offset} {-height * 0.6} {x + base_width} 0
           Z"
        fill="{color}"
        transform-origin="{x + base_width/2}px 0px"
    >
        <animateTransform
            attributeName="transform"
            type="rotate"
            values="-3;3;-3"
            dur="{1.5 + animation_delay}s"
            repeatCount="indefinite"
            keyTimes="0;0.5;1"
            calcMode="spline"
            keySplines="0.4 0 0.6 1; 0.4 0 0.6 1"
        />
    </path>"""
    return path


def generate_flower(x: float, y: float, color: str, size: float, flower_id: int) -> str:
    """Generate a simple flower."""
    petals = ""
    num_petals = random.choice([5, 6])

    for i in range(num_petals):
        angle = (360 / num_petals) * i
        petals += f"""
        <ellipse
            cx="{x}"
            cy="{y - size}"
            rx="{size * 0.4}"
            ry="{size}"
            fill="{color}"
            transform="rotate({angle} {x} {y})"
            opacity="0.9"
        />"""

    # Flower center
    center = f"""
    <circle cx="{x}" cy="{y}" r="{size * 0.3}" fill="#ffeb3b"/>"""

    return f"""
    <g id="flower-{flower_id}" class="flower">
        {petals}
        {center}
    </g>"""


def generate_snowflake(
    x: float, y: float, size: float, flake_id: int, ground_y: float
) -> str:
    """Generate a falling snowflake that disappears when it lands."""
    duration = random.uniform(4, 8)
    delay = random.uniform(0, 8)
    drift_x = random.uniform(-30, 30)

    # Start above the visible area
    start_y = random.uniform(-50, -10)
    # End at ground level
    end_y = ground_y - random.uniform(5, 15)

    return f"""
    <circle
        id="snow-{flake_id}"
        cx="{x}"
        cy="{start_y}"
        r="{size}"
        fill="white"
        opacity="0"
    >
        <animate
            attributeName="cy"
            values="{start_y};{end_y}"
            dur="{duration}s"
            repeatCount="indefinite"
            begin="{delay}s"
        />
        <animate
            attributeName="cx"
            values="{x};{x + drift_x}"
            dur="{duration}s"
            repeatCount="indefinite"
            begin="{delay}s"
        />
        <animate
            attributeName="opacity"
            values="0;0.9;0.9;0"
            keyTimes="0;0.05;0.85;1"
            dur="{duration}s"
            repeatCount="indefinite"
            begin="{delay}s"
        />
    </circle>"""


def generate_snowman(x: float, ground_y: float, snowman_id: int) -> str:
    """Generate a cute snowman with gentle swaying animation."""
    # Snowman body sizes (fixed size)
    bottom_r = 22
    middle_r = bottom_r * 0.7
    top_r = middle_r * 0.65

    # Calculate positions
    bottom_y = ground_y - bottom_r * 0.7
    middle_y = bottom_y - bottom_r - middle_r * 0.8
    top_y = middle_y - middle_r - top_r * 0.8

    # Hat dimensions
    hat_width = top_r * 1.8
    hat_height = top_r * 1.2
    hat_brim = top_r * 2.2

    # Animation timing
    sway_duration = 4

    return f"""
    <g id="snowman-{snowman_id}" transform-origin="{x}px {ground_y}px">
        <animateTransform
            attributeName="transform"
            type="rotate"
            values="-2;2;-2"
            dur="{sway_duration}s"
            repeatCount="indefinite"
            keyTimes="0;0.5;1"
            calcMode="spline"
            keySplines="0.4 0 0.6 1; 0.4 0 0.6 1"
        />
        <!-- Bottom body -->
        <circle cx="{x}" cy="{bottom_y}" r="{bottom_r}" fill="#ffffff" stroke="#e0e0e0" stroke-width="1"/>
        <!-- Middle body -->
        <circle cx="{x}" cy="{middle_y}" r="{middle_r}" fill="#ffffff" stroke="#e0e0e0" stroke-width="1"/>
        <!-- Top body (head) -->
        <circle cx="{x}" cy="{top_y}" r="{top_r}" fill="#ffffff" stroke="#e0e0e0" stroke-width="1"/>
        
        <!-- Eyes -->
        <circle cx="{x - top_r * 0.35}" cy="{top_y - top_r * 0.2}" r="{top_r * 0.12}" fill="#333333"/>
        <circle cx="{x + top_r * 0.35}" cy="{top_y - top_r * 0.2}" r="{top_r * 0.12}" fill="#333333"/>
        
        <!-- Carrot nose -->
        <polygon points="{x},{top_y + top_r * 0.05} {x + top_r * 0.8},{top_y + top_r * 0.15} {x},{top_y + top_r * 0.25}" fill="#ff7043"/>
        
        <!-- Smile (coal dots) -->
        <circle cx="{x - top_r * 0.4}" cy="{top_y + top_r * 0.35}" r="{top_r * 0.08}" fill="#333333"/>
        <circle cx="{x - top_r * 0.2}" cy="{top_y + top_r * 0.42}" r="{top_r * 0.08}" fill="#333333"/>
        <circle cx="{x}" cy="{top_y + top_r * 0.45}" r="{top_r * 0.08}" fill="#333333"/>
        <circle cx="{x + top_r * 0.2}" cy="{top_y + top_r * 0.42}" r="{top_r * 0.08}" fill="#333333"/>
        <circle cx="{x + top_r * 0.4}" cy="{top_y + top_r * 0.35}" r="{top_r * 0.08}" fill="#333333"/>
        
        <!-- Buttons -->
        <circle cx="{x}" cy="{middle_y - middle_r * 0.3}" r="{middle_r * 0.12}" fill="#333333"/>
        <circle cx="{x}" cy="{middle_y + middle_r * 0.1}" r="{middle_r * 0.12}" fill="#333333"/>
        <circle cx="{x}" cy="{middle_y + middle_r * 0.5}" r="{middle_r * 0.12}" fill="#333333"/>
        
        <!-- Hat -->
        <rect x="{x - hat_width/2}" y="{top_y - top_r - hat_height}" width="{hat_width}" height="{hat_height}" fill="#333333" rx="2"/>
        <rect x="{x - hat_brim/2}" y="{top_y - top_r - 2}" width="{hat_brim}" height="4" fill="#333333"/>
        
        <!-- Scarf -->
        <rect x="{x - middle_r * 0.9}" y="{middle_y - middle_r - 2}" width="{middle_r * 1.8}" height="6" fill="#e53935" rx="2"/>
        <rect x="{x + middle_r * 0.5}" y="{middle_y - middle_r + 1}" width="5" height="{middle_r * 0.6}" fill="#e53935" rx="2"/>
    </g>"""


def generate_kamakura(x: float, ground_y: float, kamakura_id: int) -> str:
    """Generate a kamakura (Japanese snow hut) with warm light inside."""
    # Kamakura dimensions
    width = random.uniform(60, 80)
    height = width * 0.75

    # Entrance dimensions (door shape)
    entrance_width = width * 0.30
    entrance_height = height * 0.55

    # Light animation
    glow_duration = random.uniform(2, 4)

    return f"""
    <g id="kamakura-{kamakura_id}">
        <!-- Kamakura dome (rounded triangle shape using path) -->
        <path
            d="M {x - width/2} {ground_y}
               Q {x - width/2} {ground_y - height * 0.6} {x - width * 0.25} {ground_y - height * 0.85}
               Q {x} {ground_y - height * 1.1} {x + width * 0.25} {ground_y - height * 0.85}
               Q {x + width/2} {ground_y - height * 0.6} {x + width/2} {ground_y}
               Z"
            fill="#ffffff"
            stroke="#e0e0e0"
            stroke-width="1"
        />
        
        <!-- Entrance (door shape - rounded top rectangle) -->
        <path
            d="M {x - entrance_width/2} {ground_y}
               L {x - entrance_width/2} {ground_y - entrance_height * 0.7}
               Q {x - entrance_width/2} {ground_y - entrance_height} {x} {ground_y - entrance_height}
               Q {x + entrance_width/2} {ground_y - entrance_height} {x + entrance_width/2} {ground_y - entrance_height * 0.7}
               L {x + entrance_width/2} {ground_y}
               Z"
            fill="#3a3a3a"
        />
        <!-- Inner depth layer -->
        <path
            d="M {x - entrance_width/2 + 2} {ground_y}
               L {x - entrance_width/2 + 2} {ground_y - entrance_height * 0.65}
               Q {x - entrance_width/2 + 2} {ground_y - entrance_height + 3} {x} {ground_y - entrance_height + 3}
               Q {x + entrance_width/2 - 2} {ground_y - entrance_height + 3} {x + entrance_width/2 - 2} {ground_y - entrance_height * 0.65}
               L {x + entrance_width/2 - 2} {ground_y}
               Z"
            fill="#4a4a4a"
        />
        
        <!-- Warm light glow from inside -->
        <ellipse cx="{x}" cy="{ground_y - entrance_height * 0.4}" rx="{entrance_width * 0.35}" ry="{entrance_height * 0.3}" fill="#ffcc80" opacity="0.6">
            <animate
                attributeName="opacity"
                values="0.4;0.7;0.4"
                dur="{glow_duration}s"
                repeatCount="indefinite"
            />
        </ellipse>
        <ellipse cx="{x}" cy="{ground_y - entrance_height * 0.4}" rx="{entrance_width * 0.2}" ry="{entrance_height * 0.18}" fill="#ffab40" opacity="0.5">
            <animate
                attributeName="opacity"
                values="0.3;0.6;0.3"
                dur="{glow_duration * 0.7}s"
                repeatCount="indefinite"
            />
        </ellipse>
        
        <!-- Small snow pile at entrance -->
        <ellipse cx="{x}" cy="{ground_y + 2}" rx="{entrance_width * 0.5}" ry="4" fill="#ffffff"/>
    </g>"""


def generate_snow_ground(width: float, height: float) -> str:
    """Generate snowy ground with gentle bumps."""
    bumps = ""
    num_bumps = int(width / 15)

    for i in range(num_bumps):
        x = random.uniform(-10, width + 10)
        bump_width = random.uniform(20, 50)
        bump_height = random.uniform(8, 18)
        y_offset = random.uniform(-3, 3)

        bumps += f"""
        <ellipse
            cx="{x}"
            cy="{height + y_offset}"
            rx="{bump_width}"
            ry="{bump_height}"
            fill="white"
            opacity="0.95"
        />"""

    # Add some smaller snow details
    for i in range(int(num_bumps * 1.5)):
        x = random.uniform(0, width)
        small_width = random.uniform(8, 20)
        small_height = random.uniform(4, 10)
        y_offset = random.uniform(-8, 0)

        bumps += f"""
        <ellipse
            cx="{x}"
            cy="{height + y_offset}"
            rx="{small_width}"
            ry="{small_height}"
            fill="#f5f5f5"
            opacity="0.9"
        />"""

    return f"""
    <g id="snow-ground">
        <!-- Base snow layer -->
        <rect x="0" y="{height - 15}" width="{width}" height="30" fill="white"/>
        {bumps}
    </g>"""


# =============================================================================
# Season Renderers
# =============================================================================


class SeasonRenderer(ABC):
    """Base class for season-specific rendering."""

    def __init__(self, width: int, height: int, theme: SeasonTheme, date: datetime):
        self.width = width
        self.height = height
        self.theme = theme
        self.date = date

    @abstractmethod
    def render(self) -> list[str]:
        """Render season-specific SVG elements. Returns list of SVG strings."""
        pass

    def _generate_grass_layer(self) -> str:
        """Generate the grass layer."""
        grass_group = [
            f'    <g id="grass-layer" transform="translate(0, {self.height})">'
        ]
        num_blades = int(self.width * 1.5)

        for i in range(num_blades):
            x = random.uniform(-10, self.width + 10)
            blade_height = random.uniform(30, 80)
            color = random.choice(self.theme.grass_colors)
            delay = random.uniform(0, 1)
            grass_group.append(generate_grass_blade(x, blade_height, color, delay, i))

        grass_group.append("    </g>")
        return "\n".join(grass_group)

    def _generate_flower_layer(self) -> str:
        """Generate the flower layer."""
        if not self.theme.flower_colors:
            return ""

        flower_group = [
            f'    <g id="flower-layer" transform="translate(0, {self.height - 5})">'
        ]
        num_flowers = random.randint(8, 15)

        for i in range(num_flowers):
            x = random.uniform(20, self.width - 20)
            y = random.uniform(-25, -15)
            color = random.choice(self.theme.flower_colors)
            size = random.uniform(4, 8)
            flower_group.append(generate_flower(x, y, color, size, i))

        flower_group.append("    </g>")
        return "\n".join(flower_group)


class SpringRenderer(SeasonRenderer):
    """Renderer for spring season."""

    def render(self) -> list[str]:
        elements = []
        # Young short grass with sprouting animation
        elements.append(self._generate_spring_grass_layer())
        # Sprouting buds
        elements.append(self._generate_sprouts())
        # Flowers
        flower_layer = self._generate_flower_layer()
        if flower_layer:
            elements.append(flower_layer)
        return elements

    def _generate_spring_grass_layer(self) -> str:
        """Generate short young grass for spring."""
        grass_group = [
            f'    <g id="grass-layer" transform="translate(0, {self.height})">'
        ]
        num_blades = int(self.width * 1.2)  # Slightly less dense

        for i in range(num_blades):
            x = random.uniform(-10, self.width + 10)
            # Shorter grass for spring (young growth)
            blade_height = random.uniform(15, 40)
            color = random.choice(self.theme.grass_colors)
            delay = random.uniform(0, 1)
            grass_group.append(generate_grass_blade(x, blade_height, color, delay, i))

        grass_group.append("    </g>")
        return "\n".join(grass_group)

    def _generate_sprouts(self) -> str:
        """Generate small flowers that bloom with animation."""
        bloom_group = [
            f'    <g id="bloom-layer" transform="translate(0, {self.height})">'
        ]
        num_blooms = random.randint(12, 20)

        for i in range(num_blooms):
            x = random.uniform(15, self.width - 15)
            bloom_group.append(self._generate_blooming_flower(x, i))

        bloom_group.append("    </g>")
        return "\n".join(bloom_group)

    def _generate_blooming_flower(self, x: float, flower_id: int) -> str:
        """Generate a small flower that blooms with animation."""
        stem_height = random.uniform(35, 55)
        duration = random.uniform(5, 8)
        delay = random.uniform(0, 4) if random.random() > 0.3 else 0

        # Stem color
        stem_color = random.choice(["#8bc34a", "#9ccc65", "#7cb342"])

        # Flower colors (cute pastel colors)
        petal_colors = [
            "#f8bbd9",
            "#f48fb1",
            "#ce93d8",
            "#b39ddb",
            "#fff59d",
            "#ffcc80",
        ]
        petal_color = random.choice(petal_colors)
        center_color = "#ffeb3b"

        stem_width = 2
        num_petals = random.choice([5, 6])
        petal_size = random.uniform(4, 7)

        # Generate petals that bloom
        petals = ""
        for i in range(num_petals):
            angle = (360 / num_petals) * i
            petals += f"""
            <ellipse
                cx="{x + stem_width / 2}"
                cy="{-stem_height - petal_size}"
                rx="0"
                ry="0"
                fill="{petal_color}"
                transform="rotate({angle} {x + stem_width / 2} {-stem_height})"
                opacity="0"
            >
                <animate
                    attributeName="rx"
                    values="0;0;{petal_size * 0.5};{petal_size * 0.5}"
                    keyTimes="0;0.5;0.8;1"
                    dur="{duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                />
                <animate
                    attributeName="ry"
                    values="0;0;{petal_size};{petal_size}"
                    keyTimes="0;0.5;0.8;1"
                    dur="{duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                />
                <animate
                    attributeName="opacity"
                    values="0;0;0.9;0.9"
                    keyTimes="0;0.45;0.7;1"
                    dur="{duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                />
            </ellipse>"""

        sway_duration = random.uniform(1.5, 2.5)

        return f"""
        <g id="bloom-{flower_id}" transform-origin="{x + stem_width / 2}px 0px">
            <!-- Stem -->
            <rect
                x="{x}"
                y="0"
                width="{stem_width}"
                height="0"
                fill="{stem_color}"
                rx="1"
            >
                <animate
                    attributeName="height"
                    values="0;{stem_height};{stem_height}"
                    keyTimes="0;0.4;1"
                    dur="{duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                />
                <animate
                    attributeName="y"
                    values="0;{-stem_height};{-stem_height}"
                    keyTimes="0;0.4;1"
                    dur="{duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                />
            </rect>
            <!-- Petals that bloom -->
            {petals}
            <!-- Flower center -->
            <circle
                cx="{x + stem_width / 2}"
                cy="{-stem_height}"
                r="0"
                fill="{center_color}"
                opacity="0"
            >
                <animate
                    attributeName="r"
                    values="0;0;{petal_size * 0.35};{petal_size * 0.35}"
                    keyTimes="0;0.5;0.8;1"
                    dur="{duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                />
                <animate
                    attributeName="opacity"
                    values="0;0;1;1"
                    keyTimes="0;0.5;0.7;1"
                    dur="{duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                />
            </circle>
            <!-- Sway animation for the whole flower -->
            <animateTransform
                attributeName="transform"
                type="rotate"
                values="-3;3;-3"
                dur="{sway_duration}s"
                repeatCount="indefinite"
                keyTimes="0;0.5;1"
                calcMode="spline"
                keySplines="0.4 0 0.6 1; 0.4 0 0.6 1"
            />
        </g>"""


class SummerRenderer(SeasonRenderer):
    """Renderer for summer season - Beach scene."""

    def render(self) -> list[str]:
        elements = []
        # Sun in the top right
        elements.append(self._generate_sun())
        # Ocean and waves on the right
        elements.append(self._generate_ocean())
        # Sandy beach on the left
        elements.append(self._generate_beach())
        # Parasol on the beach
        elements.append(self._generate_parasol())
        return elements

    def _generate_sun(self) -> str:
        """Generate a shining sun."""
        sun_x = self.width * 0.85
        sun_y = 35
        sun_radius = 25
        ray_length = 15
        num_rays = 12

        # Sun rays with animation
        rays = ""
        for i in range(num_rays):
            angle = (360 / num_rays) * i
            import math

            rad = math.radians(angle)
            x1 = sun_x + (sun_radius + 5) * math.cos(rad)
            y1 = sun_y + (sun_radius + 5) * math.sin(rad)
            x2 = sun_x + (sun_radius + 5 + ray_length) * math.cos(rad)
            y2 = sun_y + (sun_radius + 5 + ray_length) * math.sin(rad)

            rays += f"""
            <line
                x1="{x1}" y1="{y1}"
                x2="{x2}" y2="{y2}"
                stroke="#ffeb3b"
                stroke-width="3"
                stroke-linecap="round"
                opacity="0.8"
            />"""

        return f"""
    <g id="sun">
        <!-- Sun glow -->
        <circle cx="{sun_x}" cy="{sun_y}" r="{sun_radius + 20}" fill="#fff9c4" opacity="0.3">
            <animate
                attributeName="r"
                values="{sun_radius + 15};{sun_radius + 25};{sun_radius + 15}"
                dur="3s"
                repeatCount="indefinite"
            />
            <animate
                attributeName="opacity"
                values="0.3;0.5;0.3"
                dur="3s"
                repeatCount="indefinite"
            />
        </circle>
        <circle cx="{sun_x}" cy="{sun_y}" r="{sun_radius + 10}" fill="#ffee58" opacity="0.5">
            <animate
                attributeName="r"
                values="{sun_radius + 8};{sun_radius + 15};{sun_radius + 8}"
                dur="2.5s"
                repeatCount="indefinite"
            />
        </circle>
        <!-- Sun rays -->
        <g id="sun-rays">
            {rays}
            <animateTransform
                attributeName="transform"
                type="rotate"
                from="0 {sun_x} {sun_y}"
                to="360 {sun_x} {sun_y}"
                dur="60s"
                repeatCount="indefinite"
            />
        </g>
        <!-- Sun body -->
        <circle cx="{sun_x}" cy="{sun_y}" r="{sun_radius}" fill="#ffc107"/>
        <circle cx="{sun_x}" cy="{sun_y}" r="{sun_radius - 5}" fill="#ffeb3b"/>
    </g>"""

    def _generate_ocean(self) -> str:
        """Generate the ocean with 4 layered wave rectangles."""
        # Waves extend from left edge to right edge (will be covered by beach)
        wave_height = 25  # Shallow water depth

        # 4 wave layers: back to front, darker to lighter
        wave_layers = [
            {"y_offset": 0, "color": "#0d47a1", "delay": 0},  # Darkest (back)
            {"y_offset": 5, "color": "#1565c0", "delay": 0.5},
            {"y_offset": 10, "color": "#1976d2", "delay": 1.0},
            {"y_offset": 15, "color": "#42a5f5", "delay": 1.5},  # Lightest (front)
        ]

        waves = ""
        for i, layer in enumerate(wave_layers):
            base_y = self.height - wave_height + layer["y_offset"]
            duration = 2.0

            # Create wavy path animation
            waves += f"""
        <path
            id="wave-layer-{i}"
            d="M -20 {base_y}
               Q 60 {base_y - 8} 140 {base_y}
               Q 220 {base_y + 8} 300 {base_y}
               Q 380 {base_y - 8} 460 {base_y}
               Q 540 {base_y + 8} 620 {base_y}
               L {self.width + 20} {base_y}
               L {self.width + 20} {self.height + 20}
               L -20 {self.height + 20} Z"
            fill="{layer['color']}"
            opacity="0.9"
        >
            <animate
                attributeName="d"
                values="M -20 {base_y} Q 60 {base_y - 8} 140 {base_y} Q 220 {base_y + 8} 300 {base_y} Q 380 {base_y - 8} 460 {base_y} Q 540 {base_y + 8} 620 {base_y} L {self.width + 20} {base_y} L {self.width + 20} {self.height + 20} L -20 {self.height + 20} Z;
                       M -20 {base_y} Q 60 {base_y + 8} 140 {base_y} Q 220 {base_y - 8} 300 {base_y} Q 380 {base_y + 8} 460 {base_y} Q 540 {base_y - 8} 620 {base_y} L {self.width + 20} {base_y} L {self.width + 20} {self.height + 20} L -20 {self.height + 20} Z;
                       M -20 {base_y} Q 60 {base_y - 8} 140 {base_y} Q 220 {base_y + 8} 300 {base_y} Q 380 {base_y - 8} 460 {base_y} Q 540 {base_y + 8} 620 {base_y} L {self.width + 20} {base_y} L {self.width + 20} {self.height + 20} L -20 {self.height + 20} Z"
                dur="{duration}s"
                begin="{layer['delay']}s"
                repeatCount="indefinite"
            />
        </path>"""

        return f"""
    <g id="ocean-layer">
        {waves}
    </g>"""

    def _generate_beach(self) -> str:
        """Generate the sandy beach."""
        beach_end = self.width * 0.45
        sand_color = "#ffe0b2"
        sand_dark = "#ffcc80"

        # Create beach with gentle slope
        sand_details = ""
        # Add some fixed sand texture/dots
        sand_positions = [
            (0.05, 0.7, 1.5),
            (0.12, 0.4, 2.0),
            (0.08, 0.9, 1.2),
            (0.20, 0.6, 1.8),
            (0.15, 0.3, 1.0),
            (0.25, 0.8, 2.2),
            (0.30, 0.5, 1.5),
            (0.18, 0.2, 1.3),
            (0.35, 0.7, 1.8),
            (0.28, 0.4, 2.0),
            (0.40, 0.6, 1.2),
            (0.22, 0.9, 1.6),
            (0.07, 0.5, 1.4),
            (0.33, 0.3, 1.9),
            (0.38, 0.8, 1.1),
        ]
        for x_ratio, y_ratio, size in sand_positions:
            x = beach_end * x_ratio
            y = self.height - 40 + 35 * y_ratio
            sand_details += f"""
            <circle cx="{x}" cy="{y}" r="{size}" fill="{sand_dark}" opacity="0.5"/>"""

        return f"""
    <g id="beach-layer">
        <!-- Main beach -->
        <path
            d="M 0 {self.height - 30}
               Q {beach_end * 0.3} {self.height - 35} {beach_end * 0.6} {self.height - 25}
               Q {beach_end * 0.8} {self.height - 15} {beach_end} {self.height - 5}
               L {beach_end + 30} {self.height + 20}
               L 0 {self.height + 20} Z"
            fill="{sand_color}"
        />
        <!-- Beach edge meeting water -->
        <path
            d="M {beach_end - 30} {self.height - 10}
               Q {beach_end} {self.height - 5} {beach_end + 20} {self.height}
               L {beach_end + 20} {self.height + 20}
               L {beach_end - 30} {self.height + 20} Z"
            fill="#ffecb3"
            opacity="0.8"
        />
        {sand_details}
    </g>"""

    def _generate_parasol(self) -> str:
        """Generate a beach parasol that sways in the wind."""
        import math

        parasol_x = self.width * 0.15
        pole_height = 65  # Pole length
        ground_offset = 10  # How far above the image bottom the pole ends
        canopy_radius = 45  # Radius of parasol
        canopy_depth = 8  # How much the umbrella curves down (smaller = more gentle)
        canopy_height = 15  # Height of the umbrella dome (top to base)
        sway_duration = 4.0  # Slower sway

        # Parasol colors (stripes)
        colors = ["#e53935", "#ffffff"]

        # Create striped umbrella canopy using triangles radiating from center top
        # The center is at the top, and the arc curves down (like a real umbrella)
        stripes = ""
        num_stripes = 8

        # Pole bottom position (pivot point for sway)
        pole_bottom = -ground_offset
        # Top of pole (where canopy attaches)
        pole_top = pole_bottom - pole_height
        # Top center point of umbrella
        top_y = pole_top - canopy_height

        for i in range(num_stripes):
            color = colors[i % 2]
            # Angles for this stripe (0 to 180 degrees for lower half arc)
            start_angle = (180 / num_stripes) * i
            end_angle = (180 / num_stripes) * (i + 1)

            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)

            # Points on the arc (bottom edge of umbrella)
            x1 = parasol_x - canopy_radius + canopy_radius * 2 * (start_angle / 180)
            y1 = pole_top + canopy_depth * math.sin(start_rad)
            x2 = parasol_x - canopy_radius + canopy_radius * 2 * (end_angle / 180)
            y2 = pole_top + canopy_depth * math.sin(end_rad)

            # Triangle from top center to bottom arc edge
            stripes += f"""
            <path
                d="M {parasol_x} {top_y}
                   L {x1} {y1}
                   L {x2} {y2}
                   Z"
                fill="{color}"
            />"""

        # Bottom arc edge path (the curved bottom of umbrella)
        arc_path = f"M {parasol_x - canopy_radius} {pole_top}"
        for angle in range(0, 181, 10):
            rad = math.radians(angle)
            x = parasol_x - canopy_radius + canopy_radius * 2 * (angle / 180)
            y = pole_top + canopy_depth * math.sin(rad)
            arc_path += f" L {x} {y}"

        return f"""
    <g id="parasol" transform="translate(0, {self.height})">
        <g transform-origin="{parasol_x}px {pole_bottom}px">
            <!-- Pole -->
            <rect
                x="{parasol_x - 2}"
                y="{pole_top}"
                width="4"
                height="{pole_height}"
                fill="#8d6e63"
                rx="2"
            />
            <!-- Canopy (umbrella shape with triangles) -->
            <g id="canopy">
                {stripes}
                <!-- Canopy bottom arc edge -->
                <path
                    d="{arc_path}"
                    fill="none"
                    stroke="#bdbdbd"
                    stroke-width="1.5"
                />
                <!-- Top finial -->
                <circle
                    cx="{parasol_x}"
                    cy="{top_y - 2}"
                    r="3"
                    fill="#ffeb3b"
                />
            </g>
            <!-- Gentle sway animation -->
            <animateTransform
                attributeName="transform"
                type="rotate"
                values="-1.5;1.5;-1.5"
                dur="{sway_duration}s"
                repeatCount="indefinite"
                keyTimes="0;0.5;1"
                calcMode="spline"
                keySplines="0.4 0 0.6 1; 0.4 0 0.6 1"
            />
        </g>
    </g>"""


class AutumnRenderer(SeasonRenderer):
    """Renderer for autumn season."""

    def render(self) -> list[str]:
        elements = []
        # Short autumn grass (shorter than spring)
        elements.append(self._generate_autumn_grass_layer())
        # Mushrooms growing on the left
        elements.append(self._generate_mushrooms())
        # Falling leaves
        elements.append(self._generate_falling_leaves())
        return elements

    def _generate_autumn_grass_layer(self) -> str:
        """Generate short grass for autumn (shorter than spring)."""
        grass_group = [
            f'    <g id="grass-layer" transform="translate(0, {self.height})">'
        ]
        num_blades = int(self.width * 1.0)  # Less dense

        for i in range(num_blades):
            x = random.uniform(-10, self.width + 10)
            # Shorter grass for autumn
            blade_height = random.uniform(10, 30)
            color = random.choice(self.theme.grass_colors)
            delay = random.uniform(0, 1)
            grass_group.append(generate_grass_blade(x, blade_height, color, delay, i))

        grass_group.append("    </g>")
        return "\n".join(grass_group)

    def _generate_mushrooms(self) -> str:
        """Generate mushrooms that grow on the left side."""
        mushrooms = [
            f'    <g id="mushroom-layer" transform="translate(0, {self.height})">'
        ]

        # Three mushrooms - two on left, one medium on right
        mushroom_configs = [
            {"x": 40, "cap_width": 54, "cap_height": 36, "stem_height": 45, "delay": 0},
            {
                "x": 100,
                "cap_width": 42,
                "cap_height": 27,
                "stem_height": 36,
                "delay": 0.8,
            },
            {
                "x": self.width - 60,
                "cap_width": 48,
                "cap_height": 32,
                "stem_height": 40,
                "delay": 0.4,
            },
        ]

        cap_colors = ["#d32f2f", "#c62828"]  # Red mushroom caps
        stem_color = "#f5f5f5"

        for i, config in enumerate(mushroom_configs):
            x = config["x"]
            cap_width = config["cap_width"]
            cap_height = config["cap_height"]
            stem_height = config["stem_height"]
            stem_width = cap_width * 0.4
            delay = config["delay"]
            grow_duration = 1.6  # Time to grow
            hold_duration = 3.0  # Time to stay visible
            total_duration = grow_duration + hold_duration
            # Calculate keyTimes: grow phase ends at grow_duration/total_duration
            grow_end = grow_duration / total_duration
            cap_color = cap_colors[i % len(cap_colors)]

            # Initial cap size - larger to cover stem
            cap_width_small = cap_width * 0.4
            cap_height_small = cap_height * 0.4

            # Mushroom cap path (curved dome shape with rounded edges)
            # Cap positioned slightly above gill area
            cap_bottom_y = -stem_height + cap_height * 0.15

            # Small initial cap - rounded dome shape
            small_cap_path = (
                f"M {x - cap_width_small / 2} {cap_bottom_y - cap_height_small * 0.2} "
                f"Q {x - cap_width_small / 2} {cap_bottom_y - cap_height_small} {x} {cap_bottom_y - cap_height_small} "
                f"Q {x + cap_width_small / 2} {cap_bottom_y - cap_height_small} {x + cap_width_small / 2} {cap_bottom_y - cap_height_small * 0.2} "
                f"Q {x} {cap_bottom_y + cap_height_small * 0.1} {x - cap_width_small / 2} {cap_bottom_y - cap_height_small * 0.2}"
            )
            # Full size cap - rounded dome shape
            full_cap_path = (
                f"M {x - cap_width / 2} {cap_bottom_y - cap_height * 0.2} "
                f"Q {x - cap_width / 2} {cap_bottom_y - cap_height} {x} {cap_bottom_y - cap_height} "
                f"Q {x + cap_width / 2} {cap_bottom_y - cap_height} {x + cap_width / 2} {cap_bottom_y - cap_height * 0.2} "
                f"Q {x} {cap_bottom_y + cap_height * 0.15} {x - cap_width / 2} {cap_bottom_y - cap_height * 0.2}"
            )

            # Gill area (横向きの葉っぱ型) - slightly darker than stem
            gill_color = "#c9a68a"  # Darker than stem_color (#e8d4b8)
            # Horizontal leaf shape (gill area) - positioned at stem top
            gill_width_small = cap_width_small * 0.8
            gill_height_small = cap_height_small * 0.25
            gill_width_full = cap_width * 0.8
            gill_height_full = cap_height * 0.25
            gill_y_small = -stem_height
            gill_y_full = -stem_height

            small_gill_path = (
                f"M {x - gill_width_small / 2} {gill_y_small} "
                f"Q {x} {gill_y_small - gill_height_small} {x + gill_width_small / 2} {gill_y_small} "
                f"Q {x} {gill_y_small + gill_height_small} {x - gill_width_small / 2} {gill_y_small}"
            )
            full_gill_path = (
                f"M {x - gill_width_full / 2} {gill_y_full} "
                f"Q {x} {gill_y_full - gill_height_full} {x + gill_width_full / 2} {gill_y_full} "
                f"Q {x} {gill_y_full + gill_height_full} {x - gill_width_full / 2} {gill_y_full}"
            )

            # Static stem (no growing animation) - flat top to connect with gill
            stem_path = (
                f"M {x - stem_width * 0.4} 0 "
                f"C {x - stem_width * 0.5} {-stem_height * 0.15} {x - stem_width * 0.45} {-stem_height * 0.3} {x - stem_width * 0.3} {-stem_height * 0.4} "
                f"C {x - stem_width * 0.2} {-stem_height * 0.5} {x - stem_width * 0.2} {-stem_height * 0.6} {x - stem_width * 0.25} {-stem_height * 0.7} "
                f"C {x - stem_width * 0.3} {-stem_height * 0.85} {x - stem_width * 0.25} {-stem_height} {x - stem_width * 0.2} {-stem_height} "
                f"L {x + stem_width * 0.2} {-stem_height} "
                f"C {x + stem_width * 0.25} {-stem_height} {x + stem_width * 0.3} {-stem_height * 0.85} {x + stem_width * 0.25} {-stem_height * 0.7} "
                f"C {x + stem_width * 0.2} {-stem_height * 0.6} {x + stem_width * 0.2} {-stem_height * 0.5} {x + stem_width * 0.3} {-stem_height * 0.4} "
                f"C {x + stem_width * 0.45} {-stem_height * 0.3} {x + stem_width * 0.5} {-stem_height * 0.15} {x + stem_width * 0.4} 0 Z"
            )

            mushrooms.append(
                f"""
        <g id="mushroom-{i}">
            <!-- Cap (rounded dome) - opens in place -->
            <path
                d="{small_cap_path}"
                fill="{cap_color}"
            >
                <animate
                    attributeName="d"
                    values="{small_cap_path};{full_cap_path};{full_cap_path}"
                    keyTimes="0;{grow_end};1"
                    dur="{total_duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                    calcMode="spline"
                    keySplines="0.25 0.1 0.25 1; 0 0 1 1"
                />
            </path>
            <!-- Gill area (horizontal leaf shape at stem top) -->
            <path
                d="{small_gill_path}"
                fill="{gill_color}"
            >
                <animate
                    attributeName="d"
                    values="{small_gill_path};{full_gill_path};{full_gill_path}"
                    keyTimes="0;{grow_end};1"
                    dur="{total_duration}s"
                    begin="{delay}s"
                    repeatCount="indefinite"
                />
            </path>
            <!-- Stem (static gourd/hourglass shape) -->
            <path
                d="{stem_path}"
                fill="{stem_color}"
            />
        </g>"""
            )

        mushrooms.append("    </g>")
        return "\n".join(mushrooms)

    def _generate_falling_leaves(self) -> str:
        """Generate falling autumn leaves."""
        leaves = [f'    <g id="falling-leaves-layer">']
        num_leaves = random.randint(15, 25)

        leaf_colors = ["#ff6f00", "#ff8f00", "#ffa000", "#e65100", "#bf360c", "#d84315"]

        for i in range(num_leaves):
            x = random.uniform(0, self.width)
            start_y = random.uniform(-50, -10)
            end_y = self.height - random.uniform(5, 15)  # End near ground level
            size = random.uniform(6, 12)
            color = random.choice(leaf_colors)
            duration = random.uniform(6, 9)
            delay = random.uniform(0, 5)
            drift_x = random.uniform(-5, 5)
            rotation = random.choice([90, -90, 180, -180])  # Gentle spin

            # Calculate sway path (left-right movement while falling)
            fall_dist = end_y - start_y
            sway = random.uniform(3, 6)  # Horizontal sway amount
            sway_dir = random.choice([1, -1])
            # Create zigzag path: sway left, right, left, right while falling
            translate_values = (
                f"0 0; "
                f"{sway * sway_dir} {fall_dist * 0.25}; "
                f"{-sway * sway_dir} {fall_dist * 0.5}; "
                f"{sway * sway_dir} {fall_dist * 0.75}; "
                f"{drift_x} {fall_dist}"
            )

            leaves.append(
                f"""
        <g id="leaf-{i}" opacity="0">
            <animate
                attributeName="opacity"
                values="0;0.9;0.9;0"
                keyTimes="0;0.05;0.85;1"
                dur="{duration}s"
                repeatCount="indefinite"
                begin="{delay}s"
            />
            <animateTransform
                attributeName="transform"
                type="translate"
                values="{translate_values}"
                dur="{duration}s"
                begin="{delay}s"
                repeatCount="indefinite"
            />
            <animateTransform
                attributeName="transform"
                type="rotate"
                values="0 {x} {start_y}; {rotation} {x} {start_y}"
                dur="{duration}s"
                begin="{delay}s"
                repeatCount="indefinite"
                additive="sum"
            />
            <path
                d="M {x} {start_y}
                   Q {x - size * 0.3} {start_y + size * 0.5} {x} {start_y + size}
                   Q {x + size * 0.3} {start_y + size * 0.5} {x} {start_y}
                   M {x} {start_y + size * 0.3}
                   L {x} {start_y + size * 0.8}"
                fill="{color}"
                stroke="{color}"
                stroke-width="0.5"
            />
        </g>"""
            )

        leaves.append("    </g>")
        return "\n".join(leaves)


class WinterRenderer(SeasonRenderer):
    """Renderer for winter season."""

    def render(self) -> list[str]:
        elements = []
        # Snow-covered ground (no grass)
        elements.append(generate_snow_ground(self.width, self.height))
        # Kamakura (snow hut)
        elements.append(self._generate_kamakura())
        # Snowmen
        elements.append(self._generate_snowmen())
        # Falling snow
        elements.append(self._generate_falling_snow())
        return elements

    def _generate_falling_snow(self) -> str:
        """Generate the falling snow layer."""
        snow_group = ['    <g id="snow-layer">']
        num_flakes = random.randint(40, 60)

        for i in range(num_flakes):
            x = random.uniform(0, self.width)
            size = random.uniform(1.5, 4)
            snow_group.append(generate_snowflake(x, 0, size, i, self.height))

        snow_group.append("    </g>")
        return "\n".join(snow_group)

    def _generate_kamakura(self) -> str:
        """Generate kamakura (Japanese snow huts) on the right side."""
        kamakura_group = ['    <g id="kamakura-layer">']

        # Place 1 kamakura on the far right side
        x = random.uniform(self.width * 0.78, self.width * 0.92)
        kamakura_group.append(generate_kamakura(x, self.height - 10, 0))

        kamakura_group.append("    </g>")
        return "\n".join(kamakura_group)

    def _generate_snowmen(self) -> str:
        """Generate a snowman on the left side."""
        snowmen_group = ['    <g id="snowmen-layer">']

        # Place 1 snowman on the far left side
        x = self.width * 0.12
        snowmen_group.append(generate_snowman(x, self.height - 5, 0))

        snowmen_group.append("    </g>")
        return "\n".join(snowmen_group)


# Registry of season renderers
SEASON_RENDERERS: dict[str, type[SeasonRenderer]] = {
    "spring": SpringRenderer,
    "summer": SummerRenderer,
    "autumn": AutumnRenderer,
    "winter": WinterRenderer,
}


# =============================================================================
# Main SVG Generator
# =============================================================================


def generate_seasons_svg(
    width: int = 800,
    height: int = 200,
    season: str | None = None,
    seed: int | None = None,
    date: datetime | None = None,
) -> str:
    """Generate the complete seasons SVG."""
    if seed is not None:
        random.seed(seed)

    if date is None:
        date = datetime.now()

    if season is None:
        season = get_current_season(date)

    theme = SEASONS[season]

    # SVG header with transparent background
    svg_parts = [
        f"""<svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 {width} {height}"
    width="{width}"
    height="{height}"
>
"""
    ]

    # Get the appropriate renderer for the season
    renderer_class = SEASON_RENDERERS[season]
    renderer = renderer_class(width, height, theme, date)

    # Render season-specific elements
    svg_parts.extend(renderer.render())

    # Close SVG
    svg_parts.append("\n</svg>")

    return "\n".join(svg_parts)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate an animated seasons SVG for GitHub README"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("seasons.svg"),
        help="Output file path (default: seasons.svg)",
    )
    parser.add_argument(
        "-s",
        "--season",
        choices=["spring", "summer", "autumn", "winter"],
        help="Force a specific season (default: auto-detect)",
    )
    parser.add_argument(
        "-W",
        "--width",
        type=int,
        default=800,
        help="SVG width in pixels (default: 800)",
    )
    parser.add_argument(
        "-H",
        "--height",
        type=int,
        default=200,
        help="SVG height in pixels (default: 200)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible output",
    )

    args = parser.parse_args()

    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Generate SVG
    current_season = args.season or get_current_season()
    print(f"🌿 Generating {current_season} seasons SVG...")

    svg_content = generate_seasons_svg(
        width=args.width,
        height=args.height,
        season=args.season,
        seed=args.seed,
    )

    # Write output
    args.output.write_text(svg_content)
    print(f"✅ Saved to {args.output}")


if __name__ == "__main__":
    main()
