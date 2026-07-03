from dataclasses import dataclass


@dataclass
class BrandConfig:
    primary_color: str = "#000000"
    secondary_color: str = "#FFFFFF"
    logo_path: str = "assets/logo.png"
    font_family: str = "Arial"


class BrandingManager:
    def __init__(self, config: BrandConfig = None):
        self.config = config or BrandConfig()

    def get_style_overrides(self) -> dict:
        return {
            "color": self.config.primary_color,
            "font-family": self.config.font_family,
        }
