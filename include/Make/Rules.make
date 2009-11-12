
# first found target
first: pre default

# create platform dirs 
ARCH_DIRS = $(ARCH_DISTDIR) $(ARCH_BINDIR) $(ARCH_INCDIR) $(ARCH_LIBDIR) \
	$(BIN) $(ETC) \
	$(DRIVERDIR) $(DBDRIVERDIR) $(FONTDIR) $(DOCSDIR) $(HTMLDIR) \
	$(MANBASEDIR) $(MANDIR) $(TOOLSDIR)

pre: | $(ARCH_DIRS)

default:

$(ARCH_DIRS):
	$(MKDIR) $@

$(OBJDIR):
	-test -d $(OBJDIR) || $(MKDIR) $(OBJDIR)

$(ARCH_INCDIR)/%.h: %.h
	$(INSTALL_DATA) $< $@

ifneq ($(MINGW),)
mkpath = $(shell PATH="$(GISBASE)/bin:$(ARCH_LIBDIR):$$PATH" GISRC=$(RUN_GISRC) $(BIN)/g.dirseps$(EXE) -h $(1));$(2)
else
mkpath = $(1):$(2)
endif

run_grass = \
	GISRC=$(RUN_GISRC) \
	GISBASE=$(RUN_GISBASE) \
	PATH="$(GISBASE)/bin:$$PATH" \
	PYTHONPATH="$(call mkpath,$(GISBASE)/etc/python,$$PYTHONPATH)" \
	$(LD_LIBRARY_PATH_VAR)="$(BIN):$(ARCH_LIBDIR):$(BASE_LIBDIR):$($(LD_LIBRARY_PATH_VAR))" \
	LC_ALL=C \
	$(1)

# default clean rules
clean:
	-rm -rf $(OBJDIR) $(EXTRA_CLEAN_DIRS)
	-rm -f $(EXTRA_CLEAN_FILES) *.tab.[ch] *.yy.c *.output *.backup *.tmp.html *.pyc
	-if [ "$(CLEAN_SUBDIRS)" != "" ] ; then \
		for dir in $(CLEAN_SUBDIRS) ; do \
			$(MAKE) -C $$dir clean ; \
		done ; \
	fi

