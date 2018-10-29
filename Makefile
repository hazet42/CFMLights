PREFIX = /usr/local

CFMlights: sunlight.py program.py output.py control.py
	python3 -m py_compile sunlight.py program.py output.py control.py init.py

.PHONY: install
install: CFMlights
	mkdir -p $(DESTDIR)$(PREFIX)/bin/CFMlights
	cp sunlight.py $(DESTDIR)$(PREFIX)/bin/CFMlights
	cp program.py $(DESTDIR)$(PREFIX)/bin/CFMlights
	cp output.py $(DESTDIR)$(PREFIX)/bin/CFMlights
	cp control.py $(DESTDIR)$(PREFIX)/bin/CFMlights
	cp init.py $(DESTDIR)$(PREFIX)/bin/CFMlights
	cp CFMLights.cfg $(DESTDIR)$(PREFIX)/bin/CFMlights
	chown pi.pi $(DESTDIR)$(PREFIX)/bin/CFMlights/*.py
	chown pi.pi $(DESTDIR)$(PREFIX)/bin/CFMlights/*.cfg
	cp CFMlights.service /lib/systemd/system/
	chown root.root /lib/systemd/system/CFMlights.service
	ln -s  -f /lib/systemd/system/CFMlights.service /etc/systemd/system/CFMlights.service
	systemctl enable CFMlights

.PHONY: uninstall
uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/CFMlights
	rm -f /lib/systemd/system/CFMlights.service
	rm -f /etc/systemd/system/CFMlights.service
