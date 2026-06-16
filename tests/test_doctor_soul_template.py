from pathlib import Path


def test_doctor_seeds_canonical_soul_template():
    doctor_py = Path(__file__).resolve().parents[1] / "hermes_cli" / "doctor.py"
    content = doctor_py.read_text(encoding="utf-8")
    assert "You are Lil Skrrt, a helpful AI assistant." not in content
    assert "soul_path.write_text(DEFAULT_SOUL_MD, encoding=\"utf-8\")" in content
