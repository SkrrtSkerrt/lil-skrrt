class HermesAgent < Formula
  include Language::Python::Virtualenv

  desc "Self-improving AI agent that creates skills from experience"
  homepage "https://github.com/SkrrtSkerrt/lil-skrrt"
  url "https://github.com/SkrrtSkerrt/lil-skrrt/archive/refs/tags/v1.0.1.tar.gz"
  version "0.14.0"
  sha256 "5856f90ffca847fd788afc42ad5b683c88b37e20b0d264187feaefdd22a9c819"
  license "MIT"

  depends_on "certifi" => :no_linkage
  depends_on "cryptography" => :no_linkage
  depends_on "libyaml"
  depends_on "python@3.14"

  # Refresh resource stanzas after bumping the source url/version:
  #   brew update-python-resources --print-only hermes-agent
  #
  # Keep source-build-hostile optional extras out of the base formula. Voice,
  # messaging, Matrix, image generation, and premium TTS dependencies are lazy
  # installed by Lil Skrrt when a user enables those providers.

  def install
    venv = virtualenv_create(libexec, "python3.14")
    venv.pip_install resources
    venv.pip_install buildpath

    pkgshare.install "skills", "optional-skills"

    %w[hermes hermes-agent hermes-acp a lil-skrrt].each do |exe|
      next unless (libexec/"bin"/exe).exist?

      (bin/exe).write_env_script(
        libexec/"bin"/exe,
        HERMES_BUNDLED_SKILLS: pkgshare/"skills",
        HERMES_OPTIONAL_SKILLS: pkgshare/"optional-skills",
        HERMES_MANAGED: "homebrew"
      )
    end
  end

  test do
    ENV["HERMES_HOME"] = testpath/"hermes-home"

    assert_match "Lil Skrrt v#{version}", shell_output("#{bin}/hermes version")
    assert_match "Lil Skrrt v#{version}", shell_output("#{bin}/lil-skrrt --version")

    managed = shell_output("#{bin}/hermes update 2>&1")
    assert_match "managed by Homebrew", managed
    assert_match "brew upgrade hermes-agent", managed
  end
end
