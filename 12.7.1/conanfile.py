from conans import ConanFile, tools
import os

class CplexConan(ConanFile):
    name = "CPLEX"
    version = "12.7.1"
    settings = {"os": ["Windows"],
        "compiler": {"Visual Studio": {"version": ['14', '15']}},
        "arch": ["x86_64"],
        "build_type": ["Release", "Debug", "RelWithDebInfo"]}


    description = """IBM's ILOG CPLEX for linear optimization.
        In the current version it just sets the libraries cplex1271, ilocplex
        and concert for linking (as specified in the C++ Tutorial of CPLEX).
        If other libraries are needed this Conanfile has to be extended.
        
        In order to execute CPLEX Programs the corresponding DLLs have to be supplied
        This funcionality will be added in the near future."""

    include_dirs = [
        "concert/include/ilconcert", 
        "concert/include/ilconcert/ilsched",
        "concert/include/ilconcert/ilxml",
        "cplex/include/ilcplex",
        "cpoptimizer/include/ilcp"
    ]
    
    library_dirs = [
        "concert/lib",
        "cplex/lib",
        "cpoptimizer/lib"
    ]

    def package(self):
        cplex_install_dir = os.environ['CPLEX_STUDIO_DIR1271']

        for d in self.include_dirs:
            self.copy("*", src = cplex_install_dir + "/" + d, dst = d)
        
        if self.settings.build_type == "Release" or self.settings.build_type == "RelWithDebInfo":
            libdir = "x64_windows_vs2015/stat_mda"
        elif self.settings.build_type == "Debug":
            libdir = "x64_windows_vs2015/stat_mdd"
        else:
            exit(1)
        print("Getting libraries from: " + libdir)
        for d in self.library_dirs:
            self.copy("*", src = cplex_install_dir + "/" + d +  "/" + libdir, dst = d)

    def package_info(self):
        self.cpp_info.includedirs = [
            "concert/include", 
            "cplex/include",
            "cpoptimizer/include"
        ]
        
        self.cpp_info.libs = [
            "cplex1271.lib",
            "ilocplex.lib",
            "concert.lib"
        ]
        
        self.cpp_info.libdirs = self.library_dirs
        