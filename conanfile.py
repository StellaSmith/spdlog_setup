#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan import ConanFile
from conan.tools.files import copy
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import check_min_cppstd


class SpdlogSetupConan(ConanFile):
    name = "spdlog_setup"
    version = "1.1.0"
    description = "TOML config for spdlog"
    url = "https://github.com/gegles/spdlog_setup"
    topics = ("spdlog", "logging", "header-only", "TOML", "cpptoml")
    license = "MIT"

    settings = "os", "arch", "compiler", "build_type"
    exports_sources = "include/*", "test/*", "CMakeLists.txt"
    no_copy_source = True
    generators = "CMakeToolchain", "CMakeDeps"

    def config_options(self):
        self.options["fmt"].header_only = True
        self.options["spdlog"].header_only = True

    def build_requirements(self):
        self.test_requires("catch2/[>=3.1.0]")

    def requirements(self):
        self.requires("cpptoml/[>=0.1.1]")
        self.requires("spdlog/[>=1.11.0]")
        self.requires("fmt/[>=9.1.0]")

    def validate(self):
        check_min_cppstd(self, 17)

    def layout(self):
        cmake_layout(self)

    def build(self):
        if not self.conf.get("tools.build:skip_test", default=False):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            cmake.test()

    def package(self):
        copy(self, "*.hpp", self.source_folder, self.package_folder)

    def package_id(self):
        self.info.clear()
