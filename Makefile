.PHONY: clean

# W3C spec generator, used by the `online=1` build. It returns HTTP 422 and a
# JSON list of messages if any message reaches its `die-on` threshold, which
# defaults to `fatal` for Bikeshed and so matches the local build below.
SPEC_GENERATOR = https://www.w3.org/publications/spec-generator/

all: index.html

index.html: index.bs
	python3 tools/reformat-js.py
ifdef online
	curl --fail-with-body -sS $(SPEC_GENERATOR) -F file=@index.bs -F type=bikeshed-spec -o index.html.tmp \
		&& mv index.html.tmp index.html \
		|| { cat index.html.tmp; rm -f index.html.tmp; exit 1; }
else
#	bikeshed -f spec index.bs
	bikeshed --die-on=fatal spec index.bs
endif
	node tools/lint.mjs --verbose

clean:
	rm -f index.html index.html.tmp
