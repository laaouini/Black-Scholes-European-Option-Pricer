"""Interface graphique Tkinter pour le calcul du prix d'une option européenne (BSM)."""

import tkinter as tk
from tkinter import ttk

from black_scholes import CALL, PUT, bsm_price

FIELDS = (
    ("S0", "Prix du sous-jacent S0", "100"),
    ("K", "Strike K", "100"),
    ("T", "Maturité T (années)", "1"),
    ("r", "Taux sans risque r (%)", "5"),
    ("sigma", "Volatilité sigma (%)", "20"),
    ("q", "Rendement des dividendes q (%)", "0"),
)


class BlackScholesApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self.grid(sticky="nsew")
        master.title("Black-Scholes-Merton — Option européenne")
        master.resizable(False, False)

        self.vars = {}
        for row, (key, label, default) in enumerate(FIELDS):
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", pady=3)
            var = tk.StringVar(value=default)
            ttk.Entry(self, textvariable=var, width=14, justify="right").grid(
                row=row, column=1, sticky="e", pady=3, padx=(12, 0)
            )
            self.vars[key] = var

        row = len(FIELDS)
        ttk.Label(self, text="Type d'option").grid(row=row, column=0, sticky="w", pady=3)
        self.option_type = tk.StringVar(value=CALL)
        type_frame = ttk.Frame(self)
        type_frame.grid(row=row, column=1, sticky="e", pady=3)
        ttk.Radiobutton(type_frame, text="Call", value=CALL, variable=self.option_type).pack(side="left")
        ttk.Radiobutton(type_frame, text="Put", value=PUT, variable=self.option_type).pack(side="left", padx=(8, 0))

        ttk.Button(self, text="Calculer", command=self.compute).grid(
            row=row + 1, column=0, columnspan=2, sticky="ew", pady=(12, 6)
        )

        self.result = tk.StringVar(value="Prix : —")
        ttk.Label(self, textvariable=self.result, font=("Segoe UI", 12, "bold")).grid(
            row=row + 2, column=0, columnspan=2
        )
        self.error = tk.StringVar()
        ttk.Label(self, textvariable=self.error, foreground="red", wraplength=320).grid(
            row=row + 3, column=0, columnspan=2
        )

        master.bind("<Return>", lambda _event: self.compute())

    def _read(self, key, label):
        text = self.vars[key].get().strip().replace(",", ".")
        try:
            return float(text)
        except ValueError:
            raise ValueError(f"« {label} » doit être un nombre.") from None

    def compute(self):
        self.error.set("")
        try:
            values = {key: self._read(key, label) for key, label, _ in FIELDS}
            price = bsm_price(
                S0=values["S0"],
                K=values["K"],
                T=values["T"],
                r=values["r"] / 100,
                sigma=values["sigma"] / 100,
                q=values["q"] / 100,
                option_type=self.option_type.get(),
            )
        except ValueError as exc:
            self.result.set("Prix : —")
            self.error.set(str(exc))
            return
        label = "Call" if self.option_type.get() == CALL else "Put"
        self.result.set(f"Prix du {label} : {price:.6f}")


def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    BlackScholesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
