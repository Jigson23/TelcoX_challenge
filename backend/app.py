# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com

from __future__ import annotations

from backend.app_factory import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
