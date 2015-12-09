from colorama import Style, Fore

from . import webserver

PORT = 3032

try:
    from pylinkchecker.api import crawl
    from pylinkchecker.reporter import truncate

    def report_linkcheck_errors(pages):
        for page in pages.values():
            print Style.BRIGHT + Fore.RED
            print "\n  {0}: {1}".format(page.get_status_message(),
                                        page.url_split.geturl())
            print Style.RESET_ALL
            for source in page.sources:
                print "    from {0}".format(source.origin.geturl())
                print "      {0}".format(truncate(source.origin_str))


    def linkcheck_site(root_dir):
        webserver.start(root_dir=root_dir, port=PORT)
        crawled_site = crawl('http://127.0.0.1:%d/' % PORT)

        if crawled_site.error_pages:
            report_linkcheck_errors(crawled_site.error_pages)
            return False
        return True
except ImportError:
    def linkcheck_site(root_dir):
        print "pylinkchecker unavailable, skipping link checking."
        return True
