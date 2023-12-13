# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import logging
import re
from datetime import datetime, timedelta

import pywikibot
import requests
from pywikibot import pagegenerators as pg

log = logging.getLogger(__name__)


class Plugin(object):
    def __init__(self, bot, args):
        self.args = args
        self.bot = bot
        self.reset_cache()
        self.title_translation = {}
        self.dbname2item = {}

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "--verification-delay",
            type=int,
            default=30,
            help="days to wait before verifying a claim again",
        )
        return parser

    def get_query(self, filter):
        query = """
        SELECT DISTINCT ?item WHERE {{
          ?item wdt:{source_code_repository_url} ?url.
        }} ORDER BY ?item
        """.format(
            source_code_repository_url=self.P_source_code_repository_URL
        )
        return query

    def debug(self, item, message):
        self.log(log.debug, item, message)

    def info(self, item, message):
        self.log(log.info, item, message)

    def error(self, item, message):
        self.log(log.error, item, message)

    def log(self, fun, item, message):
        label = item.labels.get("en", "no label")
        fun(
            "http://wikidata.org/wiki/"
            + item.getID()
            + " "
            + label
            + " "
            + self.__class__.__name__
            + " "
            + message
        )

    def run_catch(self, item):
        try:
            if self.args.show:
                return self.show(item)
            else:
                return self.run(item)
        except:
            self.error(item, "failed with an exception")
            raise

    def reset_cache(self):
        self.bot.entities = {
            "property": {},
            "item": {},
        }

    def lookup_entity(self, name, **kwargs):
        type = kwargs["type"]
        found = self.bot.entities[type].get(name)
        if found:
            return found
        found = self.search_entity(self.bot.site, name, **kwargs)
        if found:
            if type == "property":
                found = found["id"]
            self.bot.entities[type][name] = found
        return found

    #
    # Hardcode the desired wikidata item when there are
    # multiple items with the same english label and no
    # trivial way to disambiguate them.
    #
    authoritative = {
        "wikidata": {
            "repository": "Q3133368",
            "issue_tracking_system": "Q1480561",
            "continuous_integration_software": "Q16947796",
            "code_reviewing_software": "Q16920237",
            "collaborative_wiki_software": "Q6686945",
            "electronic_mailing_list_manager": "Q63067479",
            "software_repository": "Q1334294",
            "pull_request": "Q68712963",
            "forge": "Q3077240",
            "website": "Q35127",
        },
        "test": {},
    }

    @staticmethod
    def normalize_name(name):
        return re.sub("[-_]", " ", name)

    def search_entity(self, site, name, **kwargs):
        if name in Plugin.authoritative[site.code]:
            candidate = pywikibot.ItemPage(
                site, Plugin.authoritative[site.code][name], 0
            )
            if candidate.get()["labels"]["en"] == name:
                return candidate
        candidates = []
        for p in site.search_entities(name, "en", **kwargs):
            log.debug("looking for entity `" + name + "`, found " + str(p))
            if "label" in p and Plugin.normalize_name(
                p["label"]
            ) == Plugin.normalize_name(name):
                if kwargs["type"] == "property":
                    candidates.append(p)
                else:
                    candidates.append(pywikibot.ItemPage(site, p["id"], 0))
        if len(candidates) == 0:
            return None
        elif len(candidates) > 1 and kwargs["type"] == "item":
            found = []
            for candidate in candidates:
                item = candidate.get()
                ok = True
                for instance_of in item["claims"].get(self.P_instance_of, []):
                    if instance_of.getTarget() == self.Q_Wikimedia_disambiguation_page:
                        log.debug(
                            "ignore disambiguation page "
                            + candidate.getID()
                            + " for "
                            + name
                        )
                        ok = False
                        break
                if ok:
                    found.append(candidate)
            if len(found) != 1:
                raise ValueError("found multiple items for " + name + " " + str(found))
            return found[0]
        else:
            return candidates[0]

    lookup_item = lookup_entity

    def lookup_property(self, name):
        return self.lookup_entity(self.bot.site, name, type="property")

    def create_entity(self, type, name):
        found = self.search_entity(self.bot.wikidata_site, name, type=type)
        entity = {
            "labels": {
                "en": {
                    "language": "en",
                    "value": name,
                }
            },
        }
        if type == "property":
            assert found, type + " " + name + " must exist in wikidata"
            id = found["id"]
            found = self.bot.wikidata_site.loadcontent({"ids": id}, "datatype")
            assert found, "datatype of " + id + " " + name + " is not found"
            entity["datatype"] = found[id]["datatype"]
        log.debug("create " + type + " " + str(entity))
        self.bot.site.editEntity({"new": type}, entity)

    def clear_entity_label(self, id):
        self.set_entity_label(id, "")

    def set_entity_label(self, id, label):
        data = {
            "labels": {
                "en": {
                    "language": "en",
                    "value": label,
                }
            }
        }
        log.debug("set " + id + " label to '" + label + "'")
        self.bot.site.editEntity({"id": id}, data)
        while True:
            if id.startswith("P"):
                entity = pywikibot.PropertyPage(self.bot.site, id)
            else:
                entity = pywikibot.ItemPage(self.bot.site, id, 0)
            entity.get(force=True)
            if label == "" and entity.labels.get("en") is None:
                break
            if label != "" and label == entity.labels.get("en"):
                break
        self.reset_cache()
        return entity

    def __getattribute__(self, name):
        if name.startswith("P_"):
            type = "property"
        elif name.startswith("Q_"):
            type = "item"
        else:
            return super(Plugin, self).__getattribute__(name)
        label = " ".join(name.split("_")[1:])
        found = self.lookup_entity(label, type=type)
        if not found:
            if self.args.test:
                self.create_entity(type, label)
                for _ in range(120):
                    found = self.lookup_entity(label, type=type)
                    if found is not None:
                        break
            else:
                raise ValueError("found no items for " + name)
        return found

    def get_source(self, claim, id):
        for source in claim.getSources():
            if id in source:
                return source[id]
        return None

    def need_verification(self, claim):
        previous = self.get_source(claim, self.P_retrieved)
        if previous:
            now = datetime.utcnow()
            previous = previous[0].getTarget()
            previous = datetime(
                year=previous.year, month=previous.month, day=previous.day
            )
            return now - previous >= timedelta(days=self.args.verification_delay)
        else:
            return True

    def set_retrieved(self, item, claim, now=datetime.utcnow()):
        when = pywikibot.WbTime(now.year, now.month, now.day)
        retrieved = self.get_source(claim, self.P_retrieved)
        if retrieved:
            self.debug(item, "updating retrieved")
            retrieved[0].setTarget(when)
            if not self.args.dry_run:
                self.bot.site.save_claim(claim)
        else:
            self.debug(item, "setting retrieved")
            retrieved = pywikibot.Claim(
                self.bot.site, self.P_retrieved, is_reference=True
            )
            retrieved.setTarget(when)
            if not self.args.dry_run:
                claim.addSource(retrieved)

    def http_get(self, url):
        try:
            #
            # although head() would be more light weight, some
            # servers do not respond to it. For instance
            # https://src.openvz.org/projects/OVZ/ returned 405
            #
            # The user agent is required for some servers. For
            # instance http://marabunta.laotracara.com/descargas/
            # returns 406 if no User-Agent header is set.
            #
            r = requests.get(url, headers={"User-Agent": "f3wikidatabot"}, verify=False)
            log.debug("GET " + url + " status " + str(r.status_code))
            if r.status_code != requests.codes.ok:
                log.debug("GET " + url + " " + r.text)
            if r.status_code == requests.codes.ok:
                return r
            else:
                return None
        except Exception as e:
            log.debug("GET failed with " + str(e))
            return None

    def get_template_field(self, item, lang2field, lang2pattern):
        """For a given `item`, look into all wikipedia pages linked to it.
        Look for known templates in the page in accordance to `lang2pattern`.
        If a known template is found, look for a field as listed in `lang2field`
        and return the associated value."""
        lang2value = {}
        for dbname in item.sitelinks.keys():
            site = pywikibot.site.APISite.fromDBName(dbname)
            pattern = lang2pattern.get(site.code, lang2pattern["*"])
            p = pywikibot.Page(site, item.sitelinks[dbname].title)
            for template, pairs in p.templatesWithParams():
                self.debug(item, site.code + " template " + template.title())
                if pattern in template.title():
                    for pair in pairs:
                        found = pair.split("=", 1)
                        if len(found) == 1:
                            continue
                        (name, value) = found
                        if site.code in lang2field:
                            translated = lang2field[site.code]
                        elif "en" in lang2field:
                            translated = self.translate_title(
                                lang2field["en"], site.code
                            )
                        else:
                            translated = None
                        self.debug(
                            item,
                            site.code
                            + " compare "
                            + str(translated).lower()
                            + " and "
                            + name.lower(),
                        )
                        if value and translated and name.lower() == translated.lower():
                            lang2value[site.code] = value
        self.debug(item, "get_template_field " + str(lang2value))
        return lang2value

    def translate_title(self, title, lang):
        if title not in self.title_translation:
            site = pywikibot.site.APISite.fromDBName("enwiki")
            translation = {"en": title}
            p = pywikibot.Page(site, title)
            for l in p.langlinks():
                # License (juridique): the (...) is for disambiguation
                translation[l.site.code] = re.sub("\s*\([^)]*\)", "", l.title)
            self.title_translation[title] = translation
        return self.title_translation[title].get(lang)

    def get_redirects(self, title, lang):
        site = pywikibot.site.APISite.fromDBName(lang + "wiki")
        p = pywikibot.Page(site, title)
        r = [
            r.title()
            for r in p.getReferences(
                follow_redirects=False,
                with_template_inclusion=False,
                filter_redirects=True,
                total=5000,
            )
        ]
        log.debug("get_redirects " + title + " " + lang + " " + str(r))
        return r

    def get_sitelink_item(self, dbname):
        if dbname not in self.dbname2item:
            query = """
            SELECT DISTINCT ?item WHERE {{
              ?item wdt:{Wikimedia_database_name} '{dbname}'.
            }}
            """.format(
                Wikimedia_database_name=self.P_Wikimedia_database_name,
                dbname=dbname,
            )
            for item in pg.WikidataSPARQLPageGenerator(query, site=self.bot.site):
                item.get()
                assert (
                    dbname == item.claims[self.P_Wikimedia_database_name][0].getTarget()
                )
                self.dbname2item[dbname] = item
        return self.dbname2item[dbname]
