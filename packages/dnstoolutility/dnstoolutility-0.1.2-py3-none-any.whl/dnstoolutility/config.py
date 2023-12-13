import json
import os
from pathlib import Path

GOOGLE = "Google"
GMAIL = "Gmail"
OUTLOOK = "Outlook"
QBOXMAIL = "QBoxMail"
SELFHOSTED = "Self Hosted"
ARUBA_PEC = "Aruba Pec"
ARUBA_MAIL = "Aruba Mail"


class Config:
    def __init__(self, path: str):
        self.path = Path(os.path.expanduser(path)).absolute()
        self.path.parent.mkdir(exist_ok=True, parents=True)
        if not os.path.isfile(self.path):
            with open(self.path, "w") as f:
                f.write(json.dumps(Config._template_data(), indent=4))
        file = open(self.path)
        content = file.read()
        data = json.loads(content)
        file.close()

        self.data = data

    def save(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.data, indent=4))

    def override_default(self):
        self.data["ns"] = self.data.get("ns", {}) | Config._template_data_ns()
        self.data["mx"] = self.data.get("mx", {}) | Config._template_data_mx()
        self.data["a"] = self.data.get("a", {}) | Config._template_data_a()
        self.data["pec"] = (
            self.data.get("pec", {}) | Config._template_data_pec()
        )
        self.data["autodiscover"] = (
            self.data.get("autodiscover", {})
            | Config._template_data_autodiscover()
        )
        self.save()

    @classmethod
    def _template_data(cls) -> dict:
        data = {}
        mx = Config._template_data_mx()
        a = Config._template_data_a()
        ns = Config._template_data_ns()
        pec = Config._template_data_pec()
        autodiscover = Config._template_data_autodiscover()

        data["ns"] = ns
        data["mx"] = mx
        data["a"] = a
        data["pec"] = pec
        data["autodiscover"] = autodiscover
        return data

    @classmethod
    def _template_data_a(cls) -> dict:
        data = {}
        return data

    @classmethod
    def _template_data_autodiscover(cls) -> dict:
        data = {
            "autodiscover.outlook.com": OUTLOOK,
            "autodiscover.qboxmail.com": QBOXMAIL,
        }
        return data

    @classmethod
    def _template_data_mx(cls) -> dict:
        data = {
            "alt4.aspmx.l.google.com": GMAIL,
            "alt3.aspmx.l.google.com": GMAIL,
            "aspmx.l.google.com": GMAIL,
            "alt2.aspmx.l.google.com": GMAIL,
            "alt1.aspmx.l.google.com": GMAIL,
        }
        return data

    @classmethod
    def _template_data_ns(cls) -> dict:
        data = {
            "ns-cloud-d4.googledomains.com": GOOGLE,
            "ns-cloud-d2.googledomains.com": GOOGLE,
            "ns-cloud-d3.googledomains.com": GOOGLE,
            "ns-cloud-d1.googledomains.com": GOOGLE,
        }
        return data

    @classmethod
    def _template_data_pec(cls) -> dict:
        data = {"mx.pec.aruba.it": ARUBA_PEC}
        return data
