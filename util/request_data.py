from dataclasses import dataclass

@dataclass
class RequestData:
    language: str
    text: str
    length_scale: float = 1.0
    noise_scale: float = 0.3
    noise_w: float = 1.0