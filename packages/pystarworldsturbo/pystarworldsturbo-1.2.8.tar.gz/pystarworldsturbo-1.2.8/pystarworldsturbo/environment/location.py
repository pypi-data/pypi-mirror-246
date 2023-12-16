from .location_appearance import LocationAppearance


class Location():
    def generate_appearance(self) -> LocationAppearance:
        # Abstract.
        raise NotImplementedError()
