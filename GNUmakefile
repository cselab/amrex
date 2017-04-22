AMREX_HOME := $(shell pwd)

PRECISION = DOUBLE

PROFILE = FALSE

DEBUG = FALSE

DIM = 3

COMP = gnu

USE_MPI = TRUE

USE_OMP = FALSE

USE_PARTICLES = TRUE
USE_FORTRAN_INTERFACE = TRUE

include $(AMREX_HOME)/Tools/GNUMake/Make.defs

Pdirs := Base AmrCore Amr Boundary
ifeq ($(USE_PARTICLES),TRUE)
    Pdirs += Particle
endif
ifeq ($(USE_FORTRAN_INTERFACE),TRUE)
    Pdirs += F_Interfaces/Base F_Interfaces/Octree F_Interfaces/AmrCore
endif
Ppack := $(foreach dir, $(Pdirs), $(AMREX_HOME)/Src/$(dir)/Make.package)
include $(Ppack)

AMREX_INSTALL_DIR = tmp_install_dir

all: $(amrexlib)
	@echo SUCCESS

include $(AMREX_HOME)/Tools/GNUMake/Make.rules
