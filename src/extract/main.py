"""Gera a fotografia diária de preços a partir da fixture imutável."""

import json
import random
from pathlib import Path
from typing import Any

ROOT_PATH = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT_PATH / "fixtures" / "products.jsonl"
OUTPUT_PATH = ROOT_PATH / "data" / "products.jsonl"
EXPECTED_PRODUCT_COUNT = 500


class Extractor:
    """Cria dados dinâmicos sem modificar os atributos fixos dos produtos."""

    def __init__(self, fixture_path: Path = FIXTURE_PATH, output_path: Path = OUTPUT_PATH,
                 random_generator: random.Random | None = None) -> None:
        self.fixture_path = fixture_path
        self.output_path = output_path
        self.random = random_generator or random.Random()

    def extract(self) -> list[dict[str, Any]]:
        """Lê e valida a fixture, que é a única fonte de produtos."""
        with self.fixture_path.open("r", encoding="utf-8") as file:
            products = [json.loads(line) for line in file if line.strip()]
        if len(products) != EXPECTED_PRODUCT_COUNT:
            raise ValueError(
                f"A fixture deve conter exatamente {EXPECTED_PRODUCT_COUNT} produtos; "
                f"foram encontrados {len(products)}."
            )
        return products

    @staticmethod
    def _parse_price(value: str | int | float | None) -> float:
        """Converte o formato da fixture (ex.: '6.439') para número."""
        if value is None:
            raise ValueError("O produto da fixture não possui preço base.")
        if isinstance(value, str):
            value = value.replace(".", "").replace(",", ".")
        price = float(value)
        if price <= 0:
            raise ValueError("O preço base deve ser maior que zero.")
        return price

    @staticmethod
    def _format_price(value: float) -> str:
        """Mantém o formato monetário já esperado pelo Transform."""
        return f"{max(1, round(value)):,.0f}".replace(",", ".")

    def _stable_price(self, base: float) -> tuple[float, float]:
        current = base * (1 + self.random.uniform(-0.005, 0.005))
        return current, current

    def _small_increase(self, base: float) -> tuple[float, float]:
        return base * (1 + self.random.uniform(0.01, 0.05)), base

    def _small_drop(self, base: float) -> tuple[float, float]:
        return base * (1 - self.random.uniform(0.01, 0.06)), base

    def _promotion(self, base: float) -> tuple[float, float]:
        old = base * (1 + self.random.uniform(0.02, 0.08))
        return old * (1 - self.random.uniform(0.10, 0.20)), old

    def generate_price(self, products: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Aplica cenários moderados de mercado e alguns preços atuais nulos."""
        scenarios = (self._stable_price, self._small_increase, self._small_drop, self._promotion)
        generated: list[dict[str, Any]] = []
        for original in products:
            product = original.copy()
            base = self._parse_price(product.get("currentPrice") or product.get("price"))
            scenario = self.random.choices(scenarios, weights=(55, 15, 22, 8), k=1)[0]
            current, old = scenario(base)
            product["currentPrice"] = self._format_price(current)
            product["oldPrice"] = self._format_price(old)
            generated.append(product)

        null_count = max(1, round(len(generated) * 0.02))
        for index in self.random.sample(range(len(generated)), null_count):
            generated[index]["currentPrice"] = None
        return generated

    def save(self, products: list[dict[str, Any]]) -> Path:
        """Substitui a fotografia anterior somente após gerar o arquivo completo."""
        if len(products) != EXPECTED_PRODUCT_COUNT:
            raise ValueError(f"A saída deve conter exatamente {EXPECTED_PRODUCT_COUNT} produtos.")
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.output_path.with_suffix(".jsonl.tmp")
        with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
            for product in products:
                file.write(json.dumps(product, ensure_ascii=False) + "\n")
        temporary_path.replace(self.output_path)
        return self.output_path

    def execute(self) -> Path:
        """Executa leitura, geração dinâmica e persistência do JSONL."""
        return self.save(self.generate_price(self.extract()))


if __name__ == "__main__":
    print(Extractor().execute())
